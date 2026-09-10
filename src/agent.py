from __future__ import annotations

import argparse
import json
from typing import Any

from execution import ActionRejected, EventRun
from model_config import resolve_bedrock_settings
from qc_policy import ObservationEvent, QCDecision, evaluate_event


class InvocationLimits:
    """Bound the SDK loop and reject unexpected tool names/arguments before execution."""

    def __init__(self, run: EventRun) -> None:
        self.run = run
        self.model_calls = 0
        self.tool_calls = 0

    def register_hooks(self, registry, **kwargs) -> None:
        from strands.hooks import BeforeModelCallEvent, BeforeToolCallEvent
        registry.add_callback(BeforeModelCallEvent, self.before_model)
        registry.add_callback(BeforeToolCallEvent, self.before_tool)

    def before_model(self, event) -> None:
        self.model_calls += 1
        if self.model_calls > 2:
            self.run.invalidate()
            raise ActionRejected("model-call limit reached for this event")

    def before_tool(self, event) -> None:
        self.tool_calls += 1
        if self.tool_calls != 1:
            self.run.invalidate()
            raise ActionRejected("only one tool request is allowed per event")
        if event.tool_use["name"] != self.run.decision.action or event.tool_use["input"] != {}:
            self.run.invalidate()
            raise ActionRejected("tool must match QC and take no model-supplied arguments")


def build_tools(run: EventRun) -> list:
    # Lazy imports keep all offline commands usable without AWS or Strands installed.
    from strands import tool

    @tool
    def record_observation() -> dict[str, Any]:
        """Record this bound observation only when its local QC decision is PASS."""
        return run.execute("record_observation")

    @tool
    def request_caregiver_confirmation() -> dict[str, Any]:
        """Queue this bound observation for human review only when QC is HOLD."""
        return run.execute("request_caregiver_confirmation")

    @tool
    def stop_and_check_signal() -> dict[str, Any]:
        """Record a local safety alert only when this bound observation is STOP."""
        return run.execute("stop_and_check_signal")

    return [record_observation, request_caregiver_confirmation, stop_and_check_signal]


def build_agent(run: EventRun, model_id: str | None = None, region_name: str | None = None,
                *, provider: str = "bedrock"):
    """Construct a fresh Strands agent for one event, never a shared care conversation."""
    if run.event.contains_personal_data:
        raise ValueError("privacy-flagged events must stop locally, not construct a model")
    from strands import Agent
    if provider == "ollama":
        from local_model import build_local_model, validate_model_id
        model = build_local_model(validate_model_id(model_id))
    elif provider == "bedrock":
        from strands.models import BedrockModel
        from botocore.config import Config
        settings = resolve_bedrock_settings(model_id, region_name)
        model = BedrockModel(
            model_id=settings.model_id, region_name=settings.region_name,
            temperature=0.0, max_tokens=512,
            boto_client_config=Config(
                connect_timeout=10, read_timeout=60,
                retries={"total_max_attempts": 1, "mode": "standard"},
            ),
        )
    else:
        raise ValueError("provider must be bedrock or ollama")
    return Agent(
        model=model,
        callback_handler=None,
        retry_strategy=None,
        hooks=[InvocationLimits(run)],
        system_prompt=(
            "You are a privacy-first family-care observation agent, not a diagnostic system. "
            "Follow the supplied deterministic QC action exactly: PASS uses record_observation; "
            "HOLD uses request_caregiver_confirmation; STOP uses stop_and_check_signal. "
            "Call exactly one tool, with no arguments. The local guard supplies validated values "
            "and rejects incorrect or duplicate writes. Do not retry a rejected call. "
            "Do not request identity data. Keep your final explanation short."
        ),
        tools=build_tools(run),
    )


def _build_prompt(event: ObservationEvent, decision: QCDecision) -> str:
    return (
        "Process this non-identifying observation using exactly the required tool.\n"
        f"EVENT:\n{json.dumps(event.to_dict(), ensure_ascii=False)}\n"
        f"QC DECISION:\n{json.dumps(decision.to_dict(), ensure_ascii=False)}"
    )


def run_live_event(
    run: EventRun, model_id: str | None = None, region_name: str | None = None,
    *, allow_paid_model: bool = False, provider: str = "bedrock",
) -> dict[str, Any]:
    # A privacy STOP must happen before model construction or credential access.
    if run.event.contains_personal_data:
        run.execute("stop_and_check_signal")
        return {**run.verify(), "bedrock_called": False, "model_called": False, "execution": "local_privacy_stop"}
    if provider not in {"bedrock", "ollama"}:
        raise ValueError("provider must be bedrock or ollama")
    if provider == "bedrock" and not allow_paid_model:
        raise ValueError("live Bedrock calls require explicit allow_paid_model=True")
    try:
        agent = build_agent(run, model_id, region_name, provider=provider)
        agent(_build_prompt(run.event, run.decision))
    except Exception:
        run.invalidate()
        raise
    return {**run.verify(), "bedrock_called": provider == "bedrock",
            "model_called": True, "execution": "strands_" + provider}


def main() -> None:
    parser = argparse.ArgumentParser(description="Process one privacy-minimized observation.")
    parser.add_argument("--event", required=True)
    parser.add_argument("--confidence-threshold", type=float, default=0.80)
    parser.add_argument("--runtime-dir", default="runtime")
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--region", default=None)
    parser.add_argument("--provider", choices=("bedrock", "ollama"), default="bedrock")
    parser.add_argument("--dry-run", action="store_true", help="No model or care-log writes")
    parser.add_argument("--allow-paid-model", action="store_true", help="Explicitly permit Bedrock costs")
    args = parser.parse_args()
    event = ObservationEvent.from_json_file(args.event)
    decision = evaluate_event(event, args.confidence_threshold)
    if args.dry_run:
        settings = resolve_bedrock_settings(args.model_id, args.region)
        print(json.dumps({
            "event": event.to_dict(), "qc_decision": decision.to_dict(),
            "model": {"provider": args.provider,
                      "model_id": args.model_id if args.provider == "ollama" else settings.model_id,
                      "region": settings.region_name if args.provider == "bedrock" else None,
                      "called": False},
        }, ensure_ascii=False, indent=2))
        return
    if args.provider == "bedrock" and not args.allow_paid_model and not event.contains_personal_data:
        parser.error("use --dry-run, or explicitly authorize costs with --allow-paid-model")
    run = EventRun(event, args.runtime_dir, args.confidence_threshold)
    print(json.dumps(run_live_event(
        run, args.model_id, args.region, allow_paid_model=args.allow_paid_model,
        provider=args.provider,
    ), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
