"""Summarize completed local cases from their frozen plan, raw traces and JUnit."""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


def snapshot_teardown_coverage(tests):
    """Coverage only: retain outcomes, remove paired duplicate snapshot error records."""
    identity = lambda t: (t.get("classname", ""), t.get("name", ""))
    failed = Counter(identity(t) for t in tests if t.find("failure") is not None)
    retained, duplicates = [], 0
    for test in tests:
        error = test.find("error")
        paired = (error is not None and test.find("failure") is None
                  and test.find("skipped") is None and failed[identity(test)] > 0
                  and error.get("message", "").startswith("failed on teardown with")
                  and "some snapshots in this test have incorrect values." in "".join(error.itertext()))
        if paired:
            failed[identity(test)] -= 1
            duplicates += 1
        else:
            retained.append(test)
    text = re.sub(r"/tmp/swegemma_sandbox_[^/]+/workspace/", "/workspace/",
                  json.dumps(sorted(identity(t) for t in retained), sort_keys=True))
    return {"junit_snapshot_teardown_normalized_case_names_sha256": hashlib.sha256(text.encode()).hexdigest() if tests else None,
            "junit_snapshot_teardown_duplicate_records": duplicates}


def source_syntax_collection_evidence(tests, patch_paths):
    """Identify failed collection in actually patched Python implementation files."""
    errors = [t.find("error") for t in tests if t.find("error") is not None]
    paths = []
    for error in errors:
        text = "".join(error.itertext())
        files = re.findall(r'File "[^"\n]*/workspace/([^"\n]+)", line \d+', text)
        if (error.get("message") != "collection failure" or not files
                or not re.search(r"(?:SyntaxError|IndentationError|TabError):", text)):
            return {"patch_source_syntax_collection_failure": False}
        path = files[-1]
        if (path not in patch_paths or not path.endswith(".py")
                or {"test", "tests"}.intersection(Path(path).parts)
                or Path(path).name.startswith("test_") or Path(path).name == "conftest.py"):
            return {"patch_source_syntax_collection_failure": False}
        paths.append(path)
    return {"patch_source_syntax_collection_failure": bool(errors),
            "syntax_failure_patched_source_paths": sorted(set(paths))}


