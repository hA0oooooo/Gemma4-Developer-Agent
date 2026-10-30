"""Download official runtime, one task's inputs, and the selected Gemma model."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle_network import configure_kaggle_network

ROOT = Path(__file__).resolve().parents[1]
COMPETITION = "gemma-4-developer-agent"


def prepare_nvml(version):
    target = ROOT / "data" / "nvidia"
    library_name = f"libnvidia-ml.so.{version}"
    if (target / library_name).exists():
        return
    package_name = f"NVIDIA-Linux-x86_64-{version}-no-compat32.run"
    url = f"https://download.nvidia.com/XFree86/Linux-x86_64/{version}/{package_name}"
    with tempfile.TemporaryDirectory(prefix="gemma-nvml-") as folder:
        work = Path(folder)
        package = work / package_name
        with urllib.request.urlopen(url, timeout=60) as source, package.open("wb") as dest:
            shutil.copyfileobj(source, dest)
        with urllib.request.urlopen(url + ".sha256sum", timeout=60) as response:
            expected = re.search(r"[0-9a-fA-F]{64}", response.read().decode()).group().lower()
        with package.open("rb") as source:
            assert hashlib.file_digest(source, "sha256").hexdigest() == expected
        subprocess.run(["sh", str(package), "--extract-only", "--target",
                        str(work / "extracted")], check=True, stdout=subprocess.DEVNULL)
        library = next((work / "extracted").rglob(library_name))
        target.mkdir(exist_ok=True)
        shutil.copy2(library, target / library_name)
        link = target / "libnvidia-ml.so.1"
        link.unlink(missing_ok=True)
        link.symlink_to(library_name)


def main():
    configure_kaggle_network()
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", default="fastapi_15661")
    parser.add_argument("--model-name", default="gemma-4-12b-it-qat-w4a16-ct")
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--model-version", type=int, default=2)
    parser.add_argument("--task-only", action="store_true")
    parser.add_argument("--nvml-driver", help="Prepare matching user-level NVML only")
    args = parser.parse_args()
    if args.nvml_driver:
        prepare_nvml(args.nvml_driver)
        print("User-level NVML ready")
        return
    api = KaggleApi()
    data = ROOT / "data" / "competition"

    def authenticate():
        if not getattr(api, "_authenticated", False):
            api.authenticate()

    def download(name):
        target = data / name
        if not target.exists():
            authenticate()
            target.parent.mkdir(parents=True, exist_ok=True)
            api.competition_download_file(COMPETITION, name,
                                          path=str(target.parent), quiet=True)

    download("tasks.jsonl")
    task = next(json.loads(line) for line in (data / "tasks.jsonl").read_text().splitlines()
                if json.loads(line)["instance_id"] == args.task_id)
    prefix = task["repo"].split("/")[-1]
    stem = f"{prefix}_{task['base_commit']}"
    inputs = ["sandbox/setup.py", f"snapshots/{args.task_id}.tgz",
              f"graphs/{stem}.json", f"embeddings/{stem}.npz"]
    if not any((data / "wheels").glob("*.whl")):
        authenticate()
        token = None
        while True:
            response = api.competition_list_files(COMPETITION, page_size=200,
                                                 page_token=token)
            inputs.extend(f.name for f in response.files if f.name.startswith("wheels/"))
            token = response.next_page_token
            if not token:
                break
    if any(not (data / name).exists() for name in inputs):
        authenticate()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(download, inputs))

    if not args.task_only:
        wheelhouse = ROOT / "data" / "wheelhouse"
        if not (wheelhouse / "swegemma-0.2.11-py3-none-any.whl").exists():
            authenticate()
            api.dataset_download_files("metric/gemma-4-developer-agent-wheelhouse",
                                       path=str(wheelhouse), unzip=True, quiet=True)
        model = args.model_dir or ROOT / "data" / "models" / args.model_name.split("-")[2]
        source = f"google/gemma-4/Other/{args.model_name}/{args.model_version}"
        record = model / "source.json"
        if record.exists() and json.loads(record.read_text())["kaggle_model"] != source:
            raise ValueError("Model directory belongs to a different official input")
        if not (model / "config.json").exists():
            authenticate()
            model.mkdir(parents=True, exist_ok=True)
            record.write_text(json.dumps({"kaggle_model": source}, indent=2))
            cache = model / "download.part"
            configure_kaggle_network(download_cache=cache)
            api.model_instance_version_download(
                source,
                path=str(model), untar=True, quiet=True,
            )
            cache.unlink()
    print(f"Official inputs ready for {args.task_id}")


if __name__ == "__main__":
    main()
