"""Optional local isolation must not silently change the default SDK profile."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from local_sandbox import configure_local_sandbox
from run_baseline import legacy_runtime_requirements


class FakeManager:
    def __init__(self):
        self.system_site_packages = True
        self.commands = []
        self.sandboxes = {}

    def start(self):
        return 'task'

    def stop(self, sandbox_id):
        pass

    def exec(self, sandbox_id, command, *, timeout=None):
        self.commands.append(command)
        stdout = '[{"name":"pytest","version":"9.1.1"}]' if 'pip list' in command else ''
        return SimpleNamespace(exit_code=0, stdout=stdout, stderr='')


class TaskEnvironmentTests(unittest.TestCase):
    def test_legacy_named_runtime_list_is_read_without_executing_setup(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'setup.py'
            path.write_text('raise RuntimeError("never execute")\n'
                'requires = ["urllib3>=1.21,<3", "idna>=2.5"]\nsetup(install_requires=requires)\n')
            self.assertEqual(legacy_runtime_requirements(path), ['urllib3', 'idna'])

    def test_legacy_inline_markers_and_undeclared_packages(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'setup.py'
            path.write_text('setup(install_requires=["certifi", "unused; python_version < \'2\'"])')
            self.assertEqual(legacy_runtime_requirements(path), ['certifi'])

    def test_no_profile_keeps_native_inheritance(self):
        with TemporaryDirectory() as tmp:
            manager = configure_local_sandbox(FakeManager(), Path(tmp))
            manager.start()
            self.assertTrue(manager.system_site_packages)

    def test_isolation_pins_and_inventory_are_recorded(self):
        with TemporaryDirectory() as tmp:
            deps = dict(system_site_packages=False, requested_packages=['pytest==9.1.1'],
                        task_environment_profile='isolated-baseline-root-versions')
            manager = configure_local_sandbox(FakeManager(), Path(tmp), wheels=Path('/wheels'),
                                               dependencies=deps)
            manager.start()
            report = json.loads((Path(tmp) / 'test_deps.json').read_text())
            self.assertFalse(manager.system_site_packages)
            self.assertIn('pytest==9.1.1', manager.commands[0])
            self.assertEqual(report['sandbox_installs'][0]['installed_packages'],
                             [dict(name='pytest', version='9.1.1')])
            self.assertEqual(report['pip_exit_code'], 0)


if __name__ == '__main__':
    unittest.main()
