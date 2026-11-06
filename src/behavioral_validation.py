"""Additional public-requirement behavior checks, separate from the official verifier."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import time

from local_sandbox import configure_local_sandbox
from run_baseline import provision_test_deps
from swegemma.harness.verification import extract_snapshot, apply_patch_in_container
from swegemma.sandbox import SubprocessManager

PROBES = {
"rich_3676": ("rich", """
import io
from rich.console import Console
from rich.traceback import Traceback
for notes in [[], ["first calibration note"], ["second α note", "last line"]]:
    try:
        raise ValueError("base exception remains visible")
    except ValueError as error:
        for note in notes: error.add_note(note)
        trace = Traceback.from_exception(type(error), error, error.__traceback__)
        stream = io.StringIO()
        Console(file=stream, color_system=None, width=120).print(trace)
        text = stream.getvalue()
        assert "base exception remains visible" in text
        assert all(note in text for note in notes)
        positions = [text.index(note) for note in notes]
        assert positions == sorted(positions)
"""),
"fastapi_14605": ("fastapi", """
import warnings
from fastapi import exceptions, utils
category = getattr(exceptions, "FastAPIDeprecationWarning", None)
assert isinstance(category, type) and issubclass(category, Warning)
for name, path, method in [("probe", "/item", "GET"), ("changed-name", "/other", "POST")]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        identifier = utils.generate_operation_id_for_path(name=name, path=path, method=method)
    assert isinstance(identifier, str) and identifier
    assert any(issubclass(w.category, category) for w in caught)
"""),
"fastapi_5624": ("fastapi", """
from fastapi import FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient
for prefix in ["alpha", "renamed"]:
    async def left(scopes: SecurityScopes): return list(scopes.scopes)
    async def right(scopes: SecurityScopes): return list(scopes.scopes)
    async def parent(a=Security(left, scopes=[prefix+":left"]), b=Security(right, scopes=[prefix+":right"])):
        return {"left": a, "right": b}
    app = FastAPI()
    @app.get("/scopes")
    async def endpoint(value=Security(parent, scopes=[prefix+":root"])): return value
    with TestClient(app) as client:
        first = client.get("/scopes")
        second = client.get("/scopes")
    expected = {"left": [prefix+":root", prefix+":left"], "right": [prefix+":root", prefix+":right"]}
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json() == expected
"""),
"requests_7433": ("requests", """
import io
from collections.abc import Iterable
import requests
from requests.utils import rewind_body
class Proxy:
    def __init__(self, stream): self.stream = stream
    def __getattr__(self, name): return getattr(self.stream, name)
for payload, offset in [(b"first payload", 0), (b"another payload", 3)]:
    source = io.BytesIO(payload)
    source.seek(offset)
    proxy = Proxy(source)
    assert hasattr(proxy, "__iter__") and not isinstance(proxy, Iterable)
    prepared = requests.Request("POST", "http://behavior.invalid", data=proxy).prepare()
    assert prepared.body is proxy
    assert int(prepared.headers["Content-Length"]) == len(payload)-offset
    proxy.read(2)
    rewind_body(prepared)
    assert proxy.tell() == offset and proxy.read() == payload[offset:]
for value in ["plain", b"bytes", {"a": "one"}, [("a", "one")]]:
    prepared = requests.Request("POST", "http://behavior.invalid", data=value).prepare()
    assert isinstance(prepared.body, (str, bytes))
"""),
"requests_6589": ("requests", """
import requests
from requests.utils import super_len
for value in ["", "ASCII", "你好", "α🚀", "e\u0301"]:
    assert super_len(value) == len(value.encode("utf-8"))
    assert super_len(value.encode("utf-8")) == len(value.encode("utf-8"))
    if value:
        prepared = requests.Request("POST", "http://behavior.invalid", data=value).prepare()
        assert int(prepared.headers["Content-Length"]) == len(value.encode("utf-8"))
"""),
}
BOUNDARY = "Additional limited public-requirement check, not a full-repair oracle, official score or new independent task"

def probe_program(task_id):
    package, code = PROBES[task_id]
    # Keep task source provenance and operational errors visible in the result
    return """import importlib,json,pathlib,traceback
root=pathlib.Path.cwd().resolve()
report={}
try:
    module=importlib.import_module(PACKAGE)
    origin=pathlib.Path(module.__file__).resolve()
    if not origin.is_relative_to(root):
        raise RuntimeError("imported package outside task workspace")
    report["module_origin"]=str(origin)
    exec(CODE, {"__name__":"__behavior_check__"})
    report["status"]="behavior_passed"
except AssertionError as error:
    report.update(status="behavior_failed",error_type=type(error).__name__,message=str(error),traceback=traceback.format_exc()[-2500:])
except BaseException as error:
    report.update(status="execution_error",error_type=type(error).__name__,message=str(error),traceback=traceback.format_exc()[-2500:])
print(json.dumps(report))
""".replace("PACKAGE", repr(package)).replace("CODE", repr(code))

def run_behavior_check(task_id, patch_path, output):
    root = Path(__file__).resolve().parents[1]
    data = root/"data/competition"
    output = output.resolve()
    output.mkdir(parents=True)
    if task_id not in PROBES:
        raise ValueError("No qualified additional behavior probe for this task")
    started = time.monotonic()
    dependencies = provision_test_deps(data, task_id, output)
    manager = configure_local_sandbox(SubprocessManager(), output, wheels=data/"wheels", dependencies=dependencies)
    program = probe_program(task_id)
    source = output/"probe.py"
    source.write_text(program)
    identity = None
    try:
        identity = manager.start()
        extract_snapshot(manager, identity, data/"snapshots"/(task_id+".tgz"))
        if patch_path is not None:
            manager.copy_to(identity, patch_path.resolve(), "/tmp/behavior.patch")
            code, stdout, stderr = apply_patch_in_container(manager, identity, "/tmp/behavior.patch")
            if code:
                result = dict(status="patch_apply_error",exit_code=code,stdout=stdout[-1500:],stderr=stderr[-1500:])
            else:
                result = None
        else:
            result = None
        if result is None:
            manager.copy_to(identity, source, "/tmp/behavior_probe.py")
            execution = manager.exec(identity, shlex.join(["python3","-B","/tmp/behavior_probe.py"]), timeout=30)
            try:
                result = json.loads(execution.stdout.splitlines()[-1])
            except (ValueError, IndexError):
                result = dict(status="unverified",reason="missing_structured_result")
            result.update(exit_code=execution.exit_code,stdout=execution.stdout[-3500:],stderr=execution.stderr[-1500:])
            if execution.exit_code != 0:
                result["status"]="unverified"
    finally:
        manager.cleanup_all()
    result.update(task_id=task_id,patch_sha256=hashlib.sha256(patch_path.read_bytes()).hexdigest() if patch_path else None,
        probe_sha256=hashlib.sha256(program.encode()).hexdigest(),sandbox_id=identity,
        full_seconds=time.monotonic()-started,official_result_unchanged=True,
        complete_repair_verified=False,boundary=BOUNDARY)
    (output/"summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id",required=True,choices=PROBES)
    parser.add_argument("--patch",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=run_behavior_check(args.task_id,args.patch,args.output)
    print(json.dumps({k:result.get(k) for k in ["task_id","status","error_type","full_seconds","sandbox_id"]}))

if __name__=="__main__":main()
