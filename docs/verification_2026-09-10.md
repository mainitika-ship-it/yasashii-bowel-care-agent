# Implementation verification — 2026-09-10

## Scope

This update strengthens and rehearses the synthetic observation pipeline. It is not a clinical validation, physical camera test, live Bedrock success claim, or final hackathon submission.

## Implemented

- Validated event values are bound to no-argument tools. Local guards reject a tool that conflicts with QC, injected arguments, and a second write within the same run.
- Privacy-flagged events stop locally before model construction. Input schema rejects free-text extra fields and malformed measurements.
- Explicit paid-model opt-in, per-event fresh agents, a two-cycle model limit, disabled retries, and bounded response length.
- Offline PASS / HOLD / STOP actions, fresh per-run JSONL files, a pending caregiver queue, and a handoff that counts only PASS observations.
- Machine-readable reports with mode, hashes, action receipts, log counts, and explicit separation between offline and live evidence. Failed live attempts remain incomplete and may still incur cost.
- Allowlisted standalone export with a root README, MIT license, CI workflow, and integrity manifest. It does not publish or create a repository.

## Verification commands

Local result: **72 tests passed** on Python 3.12 with Strands Agents 1.55.1 and boto3 1.43.91. The standard-library-only offline run produced PASS, HOLD, STOP, one entry per log, and one handoff observation with `is_live_evidence: false`.

```bash
python -m pytest -q
python -S src/demo.py --mode offline
python src/demo.py --mode qc
python tools/export_submission.py
```

The test suite includes the actual Strands SDK event loop with a scripted in-memory model and forbids network connections. This proves the tested code/tool wiring, not real Nova tool selection or AWS permissions. Tests also exercise input validation, wrong/injected/duplicate calls, concurrent duplicates, privacy-stop bypass, paid-model permission gates, error redaction, fresh-run isolation, handoff counts, and archive boundaries. The standalone archive is extracted and tested independently before handoff.

## Initial remaining items (before the follow-ups below)

- Live Strands + Amazon Bedrock three-case execution and its recording.
- Physical/local-vision integration, caregiver decision UI, and cross-process idempotency.
- Final license display and published CI in the newly owner-created dedicated repository.
- Public demo video, updated diagram attachment, final Devpost required fields, and final Submit.

No AWS request, repository creation, Devpost field change, or final Submit is part of this update. Existing unrelated project files are preserved.

## Dedicated repository follow-up

The owner subsequently created `mainitika-ship-it/yasashii-bowel-care-agent`. The reviewed source is transferred there with a Japanese quick-start guide and a local English/Japanese result screen. The screen distinguishes offline from live evidence and incomplete attempts, escapes displayed fields, does not render raw SDK errors, and has no scripts or external resources. It is a read-only result, not an implemented caregiver approval flow. New renderer tests are additional to the 72 tests reported above; published CI provides the current total and result.

Follow-up result: **76 tests passed locally**, the standard-library-only offline demo succeeded, and standalone source export succeeded. Dedicated-repository [GitHub CI passed](https://github.com/mainitika-ship-it/yasashii-bowel-care-agent/actions/runs/34472636948) on commit `02191d53a787a050b955a6fa8260a10777298a6c`. Root README and LICENSE were fetched after publication; GitHub repository metadata reports the MIT SPDX identifier. No runtime logs or private files were published. Live Bedrock execution, public video, and final Submit remain unperformed.

## Official-requirement and local-provider follow-up

The latest [official recheck](hackathon_recheck.md) confirms that Strands is required but a specific model is not. The implementation now supports an already installed Ollama model as an alternative to explicitly authorized Bedrock. Local metadata checks reject remote forwarding, missing local-weight metadata, and absent or malformed tool capabilities. Local requests disable proxies and redirects, and failures never trigger a paid-provider fallback. These are checks of the local server's claims, not hardware attestation or proof of network isolation.

Local result: **99 tests passed** on Python 3.12, with Strands Agents 1.55.1, boto3 1.43.91, and Ollama Python client 0.6.2. Tests include actual installed SDK model construction and the actual Strands event loop using a scripted in-memory model for the local route. Network connections are forbidden in the test fixture. These tests do **not** establish actual Ollama inference on the owner's Mac or Bedrock model behavior.

Provider-specific result banners and the new `is_live_agent_evidence` flag distinguish completed local-model and Bedrock runs from offline rehearsal and failures. The legacy `is_live_evidence` flag remains Bedrock-only. A reproducible English [architecture PNG](architecture.png) is prepared for the required file attachment and has been visually checked for readable labels and correct action paths. README, Japanese guide, recording storyboard, and readiness checklist now describe both model routes and the current implementation boundary.

Remaining: a real-model three-case run, public video of at most five minutes, owner-reviewed Devpost source URL and diagram update, required-field verification, and final Submit. No real-model inference, Devpost form edit, or final Submit was performed by this follow-up.
