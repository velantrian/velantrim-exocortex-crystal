<!-- d2-source-contract: CURRENT -->
<!-- d2-source-scope: reviewer-security-privacy-failure -->
# Failure Modes and Mitigations

**Status date:** 2026-08-08  
**Authority:** this matrix summarizes current boundaries. Use
[`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md), executable tests and exact CI for
implementation proof.

Mitigations do not prove perfect truth or production safety. They make unsupported state
blocked, labelled, refused, bounded or auditable.

| Failure mode | Risk | Safe behaviour / mitigation | Status |
|---|---|---|---|
| TruthGate bypass | unverified material silently becomes trusted | Guardian/TruthGate remain admission authority; explicit curator override is attributed and audited | implemented |
| LLM self-certification | model output promotes itself to verified world fact | LLM output remains unverified and cannot independently satisfy world-fact admission | implemented |
| Public query writes | `ask`, receipt or inspection mutates memory | `core.query_pipeline.query()` and public inspection surfaces are read-only; behaviour pinned by tests | implemented |
| Weak grounding | answer is produced without sufficient evidence | bounded refusal/abstention instead of invented grounding | implemented |
| Physical graph read as all true | multi-status L3 is confused with strict Canon | strict Canon is a deny-dominant trusted read projection, not the whole graph | implemented |
| Contradiction hidden or destructive | conflicting knowledge is lost or answered confidently | explicit contradiction links and dispositions preserve history; answer policy remains evidence-aware | partial/implemented baseline |
| Missing provenance | claim cannot be attributed | source/evidence vocabulary, spans, receipts and strict replay checks; unsupported world facts are blocked | implemented |
| Silent curator override | governance action changes state without accountability | override is explicit, scoped, attributed and audit-recorded; it does not rewrite TruthGate policy | implemented |
| Receipt or audit tampering | trace appears valid after modification | digest/hash-chain verification fails closed | implemented |
| Durable backend drift | process silently opens a different graph | locked storage profile, locator digest and conflict checks fail before caching | implemented |
| Automatic ephemeral fallback | durable deployment appears empty in Mock | first durable `auto` must select LadybugDB or SQLite; implicit Mock fallback is rejected | implemented |
| SQLite backup corruption | restore introduces unverified state | independent verification and inactive restore; restored data is not automatically admitted | implemented |
| Unbounded migration memory/disk | export/import exhausts resources | fixed limits, batches, disk-backed ordering/reference checks and cleanup | implemented within documented envelope |
| PostgreSQL import failure | partial target or exposed error activates runtime | serializable transaction, rollback, redacted errors and `active=false` target | implemented inactive path |
| Import mistaken for activation | successful equivalence selects PostgreSQL | target absent from normal runtime composition; no automatic switch/cutover | implemented boundary |
| ANN retrieval treated as exact evidence | approximate result gains authority | ANN acceptance/evaluation remains separate and unimplemented | not implemented / blocked from claim |
| Secret leakage | credentials enter receipts, logs or public records | DSN supplied by named environment variable; non-secret locator digest; bounded redaction | implemented baseline |
| API exposed broadly | local claims become network-accessible | loopback documented default, token baseline, TLS/auth required before wider exposure | partial; operator responsibility |
| Personal data survives erasure | copies remain in backups/exports/providers | active-store erasure plus explicit copy inventory and external deletion policy | partial; operator responsibility |
| Encryption assumed universal | unencrypted L3/backups/logs are overlooked | field-level L1 encryption limits documented; host/storage controls required | partial |
| Optional dependency unavailable | runtime silently changes semantics | explicit bounded failure or locked alternative; no hidden durable switch | implemented baseline |
| Research concept read as runtime | roadmap/RFC is presented as implemented | status map and authority hierarchy distinguish research, RFC and merged runtime | implemented docs boundary |
| Biological metaphor read as consciousness | architecture language overstates system nature | explicit non-goals; metaphors are engineering inspiration only | implemented docs boundary |
| Grant baseline re-budgeted | merged work is counted again as future funding | baseline/funded-delta matrix and no-award/no-budget-change controls | implemented docs boundary |

## Status vocabulary

- **implemented** — merged code plus executable evidence enforces the stated boundary;
- **partial** — a useful mechanism exists, but operator policy or additional hardening remains;
- **not implemented / blocked from claim** — the capability is absent and documentation must
  not imply it exists;
- **operator responsibility** — the repository provides a baseline, but deployment choices
  determine the final exposure.

## Explicit non-claims

Nothing in this matrix claims:

- elimination of model error or hallucination;
- security, legal or GDPR certification;
- arbitrary-scale or production-readiness proof;
- active PostgreSQL runtime, automatic switching, cutover, rollback or dual-write;
- globally complete erasure across external copies;
- awarded NLnet funding.

For a compact translation-oriented overview, read
[`SAFETY_PRIVACY_AND_FAILURES.md`](./SAFETY_PRIVACY_AND_FAILURES.md).
