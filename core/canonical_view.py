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

import math
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional


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

# ESM states eligible for strict grounding — a POSITIVE allowlist, not a
# blocklist of known-bad states. Only a fact that has actually completed
# TruthGate admission (Validated) or is a permanently entrenched Ring Zero /
# VALUES_CORE fact (ImmutableCore) qualifies. Everything else — Observed,
# Hypothesized, Supported (pre-canonical/pending), Contradicted, Deprecated,
# Collapsed (post-canonical/superseded), a missing epistemic_state, or an
# unknown/malformed value — fails closed. A blocklist-only design would let a
# pre-canonical or malformed epistemic_state slip through if truth_status
# happened to read VERIFIED (e.g. a fact can carry a STALE truth_status from
# before it entered a bad state: core/l3_graph.py's merge_fact() does a
# partial dict update, and core/reconcile.py's _sync_l3() merges via
# get_fact() — an L1 record that never carries truth_status at all — so an
# earlier VERIFIED value already on the L3 node is preserved, not cleared).
# Checking epistemic_state independently of, and as strictly as, truth_status
# is therefore required, not redundant (see this module's tests).
STRICT_CANONICAL_ESM_STATES = frozenset({"Validated", "ImmutableCore"})

# Identity/provenance fields a strict-canonical fact must carry, non-empty.
# Mirrors the same fields core/pipeline.py's Guardian already treats as
# structurally mandatory before a fact may reach the TruthGate at all
# (guardian_diagnose: all_have_fact_id / all_have_claim / all_have_source).
_REQUIRED_STRING_FIELDS = ("fact_id", "source", "claim")


def _has_required_fields(fact: Mapping[str, Any]) -> bool:
    """True only if every required field is a real, non-blank string.

    A truthy NON-string value (e.g. `claim=["bad"]`, `source={"x": 1}`,
    `fact_id=123`) must fail closed here, not be treated as present: these
    fields are declared as required STRING fields, and a caller that skips
    its own sanitation (or a corrupted L3 node) must not be able to smuggle a
    list/dict/number through as if it were valid identity/provenance (#257
    corrective hardening, review round 5)."""
    return all(
        isinstance(fact.get(field), str) and bool(fact[field].strip())
        for field in _REQUIRED_STRING_FIELDS
    )


