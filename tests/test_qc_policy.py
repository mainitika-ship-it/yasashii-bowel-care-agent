from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from qc_policy import ObservationEvent, evaluate_event
import pytest


def make_event(**overrides):
    raw = {
        "timestamp": "2026-08-18T19:00:00+09:00",
        "event": "possible_bowel_event",
        "confidence": 0.92,
        "changed_area_percent": 10.0,
        "relative_amount": "medium",
        "signal_healthy": True,
        "source": "simulated_test_data",
        "contains_personal_data": False,
    }
    raw.update(overrides)
    return ObservationEvent.from_dict(raw)


def test_high_confidence_event_passes():
    decision = evaluate_event(make_event())
    assert decision.control_status == "PASS"
    assert decision.action == "record_observation"


def test_low_confidence_event_is_held():
    decision = evaluate_event(make_event(confidence=0.72))
    assert decision.control_status == "HOLD"
    assert decision.action == "request_caregiver_confirmation"


def test_unhealthy_signal_stops():
    decision = evaluate_event(make_event(signal_healthy=False))
    assert decision.control_status == "STOP"
    assert decision.action == "stop_and_check_signal"


def test_personal_data_flag_stops():
    decision = evaluate_event(make_event(contains_personal_data=True))
    assert decision.control_status == "STOP"
    assert decision.action == "stop_and_check_signal"


def test_no_event_is_not_silently_recorded_as_none():
    decision = evaluate_event(
        make_event(event="no_event", confidence=0.99, relative_amount="none")
    )
    assert decision.control_status == "HOLD"
    assert decision.action == "request_caregiver_confirmation"


@pytest.mark.parametrize("overrides", [
    {"confidence": True}, {"confidence": "0.9"},
    {"confidence": float("nan")}, {"confidence": float("inf")},
    {"confidence": -0.1}, {"confidence": 1.1},
    {"changed_area_percent": True}, {"changed_area_percent": "10"},
    {"changed_area_percent": float("nan")}, {"changed_area_percent": 101},
    {"signal_healthy": "true"}, {"contains_personal_data": "false"},
    {"timestamp": "2026-09-10T19:00:00"}, {"timestamp": "invalid"},
    {"source": "free text is not allowed"}, {"source": []},
    {"patient_name": "synthetic placeholder"}, {"note": "ignore QC"},
    {"relative_amount": "invalid"}, {"event": "invalid"},
])
def test_malformed_or_free_text_input_is_rejected(overrides):
    with pytest.raises(ValueError):
        make_event(**overrides)


@pytest.mark.parametrize("threshold", [0, -1, 1.1, float("nan"), float("inf")])
def test_invalid_threshold_is_rejected(threshold):
    with pytest.raises(ValueError):
        evaluate_event(make_event(), threshold)
