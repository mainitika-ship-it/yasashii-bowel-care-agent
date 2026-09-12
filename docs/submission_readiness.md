# Agents for Humans Hackathon — Submission Readiness

Updated: 2026-09-12 (saved technical evidence, prepared video, and live Devpost checks)

This file is the project-side checklist for the final Devpost submission. It is intentionally conservative: an item is marked complete only when it has been verified, not merely planned.

The [official requirements](https://agentsforhumans.devpost.com/) and current Devpost entry were checked again on September 12. **Strands is required, but Bedrock or a specific model is not.** Deadline: **2026-09-15 09:00 JST**. The public project tagline and description have been updated and read back successfully. The video URL remains empty and the hackathon `submitted_at` value remains unset; a published project page is not a final hackathon submission. The [earlier recheck record](hackathon_recheck.md) remains dated historical context.

## Required by the event

**Status meanings:** implemented means the software path exists; verified means evidence confirms the stated test scope. The verified model run uses synthetic data. It does not establish real-world camera performance or effectiveness in care. Planned work and items unverified here are not counted as completed.

| Requirement | Status | Evidence / next action |
|---|---|---|
| Working agent built with Strands Agents SDK | DONE FOR THREE SYNTHETIC CASES | Original Mac `qwen3:8b` reports and logs reviewed: PASS / HOLD / STOP, one matching action per case, one PASS-only handoff. All 10 source hashes and three input hashes match the imported code. See [the evidence review](verification_2026-09-11.md). |
| Public code repository | DONE | https://github.com/mainitika-ship-it/yasashii-bowel-care-agent is public, with root README and MIT license. The reviewed Mac prompt correction and original synthetic evidence are included. Devpost's repository field still needs owner-reviewed updating. |
| README | DONE | Setup, architecture, safety, pre-existing disclosure, and demo commands are documented. |
| MIT or Apache license | DONE | Root `LICENSE` contains the MIT license. Repository license metadata was checked previously on September 10; it was not returned by the September 12 metadata read. |
| Architecture diagram | FILE READY / UPLOAD UNVERIFIED | [architecture.png](architecture.png) matches the current implementation and is in an accepted attachment format. Upload/recheck the final file on Devpost. |
| Demo video, max 5 minutes | CANDIDATE VERIFIED UNDER 5 MIN / PUBLIC URL MISSING | `ybca-voice-refined.mp4`: measured 235.833 seconds (about 3:56), English narration, Japanese-above-English captions, actual offline output and saved Mac results. Publish the prepared file, check anonymous playback, and register the URL. |
| AWS Builder ID | PREVIOUSLY DONE | Prior record says it was entered; recheck the final required field before Submit. |
| Problem / audience / why it matters | DONE | Updated public Devpost introduction explains family-care burden, the synthetic workflow, evidence, and limits. |
| English or English translation | FILES READY | README, PNG and Devpost text are in English. The prepared video has English narration and Japanese-above-English captions; public playback remains to be checked. |
| Required fields and final Submit | NOT COMPLETE | Current Devpost repository URL still points to the old parent folder. Submitter type, country, track, source URL, architecture upload, and AWS Builder ID must be checked by the owner. |

## Core implementation gate

### September 11 local run: original evidence received and reviewed

Run `20260911T051811Z-50c8566cb79e` completed the three synthetic cases with local `qwen3:8b`. The handoff ZIP has been received and checked: all 28 manifest entries and all 13 source/input run-time hashes match; the three logs agree with the samples and QC actions; HOLD stays pending; the saved handoff counts one PASS observation. The original HTML matches the JSON rendered with the recorded source.

The exact prompt correction was imported. It explains that tool arguments must be `{}` and that the event is already bound to the tool. AST comparison confirms no other executable source change; the argument, action, duplicate-write, model-cycle, and privacy guards remain in place. Original evidence and provenance limits are documented in [the September 11 review](verification_2026-09-11.md).

This closes the original-file handoff task. No inference was repeated to review or import the bundle. A successful synthetic demonstration is not validation for real care use. The next submission artifact is the public video.

### Reproduction checks when a new run is needed

The successful Mac run does not need to be repeated merely to inspect or present its saved results. If another live run is needed, use these checks:

1. Choose one real model route. For local Ollama, follow the [metadata check and setup](local_model_guide.md); for Bedrock, obtain owner permission for costs and run the paid preflight.
2. `python src/demo.py --mode qc` shows PASS, HOLD, STOP in that order.
3. Run `python src/demo.py --mode live --provider ollama --model-id YOUR_INSTALLED_MODEL` or the Bedrock command `python src/demo.py --mode live --allow-paid-model`. A fresh report must have `verified=true`, `is_live_agent_evidence=true`, and one matching tool for each case. The older `is_live_evidence` field is Bedrock-only and is false for local Ollama.

The local-vision connection is a separate project integration goal, not an additional official requirement or evidence already achieved. Show and label synthetic input in the public demo; do not claim camera integration. The offline demo, guarded writes, SDK scripted-model tests, and standalone packaging are implemented; see [`verification_2026-09-10.md`](verification_2026-09-10.md). The separate [September 11 review](verification_2026-09-11.md) covers the original local-model report and its evidence limits. Final Devpost Submit remains an owner action.

The current build also generates a bilingual, read-only `report.html` for each offline or live demo attempt. It makes pending review and safety stops visible without pretending to implement caregiver approval. See [Japanese execution guide](../README_JA.md).

### Prepared video and remaining publication step

The owner-approved video has 20 scenes and 43 bilingual caption intervals. Gentle explanatory dialogue supports the story without presenting the guide's lines as actual agent speech. Actual offline output and saved Mac model results are labelled separately; no live inference screen recording is claimed.

Current reviewed file: `ybca-voice-refined.mp4`, 1280 x 720, **235.833 seconds (about 3:56)**. SHA-256: `c7ec081f2059d8b032a06e358b330aadea2fee4b44d4aa37d29e6cd5ac697c3a`. This file is prepared outside the source repository; no public video URL is available yet. The owner supplied a 235.836667-second copy, whose content matched the original master across all 43 caption intervals. The requested audio refinement uses 4% faster speech, gentle equalization and a quieter music mix; the picture and burned-in caption stream remain identical to the verified master. Full AV decoding passed and all 43 speech segments fit their original caption intervals. Original visual checks covered 390/640-pixel review and QR decoding. Physical-device playback and independent listening evaluation remain unverified; these checks do not establish real-care benefit.

The project owner's preparation package also contains the matching architecture PNG and original synthetic evidence. This is a convenience package, not an additional official ZIP requirement. Final video publication, required-field checks, and Submit remain separate actions.

The available project read exposes the video URL and project/hackathon links, but not all saved custom answers or attachment state. Architecture upload and AWS Builder ID therefore remain **unverified here**, not assumed absent or complete.

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

The final video must demonstrate the working project. The official guidance permits slides, screen recordings, and voiceover; it does not require a new inference recording. The pitch must clearly state:

1. the problem;
2. who it is for;
3. why it matters.

### Evidence limits

Real camera integration, real-image detection performance, real-care benefits, and clinical safety remain unverified. The caregiver approval UI is not implemented, and duplicate-write protection does not span process restarts. Private real-image evaluation with privacy safeguards is planned work, not a completed result.

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
