import json
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

import agent
from execution import ACTION_FILES, ActionRejected, EventRun
from test_qc_policy import make_event


@pytest.mark.parametrize("overrides,action", [
    ({}, "record_observation"),
    ({"confidence": 0.2}, "request_caregiver_confirmation"),
    ({"signal_healthy": False}, "stop_and_check_signal"),
    ({"contains_personal_data": True}, "stop_and_check_signal"),
])
def test_expected_action_writes_once(tmp_path, overrides, action):
    run = EventRun(make_event(**overrides), tmp_path)
    payload = run.execute(action)
    assert run.verify()["verified"]
    assert payload["action"] == action
    assert len(list(tmp_path.iterdir())) == 1
    records = (tmp_path / ACTION_FILES[action]).read_text().splitlines()
    assert len(records) == 1
    assert json.loads(records[0]) == payload
    with pytest.raises(ActionRejected):
        run.execute(action)
    assert len((tmp_path / ACTION_FILES[action]).read_text().splitlines()) == 1
    assert not run.receipt()["verified"]


@pytest.mark.parametrize("overrides,wrong_action", [
    ({"confidence": 0.2}, "record_observation"),
    ({"signal_healthy": False}, "record_observation"),
    ({"contains_personal_data": True}, "request_caregiver_confirmation"),
    ({}, "unknown_tool"),
])
def test_wrong_action_never_writes(tmp_path, overrides, wrong_action):
    run = EventRun(make_event(**overrides), tmp_path / "not_created")
    with pytest.raises(ActionRejected):
        run.execute(wrong_action)
    assert not run.runtime_dir.exists()


def test_concurrent_duplicate_is_rejected(tmp_path):
    run = EventRun(make_event(), tmp_path)
    def attempt(_):
        try:
            run.execute("record_observation")
            return True
        except ActionRejected:
            return False
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(20))) == 1
    assert len((tmp_path / "event_log.jsonl").read_text().splitlines()) == 1


def test_no_action_cannot_be_verified(tmp_path):
    with pytest.raises(ActionRejected):
        EventRun(make_event(), tmp_path).verify()


def test_privacy_stop_never_constructs_model(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("privacy event must not reach the model")
    monkeypatch.setattr(agent, "build_agent", forbidden)
    receipt = agent.run_live_event(EventRun(make_event(contains_personal_data=True), tmp_path))
    assert receipt["verified"] and receipt["bedrock_called"] is False
    assert not (tmp_path / "event_log.jsonl").exists()


def test_live_permission_is_checked_before_model_construction(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unapproved model construction")
    monkeypatch.setattr(agent, "build_agent", forbidden)
    with pytest.raises(ValueError, match="allow_paid_model"):
        agent.run_live_event(EventRun(make_event(), tmp_path))
    assert not list(tmp_path.iterdir())


def test_build_agent_also_rejects_privacy_flag(tmp_path):
    with pytest.raises(ValueError, match="privacy"):
        agent.build_agent(EventRun(make_event(contains_personal_data=True), tmp_path))


def test_model_failure_after_write_is_not_verified(tmp_path, monkeypatch):
    run = EventRun(make_event(), tmp_path)
    def fail_after_write(prompt):
        run.execute("record_observation")
        raise RuntimeError("acknowledgement failed")
    monkeypatch.setattr(agent, "build_agent", lambda *args, **kwargs: fail_after_write)
    with pytest.raises(RuntimeError):
        agent.run_live_event(run, allow_paid_model=True)
    assert run.receipt()["execution_failed"] is True
    assert run.receipt()["verified"] is False


def test_model_budget_stops_third_cycle(tmp_path):
    limits = agent.InvocationLimits(EventRun(make_event(), tmp_path))
    limits.before_model(None)
    limits.before_model(None)
    with pytest.raises(ActionRejected, match="model-call limit"):
        limits.before_model(None)


@pytest.mark.parametrize("name,arguments", [
    ("stop_and_check_signal", {}),
    ("record_observation", {"amount": "large"}),
    ("record_observation", {"note": "untrusted free text"}),
])
def test_hook_rejects_wrong_tools_and_injected_arguments(tmp_path, name, arguments):
    limits = agent.InvocationLimits(EventRun(make_event(), tmp_path))
    with pytest.raises(ActionRejected):
        limits.before_tool(SimpleNamespace(tool_use={"name": name, "input": arguments}))
    assert not list(tmp_path.iterdir())
