"""Validate the declarative baseline and package it at the archive root."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from adk_submission import validate_directory
from swegemma.config import build_submission_limits
from swegemma.models.discovery import validate_single_declared_model

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / "submission"
    limits, _ = build_submission_limits()
    validate_directory(source, limits)
    assert validate_single_declared_model(source) == "gemma-4-31b-it-qat-w4a16-ct"
    target = ROOT / "output" / "submission.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source).as_posix())
    print(target)


if __name__ == "__main__":
    main()
