# Reviewed Mac live demo — September 11, 2026

The owner's Mac ran Strands Agents SDK 1.55.1 with local Ollama and `qwen3:8b` on three synthetic samples. The original successful reports and logs were received in a handoff ZIP and independently checked against the enclosed source and this repository. No inference was repeated during this artifact review.

Run: `20260911T051811Z-50c8566cb79e`, started **2026-09-11 14:18:11 JST**. The observation date of August 18 is part of the synthetic fixtures; it is not the execution date or a real person's care record.

## Results from the received files

| Case | Completed tool | Saved result | Included in handoff |
|---|---|---|---|
| PASS | `record_observation` | One observation, relative amount `medium` | Yes: one observation |
| HOLD | `request_caregiver_confirmation` | One request, `confirmation_status: pending` | No |
| STOP | `stop_and_check_signal` | One safety alert | No |

Each case records one tool attempt, a matching QC action, `model_called: true`, and `execution_failed: false`. The report records `verified: true`, `is_live_agent_evidence: true`, and `model_provider: ollama`. Every case has `bedrock_called: false`; the legacy Bedrock-only `is_live_evidence: false` is expected.

Reviewed original files, copied byte-for-byte into this repository:

- [Machine-readable report](evidence/20260911T051811Z-50c8566cb79e/report.json)
- [Bilingual report screen](evidence/20260911T051811Z-50c8566cb79e/report.html) — download/open locally to view
- [PASS log](evidence/20260911T051811Z-50c8566cb79e/event_log.jsonl)
- [Pending HOLD log](evidence/20260911T051811Z-50c8566cb79e/confirmation_queue.jsonl)
- [STOP log](evidence/20260911T051811Z-50c8566cb79e/system_alerts.jsonl)
- [Saved handoff](evidence/20260911T051811Z-50c8566cb79e/handoff.json)

## Independent checks

- All **28 manifest entries** matched the received ZIP contents; there were no extra files beyond the manifest itself.
- All **10 source hashes and three executed sample hashes** in `report.json` matched the received files. They also match this repository after the prompt change below.
- Each log's exact fields and values matched its validated synthetic input and deterministic QC decision, with no model-supplied notes or extra fields.
- Recomputing the handoff from the three records produced exactly the saved handoff: one PASS observation, with HOLD and STOP excluded.
- Rendering the saved JSON through the unchanged report renderer reproduced the original HTML exactly.
- Source, samples, requirement files, and license differed from public baseline `c096cac95d239480297e2340e101ae48d1865800` in **one file only: `src/agent.py`**. An AST comparison confirmed that only the system-prompt string changed.

Handoff ZIP SHA-256: `96600f0892fc9b601232a55e3163c7116531f904ac02820fcbfd65ac4c2a6891`.

Original `report.json` SHA-256: `e1d14f0f0e3b168c546a006a1a8a296afa684da024d4aaf2991986c0007094fa`.

Original `report.html` SHA-256: `fdb5c4579235879154f901b7f848bb6bf4933f9316cec813e2d1fd7628959974`.

These hashes establish consistency with the received files, not a signed attestation of model execution. The reports contain run-time hashes for source and executed inputs; hashes for reports, outputs, and requirement files were captured at packaging time. The ZIP did not include raw inference traces or the earlier failed run, and this review did not repeat the model run.

## Prompt correction and preserved controls

The Mac handoff describes an earlier rejection when the model supplied an `event` argument to a no-argument tool. The revised prompt explicitly requires the empty JSON object `{}`, forbids extra keys, and explains that the validated event is already bound to each tool. This is the exact prompt used by the successful recorded run; no additional production-source changes were made during import.

The executable guards remain unchanged: reject model-supplied arguments, incorrect actions, repeated tool calls, or more than two model cycles; reject duplicate writes within one `EventRun`; stop privacy-flagged inputs locally; exclude pending reviews and safety alerts from the handoff. This does not add deduplication across process restarts.

The SDK regression suite now also checks the specific rejected `event` argument. **109 tests passed locally** after importing the prompt correction. Test execution is network-blocked and uses scripted models; it is a separate check from the saved Mac live run. See the repository's automated checks for the result on this change.

## Reproduce when another run is needed

With the existing local Ollama server, installed `qwen3:8b`, and project virtual environment ready:

```bash
.venv/bin/python src/demo.py --mode live --provider ollama --model-id qwen3:8b
```

This invokes a real local model and creates a new run. It is not necessary to repeat the successful run merely to inspect the saved evidence. Open the preserved HTML and JSON above for that purpose.

## Remaining scope

This evidence covers one synthetic three-case run, not repeated-run reliability, camera integration, clinical accuracy, constant monitoring, or caregiver approval controls. Bedrock was not tested in this run. A public video and the owner's final Devpost checks/Submit remain separate work.
