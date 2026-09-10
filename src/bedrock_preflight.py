from __future__ import annotations

import argparse
import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from botocore.config import Config

from model_config import resolve_bedrock_settings


def _extract_text(response: dict) -> str:
    output = response.get("output", {})
    message = output.get("message", {})
    for block in message.get("content", []):
        if isinstance(block, dict) and "text" in block:
            return str(block["text"]).strip()
    return ""


def run_preflight(
    model_id: str | None = None, region_name: str | None = None,
    *, allow_paid_model: bool = False,
) -> dict:
    """Verify AWS credentials and make one tiny Bedrock Nova request.

    The function intentionally does not return the AWS account ID or ARN so the
    preflight output can be safely shown in screenshots and demo recordings.
    """
    if not allow_paid_model:
        raise ValueError("preflight requires explicit permission for a paid model request")
    settings = resolve_bedrock_settings(model_id, region_name)
    result = {
        "credentials_ok": False,
        "bedrock_ok": False,
        "model_id": settings.model_id,
        "region": settings.region_name,
        "response": "",
    }

    try:
        config = Config(connect_timeout=10, read_timeout=60,
                        retries={"total_max_attempts": 1, "mode": "standard"})
        boto3.client("sts", region_name=settings.region_name, config=config).get_caller_identity()
        result["credentials_ok"] = True

        client = boto3.client("bedrock-runtime", region_name=settings.region_name, config=config)
        response = client.converse(
            modelId=settings.model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Reply with exactly READY"}],
                }
            ],
            inferenceConfig={"maxTokens": 16, "temperature": 0.0},
        )
        result["bedrock_ok"] = _extract_text(response) == "READY"
        result["response"] = "READY" if result["bedrock_ok"] else ""
        return result
    except (NoCredentialsError, BotoCoreError, ClientError) as exc:
        result["error_type"] = type(exc).__name__
        result["error"] = "Check AWS credentials, selected region, and model access privately."
        return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check AWS credentials and Amazon Bedrock Nova access."
    )
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--region", default=None)
    parser.add_argument("--allow-paid-model", action="store_true")
    args = parser.parse_args()
    if not args.allow_paid_model:
        parser.error("this check makes a paid Bedrock request; add --allow-paid-model to authorize")

    result = run_preflight(args.model_id, args.region, allow_paid_model=args.allow_paid_model)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["credentials_ok"] and result["bedrock_ok"] else 1)


if __name__ == "__main__":
    main()
