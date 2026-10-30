"""No-model checks for optional shared-service health and owned process cleanup."""

import asyncio
import contextlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch

import psutil
import run_experiments as runner


class ServiceGuardTests(unittest.TestCase):
    def test_healthy_first_probe(self):
        with TemporaryDirectory() as directory, patch.object(runner, "urlopen") as probe:
            probe.return_value.__enter__.return_value.status = 200
            runner.check_shared_server(8002, Path(directory))
            self.assertEqual(probe.call_count, 1)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_transient_failure_then_recovery(self):
        healthy = MagicMock()
        healthy.__enter__.return_value.status = 200
        with TemporaryDirectory() as directory, patch.object(runner, "urlopen", side_effect=[TimeoutError(), healthy]) as probe:
            runner.check_shared_server(8002, Path(directory))
            self.assertEqual(probe.call_count, 2)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_two_failures_record_metadata_and_abort(self):
        with TemporaryDirectory() as directory, patch.object(runner, "urlopen", side_effect=TimeoutError()) as probe:
            with self.assertRaisesRegex(RuntimeError, "refusing the next"):
                runner.check_shared_server(8002, Path(directory))
            self.assertEqual(probe.call_count, 2)
            receipt = json.loads((Path(directory) / "server-health-error.json").read_text())
            self.assertEqual(receipt["failed_probes"], ["TimeoutError", "TimeoutError"])
            self.assertFalse(receipt["model_request_retried"])

    def test_guard_precedes_model_evaluation(self):
        def unhealthy():
            raise RuntimeError("fixture-unhealthy")
        with TemporaryDirectory() as directory, patch.object(runner, "evaluate_case") as evaluate:
            with self.assertRaisesRegex(RuntimeError, "fixture-unhealthy"):
                asyncio.run(runner.run_cases([(None, None, None, None)], None,
                    {"cases": []}, Path(directory), health_probe=unhealthy))
            evaluate.assert_not_called()

    def test_worker_fallback_after_parent_shutdown(self):
        server = MagicMock()
        first, second = MagicMock(), MagicMock()
        with patch.object(runner.psutil, "Process") as process, patch.object(
                runner.psutil, "wait_procs", side_effect=[([first], [second]), ([second], [])]):
            process.return_value.children.return_value = [first, second]
            runner.stop_shared_server(server)
            server.stop.assert_called_once()
            first.terminate.assert_called_once()
            second.terminate.assert_called_once()
            first.kill.assert_not_called()
            second.kill.assert_called_once()

    def test_real_owned_cpu_child_cleanup(self):
        code = "import subprocess,sys,time; p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(120)']); print(p.pid,flush=True); time.sleep(120)"
        parent = subprocess.Popen([sys.executable, "-c", code], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, start_new_session=True)
        child = None
        try:
            child = psutil.Process(int(parent.stdout.readline()))
            server = MagicMock(process=parent)

            def stop_parent():
                parent.terminate()
                parent.wait(timeout=3)

            server.stop.side_effect = stop_parent
            runner.stop_shared_server(server)
            self.assertIsNotNone(parent.poll())
            self.assertTrue(not child.is_running() or child.status() == psutil.STATUS_ZOMBIE)
        finally:
            if parent.poll() is None:
                parent.kill()
                parent.wait(timeout=3)
            parent.stdout.close()
            if child is not None:
                with contextlib.suppress(psutil.NoSuchProcess):
                    child.kill()


if __name__ == "__main__":
    unittest.main()
