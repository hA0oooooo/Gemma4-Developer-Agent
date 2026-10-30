"""Exercise bounded case scheduling without inference or competition fixtures."""

import argparse
import asyncio
import contextlib
import io
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import run_experiments


async def check(workers):
    active = peak = 0

    async def evaluate(current, *_):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.02)
        destination = current.output / "evaluation/task_results.jsonl"
        destination.parent.mkdir(parents=True)
        destination.write_text(json.dumps({"resolved": True, "error": None, "duration_seconds": 0.02}))
        active -= 1

    def audit(command, **_):
        destination = Path(command[command.index("--output") + 1])
        destination.mkdir()
        (destination / "summary.json").write_text(json.dumps({
            "resolved": True, "junit_saved": True, "test_exit_code": 0}))

    with tempfile.TemporaryDirectory(prefix="gemma_case_schedule_") as directory:
        output = Path(directory)
        prepared = []
        for index in range(4):
            current = argparse.Namespace(output=output / str(index), seed=index, task_id=f"invented-{index}")
            prepared.append((current, None, None, None))
        report = {"cases": []}
        with patch.object(run_experiments, "evaluate_case", evaluate), \
                patch.object(run_experiments.subprocess, "run", audit), \
                contextlib.redirect_stdout(io.StringIO()):
            await run_experiments.run_cases(prepared, None, report, output, workers)
        assert peak == workers
        assert report["peak_active_cases"] == workers
        assert len(report["cases"]) == 4
        assert len({case["output"] for case in report["cases"]}) == 4
        assert all(case["resolved"] == case["audited_resolved"] for case in report["cases"])
        assert report["evaluation_wall_seconds"] > 0


async def main():
    for workers in [1, 2, 4]:
        await check(workers)
    print("Three bounded schedules passed on invented cases; not a model result")


if __name__ == "__main__":
    asyncio.run(main())
