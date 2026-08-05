## Summary

<!--
What does this change do, and why? Focus on the what and why — not the how.
The diff shows the how.
-->

## Grant alignment

<!--
Optional. If this PR addresses a funded work package, note it here.
Examples: WP1 (Evidence Span Store), WP2 (Import Sessions), WP3 (Evaluation Harness),
          WP4 (Knowledge Adapters), WP5 (Documentation & Demonstrators)
Leave blank if not applicable.
-->

- WP addressed (if any):

## Test plan

- [ ] New tests added (or existing tests updated) to cover the change.
- [ ] Coverage gate passes (`python -m pytest tests/ --cov=. --cov-fail-under=100 -q`).
- [ ] Coverage gate was not bypassed (no `# pragma: no cover` added without justification).

## Security checklist

- [ ] No direct write to L3 canon that bypasses Guardian/TruthGate.
- [ ] TruthGate remains the only automatic canon write path.
- [ ] No new bypass of stdlib-level integrity controls (`ImmutableCore`, HMAC chain, audit log).
- [ ] No secrets, personal data, private datasets or API keys are committed.
- [ ] Any new optional external service is opt-in and documented.

## Documentation synchronization

Follow [`docs/DOCUMENTATION_SYNC_PROTOCOL.md`](../docs/DOCUMENTATION_SYNC_PROTOCOL.md).
Do not remove this block; it is the change-history contract for humans and AI agents.

- Documentation impact: `NONE` / `GITHUB_ONLY` / `GITHUB_AND_NOTION`
- GitHub documentation updated (paths, or `NOT_REQUIRED` with reason):
- Public capability/status/grant claims reviewed: `YES` / `NOT_REQUIRED` with reason
- Notion synchronization: `NOT_REQUIRED` / `PLANNED` / `DONE` / `BLOCKED`
- Notion record (safe title, internal reference, or public URL):
- Decision / ADR reference:
- Historical note: what changed from the original plan, if anything?

For `GITHUB_AND_NOTION`, keep the PR draft until the Notion record contains the
motivation, intended function, decision, alternatives, trust/authority boundaries,
grant or roadmap impact, evidence, exact reality status, limitations, and PR link.
After merge, add the final merge SHA and verified checkpoint to Notion.

## Notes for reviewer

<!--
Anything that deserves special attention: subtle logic, known trade-offs,
follow-up issues filed, or areas where you are uncertain.
-->
