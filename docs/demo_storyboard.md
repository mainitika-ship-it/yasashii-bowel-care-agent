# Demo Video Storyboard — target 4:30 or less

The event allows a maximum 5-minute video. This storyboard leaves buffer for upload / playback differences.

Before recording, capture a successful three-case run with a real tool-capable model. Strands is mandatory; Bedrock is optional. Use one route for the whole recording and show its honest execution-mode banner. The implementation currently has SDK tests, not a recorded real-model run. Use [architecture.png](architecture.png) as the matching visual.

## 0:00–0:30 — Problem

Visual: simple title + caregiver routine.

Message:

- Family caregivers can end up repeatedly checking, remembering, recording, and sharing bowel-movement observations.
- The burden is small each time but repetitive and intrusive.
- Yasashii Bowel Care Agent aims to reduce that burden while protecting dignity and keeping uncertain decisions with a human.

## 0:30–1:00 — What the system does

Visual: QC architecture diagram.

Explain the single end-to-end loop:

`local observation → structured event → PASS/HOLD/STOP → Strands tool → record or caregiver confirmation → handoff summary`

State clearly that the public demo uses synthetic data and is not a medical diagnosis.

## 1:00–1:40 — PASS case

Run:

```bash
python src/agent.py --event sample_data/high_confidence_event.json --dry-run
```

Then show the live Strands version using an installed local model after its [metadata check](local_model_guide.md):

```bash
python src/agent.py --event sample_data/high_confidence_event.json --provider ollama --model-id YOUR_INSTALLED_MODEL
```

Alternatively, after owner-approved AWS setup and preflight:

```bash
python src/agent.py --event sample_data/high_confidence_event.json --allow-paid-model
```

Expected story: healthy signal + high confidence + valid relative amount → quiet record.

Show the resulting local `event_log.jsonl` entry without any identity data.

## 1:40–2:20 — HOLD case

Run the uncertain synthetic event.

Expected story: confidence below the QC threshold → agent does **not** silently decide → caregiver confirmation is queued.

Show the pending queue. Explain `Yes / No / Hold` as a planned human decision concept, not an implemented approval UI.

## 2:20–3:00 — STOP case

Run the bad-signal synthetic event.

Expected story: failed signal / privacy control → automatic recording stops.

This demonstrates that safety controls can override convenience.

## 3:00–3:35 — Daily handoff

Run:

```bash
python src/handoff.py --runtime-dir runtime/demo/<run-id> --date 2026-08-18
```

Show only privacy-minimized counts / relative amounts and the disclaimer that missing observations do not prove no bowel movement occurred.

## 3:35–4:05 — Technical implementation

Visual: code + architecture diagram.

Mention:

- Python
- Strands Agents SDK
- the model actually used in the recording: installed Ollama model or Amazon Bedrock / Nova Lite
- deterministic QC policy
- tool calling
- local JSONL handoff data
- public tests

If AgentCore is later added, mention it here only after it actually works.

## 4:05–4:30 — Why it matters / close

End with three statements:

1. Built for family caregivers.
2. The agent works quietly when confidence is high and asks a human when judgment is needed.
3. Privacy, dignity, and explainable uncertainty are product requirements, not afterthoughts.

## Recording rules

- No real patient images.
- No family names, addresses, AWS account IDs, access keys, emails, or local file paths containing personal data.
- Do not show AWS credential screens.
- Blur or crop browser UI if an account identifier appears.
- Keep the final public video at or below 5:00.

## Recording rehearsal added 2026-09-10

Run `python src/demo.py --mode offline` first to rehearse the complete local loop at no cost. For final live footage, use `python src/demo.py --mode live --provider ollama --model-id YOUR_INSTALLED_MODEL`, or `python src/demo.py --mode live --allow-paid-model` after owner-approved AWS setup. Use its printed unique run directory and show `report.json` with `verified: true` and `is_live_agent_evidence: true`. The legacy `is_live_evidence` flag is Bedrock-only. Do not label offline or scripted-model tests as a real-model demonstration. Use English narration or English subtitles; no public video has been produced by this code update.

The command also prints `view_path`. Open that `report.html` for the readable three-case result and handoff count. Keep the execution-mode banner in the recording, including the local-provider label when applicable. An offline rehearsal screen must never stand in for actual model evidence. If the page says an attempt is incomplete, inspect local logs before repeating it because a write may already have occurred; Bedrock attempts may also have incurred a charge.
