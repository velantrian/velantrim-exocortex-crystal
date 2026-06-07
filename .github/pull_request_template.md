## Summary

<!-- What does this change do? -->

## Type of change

- [ ] Documentation only
- [ ] Tests only
- [ ] Bug fix
- [ ] New feature
- [ ] Refactor / maintenance
- [ ] Security / privacy hardening

## Truth / memory invariants

- [ ] This change does not bypass Guardian or TruthGate for L3 writes.
- [ ] This change preserves `source`, `source_status`, `claim_type` and epistemic state handling.
- [ ] This change does not promote subjective input or LLM output into world facts without evidence.
- [ ] This change does not weaken erasure, restriction, audit, receipt or provenance behaviour.

## Local-first / privacy check

- [ ] No new outbound network call is introduced by default.
- [ ] No telemetry is introduced.
- [ ] Optional external services are opt-in and documented.
- [ ] No secrets, logs, databases or personal data are committed.

## Tests

Commands run:

```bash
# paste commands here
```

## Documentation

- [ ] README updated if user-facing behaviour changed.
- [ ] ROADMAP updated if delivered/planned status changed.
- [ ] TEST_REPORT / EVAL docs updated if evaluation behaviour changed.

## Notes for reviewers

<!-- Anything that deserves special attention. -->
