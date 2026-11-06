"""Self-authored contract diagnostics, separate from competition tasks and holdouts."""
import argparse
import ast
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def task(name, family, issue, files, valid, alternate, incomplete, checks):
    return dict(instance_id="diagnostic_" + name, family=family, issue=issue,
                files=files, valid=valid, alternate=alternate,
                incomplete=incomplete, checks=checks)


def definitions():
    warning = {
        "notice.py": "class LegacyNotice(DeprecationWarning):\n    pass\n\nLABEL = 'LegacyNotice'\n",
        "api.py": "import warnings\nfrom notice import LegacyNotice\n\ndef emit():\n    warnings.warn('api', DeprecationWarning)\n",
        "helper.py": "import warnings\nfrom notice import LegacyNotice\n\ndef emit():\n    warnings.warn('helper', category=DeprecationWarning)\n"}
    fixed_warning = {p: s.replace("LegacyNotice", "ProjectLegacyNotice").replace(
        "'ProjectLegacyNotice'", "'LegacyNotice'").replace(
        "warnings.warn('api', DeprecationWarning)", "warnings.warn('api', ProjectLegacyNotice)").replace(
        "category=DeprecationWarning", "category=ProjectLegacyNotice") for p, s in warning.items()}
    alt_warning = dict(fixed_warning, **{
        p: s.replace("from notice import ProjectLegacyNotice", "import notice").replace(
            ", ProjectLegacyNotice)", ", notice.ProjectLegacyNotice)").replace(
            "category=ProjectLegacyNotice", "category=notice.ProjectLegacyNotice")
        for p, s in fixed_warning.items() if p != "notice.py"})
    wrong_warning = dict(fixed_warning, **{"helper.py": fixed_warning["helper.py"].replace(
        "category=ProjectLegacyNotice", "category=DeprecationWarning")})

    errors = {"errors.py": "class ConfigError(ValueError):\n    pass\n\nMESSAGE = 'ConfigError'\n",
              "reader.py": "from errors import ConfigError\n\ndef read(value):\n    if value == 'bad':\n        raise ConfigError('bad input')\n    return value\n",
              "writer.py": "from errors import ConfigError\n\ndef write(value):\n    if value is None:\n        raise ConfigError('missing')\n    return str(value)\n"}
    fixed_errors = {p: s.replace("ConfigError", "ProjectConfigError").replace(
        "'ProjectConfigError'", "'ConfigError'") for p, s in errors.items()}
    alt_errors = dict(fixed_errors)
    for p in ["reader.py", "writer.py"]:
        alt_errors[p] = fixed_errors[p].replace("from errors import ProjectConfigError", "import errors").replace(
            "raise ProjectConfigError(", "raise errors.ProjectConfigError(")
    wrong_errors = dict(fixed_errors, **{"writer.py": errors["writer.py"]})

    env = "def enabled(value, automatic):\n    if value is not None:\n        return True\n    return automatic\n"
    env_fixed = "def enabled(value, automatic):\n    if value is None or value == '':\n        return automatic\n    if value == '0':\n        return False\n    if value == '1':\n        return True\n    raise ValueError(value)\n"
    env_alt = "def enabled(value, automatic):\n    if value in (None, ''):\n        return automatic\n    try:\n        return {'0': False, '1': True}[value]\n    except KeyError:\n        raise ValueError(value)\n"

    length = "def byte_length(body):\n    if body is None:\n        return 0\n    return len(body)\n\ndef headers(body):\n    return {'content-length': str(byte_length(body))}\n"
    length_fixed = length.replace("return len(body)", "return len(body.encode('utf-8') if isinstance(body, str) else body)")
    length_alt = length.replace("return len(body)", "if isinstance(body, str):\n        body = body.encode('utf-8')\n    return len(body)")

    notes = {"model.py": "from dataclasses import dataclass\n\n@dataclass\nclass Entry:\n    body: str\n    note: str | None = None\n",
             "parse.py": "from model import Entry\n\ndef parse(body, note=None):\n    return Entry(body, note)\n",
             "render.py": "def render(entry):\n    return entry.body\n"}
    notes_fixed = dict(notes, **{"render.py": "def render(entry):\n    if entry.note:\n        return entry.body + ' [' + entry.note + ']'\n    return entry.body\n"})
    notes_alt = dict(notes, **{"render.py": "def render(entry):\n    return f'{entry.body} [{entry.note}]' if entry.note else entry.body\n"})
    notes_wrong = dict(notes, **{"parse.py": notes["parse.py"].replace("Entry(body, note)", "Entry(body, note or '')")})

    clone = "class Settings:\n    def __init__(self, values):\n        self.values = values\n\n    def clone(self):\n        return Settings(dict(self.values))\n"
    clone_fixed = "from copy import deepcopy\n\n" + clone.replace("Settings(dict(self.values))", "Settings(deepcopy(self.values))")
    clone_alt = "import copy\n\n" + clone.replace("Settings(dict(self.values))", "type(self)(copy.deepcopy(self.values))")

    cache = "class Cache:\n    def __init__(self):\n        self.items = {}\n\n    def put(self, user, scopes, value):\n        self.items[user] = value\n\n    def get(self, user, scopes):\n        return self.items.get(user)\n"
    cache_fixed = cache.replace("self.items[user]", "self.items[(user, frozenset(scopes))]").replace(
        "self.items.get(user)", "self.items.get((user, frozenset(scopes)))")
    cache_alt = cache.replace("self.items[user]", "self.items[(user, tuple(sorted(set(scopes))))]").replace(
        "self.items.get(user)", "self.items.get((user, tuple(sorted(set(scopes)))))")
    cache_wrong = cache.replace("self.items[user]", "self.items[(user, frozenset(scopes))]")

    stream = "def remaining_bytes(stream):\n    return len(stream.read())\n"
    stream_fixed = "def remaining_bytes(stream):\n    position = stream.tell()\n    try:\n        value = stream.read()\n        return len(value.encode('utf-8') if isinstance(value, str) else value)\n    finally:\n        stream.seek(position)\n"


    return [
        task("notice", "identifier_propagation",
             "Rename the public LegacyNotice class to ProjectLegacyNotice, a DeprecationWarning subclass. Both api.emit and helper.emit must emit that exact custom warning category. Update imports and uses consistently, including positional and keyword warning calls. Keep the LABEL string exactly 'LegacyNotice'. Remove the old exported class name; preserve warning messages.",
             warning, fixed_warning, alt_warning, wrong_warning,
             """import warnings
import notice
import api
import helper

def test_type():
    assert issubclass(notice.ProjectLegacyNotice, DeprecationWarning)
def test_old_export():
    assert not hasattr(notice, 'LegacyNotice')
def test_label():
    assert notice.LABEL == 'LegacyNotice'
def test_api_category():
    with warnings.catch_warnings(record=True) as got:
        warnings.simplefilter('always')
        api.emit()
    assert len(got) == 1 and got[0].category is notice.ProjectLegacyNotice
    assert str(got[0].message) == 'api'
def test_helper_category():
    with warnings.catch_warnings(record=True) as got:
        warnings.simplefilter('always')
        helper.emit()
    assert len(got) == 1 and got[0].category is notice.ProjectLegacyNotice
    assert str(got[0].message) == 'helper'
"""),
        task("errors", "identifier_propagation",
             "Rename exported ConfigError to ProjectConfigError throughout errors.py, reader.py and writer.py. read('bad') and write(None) must raise this same ValueError subclass. Other read values and string conversion in write must keep working. Remove old exported class name but preserve MESSAGE='ConfigError' and exception messages.",
             errors, fixed_errors, alt_errors, wrong_errors,
             """import pytest
import errors
from reader import read
from writer import write

def test_export():
    assert issubclass(errors.ProjectConfigError, ValueError)
    assert not hasattr(errors, 'ConfigError')
def test_reader_error():
    with pytest.raises(errors.ProjectConfigError, match='bad input'):
        read('bad')
def test_writer_error():
    with pytest.raises(errors.ProjectConfigError, match='missing'):
        write(None)
def test_reader_preservation():
    assert read('ok') == 'ok' and read(3) == 3
def test_writer_preservation():
    assert write(3) == '3' and write('ok') == 'ok'
def test_literal_preservation():
    assert errors.MESSAGE == 'ConfigError'
"""),
        task("override", "value_semantics",
             "Fix policy.enabled(value, automatic). For None or the empty string return automatic unchanged. String '0' forces False, string '1' forces True. Reject any other string with ValueError. This function must not read the process environment.",
             {"policy.py": env}, {"policy.py": env_fixed}, {"policy.py": env_alt},
             {"policy.py": env.replace("if value is not None:", "if value:")},
             """import pytest
from policy import enabled

def test_missing():
    assert enabled(None, True) is True and enabled(None, False) is False
def test_empty_true():
    assert enabled('', True) is True
def test_empty_false():
    assert enabled('', False) is False
def test_false():
    assert enabled('0', True) is False and enabled('0', False) is False
def test_true():
    assert enabled('1', False) is True and enabled('1', True) is True
def test_invalid():
    with pytest.raises(ValueError):
        enabled('yes', True)
"""),
        task("length", "encoding",
             "payload.byte_length must return the UTF-8 byte count for str, the unchanged byte count for bytes, and 0 for None. headers(body) must use this same rule for its decimal content-length string. Preserve ASCII behavior, embedded NUL and newline data.",
             {"payload.py": length}, {"payload.py": length_fixed}, {"payload.py": length_alt},
             {"payload.py": length.replace("return len(body)", "return len(body.encode('ascii', errors='ignore')) if isinstance(body, str) else len(body)")},
             """from payload import byte_length, headers

def test_ascii():
    assert byte_length('abc') == 3 and headers('abc') == {'content-length': '3'}
def test_unicode():
    assert byte_length('你好') == 6 and headers('你好') == {'content-length': '6'}
def test_supplementary():
    assert byte_length('a🙂') == 5
def test_bytes():
    assert byte_length(b'\\xff\\x00') == 2
def test_none_empty():
    assert byte_length(None) == 0 and byte_length('') == 0
def test_data_preserved():
    assert byte_length('é\\x00\\n') == 4
"""),
        task("notes", "end_to_end_wiring",
             "parse.parse already stores the optional note in Entry. Make render.render return body followed by ' [' + note + ']' when note is a nonempty string, otherwise just body. Preserve Unicode, whitespace and embedded newlines verbatim. Merely storing notes or adding style metadata does not implement display.",
             notes, notes_fixed, notes_alt, notes_wrong,
             """from parse import parse
from render import render

def test_note():
    assert render(parse('body', 'why')) == 'body [why]'
def test_missing():
    assert render(parse('body')) == 'body'
def test_empty():
    assert render(parse('body', '')) == 'body'
def test_unicode():
    assert render(parse('正文', '说明')) == '正文 [说明]'
def test_multiline():
    assert render(parse('a\\nb', 'x\\ny')) == 'a\\nb [x\\ny]'
def test_spaces():
    assert render(parse(' body ', ' x ')) == ' body  [ x ]'
"""),
        task("clone", "state_isolation",
             "Settings.clone must create an independent deep copy of nested dictionaries and lists in values. Mutating either clone or original after cloning must not affect the other. Preserve scalar values and the original constructor behavior; do not use serialization that changes Python value types.",
             {"settings.py": clone}, {"settings.py": clone_fixed}, {"settings.py": clone_alt},
             {"settings.py": clone.replace("Settings(dict(self.values))", "Settings(self.values.copy())")},
             """from settings import Settings

def test_new_object():
    s = Settings({'a': 1}); c = s.clone()
    assert c is not s and c.values == s.values and c.values is not s.values
def test_nested_list():
    s = Settings({'a': [1]}); c = s.clone(); c.values['a'].append(2)
    assert s.values == {'a': [1]}
def test_nested_dict():
    s = Settings({'a': {'b': 1}}); c = s.clone(); c.values['a']['b'] = 2
    assert s.values['a']['b'] == 1
def test_original_mutation():
    s = Settings({'a': [1]}); c = s.clone(); s.values['a'].append(2)
    assert c.values == {'a': [1]}
def test_types():
    s = Settings({'a': (1, 2), 'b': {3, 4}}); c = s.clone()
    assert type(c.values['a']) is tuple and type(c.values['b']) is set
def test_constructor():
    d = {}; s = Settings(d); assert s.values is d
"""),
        task("cache", "key_scope",
             "Cache entries must be separated by both user and scopes. Scopes is a list of strings and acts as a set: order and duplicates do not matter. Empty scopes is valid. Missing combinations return None. Preserve independent users, overwritten values and the stored value identity.",
             {"cache.py": cache}, {"cache.py": cache_fixed}, {"cache.py": cache_alt},
             {"cache.py": cache_wrong},
             """from cache import Cache

def test_user():
    c=Cache(); c.put('a', ['x'], 1); c.put('b', ['x'], 2)
    assert c.get('a',['x']) == 1 and c.get('b',['x']) == 2
def test_scope():
    c=Cache(); c.put('a',['x'],1); c.put('a',['y'],2)
    assert c.get('a',['x']) == 1 and c.get('a',['y']) == 2
def test_order():
    c=Cache(); c.put('a',['x','y'],3)
    assert c.get('a',['y','x','x']) == 3
def test_empty_missing():
    c=Cache(); c.put('a',[],4)
    assert c.get('a',[]) == 4 and c.get('a',['x']) is None
def test_overwrite():
    c=Cache(); c.put('a',['x'],1); c.put('a',['x','x'],2)
    assert c.get('a',['x']) == 2
def test_identity():
    c=Cache(); v=[]; c.put('a',['x'],v); assert c.get('a',['x']) is v
"""),
        task("stream", "cursor_and_encoding",
             "remaining_bytes(stream) must report bytes remaining from the current cursor through EOF, using UTF-8 for text streams and raw length for binary streams. Restore the cursor before returning, including when reading raises. Do not close the stream. Support seekable io.StringIO/io.BytesIO and seekable readers with the same API.",
             {"stream.py": stream}, {"stream.py": stream_fixed},
             {"stream.py": stream_fixed.replace("return len(value.encode('utf-8') if isinstance(value, str) else value)", "if isinstance(value, str):\n            value = value.encode('utf-8')\n        return len(value)")},
             {"stream.py": stream.replace("return len(stream.read())", "position = stream.tell()\n    value = stream.read()\n    stream.seek(position)\n    return len(value)")},
             """import io
import pytest
from stream import remaining_bytes

def test_binary():
    s=io.BytesIO(b'abcdef'); s.seek(2); assert remaining_bytes(s) == 4 and s.tell() == 2
def test_text():
    s=io.StringIO('a你好'); s.seek(1); assert remaining_bytes(s) == 6 and s.tell() == 1
def test_repeat():
    s=io.BytesIO(b'abc'); assert remaining_bytes(s) == remaining_bytes(s) == 3
def test_eof():
    s=io.StringIO('é'); s.seek(1); assert remaining_bytes(s) == 0 and s.tell() == 1
def test_not_closed():
    s=io.BytesIO(b'x'); remaining_bytes(s); assert not s.closed
def test_exception():
    class Broken(io.BytesIO):
        def read(self):
            super().read(1)
            raise OSError('read failed')
    s=Broken(b'abc'); s.seek(1)
    with pytest.raises(OSError):
        remaining_bytes(s)
    assert s.tell() == 1
"""),
    ]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_files(root, files):
    for name, source in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source)


