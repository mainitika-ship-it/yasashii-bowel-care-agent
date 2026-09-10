import json
import shlex
from types import SimpleNamespace

import pytest

import check_local_setup as setup


def mock_response(monkeypatch, data):
    requests = []
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, limit): return json.dumps(data).encode()
    def opened(request, timeout):
        requests.append(request)
        return Response()
    monkeypatch.setattr(setup, "build_opener", lambda *args: SimpleNamespace(open=opened))
    return requests


def test_discovery_only_reads_loopback_metadata_and_filters_unsafe_names(monkeypatch):
    requests = mock_response(monkeypatch, {"models": [
        {"name": "installed:8b"}, {"name": "installed:8b"},
        {"name": "remote:cloud"}, {"name": "x;touch /tmp/unwanted"}, {},
    ]})
    assert setup.discover_models() == (["installed:8b"], 3)
    assert len(requests) == 1
    assert requests[0].full_url == "http://127.0.0.1:11434/api/tags"
    assert requests[0].get_method() == "GET" and requests[0].data is None


@pytest.mark.parametrize("data", [[], {}, {"models": "incorrect"}])
def test_malformed_list_does_not_claim_success(monkeypatch, data):
    mock_response(monkeypatch, data)
    with pytest.raises(ValueError):
        setup.discover_models()


def test_discovery_is_bounded_and_reports_unchecked_models(monkeypatch):
    mock_response(monkeypatch, {"models": [{"name": f"model{i}:8b"} for i in range(12)]})
    names, skipped = setup.discover_models()
    assert len(names) == setup.MAX_MODELS and skipped == 4


def test_shell_command_preserves_paths_with_spaces_and_rejects_injection(monkeypatch, tmp_path):
    root = tmp_path / "project with spaces"
    monkeypatch.setattr(setup, "ROOT", root)
    command = setup.demo_command("installed:8b", "/python with space/bin/python")
    assert shlex.split(command) == ["/python with space/bin/python", str(root / "src/demo.py"),
                                  "--mode", "live", "--provider", "ollama", "--model-id", "installed:8b"]
    with pytest.raises(ValueError):
        setup.demo_command("model$(touch x)")


def test_success_only_suggests_commands_and_does_not_claim_inference(monkeypatch, capsys):
    monkeypatch.setattr(setup, "missing_dependencies", lambda: [])
    monkeypatch.setattr(setup, "discover_models", lambda: (["installed:8b"], 0))
    checked = []
    monkeypatch.setattr(setup, "inspect_local_model", lambda name: checked.append(name))
    assert setup.main() == 0
    output = capsys.readouterr().out
    assert checked == ["installed:8b"]
    assert "--provider ollama" in output and "no inference" in output
    assert "--allow-paid-model" not in output


def test_connection_error_is_redacted_and_does_not_claim_success(monkeypatch, capsys):
    monkeypatch.setattr(setup, "missing_dependencies", lambda: [])
    def failed(): raise RuntimeError("PRIVATE_SYNTHETIC_MARKER")
    monkeypatch.setattr(setup, "discover_models", failed)
    assert setup.main() == 1
    output = capsys.readouterr().out
    assert "PRIVATE_SYNTHETIC_MARKER" not in output and "Model list unavailable" in output


def test_missing_packages_blocks_live_command(monkeypatch, capsys):
    monkeypatch.setattr(setup, "missing_dependencies", lambda: ["ollama"])
    monkeypatch.setattr(setup, "discover_models", lambda: (["installed:8b"], 0))
    monkeypatch.setattr(setup, "inspect_local_model", lambda name: {})
    assert setup.main() == 1
    output = capsys.readouterr().out
    assert "requirements-local.txt" in output and "--mode live" not in output
