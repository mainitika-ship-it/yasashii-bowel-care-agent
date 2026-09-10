"""Reproducible synthetic demo. Offline success is never live Bedrock evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from uuid import uuid4

from execution import ACTION_FILES, EventRun
from handoff import build_summary, load_jsonl
from model_config import resolve_bedrock_settings
from qc_policy import ObservationEvent, evaluate_event
from report_view import render_report

DEFAULT_CASES = {
    "high_confidence_event.json": ("PASS", "record_observation"),
    "uncertain_event.json": ("HOLD", "request_caregiver_confirmation"),
    "bad_signal_event.json": ("STOP", "stop_and_check_signal"),
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_demo(
    mode: str = "offline", sample_dir: str | Path = PROJECT_ROOT / "sample_data",
    runtime_dir: str | Path = "runtime/demo", confidence_threshold: float = 0.80,
    model_id: str | None = None, region_name: str | None = None,
    *, allow_paid_model: bool = False, provider: str = "bedrock",
) -> dict:
    if mode not in {"offline", "live"}:
        raise ValueError("execution mode must be offline or live")
    if provider not in {"bedrock", "ollama"}:
        raise ValueError("provider must be bedrock or ollama")
    if mode == "live" and provider == "bedrock" and not allow_paid_model:
        raise ValueError("live demo requires explicit permission for Bedrock costs")
    if mode == "live" and provider == "ollama":
        from local_model import validate_model_id
        validate_model_id(model_id)
    settings = resolve_bedrock_settings(model_id, region_name)
    # Validate ALL cases before the first cloud request or filesystem write.
    cases = []
    for filename, expected in DEFAULT_CASES.items():
        raw_bytes = (Path(sample_dir) / filename).read_bytes()
        event = ObservationEvent.from_dict(json.loads(raw_bytes))
        if event.source != "simulated_test_data" or event.contains_personal_data:
            raise ValueError("the public demo accepts synthetic, non-identifying events only")
        decision = evaluate_event(event, confidence_threshold)
        if (decision.control_status, decision.action) != expected:
            raise ValueError("sample outcomes must be PASS, HOLD, STOP in the documented order")
        cases.append((filename, event, hashlib.sha256(raw_bytes).hexdigest()))

    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:12]
    run_dir = Path(runtime_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 2, "run_id": run_id, "created_at": now.isoformat(),
        "mode": mode, "synthetic_data_only": True,
        "is_live_evidence": False, "is_live_agent_evidence": False, "verified": False,
        "model_provider": provider if mode == "live" else None,
        "model_id": settings.model_id if mode == "live" else None,
        "region": settings.region_name if mode == "live" and provider == "bedrock" else None,
        "source_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((PROJECT_ROOT / "src").glob("*.py"))
        },
        "cases": [],
    }
    try:
        report["strands_version"] = version("strands-agents")
    except PackageNotFoundError:
        report["strands_version"] = None
    try:
        for filename, event, sample_hash in cases:
            run = EventRun(event, run_dir, confidence_threshold)
            case = {
                "sample": filename, "sample_sha256": sample_hash,
                # On a failed live attempt the outcome/cost is unknown, not zero.
                "bedrock_called": None if mode == "live" and provider == "bedrock" else False,
                "bedrock_attempted": mode == "live" and provider == "bedrock",
                "model_called": None if mode == "live" else False,
            }
            report["cases"].append(case)
            try:
                if mode == "offline":
                    run.execute(run.decision.action)
                    case.update(run.verify(), execution="offline_local")
                else:
                    from agent import run_live_event
                    case.update(run_live_event(
                        run, settings.model_id, settings.region_name,
                        allow_paid_model=allow_paid_model, provider=provider,
                    ))
            finally:
                case.update(run.receipt())
        report["log_counts"] = {
            filename: len(load_jsonl(run_dir / filename)) for filename in ACTION_FILES.values()
        }
        report["handoff"] = build_summary(
            load_jsonl(run_dir / "event_log.jsonl"), cases[0][1].timestamp[:10],
        )
        report["verified"] = (
            all(case["verified"] for case in report["cases"])
            and all(count == 1 for count in report["log_counts"].values())
            and report["handoff"]["observation_count"] == 1
        )
        report["is_live_evidence"] = (
            mode == "live" and provider == "bedrock" and report["verified"]
            and all(case["bedrock_called"] for case in report["cases"])
        )
        report["is_live_agent_evidence"] = (
            mode == "live" and report["verified"]
            and all(case["model_called"] is True for case in report["cases"])
        )
    except Exception as exc:
        # Do not leak credential details, account IDs, prompts, or SDK responses.
        report["error_type"] = type(exc).__name__
        report["error"] = "Demo incomplete. Inspect local configuration privately; do not publish raw errors."
    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    view_path = run_dir / "report.html"
    view_path.write_text(render_report(report), encoding="utf-8")
    # Keep machine/user-specific paths out of the saved evidence itself.
    return {**report, "report_path": str(report_path), "view_path": str(view_path), "runtime_dir": str(run_dir)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthetic PASS / HOLD / STOP demo and evidence.")
    parser.add_argument("--mode", choices=("qc", "offline", "live"), default="qc")
    parser.add_argument("--sample-dir", default=str(PROJECT_ROOT / "sample_data"))
    parser.add_argument("--runtime-dir", default="runtime/demo")
    parser.add_argument("--confidence-threshold", type=float, default=0.80)
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--region", default=None)
    parser.add_argument("--provider", choices=("bedrock", "ollama"), default="bedrock")
    parser.add_argument("--allow-paid-model", action="store_true")
    args = parser.parse_args()
    if args.mode == "qc":
        for filename in DEFAULT_CASES:
            event = ObservationEvent.from_json_file(Path(args.sample_dir) / filename)
            decision = evaluate_event(event, args.confidence_threshold)
            print(f"{filename} -> {decision.control_status}")
            print(json.dumps(decision.to_dict(), ensure_ascii=False))
        return
    if args.mode == "live" and args.provider == "bedrock" and not args.allow_paid_model:
        parser.error("live mode incurs Bedrock costs; explicitly add --allow-paid-model")
    report = run_demo(
        args.mode, args.sample_dir, args.runtime_dir, args.confidence_threshold,
        args.model_id, args.region, allow_paid_model=args.allow_paid_model,
        provider=args.provider,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["verified"] else 1)


if __name__ == "__main__":
    main()
