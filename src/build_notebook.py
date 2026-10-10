"""Generate a T4 GPU Notebook that produces the competition's submission.zip."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / "output" / "kaggle"
output.mkdir(parents=True, exist_ok=True)
files = {path.relative_to(ROOT / "submission").as_posix(): path.read_text()
         for path in sorted((ROOT / "submission").rglob("*")) if path.is_file()}
source = f'''from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

files = {files!r}
target = Path('/kaggle/working/submission.zip')
with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    for name, content in files.items():
        archive.writestr(name, content)
with ZipFile(target) as archive:
    assert 'agent.yaml' in archive.namelist()
    assert archive.testzip() is None
print(f'Created {{target}} ({{target.stat().st_size}} bytes)')
'''
notebook = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                 "name": "python3"}},
    "cells": [{"cell_type": "code", "id": "build-submission", "execution_count": None, "metadata": {},
               "output": [], "source": source.splitlines(keepends=True)}],
}
(output / "developer_agent.ipynb").write_text(json.dumps(notebook, indent=2))
(output / "kernel-metadata.json").write_text(json.dumps({
    "id": "haoimba/gemma4-developer-agent", "title": "gemma4-developer-agent",
    "code_file": "developer_agent.ipynb", "language": "python",
    "kernel_type": "notebook", "is_private": True,
    "enable_gpu": True, "machine_shape": "NvidiaTeslaT4", "enable_internet": False,
    "competition_sources": ["gemma-4-developer-agent"],
    "dataset_sources": [], "model_sources": [],
}, indent=2))
