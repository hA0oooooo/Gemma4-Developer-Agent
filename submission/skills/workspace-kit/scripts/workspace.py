"""Bounded source navigation, syntax-checked editing and existing-test feedback."""

import argparse
import ast
import math
import os
import re
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


SKIP = {".git", ".venv", "venv", "__pycache__", "node_modules", "build", "dist"}
STOP = set("a an and are as at be by can code do does for from has have how i in is it "
           "not of on or should that the this to was when which with fix issue bug "
           "please expected actual behavior example python import return def class".split())
LIMIT = 4300


def words(text):
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    identifiers = re.findall(r"[a-z][a-z0-9_]{2,}", text.lower())
    tokens = {w for identifier in identifiers for w in [identifier, *identifier.split("_")]}
    tokens |= {w[:-1] for w in tokens if len(w) > 4 and w.endswith("s")}
    return {w for w in tokens if len(w) > 2 and w not in STOP}


def sources(root):
    for directory, children, names in os.walk(root):
        children[:] = sorted(n for n in children if not n.startswith(".") and n not in SKIP)
        for name in sorted(names):
            path = Path(directory) / name
            if not name.startswith(".") and path.suffix == ".py" and path.stat().st_size < 512_000:
                if path.resolve().is_relative_to(root.resolve()):
                    yield path, path.read_text(errors="replace")


def search(root, query):
    terms = words(query)
    documents = [(p, text, words(text)) for p, text in sources(root)]
    frequency = Counter(w for _, _, vocabulary in documents for w in terms & vocabulary)
    ranked = []
    for path, text, vocabulary in documents:
        matches = terms & vocabulary
        if not matches:
            continue
        relative = path.relative_to(root).as_posix()
        score = sum(math.log(1 + len(documents) / frequency[w]) for w in matches)
        score += 3 * len(terms & words(relative))
        if "test" in path.parts or "tests" in path.parts or path.name.startswith("test_"):
            score *= 0.4
        ranked.append((score, relative, text, matches))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    output = []
    for _, relative, text, matches in ranked[:5]:
        output.append(f"FILE {relative}")
        hits = [(i, line) for i, line in enumerate(text.splitlines(), 1) if words(line) & matches]
        for number, line in hits[:4]:
            output.append(f"  {number}: {line[:160]}")
        stem = Path(relative).stem
        tests = [p.relative_to(root).as_posix() for p, _, _ in documents
                 if p.name in {f"test_{stem}.py", f"{stem}_test.py"}]
        if tests:
            output.append("  RELATED TESTS " + ", ".join(tests[:3]))
    return "\n".join(output)[:LIMIT] or "No matching Python source; try an exact identifier from the issue"


def show(root, filepath, symbol):
    path = (root / filepath).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Source path must stay inside /workspace")
    text = path.read_text()
    lines = text.splitlines()
    tree = ast.parse(text)
    nodes = []

    def visit(node, prefix=""):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                nodes.append((name, child))
                visit(child, name + ".")
            else:
                visit(child, prefix)

    visit(tree)
    if not symbol:
        index = ", ".join(f"{name}:{node.lineno}" for name, node in nodes)
        header = f"FILE {filepath} LINES 1-{min(len(lines), 85)}\n"
        output = header + "\n".join(lines[:85])
        if len(output) > 3000:
            output = output[:3000].rsplit("\n", 1)[0] + "\n[Source window truncated]"
        return (output + "\nSYMBOLS " + index +
                "\nFor a later method, show the exact Class.method listed above")[:LIMIT]
    selected = next((n for name, n in nodes if name == symbol), None)
    if selected is None:
        selected = next((n for name, n in nodes if name.rsplit(".", 1)[-1] == symbol), None)
    if selected is None:
        return ("Symbol not found. Available symbols: " + ", ".join(name for name, _ in nodes))[:LIMIT]
    start = min([selected.lineno, *(n.lineno for n in selected.decorator_list)]) - 1
    stop = min(selected.end_lineno, start + 85)
    output = f"FILE {filepath} SYMBOL {symbol} LINES {start + 1}-{stop}\n"
    output += "\n".join(lines[start:stop])
    if stop < selected.end_lineno:
        output += "\n[Symbol continues; request a named nested method if needed]"
    if len(output) > LIMIT:
        output = output[:LIMIT - 70].rsplit("\n", 1)[0] + "\n[Output bounded; use a more specific symbol]"
    return output


def workspace_path(root, filepath):
    path = (root / filepath).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Path must stay inside the task checkout")
    return path


CHECK_BEFORE_WRITE = True


