# Submission readiness — what remains?

> **Video link update — September 14, 2026:** the viewing link now points to the owner's replacement video. The prepared replacement is 3:14 with English above smaller Japanese text; the upload itself has not been independently rechecked here. The status, duration, caption order and verification details below describe the earlier checkpoint/edition, not a new verification of this replacement. GitHub link changes do not update Devpost.

**Updated September 14, 2026. The project is still a draft for this hackathon. Final Submit is on hold while the owner reviews the unified materials.**

提出資料を整えてから、本人が最終提出を判断します。

[Watch the video](https://youtu.be/Oej2y-0PFN8) · [Read the project](https://devpost.com/software/yasashii-bowel-care-agent) · [Open the submission list](https://devpost.com/submit-to/30317-agents-for-humans-hackathon/manage/submissions)

## Remaining owner actions

| Action | Why it remains |
|---|---|
| **Confirm the corrected custom code URL was saved** | The Additional info screenshot still showed the old `kenji/tree/main/...` URL. The dedicated URL was supplied for replacement. The next screenshot reached Submit, but did not display the saved replacement value. |
| **Review the unified materials** | Current owner request: clearer, consistent, friendly documentation before submission. |
| **Agree to the terms, then choose final Submit** | Latest screenshot showed the terms checkbox empty and final Submit incomplete. Only the owner can decide to agree and submit. |
| **Confirm the completion screen** | A public project page or four checked input steps is not final-submission proof. |

Correct code URL: [mainitika-ship-it/yasashii-bowel-care-agent](https://github.com/mainitika-ship-it/yasashii-bowel-care-agent).

**Next one operation:** review the [short introduction](../README.md). Before final submission, reopen Additional info once to confirm the corrected code URL remains saved.

The deadline is **September 15, 2026 at 09:00 JST / 00:00 UTC**. See the [official rules](https://agentsforhumans.devpost.com/rules). The submission screen's reminder asks entrants not to change submitted materials after the deadline until after the winner announcement.

## Required items — evidence of the stated scope

| Requirement | Current check |
|---|---|
| Strands workflow | **Verified on three synthetic cases** in the saved Mac run: Strands Agents SDK 1.55.1 + Ollama + `qwen3:8b` |
| Public code repository | **Public** dedicated repository with root README and MIT license; public Devpost project link points here |
| README and execution steps | **Available** in English and Japanese; offline and actual model execution are distinguished |
| MIT / Apache license | **MIT** at repository root |
| Architecture attachment | **Attachment and new bilingual preview visible** in September 14 owner screenshots; attachment bytes not independently downloaded |
| Public video under five minutes | **URL registered on Devpost; owner viewing reported**. Reviewed local file: 235.833 seconds, about 3:56 |
| English or translation | English documentation and narration; video captions Japanese above English; diagram English above Japanese |
| Submitter type, country, track | **Visible in owner screenshots:** Individual, Japan, Everyday Agents |
| AWS Builder ID | **Correct registered email visible** in owner screenshot; account profile previously checked. Email omitted from this public checklist |
| Required form steps | **Four input steps checked**, including Project details and Additional info; individual saved values still need the code-URL check above |
| Final Submit | **Not submitted**: latest screenshot is DRAFT; live project/hackathon `submitted_at` remains unset |

Implementation is not real-world validation. “Visible” describes a screenshot, “registered” describes a live project read, and “verified” describes the specific evidence stated. None means that the whole care product is finished.

## Common facts across the materials

| Topic | Shared wording / result |
|---|---|
| PASS | Record a normal observation after software QC; include it in the handoff |
| HOLD | Save a pending human-review request; exclude it from the handoff |
| STOP | Do not record a normal observation; save a separate safety alert |
| Handoff | **1 PASS observation** in the saved three-case run |
| Source/input evidence | **13 / 13 hashes matched**: ten source files, three inputs |
| Automated tests | **109 passed** in the saved regression result; scripted models and blocked network |
| Actual saved model | **Strands + Ollama + qwen3:8b**, not Bedrock |
| Not yet verified | Bedrock success, real camera integration, real-image performance, real-care benefit and clinical safety |
| Not yet implemented | Caregiver approval screen |
| Planned | Cross-restart duplicate prevention and private real-image evaluation with privacy safeguards |

Separate camera-project tests are not added to the submitted prototype's verified results. QC / IATF-inspired controls are not certification or a conformity claim.

## What the September 14 recheck established

The source was checked against public commit `4d3946bf8dc7d1d74a2b270642f9ab23c2ad78a9` before this documentation update.

- **13 / 13 hashes matched** the saved Mac report again.
- Saved receipts and three one-record logs matched the synthetic inputs; recomputed handoff contained **one PASS observation**.
- A fresh **offline** run, `20260914T014245Z-b57f38099db2`, verified all three cases without model calls. It is not new live-model evidence.
- The [preserved CI run](https://github.com/mainitika-ship-it/yasashii-bowel-care-agent/actions/runs/34735097422) succeeded for source/tests unchanged by later documentation changes. **109 is the saved test result**, not a new full-suite run during this document refresh.

[September 11 original evidence](verification_2026-09-11.md) contains the source, log and prompt-correction provenance. The successful Mac run does not need to be repeated merely to read or present its saved results.

## Video: duration and honest presentation

Current reviewed local audio-refined file: `ybca-voice-refined.mp4`, 1280 × 720, **235.833 seconds (about 3:56)**.

SHA-256: `c7ec081f2059d8b032a06e358b330aadea2fee4b44d4aa37d29e6cd5ac697c3a`.

The video has 20 scenes and 43 bilingual caption intervals. It presents actual offline output and saved Mac model results, labelled separately. The friendly guide's dialogue is narration, not the model's actual speech. It is not a continuous live inference screen recording.

Local AV decoding, caption intervals, representative frames, small-screen review and the closing repository QR were checked. These do not replace normal-speed listening or an iPhone playback test. The owner reports having watched the public YouTube video; exact correspondence between that upload and the audio-refined local file remains unconfirmed here. An earlier “3:51” reference is not the measured duration of this reviewed local file.

## Which documents are current?

| Current entry point | Purpose |
|---|---|
| [English README](../README.md) / [Japanese README](../README_JA.md) | Understand the problem and try the three cases |
| [Architecture](architecture.md) / [bilingual diagram](architecture.png) | See QC, Strands, guarded tools and the three destinations |
| [September 11 verification](verification_2026-09-11.md) | Inspect the original saved evidence |
| This readiness table | See the current preparation status and remaining actions |
| [Earlier storyboard](demo_storyboard.md) | Historical production plan, not the current remaining-work list |

The diagram's September 13 offline note and dated verification reports remain historical facts. New documentation does not turn them into new tests.

Optional live hosting, AgentCore and a builder.aws bonus article can wait. They are not added to the required submission work. The mandatory Strands workflow does not require a successful Bedrock run; see the [official requirement recheck](hackathon_recheck.md).
