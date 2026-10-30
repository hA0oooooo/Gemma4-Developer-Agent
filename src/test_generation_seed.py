"""Local plan seeds reach inline/default/included agents without YAML rewrites."""
import asyncio
from dataclasses import fields
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import ClassVar
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from adk_submission.compiler import compile_submission
from adk_submission.errors import SubmissionValidationError
from adk_submission.limits import GenerationConstraints
from adk_submission.registry import ModelRegistry
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import run_baseline as baseline

MODEL = baseline.MODEL_NAMES[0]


class RecordingModel(BaseLlm):
    seen: ClassVar[list] = []

    async def generate_content_async(self, llm_request, stream=False):
        role = str(llm_request.config.system_instruction).split("ROLE_", 1)[1].split()[0]
        previous = sum(row["role"] == role for row in self.seen)
        self.seen.append(dict(role=role, config=llm_request.config.model_dump(exclude_none=True)))
        if role == "primary" and previous == 0:
            part = types.Part.from_function_call(name="helper", args={"request": "Check the fixture."})
        else:
            part = types.Part.from_text(text="CPU fixture done")
        yield LlmResponse(content=types.Content(role="model", parts=[part]))


def fixture(root):
    source = root / "source"
    (source / "configs").mkdir(parents=True)
    (source / "agent.yaml").write_text("agent_class: SequentialAgent\nname: sequence\nsub_agents:\n"
        "  - config_path: primary.yaml\n  - config_path: included.yaml\n")
    (source / "primary.yaml").write_text(f"name: primary\nmodel: {MODEL}\ninstruction: ROLE_primary\n"
        "tools:\n  - agent_tool:\n      config_path: helper.yaml\n      skip_summarization: false\n")
    (source / "helper.yaml").write_text(f"name: helper\nmodel: {MODEL}\ninstruction: ROLE_helper\n"
        "generate_content_config:\n  seed: 599\n  temperature: 0.3\n  max_output_tokens: 512\n"
        "  thinking_config:\n    thinking_budget: 128\n    include_thoughts: true\n")
    (source / "included.yaml").write_text(f"name: included\nmodel: {MODEL}\ninstruction: ROLE_included\n"
        "generate_content_config: !include configs/nonstandard.yaml\n")
    (source / "configs/nonstandard.yaml").write_text("# Preserve this comment\nseed: 788\n"
        "temperature: 0.2\nmax_output_tokens: 1024\nthinking_config:\n  thinking_budget: 256\n")
    # This valid YAML is not a generation config and must not acquire a seed.
    (source / "configs/resource.yaml").write_text("- unrelated\n- resource\n")
    (source / "eval_config.yaml").write_text("evaluation:\n  max_time_minutes: 5\n"
        "  max_tool_calls: 24\n  max_turns: 40\n  timeout_seconds: 60\n")
    return source


def arguments(root, source, seed):
    model = root / "model-metadata"
    model.mkdir(exist_ok=True)
    (model / "config.json").write_text("{}")
    return SimpleNamespace(output=root / "case", model=model, agent_dir=source,
        model_name=MODEL, task_id="self-authored-fixture", tensor_parallel_size=1,
        data=root / "unused-data", seed=seed)