def _is_valid_confidence(value: Any) -> bool:
    """True only for a real int/float (never bool — bool is a int subclass
    but not a valid confidence type) that is finite and within [0.0, 1.0].

    CanonicalView is an independent trust boundary (#257 corrective
    hardening, section 9/11): it must not assume retrieval or Guardian
    already validated confidence, since core/pipeline.py::generate_answer()
    and other direct callers may hand it a fact dict that never passed
    through either."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value) and 0.0 <= value <= 1.0


def _in(value: Any, known: frozenset) -> bool:
    """`value in known`, but fails closed (False) instead of raising for an
    unhashable malformed value (e.g. a list/dict where a string is expected) —
    malformed trust metadata must be excluded, never crash the read path."""
    try:
        return value in known
    except TypeError:
        return False


def _normalize_restricted_bit(value: Any) -> Optional[bool]:
    """Normalize a `restricted` value read at a known storage-adapter
    boundary to bool — STRICT about both the source of "missing" and the
    exact type of a present value (#257 corrective hardening, follow-up).

    Only two things are known-good:
      - an actual `bool` (True/False);
      - a real `int` that is exactly 0 or 1 (never `float` — `0.0`/`1.0`
        must NOT compare equal here; `isinstance(value, int)` alone would
        also accept them via Python's numeric `==`, so the int check must
        run before any `== 0`/`== 1` comparison).

    A MISSING value (None) is NOT normalized to False — nor is any other
    present-but-not-0/1/bool value (another int, a string, a collection,
    ...). Both are UNKNOWN, never silently coerced to False by a permissive
    bool(value) over an arbitrary/malformed backend value.

    Lives here (not core/pipeline.py) because CanonicalView is an
    independent trust boundary that must not rely on a caller/pipeline
    having already normalized this bit — core/pipeline.py imports this
    function rather than duplicating it, so the two representations of
    "restricted" can never independently drift out of sync (#257
    independent-review round)."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return value == 1
    return None  # UNKNOWN: missing, float, out-of-range int, string, ...


def is_strict_canonical(fact: Mapping[str, Any]) -> bool:
    """
    True if `fact` may ground a strict, confident factual answer.

    At minimum, ALL of the following must hold:
      - truth_status == "VERIFIED" (exact match). Missing, malformed, or
        unknown truth_status values fail closed — this function never
        infers verification from confidence, epistemic_state, source_status,
        or anything else.
      - epistemic_state is in STRICT_CANONICAL_ESM_STATES (a positive
        allowlist: Validated / ImmutableCore only). A missing, pre-canonical
        (Observed/Hypothesized/Supported), post-canonical (Contradicted/
        Deprecated/Collapsed), or unknown/malformed epistemic_state all fail
        closed — this is checked independently of truth_status rather than
        assumed to be implied by it (see STRICT_CANONICAL_ESM_STATES).
      - `restricted` normalizes to exactly False (GDPR Art. 18 processing
        restriction) — a confirmed-True OR UNKNOWN (missing/malformed)
        restricted bit is excluded from grounding, deny-dominant, exactly
        like it is already excluded from retrieval (core/pipeline.py::retrieve)
        and from evidence/review surfaces (core/evidence.py, core/review.py).
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
    if not _in(truth_status, KNOWN_TRUTH_STATUSES):
        return False  # missing, malformed, or unknown — fail closed
    if truth_status != VERIFIED_TRUTH_STATUS:
        return False  # USER_CLAIMED / HYPOTHESIS / SUBJECTIVE / UNVERIFIED / CURATOR_OVERRIDE

    # Anti-hybrid-record check (#257 corrective hardening, section 8/9): a
    # persisted/assembled truth_status=VERIFIED label that the canonical
    # write-time policy could never have produced for this fact's
    # claim_type/source_status combination (e.g. VERIFIED + USER_REPORTED, or
    # VERIFIED + a subjective claim_type like OPINION/EMOTION/PREFERENCE) is
    # inconsistent metadata, not a real verdict — a malformed/corrupted L3
    # record or a direct generate_answer() caller must not launder
    # user-reported or subjective material into a confident factual answer
    # just because the single truth_status field reads VERIFIED in
    # isolation. Reuses the exact pure function the write/admission path uses
    # (core.pipeline._truth_status_for) rather than re-deriving the policy
    # with a second, parallel enum list that could drift out of sync.
    # Deferred import: core.pipeline imports this module at its own top
    # level, so a module-level import here would be circular.
    from core.pipeline import _truth_status_for
    claim_type = fact.get("claim_type", "WORLD_FACT")
    try:
        # _truth_status_for does a raw `source_status in {...}` set
        # membership check — an unhashable source_status (e.g. a caller-
        # supplied list/dict) raises TypeError instead of comparing False.
        # This module is an independent trust boundary and must fail
        # closed on malformed input, not crash the read path (#257
        # independent-review round).
        resolved_status = _truth_status_for(claim_type, fact.get("source_status"))
    except TypeError:
        return False
    if resolved_status != VERIFIED_TRUTH_STATUS:
        return False

    if not _in(fact.get("epistemic_state"), STRICT_CANONICAL_ESM_STATES):
        return False

    if _normalize_restricted_bit(fact.get("restricted")) is not False:
        return False  # True or UNKNOWN (missing/malformed) both fail closed

    if not _has_required_fields(fact):
        return False

    if not _is_valid_confidence(fact.get("confidence")):
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
    return [
        dict(f) for f in facts
        if _normalize_restricted_bit(f.get("restricted")) is False
    ]
