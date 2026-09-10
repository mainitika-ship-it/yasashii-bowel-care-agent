import json
from types import SimpleNamespace

import pytest

import agent
import local_model
from demo import run_demo
from execution import EventRun
from report_view import render_report
from test_qc_policy import make_event
from test_strands_integration import ScriptedModel


def local_metadata(**changes):
    result = {"details": {"format": "gguf"}, "capabilities": ["completion", "tools"],
              "model_info": {"general.parameter_count": 8_000_000_000}}
    result.update(changes)
    return result


@pytest.mark.parametrize("name", [None, "", "gpt:cloud", "gpt:120b-cloud", "https://remote/model", "model with spaces"])
def test_explicit_local_model_name_required(name):
    with pytest.raises(ValueError):
        local_model.validate_model_id(name)


@pytest.mark.parametrize("metadata", [
    local_metadata(remote_model="some-model"), local_metadata(remote_host="https://remote"),
    local_metadata(capabilities=["vision", "completion"]),
    local_metadata(capabilities="nottools"), local_metadata(capabilities={"tools": True}),
    local_metadata(model_info={}), local_metadata(details={}),
    local_metadata(model_info=[]), local_metadata(details="not an object"),
])
def test_remote_or_non_tool_model_is_rejected(metadata):
    with pytest.raises(ValueError):
        local_model.validate_local_metadata(metadata, "installed-model:8b")


def test_metadata_success_does_not_claim_inference():
    result = local_model.validate_local_metadata(local_metadata(), "installed-model:8b")
    assert result["tools_supported"]
    assert not result["inference_called"] and not result["bedrock_called"]


def test_local_client_configuration_never_uses_proxy_or_remote_host(monkeypatch):
    monkeypatch.setattr(local_model, "inspect_local_model", lambda model: {})
    import strands.models.ollama
    captured = {}
    monkeypatch.setattr(strands.models.ollama, "OllamaModel", lambda **kwargs: captured.update(kwargs))
    local_model.build_local_model("installed-model:8b")
    assert captured["host"] == "http://127.0.0.1:11434"
    assert captured["ollama_client_args"]["trust_env"] is False
    assert captured["ollama_client_args"]["follow_redirects"] is False
    assert captured["max_tokens"] == 512


def test_metadata_http_check_is_loopback_read_only(monkeypatch):
    requests = []
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, limit): return json.dumps(local_metadata()).encode()
    def opened(request, timeout):
        requests.append(request)
        return Response()
    monkeypatch.setattr(local_model, "build_opener", lambda *args: SimpleNamespace(open=opened))
    local_model.inspect_local_model("installed-model:8b")
    assert len(requests) == 1
    assert requests[0].full_url == "http://127.0.0.1:11434/api/show"
    assert json.loads(requests[0].data) == {"model": "installed-model:8b"}


def test_installed_sdk_accepts_local_model_configuration(monkeypatch):
    monkeypatch.setattr(local_model, "inspect_local_model", lambda model: {})
    model = local_model.build_local_model("installed-model:8b")
    assert model.get_config()["model_id"] == "installed-model:8b"
    assert model.get_config()["max_tokens"] == 512


def test_model_error_does_not_fall_back_to_paid_bedrock(tmp_path, monkeypatch):
    def blocked(*args): raise ValueError("local model unavailable")
    monkeypatch.setattr(local_model, "build_local_model", blocked)
    monkeypatch.setattr("strands.models.BedrockModel", lambda **kwargs: pytest.fail("paid fallback"))
    report = run_demo("live", runtime_dir=tmp_path, provider="ollama", model_id="installed-model:8b")
    assert not report["verified"] and not report["is_live_agent_evidence"]
    assert report["cases"][0]["bedrock_called"] is False


def test_privacy_stop_bypasses_local_model_as_well(tmp_path, monkeypatch):
    monkeypatch.setattr(local_model, "build_local_model", lambda *args: pytest.fail("privacy leak"))
    receipt = agent.run_live_event(EventRun(make_event(contains_personal_data=True), tmp_path), provider="ollama")
    assert receipt["verified"] and receipt["model_called"] is False


def test_real_strands_loop_with_scripted_local_provider(tmp_path, monkeypatch):
    # This verifies routing/SDK wiring only, not an actual Ollama inference.
    actions = iter(["record_observation", "request_caregiver_confirmation", "stop_and_check_signal"])
    monkeypatch.setattr(local_model, "build_local_model", lambda model: ScriptedModel(next(actions)))
    monkeypatch.setattr("strands.models.BedrockModel", lambda **kwargs: pytest.fail("AWS must not be used"))
    report = run_demo("live", runtime_dir=tmp_path, provider="ollama", model_id="installed-model:8b")
    assert report["verified"] and report["is_live_agent_evidence"]
    assert report["is_live_evidence"] is False  # Legacy field is Bedrock-only.
    assert all(c["bedrock_called"] is False and c["model_called"] is True for c in report["cases"])
    html = render_report(report)
    assert "Live local model via Strands" in html and "AWSにつないだ実行" not in html


def test_redirect_is_rejected():
    with pytest.raises(ValueError, match="redirect"):
        local_model.NoRedirect().redirect_request(None, None, 302, "", {}, "https://remote")
