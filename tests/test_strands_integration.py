"""Real Strands event loop with a scripted in-memory model, NOT live Bedrock proof."""
import json

import pytest
from strands.models import Model
from strands.types.exceptions import EventLoopException

from agent import build_agent, _build_prompt
from execution import ActionRejected, EventRun
from test_qc_policy import make_event


class ScriptedModel(Model):
    def __init__(self, action, inputs=None, repeat=False):
        self.action = action
        self.inputs = {} if inputs is None else inputs
        self.repeat = repeat
        self.calls = 0

    def update_config(self, **model_config):
        pass

    def get_config(self):
        return {"model_id": "offline-scripted-test-model"}

    async def structured_output(self, *args, **kwargs):
        raise NotImplementedError
        yield  # Abstract interface requires an async generator.

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kwargs):
        self.calls += 1
        yield {"messageStart": {"role": "assistant"}}
        if self.calls == 1 or self.repeat:
            yield {"contentBlockStart": {"contentBlockIndex": 0, "start": {
                "toolUse": {"toolUseId": f"test-{self.calls}", "name": self.action},
            }}}
            yield {"contentBlockDelta": {"contentBlockIndex": 0, "delta": {
                "toolUse": {"input": json.dumps(self.inputs)},
            }}}
            yield {"contentBlockStop": {"contentBlockIndex": 0}}
            yield {"messageStop": {"stopReason": "tool_use"}}
        else:
            yield {"contentBlockStart": {"contentBlockIndex": 0, "start": {}}}
            yield {"contentBlockDelta": {"contentBlockIndex": 0, "delta": {"text": "Done."}}}
            yield {"contentBlockStop": {"contentBlockIndex": 0}}
            yield {"messageStop": {"stopReason": "end_turn"}}
        yield {"metadata": {"usage": {"inputTokens": 1, "outputTokens": 1, "totalTokens": 2},
                            "metrics": {"latencyMs": 0}}}


@pytest.mark.parametrize("overrides", [{}, {"confidence": 0.2}, {"signal_healthy": False}])
def test_real_strands_sdk_calls_the_bound_tool(tmp_path, monkeypatch, overrides):
    run = EventRun(make_event(**overrides), tmp_path)
    model = ScriptedModel(run.decision.action)
    monkeypatch.setattr("strands.models.BedrockModel", lambda **kwargs: model)
    sdk_agent = build_agent(run)
    sdk_agent(_build_prompt(run.event, run.decision))
    assert run.verify()["verified"]
    assert model.calls == 2


@pytest.mark.parametrize("action,inputs,repeat", [
    ("stop_and_check_signal", {}, False),
    ("record_observation", {"amount": "large"}, False),
    ("record_observation", {}, True),
])
def test_real_sdk_rejects_wrong_injected_or_duplicate_call(tmp_path, monkeypatch, action, inputs, repeat):
    run = EventRun(make_event(), tmp_path)
    model = ScriptedModel(action, inputs, repeat)
    monkeypatch.setattr("strands.models.BedrockModel", lambda **kwargs: model)
    sdk_agent = build_agent(run)
    with pytest.raises(EventLoopException) as failure:
        sdk_agent(_build_prompt(run.event, run.decision))
    assert isinstance(failure.value.__cause__, ActionRejected)
    logs = list(tmp_path.glob("*.jsonl"))
    assert sum(len(path.read_text().splitlines()) for path in logs) == (1 if repeat else 0)
    assert model.calls <= 2
    assert not run.receipt()["verified"]
