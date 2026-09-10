import json

import pytest
from botocore.exceptions import ClientError

import bedrock_preflight


def test_preflight_requires_opt_in(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("client must not be created without opt-in")
    monkeypatch.setattr(bedrock_preflight.boto3, "client", blocked)
    with pytest.raises(ValueError, match="permission"):
        bedrock_preflight.run_preflight()


def test_preflight_error_does_not_expose_account_details(monkeypatch):
    def failure(*args, **kwargs):
        raise ClientError({"Error": {"Code": "AccessDenied", "Message": "PRIVATE_DETAIL"}}, "Example")
    monkeypatch.setattr(bedrock_preflight.boto3, "client", failure)
    result = bedrock_preflight.run_preflight(allow_paid_model=True)
    assert result["error_type"] == "ClientError"
    assert "PRIVATE_DETAIL" not in json.dumps(result)
    assert not result["bedrock_ok"]
