import json
import subprocess
import sys
from pathlib import Path

import pytest

import agent
from demo import DEFAULT_CASES, PROJECT_ROOT, run_demo


def test_offline_end_to_end_and_repeat_isolation(tmp_path):
    first = run_demo(runtime_dir=tmp_path)
    second = run_demo(runtime_dir=tmp_path)
    for report in [first, second]:
        assert report["verified"] is True
        assert report["is_live_evidence"] is False
        assert [case["control_status"] for case in report["cases"]] == ["PASS", "HOLD", "STOP"]
        assert all(case["tool_attempts"] == 1 for case in report["cases"])
        assert all(case["bedrock_called"] is False for case in report["cases"])
        assert report["handoff"]["observation_count"] == 1
        assert report["handoff"]["relative_amount_counts"] == {"medium": 1}
        assert all(count == 1 for count in report["log_counts"].values())
        saved = json.loads(Path(report["report_path"]).read_text())
        assert "runtime_dir" not in saved
        assert str(tmp_path) not in json.dumps(saved)
    assert first["run_id"] != second["run_id"]


def test_live_permission_required_before_any_work(tmp_path):
    with pytest.raises(ValueError, match="permission"):
        run_demo("live", runtime_dir=tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("overrides", [
    {"source": "local_vision"}, {"contains_personal_data": True},
])
def test_all_samples_validated_before_execution(tmp_path, overrides):
    samples = tmp_path / "samples"
    samples.mkdir()
    for filename in DEFAULT_CASES:
        event = json.loads((PROJECT_ROOT / "sample_data" / filename).read_text())
        if filename == "bad_signal_event.json":
            event.update(overrides)
        (samples / filename).write_text(json.dumps(event))
    runtime = tmp_path / "runtime"
    with pytest.raises(ValueError, match="synthetic"):
        run_demo(sample_dir=samples, runtime_dir=runtime)
    assert not runtime.exists()


def test_failed_live_attempt_is_not_success_or_zero_cost(tmp_path, monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("example private SDK details must not leak")
    monkeypatch.setattr(agent, "run_live_event", fail)
    report = run_demo("live", runtime_dir=tmp_path, allow_paid_model=True)
    assert not report["verified"] and not report["is_live_evidence"]
    assert report["cases"][0]["bedrock_called"] is None
    assert report["cases"][0]["bedrock_attempted"] is True
    assert "private SDK details" not in json.dumps(report)
    assert Path(report["report_path"]).exists()


def test_offline_cli_needs_no_installed_packages(tmp_path):
    result = subprocess.run(
        [sys.executable, "-S", str(PROJECT_ROOT / "src/demo.py"),
         "--mode", "offline", "--runtime-dir", str(tmp_path)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    assert report["verified"] and not report["is_live_evidence"]


def test_live_cli_fails_closed_without_opt_in(tmp_path):
    result = subprocess.run(
        [sys.executable, "-S", str(PROJECT_ROOT / "src/demo.py"),
         "--mode", "live", "--runtime-dir", str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "--allow-paid-model" in result.stderr
    assert not list(tmp_path.iterdir())
