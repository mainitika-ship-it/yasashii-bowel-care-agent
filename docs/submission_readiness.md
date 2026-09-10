# Agents for Humans Hackathon — Submission Readiness

Updated: 2026-09-10

This file is the project-side checklist for the final Devpost submission. It is intentionally conservative: an item is marked complete only when it has been verified, not merely planned.

## Required by the event

| Requirement | Status | Evidence / next action |
|---|---|---|
| Working agent built with Strands Agents SDK | IN PROGRESS | Agent and tools exist; live Bedrock three-case run still needs to be captured. |
| Public code repository | VERIFY DEPLOYED CONTENT | Owner created the public dedicated repository: https://github.com/mainitika-ship-it/yasashii-bowel-care-agent . Root source, README, license and CI are being placed there in this update; verify the published commit and CI. |
| README | DONE | Setup, architecture, safety, pre-existing disclosure, and demo commands are documented. |
| MIT or Apache license | VERIFY DISPLAY | MIT `LICENSE` is at the dedicated repository root. Confirm GitHub identifies it as MIT after publication. |
| Architecture diagram | RECHECK | Prior record says an image is on Devpost. Updated guard/privacy-bypass Mermaid source is in `docs/architecture.md`; ensure the final uploaded diagram matches. |
| Demo video, max 5 minutes | NOT STARTED | Record only after the live end-to-end flow is stable. See `docs/demo_storyboard.md`. |
| AWS Builder ID | PREVIOUSLY DONE | Prior record says it was entered; recheck the final required field before Submit. |
| Problem / audience / why it matters | DONE | Present in Devpost story and README. |

## Core implementation gate

Do not record the final video until all four checks below pass:

1. With owner permission for costs, `python src/bedrock_preflight.py --allow-paid-model` returns `credentials_ok=true` and `bedrock_ok=true`.
2. `python src/demo.py --mode qc` shows PASS, HOLD, STOP in that order.
3. `python src/demo.py --mode live --allow-paid-model` creates a fresh report with `verified=true` and `is_live_evidence=true`, and one matching tool for each case.
4. A real local-vision structured event can be handed to the same agent interface without patient-identifying data.

The local-vision connection is a project integration goal, not evidence already achieved or a reason to publish real care data. Safe synthetic data must be used in the public demo. The offline demo, guarded writes, SDK scripted-model tests, and standalone packaging are now implemented; see [`verification_2026-09-10.md`](verification_2026-09-10.md). No live AWS request or final Devpost Submit was performed in this update.

The current build also generates a bilingual, read-only `report.html` for each offline or live demo attempt. It makes pending review and safety stops visible without pretending to implement caregiver approval. See [Japanese execution guide](../README_JA.md). The report screen is preparation for recording; no public demo video has yet been produced.

## Judging alignment

### Technological Implementation

Priority evidence:

- explicit Strands Agents SDK use;
- Amazon Bedrock / Nova Lite model configuration;
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
