"""Use checkout imports and retain native JUnit without changing SDK class identity."""

import json
import shlex
import shutil


def configure_local_sandbox(manager, output, *, wheels=None, dependencies=None):
    output.mkdir(parents=True, exist_ok=True)
    execute = manager.exec
    start = manager.start
    stop = manager.stop
    installs = []
    if dependencies is not None and "system_site_packages" in dependencies:
        manager.system_site_packages = dependencies["system_site_packages"]

    def prepare_environment():
        sandbox_id = start()
        if dependencies is not None:
            extra = dependencies.get("supplementary_wheels_dir")
            extra_links = f"--find-links={shlex.quote(extra)} " if extra else ""
            constraint = dependencies.get("constraints_path")
            constraints = f"--constraint={shlex.quote(constraint)} " if constraint else ""
            command = (
                "python3 -m pip install --no-index --no-build-isolation "
                f"--find-links={shlex.quote(str(wheels))} "
                + extra_links
                + constraints
                + shlex.join(dependencies["requested_packages"])
            )
            result = execute(sandbox_id, command, timeout=300)
            installs.append({
                "sandbox_id": sandbox_id, "pip_exit_code": result.exit_code,
                "pip_stdout_tail": result.stdout[-1000:],
                "pip_stderr_tail": result.stderr[-1000:],
            })
            if result.exit_code == 0:
                inventory = execute(sandbox_id, "python3 -m pip list --format=json", timeout=30)
                installs[-1]["installed_packages_exit_code"] = inventory.exit_code
                installs[-1]["installed_packages"] = json.loads(inventory.stdout)
            report = dict(dependencies, sandbox_installs=installs,
                          pip_exit_code=max(x["pip_exit_code"] for x in installs),
                          install_scope="task_venv")
            (output / "test_deps.json").write_text(json.dumps(report, indent=2))
            if result.exit_code:
                stop(sandbox_id)
                raise RuntimeError("Task dependency installation failed; see test_deps.json")
        return sandbox_id

    def execute_checkout(sandbox_id, command, *, timeout=None):
        # The SDK translates /workspace to each sandbox's real directory.
        # Its subprocess fast path skips editable installs, so src layouts
        # otherwise import the host's installed package during verification.
        prefix = "export PYTHONPATH=/workspace/src:/workspace; "
        return execute(sandbox_id, prefix + command, timeout=timeout)

    def retain_junit(sandbox_id):
        paths = manager.sandboxes.get(sandbox_id)
        try:
            if paths:
                for report in paths["tmp"].glob("_swegemma_junit_*.xml"):
                    shutil.copy2(report, output / "junit.xml")
        finally:
            stop(sandbox_id)

    # Subclassing changes exact-class checks in the official setup routines.
    # Attach local adapters without changing the native manager's identity.
    manager.exec = execute_checkout
    manager.start = prepare_environment
    manager.stop = retain_junit
    return manager
