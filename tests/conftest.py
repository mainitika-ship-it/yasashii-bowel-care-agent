"""Tests must never open a network connection or incur model costs."""
import socket
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("network access is forbidden in this test suite")
    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)
    monkeypatch.setenv("AWS_EC2_METADATA_DISABLED", "true")
    # Ollama's import creates a default HTTPX client. Tests use scripted models
    # and deny sockets; proxy configuration must not require extra proxy drivers.
    monkeypatch.setenv("NO_PROXY", "*")
    monkeypatch.setenv("no_proxy", "*")
