"""Download the packaging Notebook output and verify the submission contents."""

import subprocess
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / "output" / "deployment"
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(ROOT / ".venv/bin/kaggle"), "kernels", "output",
                    "haoimba/gemma4-developer-agent", "-p", str(target), "--force"], check=True)
    with ZipFile(target / "submission.zip") as archive:
        assert archive.testzip() is None
        expected = {p.relative_to(ROOT / "submission").as_posix(): p.read_bytes()
                    for p in (ROOT / "submission").rglob("*") if p.is_file()}
        assert set(archive.namelist()) == set(expected)
        for name, content in expected.items():
            assert archive.read(name) == content, f"Deployed config differs: {name}"
    print(f"Verified deployed submission: {target / 'submission.zip'}")


if __name__ == "__main__":
    main()