def check_variant(spec, files, directory):
    directory.mkdir(parents=True)
    write_files(directory, files)
    (directory / "test_contract.py").write_text(spec["checks"])
    started = time.perf_counter()
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", "-o", "addopts=",
                             "--junitxml=junit.xml", "test_contract.py"],
                            cwd=directory, capture_output=True, text=True, timeout=30,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"))
    (directory / "pytest.log").write_text(result.stdout + result.stderr)
    cases = list(ET.parse(directory / "junit.xml").iter("testcase"))
    return dict(exit_code=result.returncode, tests=len(cases),
                failures=sum(c.find("failure") is not None for c in cases),
                errors=sum(c.find("error") is not None for c in cases),
                skipped=sum(c.find("skipped") is not None for c in cases),
                seconds=time.perf_counter()-started, junit_sha256=digest(directory / "junit.xml"))


def prepare(destination):
    from swegemma.models import Task
    destination.mkdir(parents=True, exist_ok=False)
    snapshots = destination / "snapshots"
    snapshots.mkdir()
    tasks, manifest = [], []
    for index, spec in enumerate(definitions()):
        name = spec["instance_id"]
        source = destination / "qualification" / name / "original-source"
        source.mkdir(parents=True)
        write_files(source, spec["files"])
        (source / ".gitignore").write_text("__pycache__/\n.pytest_cache/\n")
        (source / "pyproject.toml").write_text(
            "[build-system]\nrequires = ['setuptools']\nbuild-backend = 'setuptools.build_meta'\n\n"
            "[project]\nname = '" + name.replace("_", "-") + "'\nversion = '0.0.1'\n")
        # A visible preservation-only test; full repair checks are never in the snapshot.
        (source / "tests").mkdir()
        visible_name = ["test_label", "test_reader_preservation", "test_missing", "test_ascii",
                        "test_missing", "test_constructor", "test_user", "test_eof"][index]
        tree = ast.parse(spec["checks"])
        nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))
                 or isinstance(n, ast.FunctionDef) and n.name == visible_name]
        visible = "\n\n".join(ast.get_source_segment(spec["checks"], n) for n in nodes) + "\n"
        (source / "tests/test_smoke.py").write_text(visible)
        env = dict(os.environ, GIT_AUTHOR_DATE="2026-11-01T08:26:03+00:00",
                   GIT_COMMITTER_DATE="2026-11-01T08:26:03+00:00")
        for args in [("init", "-q"), ("config", "user.name", "Diagnostic fixture"),
                     ("config", "user.email", "diagnostic@invalid"), ("add", "."),
                     ("commit", "-qm", "self-authored diagnostic input")]:
            subprocess.run(["git", *args], cwd=source, env=env, capture_output=True, check=True)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
        snapshot = snapshots / (name + ".tgz")
        with tarfile.open(snapshot, "w:gz") as archive:
            archive.add(source, arcname=".")
        checks = spec["checks"].splitlines(keepends=True)
        test_patch = ("diff --git a/tests/test_contract.py b/tests/test_contract.py\n"
                      "new file mode 100644\n--- /dev/null\n+++ b/tests/test_contract.py\n"
                      f"@@ -0,0 +1,{len(checks)} @@\n" + "".join("+"+l for l in checks))
        task_obj = Task(instance_id=name, repo="self-authored/" + name, base_commit=commit,
                        problem_statement=spec["issue"], test_patch=test_patch,
                        FAIL_TO_PASS=tuple("tests/test_contract.py::" + line.split("(")[0].split()[1]
                                           for line in spec["checks"].splitlines() if line.startswith("def test_")))
        tasks.append(dataclasses.asdict(task_obj))
        results = {}
        for kind in ["files", "valid", "alternate", "incomplete"]:
            results[kind] = check_variant(spec, spec[kind], destination / "qualification" / name / kind)
        assert all(results[k]["exit_code"] == 0 and results[k]["skipped"] == 0 for k in ["valid", "alternate"]), results
        assert all(results[k]["exit_code"] != 0 for k in ["files", "incomplete"]), results
        assert all(results[k]["tests"] == len(task_obj.FAIL_TO_PASS) for k in ["valid", "alternate"]), results
        assert all(results[k]["tests"] == len(task_obj.FAIL_TO_PASS) or results[k]["errors"]
                   for k in ["files", "incomplete"]), results
        manifest.append(dict(task_id=name, family=spec["family"], repo=task_obj.repo,
                             base_commit=commit, problem_sha256=hashlib.sha256(spec["issue"].encode()).hexdigest(),
                             snapshot_sha256=digest(snapshot), contract_tests=len(task_obj.FAIL_TO_PASS),
                             variants=results, exposure="self_authored_development_diagnostic",
                             official_gold_read=False))
    (destination / "tasks.jsonl").write_text("".join(json.dumps(t,ensure_ascii=False)+"\n" for t in tasks))
    receipt = dict(complete=True, tasks=manifest, independent_task_families=len({x["family"] for x in manifest}),
                   task_count=len(tasks), qualification_runs=32,
                   valid_implementations_accepted=16, original_or_incomplete_rejected=16,
                   source_sha256=digest(Path(__file__)), tasks_sha256=digest(destination / "tasks.jsonl"),
                   official_tasks_modified=False, official_score_estimate=False,
                   scope="Small self-authored diagnostic repositories; author knows contracts and checks. Not new hidden-style independent acceptance.")
    (destination / "qualification.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k!="tasks"},ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", type=Path, required=True)
    prepare(parser.parse_args().prepare)
