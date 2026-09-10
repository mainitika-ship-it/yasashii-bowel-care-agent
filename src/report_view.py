"""Render a local, read-only demo report. No network, scripts, or caregiver actions."""
from __future__ import annotations

from html import escape


def text(value) -> str:
    return escape(str(value), quote=True)


def render_report(report: dict) -> str:
    """Display only selected report fields, never raw prompts or error messages."""
    complete = report.get("verified") is True
    live = (
        complete and report.get("mode") == "live"
        and report.get("is_live_evidence") is True
        and len(report.get("cases", [])) == 3
        and all(c.get("bedrock_called") is True and c.get("verified") is True
                for c in report.get("cases", []))
    )
    local_live = (
        complete and report.get("mode") == "live" and report.get("model_provider") == "ollama"
        and report.get("is_live_agent_evidence") is True
        and len(report.get("cases", [])) == 3
        and all(c.get("model_called") is True and c.get("bedrock_called") is False
                and c.get("verified") is True for c in report.get("cases", []))
    )
    if live:
        banner = "Live Bedrock run / AWSにつないだ実行"
    elif local_live:
        banner = "Live local model via Strands / ローカルAIで実行 — No Bedrock calls"
    elif report.get("mode") == "offline":
        banner = "OFFLINE rehearsal / 無料の模擬実行 — Not live Bedrock evidence"
    elif report.get("model_provider") == "ollama":
        banner = "INCOMPLETE local model attempt / ローカルAI実行は未完了"
    else:
        banner = "INCOMPLETE live attempt / AWS実行は未完了 — Costs may have occurred"
    complete = complete and (report.get("mode") == "offline" or live or local_live)
    outcome = "Demo checks passed / デモ確認成功" if complete else "Incomplete / 実行未完了"
    labels = {
        "PASS": ("Recorded / 観察を記録", "Only this observation enters the handoff. / この観察だけを申し送りに数えます。"),
        "HOLD": ("Human review pending / 人の確認待ち", "An uncertain event is queued, not recorded as fact. / 不確かなため記録を確定しません。"),
        "STOP": ("Safety stop / 安全のため停止", "No care observation is recorded. / 介護の観察記録には加えません。"),
    }
    cards = []
    for case in report.get("cases", []):
        status = case.get("control_status", "UNKNOWN")
        title, description = labels.get(status, ("Incomplete / 未完了", "No completed action was verified. / 完了を確認できていません。"))
        if case.get("verified") is not True:
            title = "Action not verified / 処理完了は未確認"
            description = "Inspect local logs before retrying; a write may have occurred. / 再実行前に記録を確認してください。一部の書込みが済んでいる場合があります。"
        css = status.lower() if status in labels else "unknown"
        cards.append(
            f'<article class="card {css}"><span class="tag">{text(status)}</span>'
            f'<h2>{text(title)}</h2><p>{text(description)}</p>'
            f'<dl><dt>Sample / 模擬入力</dt><dd>{text(case.get("sample", "—"))}</dd>'
            f'<dt>Completed action / 完了した処理</dt><dd>{text(case.get("completed_action") or "None / なし")}</dd>'
            f'<dt>Tool attempts / 処理の試行数</dt><dd>{text(case.get("tool_attempts", 0))}</dd>'
            f'<dt>Case check / 確認結果</dt><dd>{"Passed / 成功" if case.get("verified") is True else "Incomplete / 未完了"}</dd></dl></article>'
        )
    summary = report.get("handoff") or {}
    count = summary.get("observation_count", "—")
    error = f'<p>Failure type / エラー種別: {text(report["error_type"])}</p>' if report.get("error_type") else ""
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Yasashii Bowel Care Agent — Demo report</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f6f4;color:#172c24;font:16px/1.6 system-ui,sans-serif}}
main{{max-width:1120px;margin:auto;padding:28px 20px 48px}}h1{{font-size:clamp(24px,4vw,38px);line-height:1.2}}
h2{{font-size:19px}}.banner{{padding:14px 18px;background:#172c24;color:#fff;border-radius:10px;font-weight:700}}
.subtitle,dt{{color:#465950}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:16px;margin:24px 0}}
.card,.summary{{background:white;padding:22px;border:1px solid #d2ded7;border-radius:14px}}
.card{{border-top:6px solid #64746a}}.pass{{border-top-color:#247247}}.hold{{border-top-color:#b77500}}.stop{{border-top-color:#b13a39}}
.tag{{font-weight:800;letter-spacing:.06em}}dt{{font-size:13px;margin-top:14px}}dd{{margin:2px 0;overflow-wrap:anywhere}}
.count{{font-size:36px;font-weight:800}}footer{{margin-top:24px;font-size:14px}}a{{color:#185c43}}code{{overflow-wrap:anywhere}}
</style></head><body><main>
<p class="banner">{text(banner)}</p>
<h1>Yasashii Bowel Care Agent</h1>
<p class="subtitle">Synthetic demonstration / 安全な模擬データによるデモ</p>
<p><strong>{text(outcome)}</strong></p>
<div class="grid">{"".join(cards) or '<p>No completed cases / 完了したケースはありません。</p>'}</div>
<section class="summary"><h2>Daily handoff / 申し送り</h2>
<span class="count">{text(count)}</span> recorded observation(s) / 記録済みの観察件数
<p>Sample date / 模擬データの日付: {text(summary.get("date", "—"))}</p>
<p>Pending review and safety stops are excluded. / 確認待ち・安全停止は件数に含みません。</p></section>
{error}<footer>
<p>This supports observation; it is not a medical diagnosis. Missing observations do not prove no bowel movement occurred.<br>
観察の補助であり、診断ではありません。記録がないことは、排便がなかった証明にはなりません。</p>
<p>This page is read-only. Caregiver approval controls are not implemented.<br>この画面は結果の閲覧専用です。介護者の承認操作はまだ実装していません。</p>
<p>Run / 実行: <code>{text(report.get("run_id", "—"))}</code><br>Generated / 作成: {text(report.get("created_at", "—"))}</p>
<a href="report.json">Machine-readable report / 詳細データ</a>
</footer></main></body></html>'''
