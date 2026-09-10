from report_view import render_report
from demo import run_demo
from pathlib import Path


def test_offline_screen_explains_pending_review_and_counts(tmp_path):
    report = run_demo(runtime_dir=tmp_path)
    html = Path(report["view_path"]).read_text()
    assert "OFFLINE rehearsal" in html
    assert "Not live Bedrock evidence" in html
    assert "人の確認待ち" in html
    assert 'class="count">1</span>' in html
    assert "read-only" in html
    assert "<script" not in html
    assert "http://" not in html and "https://" not in html


def test_untrusted_text_is_escaped_and_raw_error_is_not_rendered():
    report = {"mode": "live", "verified": False, "is_live_evidence": True,
              "error": "PRIVATE_ERROR_DETAILS", "error_type": "<script>alert(1)</script>",
              "run_id": '<img src=x onerror="alert(1)">', "cases": []}
    html = render_report(report)
    assert "INCOMPLETE live attempt" in html
    assert "Costs may have occurred" in html
    assert "PRIVATE_ERROR_DETAILS" not in html
    assert "<script>" not in html and "<img" not in html
    assert "&lt;script&gt;" in html


def test_offline_report_cannot_be_labelled_live_by_one_flag():
    html = render_report({"mode": "offline", "verified": True, "is_live_evidence": True})
    assert "OFFLINE rehearsal" in html


def test_live_label_requires_three_completed_model_cases():
    report = {"mode": "live", "verified": True, "is_live_evidence": True,
              "cases": [{"bedrock_called": True, "verified": True}] * 3}
    assert "Live Bedrock run /" in render_report(report)
    report["cases"] = report["cases"][:2]
    assert "INCOMPLETE live attempt" in render_report(report)
