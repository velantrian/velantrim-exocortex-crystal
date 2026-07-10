# core/canonical_view.py
# Velantrim ExoCortex — CanonicalView: strict/contextual read projection
#
# Implements the smallest production-safe runtime slice of
# docs/CANONICAL_VIEW_RFC.md: a named, centralized read-time projection
# between retrieval and answer generation, closing the trust-boundary gap
# where physical L3 membership (or ESM state "Validated"/"Supported") was
# being treated as if it implied verified truth.
#
# Invariants (see docs/CANONICAL_VIEW_RFC.md and tests/test_canonical_view.py):
#   PHYSICAL_L3_MEMBERSHIP_IS_NOT_STRICT_CANON
#   USER_CLAIMED_IS_NOT_VERIFIED
#   STRICT_ANSWER_GROUNDING_REQUIRES_VERIFIED_CANON
#
# This module is READ-ONLY and PURE: it never writes to L1/L3, never calls
# TruthGate, never transitions ESM state, and never rewrites truth_status. It
# only decides which of a caller's already-fetched fact dicts may be treated
# as strict grounding for a confident factual answer. It does not resolve
# conflicts, does not infer verification from confidence, and does not
# invent a parallel epistemic state machine — it reads the same
# truth_status / epistemic_state / restricted vocabulary the rest of the
# codebase already uses (core/pipeline.py, core/memory.py, core/evidence.py).
#
# Non-goals (mirrors docs/CANONICAL_VIEW_RFC.md section 7): no new TruthGate,
# no write path, no contradiction resolver, no LLM-based verifier. A future
# `review`/`full_graph` mode from the RFC is not implemented here — only the
# two modes this PR's task requires.

from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping


class CanonicalReadMode(str, Enum):
    """Read projection mode for project_canonical(). STRICT is the default
    for factual answer grounding; CONTEXTUAL must never become the default."""
    STRICT = "strict"
    CONTEXTUAL = "contextual"


# The only truth_status values this codebase's TruthGate/pipeline/review path
# ever assigns (core/pipeline.py::_truth_status_for, core/review.py's
# CURATOR_OVERRIDE admission path). A value outside this set is malformed or
# unknown, not a new epistemic category this module should guess about — it
# fails closed in strict mode instead (see is_strict_canonical).
KNOWN_TRUTH_STATUSES = frozenset({
    "VERIFIED", "USER_CLAIMED", "UNVERIFIED", "HYPOTHESIS", "SUBJECTIVE",
    "CURATOR_OVERRIDE",
})

# Strict grounding requires exactly this truth_status. A curator override
# (core/review.py::approve(force=True)) is a distinct, accountable HUMAN
# admission path — this module intentionally does NOT equate it with an
# automated VERIFIED verdict; see this PR's documented limitations.
VERIFIED_TRUTH_STATUS = "VERIFIED"

# ESM states that make a fact non-canonical regardless of truth_status. A
# fact can carry a STALE truth_status from before it entered one of these
# states: core/l3_graph.py's merge_fact() does a partial dict update (only
# overwrites keys present in the merged payload), and core/reconcile.py's
# _sync_l3() merges a Contradicted/Deprecated fact via get_fact() — an L1
# record that never carries truth_status at all — so an earlier VERIFIED
# value already on the L3 node is preserved, not cleared. Checking
# epistemic_state independently of truth_status is therefore required, not
# redundant (see this module's tests for a regression case).
NON_CANONICAL_ESM_STATES = frozenset({"Contradicted", "Deprecated", "Collapsed"})

# Identity/provenance fields a strict-canonical fact must carry, non-empty.
# Mirrors the same fields core/pipeline.py's Guardian already treats as
# structurally mandatory before a fact may reach the TruthGate at all
# (guardian_diagnose: all_have_fact_id / all_have_claim / all_have_source).
_REQUIRED_STRING_FIELDS = ("fact_id", "source", "claim")


