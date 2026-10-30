"""Audit a patch, or a clean snapshot, with the official verifier and retain JUnit."""

import argparse
import asyncio
import json
import time
from pathlib import Path

from run_baseline import EvalConfig, provision_test_deps
from local_sandbox import configure_local_sandbox
from swegemma.harness.verification import verify_task
from swegemma.models import load_tasks
from swegemma.sandbox import SubprocessManager


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--patch", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = root / "data" / "competition"
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "junit.xml").unlink(missing_ok=True)
    task = next(t for t in load_tasks(data / "tasks.jsonl") if t.instance_id == args.task_id)
    patch = args.patch.read_text() if args.patch else ""
    config = EvalConfig(
        tasks_path=data / "tasks.jsonl", snapshots_dir=data / "snapshots",
        submission_dir=root / "submission", results_dir=output,
        wheels_dir=data / "wheels", models={}, sandbox="subprocess", display_mode="quiet",
        verification_timeout_seconds=300,
    )
    dependencies = provision_test_deps(data, args.task_id, output)
    sandbox = configure_local_sandbox(SubprocessManager(), output,
                                      wheels=data / "wheels", dependencies=dependencies)
    try:
        result = asyncio.run(verify_task(
            sandbox, config, task, data / "snapshots" / f"{args.task_id}.tgz",
            agent_patch=patch, start_time=time.perf_counter(),
        ))
    finally:
        sandbox.cleanup_all()
    (output / "test_output.log").write_text(result.test_output)
    summary = {
        "task_id": args.task_id, "patch": str(args.patch) if args.patch else None,
        "patch_size": len(patch.encode()), "resolved": result.resolved,
        "test_exit_code": result.test_exit_code, "error": result.error,
        "junit_saved": (output / "junit.xml").exists(),
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
