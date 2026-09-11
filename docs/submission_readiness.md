# Agents for Humans Hackathon — Submission Readiness

Updated: 2026-09-11 (technical progress; official/Devpost checks remain dated September 10)

This file is the project-side checklist for the final Devpost submission. It is intentionally conservative: an item is marked complete only when it has been verified, not merely planned.

Official requirements and the current Devpost entry were freshly checked on September 10; see [the recheck record](hackathon_recheck.md). **Strands is required, but Bedrock or a specific model is not.** Deadline: **2026-09-15 09:00 JST**. The current Devpost entry has an empty video URL and no hackathon `submitted_at` value; a published project page is not a final hackathon submission.

## Required by the event

| Requirement | Status | Evidence / next action |
|---|---|---|
| Working agent built with Strands Agents SDK | LOCAL SUCCESS REPORTED / ARTIFACT REVIEW PENDING | A September 11 screenshot reports a successful local `qwen3:8b` three-case run, one PASS-only handoff, and 108 passing tests. Obtain the original reports, logs, and exact source before independently verifying this claim; see the evidence handoff below. |
| Public code repository | DONE | https://github.com/mainitika-ship-it/yasashii-bowel-care-agent is public. Root source and READMEs verified at commit `02191d53a787a050b955a6fa8260a10777298a6c`; [CI passed](https://github.com/mainitika-ship-it/yasashii-bowel-care-agent/actions/runs/34472636948). Devpost's repository field still needs owner-reviewed updating. |
| README | DONE | Setup, architecture, safety, pre-existing disclosure, and demo commands are documented. |
| MIT or Apache license | DONE | Root `LICENSE` is published. GitHub repository metadata identifies its license as MIT (`spdx_id: MIT`), verified 2026-09-10. |
| Architecture diagram | FILE READY / UPLOAD UNVERIFIED | [architecture.png](architecture.png) matches the current implementation and is in an accepted attachment format. Upload/recheck the final file on Devpost. |
| Demo video, max 5 minutes | NOT STARTED | Record only after the live end-to-end flow is stable. See `docs/demo_storyboard.md`. |
| AWS Builder ID | PREVIOUSLY DONE | Prior record says it was entered; recheck the final required field before Submit. |
| Problem / audience / why it matters | DONE | Present in Devpost story and README. |
| English or English translation | TEXT READY / VIDEO PENDING | README and PNG are in English; the public video must also use English narration or translation. |
| Required fields and final Submit | NOT COMPLETE | Current Devpost repository URL still points to the old parent folder. Submitter type, country, track, source URL, architecture upload, and AWS Builder ID must be checked by the owner. |

## Core implementation gate

### September 11 local run: preserve before changing anything

The owner's screenshot shows the Mac-local coding session reporting:

- a live `qwen3:8b` PASS / HOLD / STOP run, with one record per case;
- a pending HOLD and one PASS observation in the handoff;
- 108 passing tests and a separate check of logs, source/sample hashes, and the report banner;
- a prompt-only change with the safety guards retained.

The displayed run directory is `runtime/demo/20260911T051811Z-50c8566cb79e`. **These are screenshot-reported results.** The report files, log contents, and local source change have not yet been received or independently reviewed here. The public source at `ff03843bb229a47ddfc736a6e4e56113b6e446e1` is not yet confirmed to match that run. A successful synthetic demonstration is not validation for real care use.

Next, use the existing Mac-local session to preserve the successful run rather than repeat it:

1. Read the existing `report.json`, `report.html`, and three synthetic JSONL logs; keep the originals untouched. Check `verified`, `is_live_agent_evidence`, provider/model, tool receipts, the pending HOLD, and the single PASS-only handoff against the actual files. For Ollama, a false legacy `is_live_evidence` value is expected.
2. Compare the report's `source_sha256` and sample hashes with the current files. Preserve the matching source, synthetic samples, dependency requirement files, and the exact prompt change. If any file has changed since the run, record the mismatch and do not label the current source as the executed version.
3. Create a new ZIP under the project's ignored `runtime/` directory with only the selected evidence and source files, plus a short verification/change note and reproduction command. Exclude credentials, environments, unrelated files, real care data, and raw service logs. Do not invoke a model or publish the evidence while packaging. Reveal the ZIP in Finder for owner sharing and review.

After receiving this package, reconcile the prompt change with the public repository, review the evidence, then prepare the public recording from the verified build. Do not mark the working-agent gate complete solely from this screenshot.

### Reproduction checks when a new run is needed

For the working-agent portion of the video, complete these three checks:

1. Choose one real model route. For local Ollama, follow the [metadata check and setup](local_model_guide.md); for Bedrock, obtain owner permission for costs and run the paid preflight.
2. `python src/demo.py --mode qc` shows PASS, HOLD, STOP in that order.
3. Run `python src/demo.py --mode live --provider ollama --model-id YOUR_INSTALLED_MODEL` or the Bedrock command `python src/demo.py --mode live --allow-paid-model`. A fresh report must have `verified=true`, `is_live_agent_evidence=true`, and one matching tool for each case. The older `is_live_evidence` field is Bedrock-only and is false for local Ollama.

The local-vision connection is a separate project integration goal, not an additional official requirement or evidence already achieved. Show and label synthetic input in the public demo; do not claim camera integration. The offline demo, guarded writes, SDK scripted-model tests, and standalone packaging are implemented; see [`verification_2026-09-10.md`](verification_2026-09-10.md). That September 10 verification did not run real-model inference or final Devpost Submit; the separate September 11 local report is recorded above with its evidence limits.

The current build also generates a bilingual, read-only `report.html` for each offline or live demo attempt. It makes pending review and safety stops visible without pretending to implement caregiver approval. See [Japanese execution guide](../README_JA.md). The report screen is preparation for recording; no public demo video has yet been produced.

## Judging alignment

### Technological Implementation

Priority evidence:

- explicit Strands Agents SDK use;
- explicit provider and model configuration, with local Ollama or Bedrock;
- three real tool calls rather than a chat-only mockup;
- deterministic QC gate before model orchestration;
- live demonstration if possible.

Optional later: Bedrock AgentCore deployment.

### Design

Target one coherent caregiver experience:

`observe → QC decision → quiet record OR human confirmation → daily handoff`

Avoid adding unrelated features until this single loop is smooth.

### Potential Impact

Show the repetitive burden concretely: repeated checking, remembering, recording, and handing information to family or care professionals.

Use simulated data in the public demo. Do not expose real family care data.

### Creativity & Originality

Emphasize the combination of:

- privacy-minimized local sensing;
- QC-style PASS / HOLD / STOP controls;
- an agent that deliberately knows when **not** to decide;
- human-in-the-loop confirmation only when uncertainty requires it.

### Presentation

The final video must show the project actually working, not only slides. The pitch must clearly state:

1. the problem;
2. who it is for;
3. why it matters.

## Optional score boosters

Only after the required path is stable:

- public live demo link;
- Bedrock AgentCore deployment;
- builder.aws build-journey post.

## Do not do yet

- Do not upgrade AWS to a paid plan merely for dashboard widgets.
- Do not launch EC2, RDS, or other persistent services only to earn credits.
- Do not put AWS access keys, patient images, names, addresses, Wi-Fi data, or real care logs in GitHub.
- Do not claim clinical accuracy or diagnosis.
- Do not press final Devpost Submit until the public video and final repository are verified.
