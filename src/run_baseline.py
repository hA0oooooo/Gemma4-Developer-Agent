"""Run the submitted minimal baseline with a real model on one issue.

Copy submission/, start vLLM, install task dependencies,
and invoke the official Evaluator. Budgets come from submission/eval_config.yaml;
the organizer's inference.py source is not available locally. See
agent/workflow/baseline.md for configuration and verification boundaries.
"""

import argparse
import ast
import asyncio
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import tarfile
import tomllib
from dataclasses import dataclass, fields
from pathlib import Path

import yaml
from packaging.requirements import Requirement

# Match the official offline environment before importing the serving SDK.
for name, value in {
    "TRANSFORMERS_NO_TF": "1", "TRANSFORMERS_NO_FLAX": "1",
    "TRANSFORMERS_OFFLINE": "1", "VLLM_NO_USAGE_STATS": "1",
    "VLLM_WORKER_MULTIPROC_METHOD": "spawn",
    "LITELLM_LOCAL_MODEL_COST_MAP": "True", "LITELLM_TELEMETRY": "False",
    "OTEL_SDK_DISABLED": "true", "OTEL_PYTHON_DISABLED": "true",
}.items():
    os.environ.setdefault(name, value)

from adk_submission import discover_adapters, validate_directory
from adk_submission.discovery import discover_declared_models
from adk_submission.errors import ServerStartupError
from adk_submission.limits import GenerationConstraints
from adk_submission.server import VllmConfig, VllmServer
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.apps._configs import EventsCompactionConfig
from local_sandbox import configure_local_sandbox
from swegemma.config import EvalConfig, build_submission_limits
from swegemma.evaluate import Evaluator

MODEL_NAMES = tuple(f"gemma-4-{size}-it-qat-w4a16-ct"
                    for size in ("31b", "12b", "e4b", "e2b"))


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


def legacy_runtime_requirements(path: Path) -> list[str]:
    """Read literal install_requires declarations without executing setup.py."""
    tree = ast.parse(path.read_text())
    bindings = {target.id: node.value for node in ast.walk(tree) if isinstance(node, ast.Assign)
                for target in node.targets if isinstance(target, ast.Name)}
    requirements = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
        if name != "setup":
            continue
        for keyword in node.keywords:
            if keyword.arg != "install_requires":
                continue
            value = bindings[keyword.value.id] if isinstance(keyword.value, ast.Name) else keyword.value
            for text in ast.literal_eval(value):
                requirement = Requirement(text)
                if requirement.marker is None or requirement.marker.evaluate():
                    requirements.append(requirement.name)
    return requirements


def provision_test_deps(data: Path, task_id: str, workdir: Path) -> dict:
    """Resolve the offline dependency plan; installs occur in each task venv."""
    wheels = data / "wheels"
    source = workdir / "repo-source"
    source.mkdir(parents=True, exist_ok=True)
    with tarfile.open(data / "snapshots" / f"{task_id}.tgz") as archive:
        archive.extractall(source, filter="tar")
    workspace = find_workspace(source)
    setup = load_sandbox_setup(data)
    declared = setup.collect_from_pyproject(workspace / "pyproject.toml")
    declared += setup.collect_from_requirements_files(workspace)
    metadata = tomllib.loads((workspace / "pyproject.toml").read_text())
    profile_path = os.environ.get("GEMMA_TASK_ENV_PROFILE")
    profile = json.loads(Path(profile_path).read_text()) if profile_path else None
    if profile:
        if (workspace / "setup.py").exists():
            declared += legacy_runtime_requirements(workspace / "setup.py")
        poetry = metadata.get("tool", {}).get("poetry", {})
        declared += list(poetry.get("dependencies", {}))
        declared += list(poetry.get("dev-dependencies", {}))
        for name in ("dev", "test", "tests"):
            declared += list(poetry.get("group", {}).get(name, {}).get("dependencies", {}))
        for filename in ("requirements-dev.txt", "requirements-test.txt", "requirements-tests.txt"):
            requirements = workspace / filename
            if requirements.exists():
                for line in requirements.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith(("#", "-")):
                        requirement = Requirement(line.split(" #", 1)[0])
                        if requirement.marker is None or requirement.marker.evaluate():
                            declared.append(requirement.name)
    groups = metadata.get("dependency-groups", {})

    def add_group(name):
        for item in groups.get(name, []):
            if isinstance(item, str):
                requirement = Requirement(item)
                if requirement.marker is None or requirement.marker.evaluate():
                    declared.append(requirement.name)
            else:
                add_group(item["include-group"])

    add_group("tests")
    declared.append("pytest")
    available = setup.get_available_packages(wheels_dir=wheels)
    supplementary_dir = data.parent / "local-wheels"
    supplementary = (setup.get_available_packages(wheels_dir=supplementary_dir)
                     if supplementary_dir.exists() else {})
    resolved = sorted({
        available[setup.normalize_pkg_name(dep)]
        for dep in declared
        if setup.normalize_pkg_name(dep) in available
    })
    # Install by name in each task venv so pip chooses compatible wheels;
    # the official dedup list can pick cp313 builds that py3.12 rejects.
    requested = sorted({
        setup.normalize_pkg_name(dep)
        for dep in declared
        if (setup.normalize_pkg_name(dep) in available or setup.normalize_pkg_name(dep) in supplementary
            or profile and setup.normalize_pkg_name(dep) in profile["baseline_root_package_versions"])
    })
    if profile:
        versions = profile["baseline_root_package_versions"]
        requested = [name + "==" + versions[name] if name in versions else name
                     for name in requested]
    shutil.rmtree(source)
    return {
        "workspace": str(workspace),
        "declared": sorted(set(declared)),
        "requested_packages": requested,
        "official_dedup_wheels": resolved,
        "supplementary_wheels_dir": str(supplementary_dir) if supplementary else None,
        "pip_exit_code": None,
        "install_scope": "planned_task_venv",
        **({"task_environment_profile": profile["name"],
            "task_environment_profile_sha256": hashlib.sha256(Path(profile_path).read_bytes()).hexdigest(),
            "constraints_path": str(Path(profile_path).with_name("isolated-declared-constraints.txt")),
            "system_site_packages": False} if profile else {}),
    }