def analyze_case(directory, case):
    result = json.loads((directory / "evaluation/task_results.jsonl").read_text().splitlines()[-1])
    audit = json.loads((directory / "audit/summary.json").read_text())
    protocol = json.loads((directory / "protocol.json").read_text())
    trace = json.loads((directory / "evaluation/traces" / f"trace_{case['task_id']}.json").read_text())
    calls = [c for s in trace["steps"] for c in s.get("tool_calls", [])]
    signatures = [json.dumps([c["function_name"], c.get("arguments", {})], sort_keys=True) for c in calls]
    argument_errors = sum("mandatory input parameters" in str(s.get("observation", ""))
                          or "INVALID_ARGUMENTS" in str(s.get("observation", "")) for s in trace["steps"])
    junit = directory / "audit/junit.xml"
    tests = list(ET.parse(junit).getroot().iter("testcase")) if junit.exists() else []
    identities = sorted((t.get("classname", ""), t.get("name", "")) for t in tests)
    identities = re.sub(r"/tmp/swegemma_sandbox_[^/]+/workspace/", "/workspace/",
                        json.dumps(identities, sort_keys=True))
    failures = sum(t.find("failure") is not None for t in tests)
    errors = sum(t.find("error") is not None for t in tests)
    skipped = sum(t.find("skipped") is not None for t in tests)
    passed = len(tests) - failures - errors - skipped
    patch = directory / "evaluation/patches" / f"{case['task_id']}.patch"
    paths = [line[6:] for line in patch.read_text().splitlines()
             if line.startswith("+++ b/")] if patch.exists() else []
    test_paths = [p for p in paths if {"test", "tests"}.intersection(Path(p).parts)
                  or (Path(p).name.startswith("test_") and Path(p).suffix == ".py")
                  or Path(p).name.endswith("_test.py") or Path(p).name == "conftest.py"]
    runner_paths = [p for p in paths if Path(p).name in {"pytest.ini", "tox.ini", "sitecustomize.py"}
                    or Path(p).name.startswith((".adk_exec_", "_swegemma"))]
    artifact_ok = patch.exists() and patch.stat().st_size > 0 and result["agent_patch_size"] > 0
    verified = (artifact_ok and not test_paths and not runner_paths
                and result["resolved"] and audit["resolved"] and audit["test_exit_code"] == 0
                and audit["error"] is None and passed > 0 and failures == 0 and errors == 0)
    return {
        "label": case["label"], "task_id": case["task_id"], "seed": case.get("seed"),
        "resolved": result["resolved"], "independently_verified": bool(verified),
        "verifier_agreement": result["resolved"] == audit["resolved"],
        "native_test_exit_code": result["test_exit_code"],
        "audit_test_exit_code": audit["test_exit_code"],
        "audit_resolved": audit["resolved"],
        "agent_seconds": result["duration_seconds"], "agent_error": result["error"],
        "task_seconds": result["duration_seconds"],
        "trace_elapsed_seconds": max((s.get("extra", {}).get("elapsed_s", 0)
                                      for s in trace["steps"]), default=0),
        "tool_budget_count": result["tool_calls"], "trace_interactions": len(calls),
        "identical_call_repeats": len(signatures) - len(set(signatures)),
        "steps_with_invalid_arguments": argument_errors,
        "calls_with_quoted_argument_keys": sum(
            any(key.endswith(('"', "'")) for key in c.get("arguments", {})) for c in calls),
        "calls_by_author": dict(Counter(c.get("extra", {}).get("author", "unknown") for c in calls)),
        "harness_continuation_nudges": sum(
            s.get("extra", {}).get("event_type") == "continuation_nudge" for s in trace["steps"]),
        "calls_by_tool": dict(Counter(c["function_name"] for c in calls)),
        "agent_transfers": [c.get("arguments", {}).get("agent_name") for c in calls
                            if c["function_name"] == "transfer_to_agent"],
        "recorded_model_calls_by_author": {
            author: sum(s.get("llm_call_count", 0) for s in trace["steps"]
                        if s.get("extra", {}).get("author", "unknown") == author)
            for author in {s.get("extra", {}).get("author", "unknown") for s in trace["steps"]
                           if s.get("llm_call_count", 0)}},
        "tokens": trace["final_metrics"], "patch_bytes": result["agent_patch_size"],
        "patch_files": paths, "test_like_patch_paths": test_paths,
        "verification_sensitive_patch_paths": runner_paths,
        "nonempty_patch_artifact": artifact_ok,
        "junit": {"cases": len(tests), "passed": passed, "failures": failures,
                  "errors": errors, "skipped": skipped},
        "junit_case_names_sha256": hashlib.sha256(identities.encode()).hexdigest() if tests else None,
        "junit_skipped_case_names": json.loads(re.sub(r"/tmp/swegemma_sandbox_[^/]+/workspace/", "/workspace/",
            json.dumps(sorted((t.get("classname", ""), t.get("name", ""))
                              for t in tests if t.find("skipped") is not None)))),
        **source_syntax_collection_evidence(tests, paths),
        **snapshot_teardown_coverage(tests),
        "actual_seed": protocol.get("seed"), "model": protocol["model_name"],
        "config_sha256": protocol.get("config_sha256"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    plan = json.loads((args.run_dir / "plan.json").read_text())
    rows = []
    for case in plan:
        directory = args.run_dir / case["label"] / case["task_id"]
        if (directory / "audit/summary.json").exists():
            rows.append(analyze_case(directory, case))
    report = {"planned_cases": len(plan), "completed_cases": len(rows),
              "complete_plan": len(rows) == len(plan),
              "time_scope": "task_seconds and legacy agent_seconds are native TaskResult duration, including native verification; trace elapsed is a separate trace clock, not an exact active-agent timer",
              "independently_verified": sum(r["independently_verified"] for r in rows),
              "official_score_claimed": False, "cases": rows}
    (args.run_dir / "analysis.json").write_text(json.dumps(report, indent=2))
    print(f"Analyzed {len(rows)}/{len(plan)} cases; {report['independently_verified']} independently verified")


if __name__ == "__main__":
    main()
