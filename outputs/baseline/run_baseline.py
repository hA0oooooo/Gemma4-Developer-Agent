"""Run the official sample_submission as a clean baseline on one issue.

The agent is the unchanged official sample: prompts, tools, sub_agents and
configs/sampling.yaml (temperature 0.2, top_p 0.95, max_output_tokens 16384,
thinking_budget 4096) are used exactly as shipped. The runtime matches the
organizer's scripts/inference.py (HARNESS_README section 7): budgets of
60 minutes / 100 tool calls / 500 turns / 300 s per command, automatic events
compaction (EventsCompactionConfig) and prefix caching (ContextCacheConfig),
plus the ModelRetryPlugin that agent_runner always enables. Budgets are applied
through EvalConfig at runtime; the sample's own eval_config.yaml smoke values
(1 min / 10 calls / 50 turns) are left untouched and are not read by this path.

The only deviations from the official sample are plumbing required to self-run
inside a Kaggle notebook; none of them change the agent:

1. The vLLM server is started here with the mounted model and its LoRA adapters,
   because scripts/inference.py (which normally serves the model and builds the
   runtime) is not shipped to competitors.
2. graph_dir / embeddings_dir point at the competition input (absolute) instead
   of the relative data/graphs / data/embeddings defaults, so the code-graph
   tools and the code_analyzer sub-agent resolve.
3. Test dependencies are provisioned into the host interpreter, because
   install_test_dependencies returns immediately for the subprocess sandbox and
   would leave pytest unavailable in Phase 2. SubprocessManager.exec overwrites
   PYTHONPATH with the workspace, so the sandbox venv inherits these packages
   through system_site_packages=True. Provisioning runs after the model server
   has started so the inference stack keeps the versions it loaded.

Deployment-only settings that do not change the agent: startup_timeout is 1800 s
and vLLM runs with --enforce-eager (a cold node once took 611 s just to load
weights, so CUDA-graph capture blew the 900 s health-check budget).
"""

import argparse
import asyncio
import importlib.metadata
import importlib.util
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

from adk_submission import discover_adapters, validate_directory
from adk_submission.errors import ServerStartupError
from adk_submission.server import VllmConfig, VllmServer
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.apps._configs import EventsCompactionConfig
from swegemma.config import EvalConfig
from swegemma.evaluate import Evaluator
from swegemma.models import setup_gemma_model_registry


def load_sandbox_setup(data: Path):
    """Import the official sandbox/setup.py resolver without modifying it."""
    spec = importlib.util.spec_from_file_location(
        "official_sandbox_setup", data / "sandbox" / "setup.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_workspace(source: Path) -> Path:
    """Locates the extracted repository root that carries the packaging metadata."""
    for candidate in [source, *sorted(source.iterdir())]:
        if (candidate / "pyproject.toml").exists() or (candidate / "setup.py").exists():
            return candidate
    raise FileNotFoundError(f"No packaging metadata under {source}")


def provision_test_deps(data: Path, task_id: str, workdir: Path) -> dict:
    """Installs the task's declared test dependencies into the host interpreter."""
    wheels = data / "wheels"
    source = workdir / "repo-source"
    source.mkdir(parents=True, exist_ok=True)
    with tarfile.open(data / "snapshots" / f"{task_id}.tgz") as archive:
        archive.extractall(source, filter="tar")
    workspace = find_workspace(source)
    setup = load_sandbox_setup(data)
    declared = setup.collect_from_pyproject(workspace / "pyproject.toml")
    declared += setup.collect_from_requirements_files(workspace)
    declared.append("pytest")
    available = setup.get_available_packages(wheels_dir=wheels)
    resolved = sorted({
        available[setup.normalize_pkg_name(dep)]
        for dep in declared
        if setup.normalize_pkg_name(dep) in available
    })
    # Installed by name so pip selects wheels compatible with this interpreter;
    # the official dedup list can pick cp313 builds that py3.12 rejects.
    requested = sorted({
        setup.normalize_pkg_name(dep)
        for dep in declared
        if setup.normalize_pkg_name(dep) in available
    })
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-index",
         f"--find-links={wheels}", "--no-build-isolation",
         *requested],
        capture_output=True, text=True,
    )
    return {
        "workspace": str(workspace),
        "declared": sorted(set(declared)),
        "requested_packages": requested,
        "official_dedup_wheels": resolved,
        "pip_exit_code": result.returncode,
        "pip_stdout_tail": result.stdout[-1000:],
        "pip_stderr_tail": result.stderr[-1000:],
    }


