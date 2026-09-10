"""Local, model-independent write boundary for one validated observation.

The model chooses a tool; it never supplies the content written to care logs.
Exactly-once here means within one EventRun, not across process restarts.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from qc_policy import ObservationEvent, evaluate_event

ACTION_FILES = {
    "record_observation": "event_log.jsonl",
    "request_caregiver_confirmation": "confirmation_queue.jsonl",
    "stop_and_check_signal": "system_alerts.jsonl",
}


class ActionRejected(RuntimeError):
    """The requested action would violate the local QC decision."""


class EventRun:
    def __init__(
        self, event: ObservationEvent, runtime_dir: str | Path,
        confidence_threshold: float = 0.80,
    ) -> None:
        # Revalidate even callers that constructed a dataclass directly.
        self.event = ObservationEvent.from_dict(event.to_dict())
        self.decision = evaluate_event(self.event, confidence_threshold)
        self.runtime_dir = Path(runtime_dir)
        self.attempts = 0
        self.completed_action: str | None = None
        self.failed = False
        self._write_started = False
        self._lock = Lock()

    def execute(self, action: str) -> dict[str, Any]:
        """Write trusted event values once; reject wrong or duplicate actions."""
        with self._lock:
            self.attempts += 1
            if action != self.decision.action:
                raise ActionRejected("tool does not match the deterministic QC decision")
            if self._write_started:
                raise ActionRejected("this event already attempted its one permitted write")

            event = self.event
            payload: dict[str, Any] = {
                "action": action,
                "timestamp": event.timestamp,
                "control_status": self.decision.control_status,
                "reason_codes": list(self.decision.reasons),
                "processed_at": datetime.now(timezone.utc).isoformat(),
            }
            if action == "record_observation":
                payload.update(
                    amount=event.relative_amount, confidence=event.confidence,
                    changed_area_percent=event.changed_area_percent,
                )
            elif action == "request_caregiver_confirmation":
                payload.update(
                    suggested_amount=event.relative_amount,
                    confirmation_status="pending",
                )
            # Never log model-supplied notes, arbitrary source text, or raw images.
            self.runtime_dir.mkdir(parents=True, exist_ok=True)
            path = self.runtime_dir / ACTION_FILES[action]
            self._write_started = True  # A failed/partial write must not be retried silently.
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False, allow_nan=False) + "\n")
            self.completed_action = action
            return payload

    def receipt(self) -> dict[str, Any]:
        return {
            "control_status": self.decision.control_status,
            "expected_action": self.decision.action,
            "completed_action": self.completed_action,
            "tool_attempts": self.attempts,
            "execution_failed": self.failed,
            "verified": not self.failed and self.attempts == 1 and self.completed_action == self.decision.action,
        }

    def invalidate(self) -> None:
        """A failed SDK invocation must not be represented as a successful case."""
        with self._lock:
            self.failed = True

    def verify(self) -> dict[str, Any]:
        receipt = self.receipt()
        if not receipt["verified"]:
            raise ActionRejected("expected exactly one successful matching tool call")
        return receipt
