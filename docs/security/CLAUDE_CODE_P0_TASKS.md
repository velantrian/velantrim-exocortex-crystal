# Claude Code P0 Tasks

> Date: 2026-06-17
> Scope: code tasks that require repository inspection, tests and controlled diffs.

## P0-1 Provenance chain

Verify whether the current Crystal code has a provenance-chain implementation affected by the actor/reason signature issue reported in the Titan audit.

Required tests:

- append returns success;
- non-empty chain verifies;
- tampering payload fails verification;
- tampering actor fails verification if actor is hashed;
- tampering reason fails verification if reason is hashed;
- empty chain is not equivalent to verified non-empty chain.

## P0-2 Deployment defaults

Review compose/Dockerfile/dotfiles and patch if needed:

```yaml
VELANTRIM_API_KEY=${VELANTRIM_API_KEY:?Set VELANTRIM_API_KEY}
ports:
  - "127.0.0.1:8000:8000"
```

Also verify non-root container user and `.dockerignore` exclusions.

## P1 Truth and data quality

- Decide production TruthPolicy profile.
- Add data verifier only after confirming actual data schema.
- Ensure graph/autolinker data is not called verified canon without source/evidence.

## Rule

Small PRs only. Do not combine provenance, Docker, TruthPolicy and data verifier into one broad PR.
