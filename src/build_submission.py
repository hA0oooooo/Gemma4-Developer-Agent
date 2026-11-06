"""Validate the declarative baseline and package it at the archive root."""

import argparse
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")

from adk_submission import validate_directory
from adk_submission.discovery import discover_declared_models
from swegemma.config import build_submission_limits

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "submission")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    limits, _ = build_submission_limits()
    validate_directory(source, limits)
    models = discover_declared_models(source)
    assert len(models) == 1 and models.issubset({
        f"gemma-4-{size}-it-qat-w4a16-ct" for size in ("31b", "12b", "e4b", "e2b")
    })
    target = args.output.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source).as_posix())
    print(target)


if __name__ == "__main__":
    main()
