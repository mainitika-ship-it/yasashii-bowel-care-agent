import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("export_submission", ROOT / "tools/export_submission.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


def copy_public_tree(destination):
    for name in exporter.PUBLIC_FILES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)


def test_archive_has_project_root_license_and_no_unlisted_files(tmp_path):
    root = tmp_path / "project"
    copy_public_tree(root)
    (root / ".env").write_text("DO_NOT_PUBLISH=synthetic_marker")
    (root / "private.txt").write_text("synthetic private marker")
    (root / "runtime").mkdir()
    (root / "runtime/event_log.jsonl").write_text("{}\n")
    archive_path = tmp_path / "export.zip"
    result = exporter.export_submission(archive_path, root)
    assert result["published"] is False
    with ZipFile(archive_path) as archive:
        expected = set(exporter.PUBLIC_FILES) | {".github/workflows/ci.yml", "PUBLIC_MANIFEST.json"}
        assert set(archive.namelist()) == expected
        assert archive.read("LICENSE").startswith(b"MIT License")
        assert b"Yasashii Bowel Care Agent" in archive.read("README.md")
        manifest = json.loads(archive.read("PUBLIC_MANIFEST.json"))
        for name, digest in manifest["files_sha256"].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest


def test_existing_archive_is_not_overwritten(tmp_path):
    output = tmp_path / "existing.zip"
    output.write_bytes(b"preserve")
    with pytest.raises(FileExistsError):
        exporter.export_submission(output)
    assert output.read_bytes() == b"preserve"


def test_symlink_is_not_exported(tmp_path):
    root = tmp_path / "project"
    copy_public_tree(root)
    (root / "README.md").unlink()
    (root / "README.md").symlink_to(ROOT / "README.md")
    with pytest.raises(ValueError, match="symlink"):
        exporter.export_submission(tmp_path / "blocked.zip", root)


def test_real_source_is_not_exported(tmp_path):
    root = tmp_path / "project"
    copy_public_tree(root)
    path = root / "sample_data/high_confidence_event.json"
    event = json.loads(path.read_text())
    event["source"] = "local_vision"
    path.write_text(json.dumps(event))
    with pytest.raises(ValueError, match="synthetic"):
        exporter.export_submission(tmp_path / "blocked.zip", root)
