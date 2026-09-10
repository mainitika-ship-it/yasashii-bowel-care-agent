"""Build an allowlisted, history-free archive for a dedicated public repository.

This does not create repositories, publish files, or change Devpost.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from qc_policy import ObservationEvent

# Explicit names, not directory globs: newly added local files never publish silently.
PUBLIC_FILES = (
    ".gitignore", "LICENSE", "README.md", "README_JA.md", "requirements.txt", "requirements-dev.txt",
    "docs/architecture.md", "docs/demo_storyboard.md", "docs/publication_safety.md",
    "docs/qc_method.md", "docs/submission_readiness.md", "docs/repository_transfer.md",
    "docs/verification_2026-09-10.md",
    "sample_data/bad_signal_event.json", "sample_data/high_confidence_event.json",
    "sample_data/sample_event.json", "sample_data/uncertain_event.json",
    "src/agent.py", "src/bedrock_preflight.py", "src/demo.py", "src/execution.py",
    "src/handoff.py", "src/model_config.py", "src/qc_policy.py", "src/report_view.py",
    "tests/conftest.py", "tests/test_demo.py", "tests/test_execution.py",
    "tests/test_export_submission.py", "tests/test_handoff.py", "tests/test_model_config.py",
    "tests/test_preflight.py", "tests/test_qc_policy.py", "tests/test_strands_integration.py", "tests/test_report_view.py",
    "tools/export_submission.py", "tools/standalone-ci.yml",
)
SECRET_PATTERN = re.compile(
    rb"(?:AKIA|ASIA)[A-Z0-9]{16}|gh[pousr]_[A-Za-z0-9]{20,}|"
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)


def export_submission(output: str | Path, project_root: Path = PROJECT_ROOT) -> dict:
    root = project_root.resolve()
    files: dict[str, bytes] = {}
    for relative in PUBLIC_FILES:
        path = root / relative
        # Refuse symlinks even when their target happens to be inside the project.
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            raise ValueError("public archive inputs must not be symlinks")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f"missing or unsafe public file: {relative}")
        data = path.read_bytes()
        if len(data) > 1_000_000 or SECRET_PATTERN.search(data):
            raise ValueError(f"publication review required for: {relative}")
        if relative.startswith("sample_data/"):
            event = ObservationEvent.from_dict(json.loads(data))
            if event.source != "simulated_test_data" or event.contains_personal_data:
                raise ValueError("only synthetic samples belong in the public archive")
        files[relative] = data
    if b"Yasashii Bowel Care Agent" not in files["README.md"]:
        raise ValueError("root README must identify this project")
    if not files["LICENSE"].startswith(b"MIT License"):
        raise ValueError("root MIT license is missing")
    files[".github/workflows/ci.yml"] = files["tools/standalone-ci.yml"]
    manifest = {"schema_version": 1, "files_sha256": {
        name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())
    }, "note": "Source packaging only; this is not live Bedrock or submission evidence."}
    files["PUBLIC_MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    output = Path(output)
    if output.suffix != ".zip":
        raise ValueError("output must be a .zip file")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive create: never replace an existing archive without review.
    with ZipFile(output, "x", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            archive.writestr(name, data)
    return {"archive": str(output), "file_count": len(files), "published": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dist/yasashii-bowel-care-agent.zip")
    args = parser.parse_args()
    print(json.dumps(export_submission(args.output), indent=2))


if __name__ == "__main__":
    main()
