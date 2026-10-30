"""Exercise comparison gates with synthetic metadata, not agent-quality evidence."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def fixture(root):
    plan, rows = [], []
    for task in ["synthetic_a", "synthetic_b"]:
        for seed in [17, 29]:
            for group in ["control", "candidate"]:
                label = f"{group}/seed-{seed}"
                plan.append({"label": label, "task_id": task, "seed": seed})
                rows.append({"label": label, "task_id": task, "seed": seed,
                             "actual_seed": seed, "verifier_agreement": True,
                             "independently_verified": True, "task_seconds": 2 if group == "control" else 1,
                             "tokens": {"total_tokens": 100 if group == "control" else 80},
                             "junit_case_names_sha256": "synthetic-suite",
                             "trace_interactions": 4 if group == "control" else 3})
                save(root / label / task / "protocol.json", {
                    "model_name": "synthetic-model", "tensor_parallel_size": 1,
                    "config_sha256": {"prompts/system.md": group},
                    "budget": {"max_tool_calls": 32},
                })
    return plan, rows


def compare(root, plan, rows, *, changed_file="prompts/system.md", allow_budget=False):
    save(root / "plan.json", plan)
    save(root / "analysis.json", {"cases": rows})
    output = root / "comparison.json"
    command = [sys.executable, str(Path(__file__).with_name("compare_runs.py")),
               "--runs", str(root), "--control", "control", "--candidate", "candidate",
               "--changed-file", changed_file, "--output", str(output)]
    if allow_budget:
        command += ["--budget-field", "max_tool_calls"]
    result = subprocess.run(command, text=True, capture_output=True)
    return result, json.loads(output.read_text()) if result.returncode == 0 else None


checks = []
with tempfile.TemporaryDirectory(prefix="gemma-comparison-fixtures-") as directory:
    for scenario in ["complete", "quality-win", "regression", "missing", "runtime-mismatch",
                     "unexpected-change", "one-seed", "duplicate", "seed-mismatch",
                     "non-cartesian", "allowed-budget", "unallowed-budget", "junit-mismatch",
                     "concurrency-mismatch", "prefix-cache-mismatch", "harness-incompatible"]:
        root = Path(directory) / scenario
        plan, rows = fixture(root)
        if scenario == "quality-win":
            rows[0]["independently_verified"] = False
        elif scenario == "harness-incompatible":
            rows[0]["independently_verified"] = False
            rows[0]["agent_error"] = "Sandbox execution error: No LlmAgent model available for event compaction summarizer."
        elif scenario == "regression":
            rows[1]["independently_verified"] = False
        elif scenario == "missing":
            rows.pop(1)
        elif scenario in ["runtime-mismatch", "unexpected-change"]:
            target = root / rows[1]["label"] / rows[1]["task_id"] / "protocol.json"
            protocol = json.loads(target.read_text())
            if scenario == "runtime-mismatch":
                protocol["tensor_parallel_size"] = 4
            else:
                protocol["config_sha256"]["other.yaml"] = "changed"
            save(target, protocol)
        elif scenario == "one-seed":
            plan = [c for c in plan if c["seed"] == 17]
            rows = [c for c in rows if c["seed"] == 17]
        elif scenario == "duplicate":
            rows.append(rows[0])
        elif scenario == "seed-mismatch":
            rows[1]["actual_seed"] = 7
        elif scenario == "junit-mismatch":
            rows[1]["junit_case_names_sha256"] = "different-suite"
        elif scenario == "concurrency-mismatch":
            target = root / rows[1]["label"] / rows[1]["task_id"] / "protocol.json"
            protocol = json.loads(target.read_text())
            protocol["evaluation_concurrency"] = 2
            save(target, protocol)
        elif scenario == "prefix-cache-mismatch":
            for case in rows:
                target = root / case["label"] / case["task_id"] / "protocol.json"
                protocol = json.loads(target.read_text())
                protocol["prefix_caching"] = not case["label"].startswith("candidate/")
                save(target, protocol)
        elif scenario == "non-cartesian":
            for case in plan:
                if case["task_id"] == "synthetic_b" and case["seed"] == 29:
                    case["task_id"] = "synthetic_c"
            for case in rows:
                if case["task_id"] == "synthetic_b" and case["seed"] == 29:
                    previous = root / case["label"] / case["task_id"] / "protocol.json"
                    protocol = json.loads(previous.read_text())
                    case["task_id"] = "synthetic_c"
                    save(root / case["label"] / case["task_id"] / "protocol.json", protocol)
        elif scenario in ["allowed-budget", "unallowed-budget"]:
            for case in rows:
                target = root / case["label"] / case["task_id"] / "protocol.json"
                protocol = json.loads(target.read_text())
                group = case["label"].split("/")[0]
                protocol["config_sha256"] = {"eval_config.yaml": group}
                protocol["budget"]["max_tool_calls"] = 8 if group == "candidate" else 32
                save(target, protocol)
        result, report = compare(root, plan, rows,
                                 changed_file="eval_config.yaml" if "budget" in scenario else "prompts/system.md",
                                 allow_budget=scenario == "allowed-budget")
        if scenario == "duplicate":
            assert result.returncode != 0 and "Ambiguous repeated condition" in result.stderr
        elif scenario in ["complete", "allowed-budget"]:
            assert report["complete_controlled_comparison"] and report["local_efficiency_signal"]
        elif scenario == "quality-win":
            assert report["local_quality_signal"] and not report["local_efficiency_signal"]
        else:
            assert not report["local_quality_signal"] and not report["local_efficiency_signal"]
        checks.append(scenario)
print(f"Passed {len(checks)} metadata-gate checks; not a model experiment")