def baseline_runtime(sample: Path) -> dict:
    """Use the same small budgets locally and in the submitted config."""
    return yaml.safe_load((sample / "eval_config.yaml").read_text())["evaluation"]


def driver_library_dir(data: Path) -> str:
    """Use a user-level NVML library only when it matches the loaded kernel."""
    kernel = Path("/proc/driver/nvidia/version")
    compat = data.parent / "nvidia"
    if kernel.is_file():
        version = re.search(r"\b\d{3}\.\d+\.\d+\b", kernel.read_text())
        library = compat / "libnvidia-ml.so.1"
        if version and library.is_file() and library.resolve().name.endswith(version.group()):
            return str(compat)
    return "/usr/local/nvidia/lib64"


def prepare_agent_config(output: Path, source: Path | None = None,
                         model_name: str | None = None) -> Path:
    """Copy the editable baseline used by the submission package."""
    sample = output / "agent-config"
    source = source or Path(__file__).resolve().parents[1] / "submission"
    if sample.exists():
        shutil.rmtree(sample)
    shutil.copytree(source, sample, dirs_exist_ok=True)
    # Change only the development copy, as in the official starter Notebook.
    if model_name is not None:
        for path in sample.rglob("*.yaml"):
            content = path.read_text()
            content = re.sub(r"^(\s*model:\s*).*$", rf"\g<1>{model_name}",
                             content, flags=re.MULTILINE)
            if model_name != MODEL_NAMES[0]:
                content = re.sub(r"^\s*adapter:\s*.*\n?", "", content,
                                 flags=re.MULTILINE)
            path.write_text(content)
        if model_name != MODEL_NAMES[0]:
            shutil.rmtree(sample / "adapters", ignore_errors=True)
    validate_directory(sample)
    return sample


@dataclass
class _ExecutionSeedConstraints(GenerationConstraints):
    """Apply the planned local seed to every compiler-created LLM agent."""

    execution_seed: int = 0

    def validate_config(self, config_dict, agent_name):
        seeded = dict(config_dict)
        seeded["seed"] = self.execution_seed
        return super().validate_config(seeded, agent_name)


def execution_seed_constraints(seed):
    """Preserve SDK constraints while overriding only the local execution seed."""
    if seed is None:
        return None
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("Execution seed must be an integer or None")
    _, original = build_submission_limits()
    values = {field.name: getattr(original, field.name)
              for field in fields(GenerationConstraints)}
    # The compiler consults defaults when an agent has no generation config.
    values["defaults"] = dict(original.defaults, seed=seed)
    return _ExecutionSeedConstraints(**values, execution_seed=seed)