def edit(root, filepath, old, new):
    path = workspace_path(root, filepath)
    if len(old.splitlines()) > 4 or len(new.splitlines()) > 8:
        return {"status": "rejected", "reason": "Use at most 4 OLD source lines and 8 NEW lines per exact edit"}
    if ("tests" in path.relative_to(root).parts or path.name.startswith(("test_", ".adk_exec_", "_swegemma"))
            or path.name in {"conftest.py", "sitecustomize.py"}
            or path.name.endswith("_test.py") or path.suffix != ".py"):
        return {"status": "rejected", "reason": "Edit Python implementation files, not tests or configuration"}
    before = path.read_text() if path.exists() else ""
    if not path.exists() and old:
        return {"status": "rejected", "reason": "A new implementation file requires an empty old string"}
    if path.exists() and (not old or before.count(old) != 1):
        return {"status": "rejected", "reason": "old must match exactly once; inspect the current source"}
    after = before.replace(old, new, 1) if old else new
    if not CHECK_BEFORE_WRITE:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(after)
    try:
        compile(after, filepath, "exec")
    except SyntaxError as error:
        return {"status": "rejected", "reason": "SyntaxError", "line": error.lineno,
                "message": error.msg, "original_preserved": CHECK_BEFORE_WRITE}
    if CHECK_BEFORE_WRITE:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(after)
    return {"status": "ok", "filepath": filepath, "syntax_checked": True}


def test(root, target):
    path = workspace_path(root, target.split("::", 1)[0])
    if path.suffix != ".py" or not path.is_file():
        return {"status": "rejected", "reason": "Choose one existing test file or test node, not a full suite"}
    if not ("tests" in path.relative_to(root).parts or path.name.startswith("test_")
            or path.name.endswith("_test.py")):
        return {"status": "rejected", "reason": "The target must be an existing repository test"}
    command = [sys.executable, "-m", "pytest", target, "-q", "-x", "--disable-warnings",
               "-o", "faulthandler_timeout=10"]
    environment = dict(os.environ, PYTHONPATH=f"{root / 'src'}:{root}")
    try:
        result = subprocess.run(command, cwd=root, env=environment, capture_output=True,
                                text=True, timeout=40)
        return {"status": "completed", "pytest_exit_code": result.returncode,
                "output": (result.stdout + result.stderr)[-3300:]}
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or b"") + (error.stderr or b"")
        return {"status": "timeout", "pytest_exit_code": 124,
                "output": output.decode(errors="replace")[-3300:]}


def diff(root):
    check = subprocess.run(["git", "diff", "--check"], cwd=root, capture_output=True, text=True)
    result = subprocess.run(["git", "diff", "--stat"], cwd=root, capture_output=True, text=True)
    content = subprocess.run(["git", "diff"], cwd=root, capture_output=True, text=True)
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               cwd=root, capture_output=True, text=True)
    extra = [p for p in untracked.stdout.splitlines() if not Path(p).name.startswith(".adk_exec_")]
    return {"diff_check_exit": check.returncode, "diff_check": check.stdout + check.stderr,
            "stat": result.stdout, "diff": content.stdout[:2800], "untracked": extra}


"""Same action implementation for positional and native Skill named options."""


def parse_skill_arguments(positional_parser):
    if not sys.argv[1:2] or not sys.argv[1].startswith("--"):
        return positional_parser.parse_args()
    parser = argparse.ArgumentParser(description=positional_parser.description)
    fields = {"search": ["query"], "show": ["filepath"],
              "edit": ["filepath", "old", "new"], "test": ["target"], "diff": []}
    parser.add_argument("--operation", choices=fields, required=True)
    for name in ["query", "filepath", "old", "new", "target"]:
        parser.add_argument("--" + name)
    parser.add_argument("--symbol", default="")
    args = parser.parse_args()
    for name in fields[args.operation]:
        if getattr(args, name) is None:
            parser.error(f"{args.operation} requires --{name}")
    return args


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("search").add_argument("query")
    view = commands.add_parser("show")
    view.add_argument("filepath")
    view.add_argument("symbol", nargs="?", default="")
    change = commands.add_parser("edit")
    change.add_argument("filepath")
    change.add_argument("old")
    change.add_argument("new")
    commands.add_parser("test").add_argument("target")
    commands.add_parser("diff")
    args = parse_skill_arguments(parser)
    # The skill wrapper changes cwd to its temporary extraction directory.
    # The sandbox shell's PWD remains the checkout, including in subprocess mode.
    root = Path(os.environ["PWD"])
    if args.operation == "search":
        print(search(root, args.query))
    elif args.operation == "show":
        print(show(root, args.filepath, args.symbol))
    elif args.operation == "edit":
        print(json.dumps(edit(root, args.filepath, args.old, args.new)))
    elif args.operation == "test":
        print(json.dumps(test(root, args.target)))
    else:
        print(json.dumps(diff(root)))


if __name__ == "__main__":
    main()
