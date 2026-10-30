"""Audit existing patches in isolated official sandboxes, without model inference."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    assert len({(c["label"], c["task_id"]) for c in plan}) == len(plan)

    def run_case(case):
        output = (args.output / case["label"] / case["task_id"]).resolve()
        if (output / "summary.json").exists():
            raise FileExistsError(f"Refusing to overwrite {output}")
        command = [sys.executable, "src/check_patch.py", "--task-id", case["task_id"],
                   "--patch", case["patch"], "--output", str(output)]
        started = time.perf_counter()
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        result = json.loads((output / "summary.json").read_text())
        return dict(result, label=case["label"], source_model_seed=case.get("seed"),
                    output=str(output), wall_seconds=round(time.perf_counter() - started, 3))

    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(run_case, plan))
    report = {"new_inference_started": False, "workers": args.workers,
              "wall_seconds": round(time.perf_counter() - started, 3), "cases": results}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"audits": len(results), "workers": args.workers,
                      "wall_seconds": report["wall_seconds"]}))


if __name__ == "__main__":
    main()
