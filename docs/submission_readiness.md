# Agents for Humans Hackathon — Submission Readiness

Updated: 2026-09-11 (technical progress; official/Devpost checks remain dated September 10)

This file is the project-side checklist for the final Devpost submission. It is intentionally conservative: an item is marked complete only when it has been verified, not merely planned.

Official requirements and the current Devpost entry were freshly checked on September 10; see [the recheck record](hackathon_recheck.md). **Strands is required, but Bedrock or a specific model is not.** Deadline: **2026-09-15 09:00 JST**. The current Devpost entry has an empty video URL and no hackathon `submitted_at` value; a published project page is not a final hackathon submission.

## Required by the event

| Requirement | Status | Evidence / next action |
|---|---|---|
| Working agent built with Strands Agents SDK | DONE FOR THREE SYNTHETIC CASES | Original Mac `qwen3:8b` reports and logs reviewed: PASS / HOLD / STOP, one matching action per case, one PASS-only handoff. All 10 source hashes and three input hashes match the imported code. See [the evidence review](verification_2026-09-11.md). |
| Public code repository | DONE | https://github.com/mainitika-ship-it/yasashii-bowel-care-agent is public, with root README and MIT license. The reviewed Mac prompt correction and original synthetic evidence are included. Devpost's repository field still needs owner-reviewed updating. |
| README | DONE | Setup, architecture, safety, pre-existing disclosure, and demo commands are documented. |
| MIT or Apache license | DONE | Root `LICENSE` is published. GitHub repository metadata identifies its license as MIT (`spdx_id: MIT`), verified 2026-09-10. |
| Architecture diagram | FILE READY / UPLOAD UNVERIFIED | [architecture.png](architecture.png) matches the current implementation and is in an accepted attachment format. Upload/recheck the final file on Devpost. |
| Demo video, max 5 minutes | NO PUBLIC VIDEO PROVIDED | Next: record the verified build and explain its three outcomes. See `docs/demo_storyboard.md`. A saved HTML report is not a video. |
| AWS Builder ID | PREVIOUSLY DONE | Prior record says it was entered; recheck the final required field before Submit. |
| Problem / audience / why it matters | DONE | Present in Devpost story and README. |
| English or English translation | TEXT READY / VIDEO PENDING | README and PNG are in English; the public video must also use English narration or translation. |
| Required fields and final Submit | NOT COMPLETE | Current Devpost repository URL still points to the old parent folder. Submitter type, country, track, source URL, architecture upload, and AWS Builder ID must be checked by the owner. |

## Core implementation gate

### September 11 local run: original evidence received and reviewed

Run `20260911T051811Z-50c8566cb79e` completed the three synthetic cases with local `qwen3:8b`. The handoff ZIP has been received and checked: all 28 manifest entries and all 13 source/input run-time hashes match; the three logs agree with the samples and QC actions; HOLD stays pending; the saved handoff counts one PASS observation. The original HTML matches the JSON rendered with the recorded source.

The exact prompt correction was imported. It explains that tool arguments must be `{}` and that the event is already bound to the tool. AST comparison confirms no other executable source change; the argument, action, duplicate-write, model-cycle, and privacy guards remain in place. Original evidence and provenance limits are documented in [the September 11 review](verification_2026-09-11.md).

This closes the original-file handoff task. No inference was repeated to review or import the bundle. A successful synthetic demonstration is not validation for real care use. The next submission artifact is the public video.

### Reproduction checks when a new run is needed

For the working-agent portion of the video, complete these three checks:

1. Choose one real model route. For local Ollama, follow the [metadata check and setup](local_model_guide.md); for Bedrock, obtain owner permission for costs and run the paid preflight.
2. `python src/demo.py --mode qc` shows PASS, HOLD, STOP in that order.
3. Run `python src/demo.py --mode live --provider ollama --model-id YOUR_INSTALLED_MODEL` or the Bedrock command `python src/demo.py --mode live --allow-paid-model`. A fresh report must have `verified=true`, `is_live_agent_evidence=true`, and one matching tool for each case. The older `is_live_evidence` field is Bedrock-only and is false for local Ollama.

The local-vision connection is a separate project integration goal, not an additional official requirement or evidence already achieved. Show and label synthetic input in the public demo; do not claim camera integration. The offline demo, guarded writes, SDK scripted-model tests, and standalone packaging are implemented; see [`verification_2026-09-10.md`](verification_2026-09-10.md). The separate [September 11 review](verification_2026-09-11.md) covers the original local-model report and its evidence limits. Final Devpost Submit remains an owner action.

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