def prepare_case(args):
    """Freeze one development config and record its exact inputs."""
    seed = getattr(args, "seed", None)
    execution_seed_constraints(seed)  # Reject invalid seeds before touching a case.
    args.output.mkdir(parents=True, exist_ok=True)
    if not (args.model / "config.json").is_file():
        raise FileNotFoundError(f"Model input is not mounted: {args.model}")
    sample = prepare_agent_config(args.output, args.agent_dir, args.model_name)
    declared = discover_declared_models(sample)
    if len(declared) != 1 or not declared.issubset(MODEL_NAMES):
        raise ValueError(f"Expected one supported model, got {sorted(declared)}")
    model_name = next(iter(declared))
    adapters = discover_adapters(sample, adapter_extensions={".safetensors"})
    runtime = baseline_runtime(sample)

    protocol = {
        "task_id": args.task_id,
        "model": str(args.model),
        "model_name": model_name,
        "mode": "development-evaluation",
        "budget": {k: runtime[k] for k in
                   ("max_time_minutes", "max_tool_calls", "max_turns", "timeout_seconds")},
        "tensor_parallel_size": args.tensor_parallel_size,
        "server_port": getattr(args, "port", 8000),
        "evaluation_concurrency": getattr(args, "concurrency", 1),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "max_num_seqs": 16,
        "sandbox": "subprocess",
        "source_imports": "checkout src and root",
        "task_dependencies_scope": "task_venv",
        "graph_dir": str(args.data / "graphs"),
        "embeddings_dir": str(args.data / "embeddings"),
        "wheels_dir": str(args.data / "wheels"),
        "startup_timeout": 1800,
        "enforce_eager": not getattr(args, "compiled_execution", False),
        "prefix_caching": not getattr(args, "disable_prefix_cache", False),
        "max_model_len": 32768,
        "nvidia_lib_dir": driver_library_dir(args.data),
        "context_cache": {"min_tokens": 2048, "ttl_seconds": 1800,
                          "cache_intervals": 10},
        "events_compaction": {"compaction_interval": 15, "overlap_size": 2,
                              "token_threshold": 14336, "event_retention_size": 5},
        "agent_config": str((args.agent_dir or
                             Path(__file__).resolve().parents[1] / "submission").resolve()),
        "seed": seed,
        "generation_seed_override": ({"seed": seed,
            "scope": "all compiler-created LlmAgents, including subagents and AgentTools; "
                     "not SDK background summarizer requests"} if seed is not None else None),
        "config_sha256": {str(p.relative_to(sample)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(sample.rglob("*")) if p.is_file()},
        "packages": {p: importlib.metadata.version(p) for p in
                     ["swegemma", "adk-submission", "adk-eval-core", "google-adk",
                      "google-genai", "vllm", "transformers", "torch"]},
    }
    (args.output / "protocol.json").write_text(json.dumps(protocol, indent=2))
    return sample, model_name, adapters, runtime


def create_server(args, model_name, adapters):
    """Use one local serving profile; eager execution remains the default."""
    adapter_map = adapters.adapters or {}
    ranks = [info.rank for info in adapter_map.values() if info.rank]
    return VllmServer(VllmConfig(
        model=str(args.model), tensor_parallel_size=args.tensor_parallel_size,
        port=getattr(args, "port", 8000),
        tool_call_parser="gemma4", reasoning_parser="gemma4",
        default_chat_template_kwargs={"enable_thinking": True},
        dtype="auto", max_model_len=32768,
        enable_lora=bool(adapter_map), max_loras=max(1, len(adapter_map)),
        max_lora_rank=max(ranks) if ranks else 128,
        gpu_memory_utilization=0.80,
        startup_timeout=1800,
        nvidia_lib_dir=driver_library_dir(args.data),
        extra_args=["--served-model-name", model_name,
                    "--max-num-seqs", "16",
                    *([] if getattr(args, "compiled_execution", False) else ["--enforce-eager"]),
                    *(["--no-enable-prefix-caching"] if getattr(args, "disable_prefix_cache", False) else []),
                    *(["--hf-overrides", '{"architectures": ["Gemma4ForCausalLM"], '
                       '"model_type": "gemma4"}'] if "-12b-" in model_name else [])],
    ), adapter_manifest=adapters)


async def evaluate_case(args, sample, adapters, runtime, models):
    """Create fresh task sandboxes even when the inference server is reused."""
    test_deps = provision_test_deps(args.data, args.task_id, args.output)
    (args.output / "test_deps.json").write_text(json.dumps(test_deps, indent=2))
    config = EvalConfig(
        tasks_path=args.data / "tasks.jsonl",
        snapshots_dir=args.data / "snapshots",
        submission_dir=sample, results_dir=args.output / "evaluation",
        models=models, adapter_manifest=adapters, sandbox="subprocess",
        generation_constraints=execution_seed_constraints(getattr(args, "seed", None)),
        wheels_dir=args.data / "wheels", task_ids=[args.task_id],
        graph_dir=str(args.data / "graphs"),
        embeddings_dir=str(args.data / "embeddings"),
        context_cache_config=ContextCacheConfig(
            min_tokens=2048, ttl_seconds=1800, cache_intervals=10),
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=15, overlap_size=2,
            token_threshold=14336, event_retention_size=5),
        display_mode="quiet", **runtime,
    )
    evaluator = Evaluator(config)
    configure_local_sandbox(evaluator.sandbox, args.output,
                            wheels=args.data / "wheels", dependencies=test_deps)
    return await evaluator.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task-id", default="fastapi_15661")
    parser.add_argument("--agent-dir", type=Path)
    parser.add_argument("--model-name", choices=MODEL_NAMES)
    parser.add_argument("--tensor-parallel-size", type=int, default=4)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    args.data = args.data.resolve()
    args.model = args.model.resolve()
    args.output = args.output.resolve()
    sample, model_name, adapters, runtime = prepare_case(args)
    server = create_server(args, model_name, adapters)
    try:
        server.start()
        models = server.create_model_registry(
            aliases={model_name: model_name}, model_prefix="openai/",
            api_key=os.environ.get("LOCAL_API_KEY", "EMPTY"),
        )
        result = asyncio.run(evaluate_case(args, sample, adapters, runtime, models))
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
