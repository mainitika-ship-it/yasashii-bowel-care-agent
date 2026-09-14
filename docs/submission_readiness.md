# Submission readiness — submitted

**Submitted to Agents for Humans Hackathon on September 14, 2026 at 12:36:19 JST.** The live Devpost project confirms `submitted_at: 2026-09-13T23:36:19.437-04:00`.

**提出済みです。** 以前の「下書き・未提出・最終Submit待ち」は提出前の記録です。

[Watch the updated video](https://youtu.be/Oej2y-0PFN8) · [Read the project](https://devpost.com/software/yasashii-bowel-care-agent)

## Latest update — September 14, 2026

- **Video URL:** Devpost and GitHub now point to `Oej2y-0PFN8`; the saved Devpost value was read back.
- **Caption description:** large English text above smaller Japanese translations, confirmed by reading back the Devpost description.
- **Submission:** the original submission timestamp remains present. No additional Submit was performed.
- **Prepared replacement:** the storybook edition is 3:14. Full public playback, audio, duration, thumbnail refresh and exact file correspondence were not independently verified in this update.

**Next one operation:** open the public project and play the embedded video to confirm the replacement appears.

The dedicated repository is [mainitika-ship-it/yasashii-bowel-care-agent](https://github.com/mainitika-ship-it/yasashii-bowel-care-agent). Individual custom answers and attachment bytes are not exposed by the project read API; prior screenshot checks remain distinguished below.

The deadline is **September 15, 2026 at 09:00 JST / 00:00 UTC**. See the [official rules](https://agentsforhumans.devpost.com/rules). The submission screen's reminder asks entrants not to change submitted materials after the deadline until after the winner announcement.

## Required items — evidence of the stated scope

| Requirement | Current check |
|---|---|
| Strands workflow | **Verified on three synthetic cases** in the saved Mac run: Strands Agents SDK 1.55.1 + Ollama + `qwen3:8b` |
| Public code repository | **Public** dedicated repository with root README and MIT license; public Devpost project link points here |
| README and execution steps | **Available** in English and Japanese; offline and actual model execution are distinguished |
| MIT / Apache license | **MIT** at repository root |
| Architecture attachment | **Attachment and new bilingual preview visible** in September 14 owner screenshots; attachment bytes not independently downloaded |
| Public video under five minutes | **Replacement URL registered on Devpost and read back**. Prepared edition: 3:14; public playback and duration not independently rechecked |
| English or translation | English documentation; prepared replacement video and diagram use English above Japanese |
| Submitter type, country, track | **Visible in owner screenshots:** Individual, Japan, Everyday Agents |
| AWS Builder ID | **Correct registered email visible** in owner screenshot; account profile previously checked. Email omitted from this public checklist |
| Required form steps | **Four input steps checked in earlier screenshots**. Submission timestamp now confirmed; individual custom answers not re-read by this API |
| Final Submit | **Submitted**: live project/hackathon `submitted_at` is `2026-09-13T23:36:19.437-04:00` |

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

## Previous video — archived verification, not the replacement

The measurements and checks below concern the earlier edition only; they do not certify the replacement upload.

Previously reviewed local audio-refined file: `ybca-voice-refined.mp4`, 1280 × 720, **235.833 seconds (about 3:56)**.

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