def _has_required_fields(fact: Mapping[str, Any]) -> bool:
    return all(bool((fact.get(field) or "").strip() if isinstance(fact.get(field), str)
                     else fact.get(field))
               for field in _REQUIRED_STRING_FIELDS)


def is_strict_canonical(fact: Mapping[str, Any]) -> bool:
    """
    True if `fact` may ground a strict, confident factual answer.

    At minimum, ALL of the following must hold:
      - truth_status == "VERIFIED" (exact match). Missing, malformed, or
        unknown truth_status values fail closed — this function never
        infers verification from confidence, epistemic_state, source_status,
        or anything else.
      - epistemic_state is not Contradicted / Deprecated / Collapsed (see
        NON_CANONICAL_ESM_STATES for why this is checked independently of
        truth_status rather than assumed to be implied by it).
      - the fact is not `restricted` (GDPR Art. 18 processing restriction) —
        a restricted fact is excluded from grounding exactly like it is
        already excluded from retrieval (core/pipeline.py::retrieve) and
        from evidence/review surfaces (core/evidence.py, core/review.py).
      - required identity/provenance fields (fact_id, source, claim) are
        present and non-empty.

    Tombstoned/erased facts are not checked here: erasure physically removes
    the record (core/erasure.py::erase_fact), so an erased fact_id cannot be
    represented as a `fact` mapping in the first place — there is nothing
    left for a read-time predicate to inspect. Curator-review "quarantined"
    material is covered structurally as well: only a fact the TruthGate/
    pipeline path has actually stamped truth_status == VERIFIED can pass the
    first condition, and pending/quarantined material never receives that
    value (core/review.py's own pending items stay Observed and untouched by
    _truth_status_for() until a curator explicitly approves them).

    Pure function: never writes, never calls TruthGate, never mutates `fact`.
    """
    truth_status = fact.get("truth_status")
    if truth_status not in KNOWN_TRUTH_STATUSES:
        return False  # missing, malformed, or unknown — fail closed
    if truth_status != VERIFIED_TRUTH_STATUS:
        return False  # USER_CLAIMED / HYPOTHESIS / SUBJECTIVE / UNVERIFIED / CURATOR_OVERRIDE

    if fact.get("epistemic_state") in NON_CANONICAL_ESM_STATES:
        return False

    if fact.get("restricted"):
        return False

    if not _has_required_fields(fact):
        return False

    return True


def project_canonical(
    facts: Iterable[Mapping[str, Any]],
    *,
    mode: CanonicalReadMode = CanonicalReadMode.STRICT,
) -> List[Dict[str, Any]]:
    """
    Project a candidate fact list through CanonicalView.

    mode=STRICT (the default for factual answer grounding): returns only
    facts for which is_strict_canonical() is True. Order is preserved
    relative to the input.

    mode=CONTEXTUAL: may also return `USER_CLAIMED`/non-verified material,
    labelled with its REAL truth_status — never relabeled, never promoted by
    confidence alone. Still excludes `restricted` facts unconditionally: GDPR
    Art. 18 processing restriction is a compliance boundary, not an epistemic
    strictness setting, and every other read surface in this codebase already
    treats it as absolute (core/pipeline.py::retrieve,
    core/evidence.py::public_evidence_for, core/review.py's redaction). This
    mode does not write to Canon and callers must not treat its output as
    verified truth — it exists for labelled contextual/user-memory display,
    not for confident factual answer grounding, and must never be selected as
    the default read mode for that purpose.

    Returns shallow copies of the input facts — never mutates the caller's
    dicts, never rewrites truth_status.
    """
    mode = CanonicalReadMode(mode)  # accepts the enum or its raw string value
    if mode is CanonicalReadMode.STRICT:
        return [dict(f) for f in facts if is_strict_canonical(f)]
    return [dict(f) for f in facts if not f.get("restricted")]
