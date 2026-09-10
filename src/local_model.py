"""Opt-in local Ollama route for Strands; no downloads or cloud fallback."""
from __future__ import annotations

import argparse
import json
import re
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

LOCAL_HOST = "http://127.0.0.1:11434"


def validate_model_id(model_id: str | None) -> str:
    if not isinstance(model_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/:\-]{0,119}", model_id):
        raise ValueError("choose an explicitly named, already installed local model")
    if "cloud" in model_id.lower() or "://" in model_id:
        raise ValueError("cloud models are not permitted by the local route")
    return model_id


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("local model checks must not follow redirects")


def inspect_local_model(model_id: str) -> dict:
    """Read model metadata only: no prompt, generation, pull, or account login."""
    model_id = validate_model_id(model_id)
    request = Request(
        LOCAL_HOST + "/api/show",
        data=json.dumps({"model": model_id}).encode(),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    # Explicit numeric loopback, no proxy environment, no HTTP redirects.
    opener = build_opener(ProxyHandler({}), NoRedirect())
    with opener.open(request, timeout=10) as response:
        payload = response.read(2_000_001)
    if len(payload) > 2_000_000:
        raise ValueError("model metadata exceeds the local check limit")
    return validate_local_metadata(json.loads(payload), model_id)


def validate_local_metadata(metadata: dict, model_id: str) -> dict:
    if not isinstance(metadata, dict):
        raise ValueError("model metadata must be an object")
    if metadata.get("remote_model") or metadata.get("remote_host"):
        raise ValueError("this model forwards requests to a remote host")
    details = metadata.get("details") or {}
    info = metadata.get("model_info") or {}
    if not isinstance(details, dict) or not isinstance(info, dict):
        raise ValueError("local model details are missing")
    parameters = info.get("general.parameter_count")
    if details.get("format") != "gguf" or type(parameters) is not int or parameters <= 0:
        raise ValueError("local model weights could not be verified from metadata")
    capabilities = metadata.get("capabilities")
    if not isinstance(capabilities, list) or "tools" not in capabilities:
        raise ValueError("the selected model does not advertise tool calling")
    return {"model_id": model_id, "local_metadata_ok": True, "tools_supported": True,
            "inference_called": False, "bedrock_called": False}


def build_local_model(model_id: str):
    inspect_local_model(model_id)  # Recheck immediately before each event.
    from strands.models.ollama import OllamaModel
    return OllamaModel(
        host=LOCAL_HOST, model_id=model_id, temperature=0.0, max_tokens=512,
        ollama_client_args={"trust_env": False, "timeout": 120, "follow_redirects": False},
        keep_alive="0s",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a local model without generating tokens.")
    parser.add_argument("--model-id", required=True)
    args = parser.parse_args()
    try:
        result = inspect_local_model(args.model_id)
    except Exception as exc:
        print(json.dumps({"local_metadata_ok": False, "error_type": type(exc).__name__,
                          "next": "Check local Ollama and an installed tool-capable model; no model was downloaded."}))
        raise SystemExit(1)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
