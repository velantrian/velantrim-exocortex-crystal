# Follow-up: Issue #196 — Claim rewrite / semantic integrity

**Priority:** P0/P1  
**Status:** Not implemented in PR #206 — tracked as explicit follow-up  
**Branch target:** `cursor/claim-versioning-196-0d0d` (future)

## Problem

Today, `update_fact()` can rewrite `claim` text on an existing `fact_id` without
recording claim version history or a content hash. A receipt or trace that cites
`fact_id` alone cannot detect silent semantic drift after the citation was sealed.

This is **not** fully addressed by the audit-hardening work in PR #206. Semantic
integrity of cited claims remains incomplete until this follow-up lands.

## Proposed scope (minimal)

1. Add `claim_hash` (sha256 of normalized claim) on every ingest/store path.
2. On `update_fact(claim=...)`, bump `claim_version` and append to a lightweight
   per-fact version ledger (or block claim mutation outside `supersede()`).
3. Extend `provenance.verify_receipt()` to compare sealed `claim_sha256` against
   live fact + version metadata; surface `modified` / `version_mismatch`.
4. Tests pinning receipt replay after claim rewrite.

## Non-goals for the follow-up PR

- Full bi-temporal schema (RFC backlog)
- Automatic migration of legacy facts without `claim_hash`

## Acceptance criteria

- [ ] No silent claim rewrite on existing canon ids without version audit trail
- [ ] Receipt replay flags semantic change even when `fact_id` is stable
- [ ] 100% coverage gate preserved