class SeedConstraintTests(unittest.TestCase):
    def test_invalid_seed_is_rejected_before_creating_case(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            for value in [True, False, 1.5, "17"]:
                with self.subTest(seed=value):
                    args = arguments(root, fixture(root) if not (root / "source").exists()
                                     else root / "source", value)
                    with self.assertRaises(ValueError):
                        baseline.prepare_case(args)
                    self.assertFalse(args.output.exists())

    def test_unspecified_seed_keeps_sdk_default_path(self):
        self.assertIsNone(baseline.execution_seed_constraints(None))

    def test_sdk_bounds_and_defaults_are_preserved(self):
        _, original = baseline.build_submission_limits()
        constrained = baseline.execution_seed_constraints(17)
        for field in fields(GenerationConstraints):
            if field.name != "defaults":
                self.assertEqual(getattr(constrained, field.name), getattr(original, field.name))
        self.assertEqual({k: v for k, v in constrained.defaults.items() if k != "seed"},
                         {k: v for k, v in original.defaults.items() if k != "seed"})
        self.assertEqual(constrained.validate_config({"seed": 599}, "fixture")["seed"], 17)
        self.assertNotEqual(original.defaults.get("seed"), 17)
        if original.max_output_tokens is not None:
            with self.assertRaises(SubmissionValidationError):
                constrained.validate_config({"max_output_tokens": original.max_output_tokens.max + 1}, "fixture")

    def test_prepare_preserves_every_source_file_and_records_override(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = fixture(root)
            before = {str(p.relative_to(source)): p.read_bytes() for p in source.rglob("*") if p.is_file()}
            args = arguments(root, source, 17)
            sample, _, _, _ = baseline.prepare_case(args)
            self.assertEqual(before, {str(p.relative_to(source)): p.read_bytes()
                                     for p in source.rglob("*") if p.is_file()})
            self.assertEqual(before, {str(p.relative_to(sample)): p.read_bytes()
                                     for p in sample.rglob("*") if p.is_file()})
            protocol = json.loads((args.output / "protocol.json").read_text())
            self.assertEqual(protocol["seed"], 17)
            self.assertEqual(protocol["generation_seed_override"]["seed"], 17)
            self.assertIn("not SDK background", protocol["generation_seed_override"]["scope"])


class SeedRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def run_fixture(self, source, seed):
        RecordingModel.seen.clear()
        model = RecordingModel(model="synthetic_cpu_only")
        registry = ModelRegistry()
        registry.register(MODEL, model)
        # EvalConfig supplies SDK defaults when the local seed is unspecified.
        constraints = baseline.execution_seed_constraints(seed)
        if constraints is None:
            _, constraints = baseline.build_submission_limits()
        agent = compile_submission(source, {}, registry, generation_constraints=constraints)
        sessions = InMemorySessionService()
        session = await sessions.create_session(app_name="seed_qualification", user_id="fixture")
        runner = Runner(agent=agent, app_name="seed_qualification", session_service=sessions)

        async def consume():
            return [event async for event in runner.run_async(user_id="fixture", session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part.from_text(text="Self-authored fixture")]))]
        await asyncio.wait_for(consume(), timeout=10)
        self.assertEqual([r["role"] for r in model.seen], ["primary", "helper", "primary", "included"])
        return list(model.seen)

    async def test_actual_requests_seed_inline_included_and_omitted_configs(self):
        with TemporaryDirectory() as temp:
            source = fixture(Path(temp))
            original = await self.run_fixture(source, None)
            seeded = await self.run_fixture(source, 17)
            self.assertEqual([r["config"].get("seed") for r in original], [None, 599, None, 788])
            self.assertEqual([r["config"]["seed"] for r in seeded], [17, 17, 17, 17])
            for before, after in zip(original, seeded):
                for field in ["temperature", "top_p", "max_output_tokens", "thinking_config"]:
                    self.assertEqual(before["config"].get(field), after["config"].get(field))

    async def test_core_evaluator_receives_the_plan_seed_constraints(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            args = arguments(root, fixture(root), 17)
            args.output.mkdir()
            fake_evaluator = MagicMock()
            fake_evaluator.run = AsyncMock(return_value="CPU")
            with patch.object(baseline, "provision_test_deps", return_value={}), \
                    patch.object(baseline, "Evaluator", return_value=fake_evaluator) as constructor, \
                    patch.object(baseline, "configure_local_sandbox"):
                result = await baseline.evaluate_case(args, args.agent_dir, None,
                    dict(max_time_minutes=5, max_tool_calls=24, max_turns=40, timeout_seconds=60), ModelRegistry())
            self.assertEqual(result, "CPU")
            config = constructor.call_args.args[0]
            self.assertEqual(config.generation_constraints.validate_config({"seed": 999}, "fixture")["seed"], 17)
            self.assertEqual(config.budget.tool_calls, 24)
            self.assertEqual(config.budget.time_minutes, 5)
            self.assertEqual(config.budget.turns, 40)
            self.assertEqual(config.harness.command_timeout_seconds, 60)


if __name__ == "__main__":
    unittest.main()
