# Dedicated repository provenance and packaging

Canonical public source: https://github.com/mainitika-ship-it/yasashii-bowel-care-agent

The owner created this empty public repository. The initial source was prepared from the YBCA folder at commit `5c259ed7c3aa8445fa0dbe544df491afce41b2cc` in `mainitika-ship-it/kenji`, then enhanced with a read-only bilingual result screen and Japanese setup guide. The parent repository and its unrelated project remain untouched. Its history was not copied into this repository.

`README.md`, `README_JA.md`, and `LICENSE` belong at this repository root. The license is MIT. Root CI runs the network-isolated tests, offline synthetic demo, and source packaging. No AWS credentials are required by CI.

## Rebuild a source archive

```bash
python tools/export_submission.py
```

This creates `dist/yasashii-bowel-care-agent.zip` from an explicit list of source files, adds root CI and a SHA-256 manifest, and excludes history, runtime logs, `.env`, virtual environments, and unlisted files. Symlinks, non-synthetic samples, and several common credential patterns are rejected. These checks do not replace a privacy review. Existing archives are never overwritten; use `--output dist/review-2.zip` for another build.

If source files change, regenerate the archive and its manifest. The manifest describes the exported source files, not a signed proof of execution.

## Remaining submission work

Verify the public repository's license display and CI, then use this repository URL in Devpost after owner review. The Devpost entry is not edited by repository setup. Review real-model evidence from either the local Ollama or Bedrock route, then complete a public video under five minutes, required fields, and owner-confirmed final Submit. See [the current evidence status](submission_readiness.md); the September 11 Mac-local success report still needs its original files and exact source reconciled with the public repository.
