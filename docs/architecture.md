# Architecture — AI helps. People decide.

**Prepared input → quality checks → a guarded action → a clear handoff.**

家族介護の記録を支え、不確かなときは人へ戻す構成です。

![Yasashii: synthetic input, QC checks, Strands, guarded tools, then PASS record / HOLD pending / STOP alert. Only PASS enters the handoff.](architecture.png)

[Open the full-size diagram](architecture.png) · [Try the workflow](../README.md#try-the-three-cases) · [Review the evidence](verification_2026-09-11.md)

This bilingual diagram uses English above Japanese, rounded cards and symbols as well as color. Its September 13 offline check is a dated result, not a claim of new inference. The same design is visible in the owner's September 14 Devpost attachment preview; that preview is not a byte-for-byte download verification.

## One input, three destinations

| Outcome | Plain meaning | Output | Handoff |
|---|---|---|---|
| ✓ **PASS — Record** | The prepared input passes software checks. | One normal observation | Included |
| ? **HOLD — Ask a person** | The input is uncertain. | One pending review request | Excluded |
| ! **STOP — Stop & alert** | Signal or privacy controls fail. | One separate safety alert | Excluded |

**The saved demonstration has one PASS observation in the handoff.** HOLD is not human approval: no caregiver approval screen or automatic caregiver notification is implemented.

## Where Strands is used

1. **Input:** validate prepared synthetic JSON. The camera connection is not part of the verified input path.
2. **QC:** fixed code checks signal health, the supplied privacy flag, event type, confidence and relative amount.
3. **Strands Agents SDK:** a fresh agent selects a no-argument tool matching that QC decision.
4. **Guarded tools:** a pre-tool hook and local `EventRun` reject wrong actions, invented arguments and duplicate writes within the same event execution.
5. **Handoff:** summarize only normal PASS observations; keep pending reviews and alerts separate.

Offline execution and privacy-flagged inputs skip the model and reach the same local guard directly. A privacy flag is supplied input, not an automatic detector of personal information in images.

## QC / IATF-inspired thinking

| Principle | What it means here |
|---|---|
| ✓ **Check** | Validate input and apply known rules first. |
| ◇ **Prevent** | Block wrong tool actions, invented values and repeat writes within one execution. |
| ! **React** | Keep uncertain inputs pending; separate safety alerts from observations. |
| ↗ **Trace** | Preserve reason codes, logs and source/input hashes. |

These are quality-management ideas used to explain existing controls, **not IATF 16949 certification, a conformity claim or clinical safety validation**. [QC method and thresholds](qc_method.md)

## Evidence, kept separate

| Evidence | Verified scope |
|---|---|
| Saved Mac run · September 11 | Strands Agents SDK 1.55.1 + Ollama + `qwen3:8b`; PASS / HOLD / STOP with synthetic inputs |
| Handoff | **1 PASS observation** |
| File comparison | **13 / 13 source/input hashes matched** |
| Automated tests | **109 passed**, preserved scripted-model result with network access blocked |
| Offline rehearsal | Local QC, guarded writes and handoff; **no AI model call** |

[Original reports and logs](verification_2026-09-11.md) document provenance and limits. File hashes demonstrate consistency with received evidence, not independent attestation of model execution. The source is not changed by this documentation update.

## Model routes and execution limits

**Verified saved model route:** Strands + local Ollama + `qwen3:8b`.

**Alternative implemented route:** Amazon Bedrock. Successful Bedrock execution remains unverified. Paid requests require explicit opt-in; local failures do not fall back to Bedrock.

Each event uses a fresh agent, at most two model cycles, and disabled SDK retries. No-argument tools use original validated values; the model cannot supply new care values. Duplicate prevention is within one event execution, not across processes or restarts.

The local route checks tool support and local GGUF metadata, uses numeric loopback, and disables proxies and redirects. These checks rely on truthful server metadata; they are not independent proof of network isolation. [Local model details](local_model_guide.md)

## Existing work and new hackathon work

**Pre-existing, disclosed:** local toilet-water-region monitoring, possible-event detection, changed-area measurement, relative amount classification, CSV logging and privacy/signal guards.

**New during the hackathon:** Strands orchestration, the PASS / HOLD / STOP policy, guarded tools, pending-review records, handoff summaries and repeatable verification. The separate camera prototype has not been validated as an integrated input to this submitted workflow.

## Still to validate or build

- **Unverified:** real camera integration, real-image detection performance, real-care benefits and clinical safety.
- **Not implemented:** caregiver approval screen.
- **Future work:** duplicate prevention across restarts and private real-image evaluation with privacy safeguards.

The prototype supports observation and communication; it does not diagnose illness. Missing observations are not proof that no bowel movement occurred.

<details>
<summary>Diagram history and rendering</summary>

The current `architecture.png` is the bilingual design also supplied for the Devpost attachment. The [earlier English diagram](https://github.com/mainitika-ship-it/yasashii-bowel-care-agent/blob/4d3946bf8dc7d1d74a2b270642f9ab23c2ad78a9/docs/architecture.png) remains in repository history. The existing `tools/render_architecture.py` is the earlier renderer: rerunning it would replace the current image with that earlier design. It does not reproduce the new bilingual diagram.

</details>