def official_runtime() -> dict:
    """inference.py-equivalent runtime: official budgets, compaction, caching."""
    return {
        "max_time_minutes": 60,
        "max_tool_calls": 100,
        "max_turns": 500,
        "timeout_seconds": 300,
        "events_compaction_config": EventsCompactionConfig(
            compaction_interval=5, overlap_size=2,
            token_threshold=14336, event_retention_size=5,
        ),
        "context_cache_config": ContextCacheConfig(
            min_tokens=2048, ttl_seconds=1800, cache_intervals=10,
        ),
    }


def prepare_agent_config(data: Path, output: Path) -> Path:
    """Copy the official sample_submission unchanged (no prompt/sampling edits)."""
    sample = output / "agent-config"
    shutil.copytree(data / "sample_submission", sample, dirs_exist_ok=True)
    validate_directory(sample)
    return sample


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task-id", default="fastapi_15661")
    parser.add_argument("--tensor-parallel-size", type=int, default=4)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if not (args.model / "config.json").is_file():
        raise FileNotFoundError(f"Model input is not mounted: {args.model}")
    sample = prepare_agent_config(args.data, args.output)
    adapters = discover_adapters(sample, adapter_extensions={".safetensors"})
    runtime = official_runtime()

    protocol = {
        "task_id": args.task_id,
        "model": str(args.model),
        "mode": "official-baseline",
        "budget": {k: runtime[k] for k in
                   ("max_time_minutes", "max_tool_calls", "max_turns", "timeout_seconds")},
        "events_compaction": {"compaction_interval": 5, "overlap_size": 2,
                              "token_threshold": 14336, "event_retention_size": 5},
        "context_cache": {"min_tokens": 2048, "ttl_seconds": 1800, "cache_intervals": 10},
        "tensor_parallel_size": args.tensor_parallel_size,
        "max_num_seqs": 16,
        "sandbox": "subprocess",
        "graph_dir": str(args.data / "graphs"),
        "embeddings_dir": str(args.data / "embeddings"),
        "wheels_dir": str(args.data / "wheels"),
        "startup_timeout": 1800,
        "enforce_eager": True,
        "max_model_len": 32768,
        "agent_config": "official sample_submission, prompts and sampling unchanged",
        "packages": {p: importlib.metadata.version(p) for p in
                     ["swegemma", "adk-submission", "adk-eval-core", "google-adk",
                      "google-genai", "vllm", "transformers", "torch"]},
    }
    (args.output / "protocol.json").write_text(json.dumps(protocol, indent=2))
    server = VllmServer(VllmConfig(
        model=str(args.model), tensor_parallel_size=args.tensor_parallel_size,
        tool_call_parser="gemma4", reasoning_parser="gemma4",
        default_chat_template_kwargs={"enable_thinking": True},
        dtype="auto", max_model_len=32768, max_loras=8,
        gpu_memory_utilization=0.80,
        startup_timeout=1800,
        extra_args=["--served-model-name", "gemma-4-31b-it-qat-w4a16-ct",
                    "--max-num-seqs", "16", "--enforce-eager"],
    ), adapter_manifest=adapters)
    try:
        server.start()
        models = setup_gemma_model_registry(
            api_base=server.base_url, served_model="gemma-4-31b-it-qat-w4a16-ct",
            adapter_manifest=adapters,
        )
        test_deps = provision_test_deps(args.data, args.task_id, args.output)
        (args.output / "test_deps.json").write_text(json.dumps(test_deps, indent=2))
        # The extracted repo copy is ~300MB and bloats the kernel output ZIP,
        # which truncates downloads and hides test_deps.json/submission.zip.
        shutil.rmtree(args.output / "repo-source", ignore_errors=True)
        config = EvalConfig(
            tasks_path=args.data / "tasks.jsonl",
            snapshots_dir=args.data / "snapshots",
            submission_dir=sample, results_dir=args.output / "evaluation",
            models=models, adapter_manifest=adapters, sandbox="subprocess",
            wheels_dir=args.data / "wheels", task_ids=[args.task_id],
            graph_dir=str(args.data / "graphs"),
            embeddings_dir=str(args.data / "embeddings"),
            display_mode="quiet", **runtime,
        )
        result = asyncio.run(Evaluator(config).run())
        print(f"Evaluated {result.total} issue(s), resolved {result.resolved}")
        shutil.make_archive(str(args.output / "submission"), "zip", sample)
    except ServerStartupError as error:
        (args.output / "model_server.log").write_text(str(error))
        raise
    finally:
        try:
            log_path = Path(server.log_path)
            if log_path.exists():
                shutil.copy2(log_path, args.output / "model_server.log")
        finally:
            server.stop()


if __name__ == "__main__":
    main()
