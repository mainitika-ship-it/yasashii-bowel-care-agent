# Architecture

![Yasashii Bowel Care Agent architecture](architecture.png)

This PNG is suitable for Devpost's required architecture file upload. It is generated from repository-owned shapes and English labels with `python tools/render_architecture.py` after installing `requirements-assets.txt`. File preparation does not imply the attachment has been updated on Devpost.

```mermaid
flowchart TD
    A[Synthetic JSON samples] --> C[Schema and explainable QC]
    B[Pre-existing vision: integration unverified] -.-> C
    C -->|Live and privacy check passed| E[Fresh Strands agent: Bedrock or Ollama]
    C -->|Offline or privacy stop| K[Local action guard]
    E --> K
    K -->|PASS| F[Observation record]
    K -->|HOLD| G[Pending caregiver queue]
    K -->|STOP| H[Safety alert]
    F --> J[Daily handoff]
```

## Boundary between pre-existing and hackathon work

**Pre-existing prototype, disclosed:** local toilet-water-region monitoring, possible-event detection, changed-area measurement, relative amount classification, CSV logging, privacy and signal guards.

**New during the hackathon:** Strands-based orchestration, the explainable PASS/HOLD/STOP policy, human-confirmation and safe-stop tools, privacy-minimized JSONL records, handoff summaries, tests, and the end-to-end agent behavior.

## Why the deterministic QC layer remains outside the model

The local QC policy validates critical conditions before the model is asked to act. A privacy-flagged event bypasses both model routes and creates its safety alert through the local guard. For other validated live events, the Strands agent selects the tool, but a pre-tool hook and local `EventRun` guard enforce the QC match and reject duplicate writes. The no-argument tools use original validated event values; model-generated amounts, notes, or identities cannot enter the log through tool arguments.

Each event uses a fresh agent with a two-model-cycle limit and disabled SDK retries. Offline rehearsal bypasses the model and uses the same local write guard. Offline results and scripted-model SDK tests are clearly separated from actual model inference. The per-run guard is not cross-process idempotency; this remains a synthetic demonstration prototype.

The [local Ollama route](local_model_guide.md) requires an installed model advertising tool support and local GGUF metadata. Requests use numeric loopback with proxies and redirects disabled. This is an application check, not independent proof of server behavior or network isolation. Bedrock calls require explicit paid opt-in; local failures never fall back to Bedrock. Neither provider has a captured real-model three-case success from this build environment.

## Safety principles

- Public demos use safe simulated data.
- No medical diagnosis.
- No patient identity is needed by the agent.
- Raw images are not required once the local vision layer has produced a structured event.
- Uncertainty is escalated to a human rather than silently converted into a factual claim.
- A failed signal or privacy check stops automatic recording.
