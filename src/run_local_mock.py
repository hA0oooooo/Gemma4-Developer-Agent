"""Validate the official two-phase harness locally with a scripted stub model.

Runs the submitted minimal agent configuration against one published
task with `sandbox=subprocess` and a stub OpenAI-compatible endpoint. It proves
harness plumbing only: agent loop, tool execution, patch extraction, clean-copy
verification and artifact layout. It is not a model result and must never be
reported as a baseline score.
"""

import argparse
import asyncio
from pathlib import Path

from adk_submission import discover_adapters
from adk_submission.discovery import discover_declared_models
from adk_submission.registry import ModelRegistry
from google.adk.models.lite_llm import LiteLlm
from local_sandbox import configure_local_sandbox
from mock_model_server import serve
from run_baseline import baseline_runtime, prepare_agent_config, provision_test_deps
from swegemma.config import EvalConfig
from swegemma.evaluate import Evaluator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data/competition"))
    parser.add_argument("--output", type=Path, default=Path("output/local-check"))
    parser.add_argument("--task-id", default="fastapi_15661")
    args = parser.parse_args()
    args.data = args.data.resolve()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    sample = prepare_agent_config(args.output)
    adapters = discover_adapters(sample, adapter_extensions={".safetensors"})
    server, base_url = serve()
    models = ModelRegistry()
    for name in discover_declared_models(sample):
        models.register(name, LiteLlm(model="openai/mock", api_base=base_url,
                                     api_key="EMPTY"))
    config = EvalConfig(
        tasks_path=args.data / "tasks.jsonl",
        snapshots_dir=args.data / "snapshots",
        submission_dir=sample, results_dir=args.output / "evaluation",
        models=models, adapter_manifest=adapters, sandbox="subprocess",
        wheels_dir=args.data / "wheels", graph_dir=str(args.data / "graphs"),
        embeddings_dir=str(args.data / "embeddings"),
        task_ids=[args.task_id], display_mode="quiet",
        **baseline_runtime(sample),
    )
    try:
        evaluator = Evaluator(config)
        dependencies = provision_test_deps(args.data, args.task_id, args.output)
        configure_local_sandbox(evaluator.sandbox, args.output,
                                wheels=args.data / "wheels", dependencies=dependencies)
        result = asyncio.run(evaluator.run())
    finally:
        server.shutdown()
    print(f"total={result.total} resolved={result.resolved}")


if __name__ == "__main__":
    main()
