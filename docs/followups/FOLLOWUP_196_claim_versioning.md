# Follow-up: Issue #196 — Claim rewrite / semantic integrity

**Priority:** P0/P1  
**Status:** Minimal blocking policy implemented in the Issue #196 fix PR

## Problem

Before the Issue #196 fix, `store_fact()` / `update_fact()` could rewrite claim
text on an existing promoted `fact_id` without resetting its epistemic state.
Evidence and validation for claim A could therefore silently describe claim B.

This is **not** fully addressed by the audit-hardening work in PR #206. Semantic
integrity of cited claims remains incomplete until this follow-up lands.

## Implemented minimal policy

1. `Observed` / `Hypothesized` claims may still be refined in place.
2. `Supported`, `Validated`, `ImmutableCore`, `Contradicted`, `Deprecated`, and
   `Collapsed` claims have locked text identity.
3. `store_fact()` and `update_fact(claim=...)` raise `ClaimIdentityError` when a
   locked claim's text changes; same-text and non-identity updates remain valid.
4. Replacement content must use a new `fact_id` plus `reconcile.supersede()`.
5. The store path serializes identity-check + upsert with `BEGIN IMMEDIATE`, so
   another process cannot promote a draft between the check and write.
6. Receipt/evidence modification tests now simulate out-of-band DB tampering,
   proving replay still detects unauthorized drift.

Claim hashes/version history remain a possible future enhancement for explicit
rectification workflows; they are no longer required to close the silent
promoted-claim rewrite path.

## Non-goals for the follow-up PR

- Full bi-temporal schema (RFC backlog)
- Automatic migration of legacy facts without `claim_hash`

## Acceptance criteria

- [x] No silent claim rewrite on promoted/historical canon ids
- [x] Receipt replay flags out-of-band semantic change when `fact_id` is stable
- [x] 100% coverage gate preserved
