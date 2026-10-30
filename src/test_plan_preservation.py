"""CLI-level plan provenance regressions without model or competition task execution."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import run_experiments as runner


class PlanPreservationTests(unittest.TestCase):
    def exercise(self, layout):
        with TemporaryDirectory(prefix="gemma_plan_identity_") as directory:
            root = Path(directory)
            output = root / "output"
            output.mkdir()
            destination = output / "plan.json"
            source = root / "frozen-input.json"
            cases = [{"label": "candidate/seed-17", "task_id": "invented-case",
                      "seed": 17, "agent_dir": str(root / "invented-config")}]
            original = (json.dumps(cases, indent=4) + "\n").encode()
            if layout == "same":
                source = destination
                source.write_bytes(original)
            elif layout == "symlink":
                destination.write_bytes(original)
                source.symlink_to(destination)
            elif layout == "hardlink":
                destination.write_bytes(original)
                source.hardlink_to(destination)
            else:
                source.write_bytes(original)
            before = source.stat()
            model = runner.MODEL_NAMES[0]
            server = MagicMock(log_path=str(root / "unused-server.log"))
            with patch.object(runner, "prepare_case", return_value=(root, model, SimpleNamespace(adapters={}), {})) as prepare, \
                    patch.object(runner, "create_server", return_value=server), \
                    patch.object(runner, "run_cases", new_callable=AsyncMock) as execute, \
                    patch.object(runner.sys, "argv", ["run_experiments.py", "--plan", str(source),
                        "--output", str(output), "--model", str(root / "unused-model")]):
                runner.main()
                prepare.assert_called_once()
                self.assertEqual(prepare.call_args.args[0].seed, 17)
                self.assertEqual(prepare.call_args.args[0].output, output / "candidate/seed-17/invented-case")
                server.start.assert_called_once()
                execute.assert_awaited_once()
                server.stop.assert_called_once()
            self.assertEqual(source.read_bytes(), original, "The frozen input bytes must never be reserialized")
            self.assertEqual(source.stat().st_mtime_ns, before.st_mtime_ns)
            self.assertEqual(source.stat().st_ino, before.st_ino)
            self.assertEqual(json.loads(destination.read_text()), cases)
            if layout != "separate":
                self.assertEqual(destination.read_bytes(), original)

    def test_input_in_output_directory_is_immutable(self):
        self.exercise("same")

    def test_symlink_to_input_is_not_rewritten(self):
        self.exercise("symlink")

    def test_hardlink_to_input_is_not_rewritten(self):
        self.exercise("hardlink")

    def test_separate_output_keeps_plan_artifact_and_input_bytes(self):
        self.exercise("separate")


if __name__ == "__main__":
    unittest.main()
