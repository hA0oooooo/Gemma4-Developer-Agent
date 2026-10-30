"""Run a frozen local experiment plan with one shared model and fresh task sandboxes."""

import argparse
import asyncio
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import psutil

from run_baseline import MODEL_NAMES, create_server, evaluate_case, prepare_case


def serving_metrics(port):
    names = {"prefix_cache_queries_total", "prefix_cache_hits_total",
             "request_prefill_time_seconds_sum", "request_decode_time_seconds_sum"}
    with urlopen(f"http://127.0.0.1:{port}/metrics", timeout=10) as response:
        source = response.read().decode()
    metrics = {}
    for name in names:
        values = re.findall(r"^vllm:" + name + r"(?:\{[^\n]*\})?\s+(\S+)$", source, re.MULTILINE)
        assert values, f"Expected serving counter missing: {name}"
        metrics[name] = sum(float(value) for value in values)
    return metrics


def check_shared_server(port, output):
    """Stop a batch after two failed health probes, without retrying model requests."""
    failures = []
    for _ in range(2):
        try:
            with urlopen(f"http://127.0.0.1:{port}/health", timeout=8) as response:
                if response.status != 200:
                    raise URLError("Unexpected health status")
            return
        except (URLError, TimeoutError, ConnectionError) as error:
            failures.append(type(error).__name__)
    (output / "server-health-error.json").write_text(json.dumps({
        "port": port, "failed_probes": failures, "model_request_retried": False,
        "scope": "Runtime service failure; remaining cases not started, not a strategy-quality result"}, indent=2))
    raise RuntimeError("Shared inference service failed two health probes; refusing the next model case")


def stop_shared_server(server):
    """Also stop only this API's known worker descendants after SDK shutdown."""
    children = []
    if server.process is not None:
        with contextlib.suppress(psutil.NoSuchProcess):
            children = psutil.Process(server.process.pid).children(recursive=True)
    try:
        server.stop()
    finally:
        for child in children:
            with contextlib.suppress(psutil.NoSuchProcess):
                child.terminate()
        _, alive = psutil.wait_procs(children, timeout=3)
        for child in alive:
            with contextlib.suppress(psutil.NoSuchProcess):
                child.kill()
        psutil.wait_procs(alive, timeout=3)


async def run_cases(prepared, models, report, output, concurrency=1, health_probe=None):
    slots = asyncio.Semaphore(concurrency)
    active = 0
    report["peak_active_cases"] = 0

    async def run_case(current, sample, adapters, runtime):
        if health_probe is not None:
            await asyncio.to_thread(health_probe)
        started = time.perf_counter()
        await evaluate_case(current, sample, adapters, runtime, models)
        patch = current.output / "evaluation/patches" / f"{current.task_id}.patch"
        command = [sys.executable, "src/check_patch.py", "--task-id", current.task_id,
                   "--output", str(current.output / "audit")]
        if patch.exists() and patch.stat().st_size:
            command += ["--patch", str(patch)]
        await asyncio.to_thread(subprocess.run, command, check=True)
        result = json.loads((current.output / "evaluation/task_results.jsonl")
                            .read_text().splitlines()[-1])
        audit = json.loads((current.output / "audit/summary.json").read_text())
        report["cases"].append({
            "output": str(current.output), "seed": current.seed,
            "task_id": current.task_id, "resolved": result["resolved"],
            "audited_resolved": audit["resolved"], "junit_saved": audit["junit_saved"],
            "test_exit_code": audit["test_exit_code"], "agent_error": result["error"],
            "agent_seconds": result["duration_seconds"],
            "case_wall_seconds": round(time.perf_counter() - started, 2),
        })
        (output / "summary.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report["cases"][-1]), flush=True)

    async def limited(case):
        nonlocal active
        async with slots:
            active += 1
            report["peak_active_cases"] = max(report["peak_active_cases"], active)
            try:
                await run_case(*case)
            finally:
                active -= 1

    started = time.perf_counter()
    await asyncio.gather(*(limited(case) for case in prepared))
    report["evaluation_wall_seconds"] = round(time.perf_counter() - started, 3)
    (output / "summary.json").write_text(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data/competition"))
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--model-name", choices=MODEL_NAMES, default=MODEL_NAMES[0])
    parser.add_argument("--tensor-parallel-size", type=int, default=4)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--concurrency", type=int, choices=(1, 2, 4), default=1)
    parser.add_argument("--compiled-execution", action="store_true",
                        help="Profile stock compilation/CUDA graphs locally instead of eager execution")
    parser.add_argument("--disable-prefix-cache", action="store_true",
                        help="Profile stock prefix-cache ablation locally; default stays enabled")
    parser.add_argument("--capture-service-metrics", action="store_true",
                        help="Save only aggregate serving counters after the frozen batch")
    parser.add_argument("--check-service-health", action="store_true",
                        help="Opt in to bounded health probes and owned worker cleanup between cases")
    args = parser.parse_args()
    args.data = args.data.resolve()
    args.model = args.model.resolve()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    cases = json.loads(args.plan.read_text())
    prepared = []
    for case in cases:
        values = dict(vars(args), task_id=case["task_id"],
                      agent_dir=Path(case["agent_dir"]).resolve(), seed=case.get("seed"))
        values["output"] = args.output / case["label"] / case["task_id"]
        current = argparse.Namespace(**values)
        if (current.output / "evaluation/task_results.jsonl").exists():
            raise FileExistsError(f"Refusing to overwrite {current.output}")
        sample, name, adapters, runtime = prepare_case(current)
        if name != args.model_name or adapters.adapters:
            raise ValueError("Batch experiments require one shared base model without adapters")
        prepared.append((current, sample, adapters, runtime))
    plan_output = args.output / "plan.json"
    # The caller may freeze the input in the output directory, including via an alias.
    if not (plan_output.exists() and args.plan.samefile(plan_output)):
        plan_output.write_text(json.dumps(cases, indent=2))
    server = create_server(args, args.model_name, prepared[0][2])
    report = {"mode": "local-research", "official_submission_created": False,
              "server_starts": 1, "fresh_task_sandboxes": True,
              "evaluation_concurrency": args.concurrency,
              "shared_server_health_guard": args.check_service_health, "cases": []}
    try:
        started = time.perf_counter()
        server.start()
        report["server_startup_seconds"] = round(time.perf_counter() - started, 2)
        models = server.create_model_registry(
            aliases={args.model_name: args.model_name}, model_prefix="openai/",
            api_key=os.environ.get("LOCAL_API_KEY", "EMPTY"),
        )
        health_probe = (lambda: check_shared_server(args.port, args.output)) if args.check_service_health else None
        asyncio.run(run_cases(prepared, models, report, args.output, args.concurrency, health_probe))
        if args.capture_service_metrics:
            receipt = {"port": args.port, "batch_complete": True,
                       "prefix_caching": not args.disable_prefix_cache,
                       "scope": "complete service since startup, not per-request attribution",
                       "metrics": serving_metrics(args.port)}
            (args.output / "serving-metrics.json").write_text(json.dumps(receipt, indent=2))
    finally:
        try:
            log = Path(server.log_path)
            if log.exists():
                shutil.copy2(log, args.output / "model_server.log")
        finally:
            if args.check_service_health:
                stop_shared_server(server)
            else:
                server.stop()


if __name__ == "__main__":
    main()
