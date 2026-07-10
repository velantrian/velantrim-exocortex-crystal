"""Tests for core/canonical_view.py — strict/contextual CanonicalView projection.

Covers the acceptance criteria in docs/CANONICAL_VIEW_RFC.md section 9 and
this PR's mandatory test list. Pure module-level tests only; pipeline-level
integration (refusal on non-canonical-only retrieval, existing
verified-answer/trace/receipt regression) lives in tests/test_pipeline.py.
"""
import pytest

from core.canonical_view import (
    CanonicalReadMode,
    is_strict_canonical,
    project_canonical,
    KNOWN_TRUTH_STATUSES,
    VERIFIED_TRUTH_STATUS,
    STRICT_CANONICAL_ESM_STATES,
)


def _verified_fact(**overrides):
    fact = {
        "fact_id": "f1",
        "claim": "Water boils at 100 degrees Celsius",
        "source": "physics-textbook",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "epistemic_state": "Validated",
        "confidence": 0.9,
        "restricted": False,
    }
    fact.update(overrides)
    return fact


def _user_claimed_fact(**overrides):
    fact = {
        "fact_id": "f2",
        "claim": "My cat is the smartest animal alive",
        "source": "user",
        "claim_type": "WORLD_FACT",
        "source_status": "USER_REPORTED",
        "truth_status": "USER_CLAIMED",
        "epistemic_state": "Validated",
        "confidence": 1.0,
        "restricted": False,
    }
    fact.update(overrides)
    return fact


# ─── Test 1: user claim cannot ground strict answer, confidence notwithstanding ──

def test_user_claimed_world_fact_excluded_from_strict_even_at_full_confidence():
    fact = _user_claimed_fact(
        claim_type="WORLD_FACT",
        source_status="USER_REPORTED",
        truth_status="USER_CLAIMED",
        epistemic_state="Validated",
        confidence=1.0,
    )
    assert is_strict_canonical(fact) is False
    assert project_canonical([fact]) == []


# ─── Test 2: verified fact remains groundable ───────────────────────────────────

def test_verified_fact_with_valid_metadata_is_strict_canonical():
    fact = _verified_fact()
    assert is_strict_canonical(fact) is True
    assert project_canonical([fact]) == [fact]


# ─── Test 3: mixed candidate set ────────────────────────────────────────────────

def test_strict_projection_of_mixed_set_returns_only_the_verified_fact():
    verified = _verified_fact(fact_id="v1")
    user_claimed = _user_claimed_fact(fact_id="u1")
    contradicted = _verified_fact(fact_id="c1", epistemic_state="Contradicted")
    restricted = _verified_fact(fact_id="r1", restricted=True)

    result = project_canonical([verified, user_claimed, contradicted, restricted])

    assert [f["fact_id"] for f in result] == ["v1"]


# ─── Test 4: missing/unknown/malformed trust metadata fails closed ─────────────

@pytest.mark.parametrize("truth_status", [
    None,            # missing entirely
    "",              # empty string
    "verified",      # wrong case — not an exact match
    "PROBABLY_TRUE",  # unknown/invented value
    123,             # malformed type
])
def test_missing_unknown_or_malformed_truth_status_fails_closed(truth_status):
    fact = _verified_fact(truth_status=truth_status)
    assert is_strict_canonical(fact) is False


def test_truth_status_absent_key_fails_closed():
    fact = _verified_fact()
    del fact["truth_status"]
    assert is_strict_canonical(fact) is False


@pytest.mark.parametrize("truth_status", [["VERIFIED"], {"status": "VERIFIED"}])
def test_unhashable_malformed_truth_status_fails_closed_without_crashing(truth_status):
    """A malformed non-hashable truth_status (e.g. a list/dict where a string
    is expected) must be excluded like any other malformed value — not raise
    TypeError out of a read-path predicate."""
    fact = _verified_fact(truth_status=truth_status)
    assert is_strict_canonical(fact) is False


def test_known_truth_statuses_contains_exactly_the_pipeline_vocabulary():
    """Regression guard: this set must track core.pipeline._truth_status_for()'s
    output range plus core.review.py's CURATOR_OVERRIDE — not silently drift."""
    assert KNOWN_TRUTH_STATUSES == {
        "VERIFIED", "USER_CLAIMED", "UNVERIFIED", "HYPOTHESIS", "SUBJECTIVE",
        "CURATOR_OVERRIDE",
    }
    assert VERIFIED_TRUTH_STATUS == "VERIFIED"


# ─── Test 5: contextual mode preserves labels ───────────────────────────────────

def test_contextual_mode_returns_user_claimed_with_real_status_retained():
    fact = _user_claimed_fact()
    result = project_canonical([fact], mode=CanonicalReadMode.CONTEXTUAL)
    assert len(result) == 1
    assert result[0]["truth_status"] == "USER_CLAIMED"
    assert result[0]["truth_status"] != "VERIFIED"


def test_contextual_mode_still_excludes_restricted_facts():
    """GDPR Art. 18 processing restriction is a compliance boundary, not an
    epistemic strictness setting — every other read surface in this codebase
    already treats it as absolute; CONTEXTUAL must not become a bypass."""
    fact = _user_claimed_fact(restricted=True)
    assert project_canonical([fact], mode=CanonicalReadMode.CONTEXTUAL) == []


def test_contextual_mode_does_not_relabel_or_mutate_the_input_fact():
    fact = _user_claimed_fact()
    original = dict(fact)
    result = project_canonical([fact], mode=CanonicalReadMode.CONTEXTUAL)
    assert fact == original            # input never mutated
    assert result[0] is not fact       # output is a copy, not the same object


def test_contextual_mode_is_not_the_default():
    fact = _user_claimed_fact()
    # Calling project_canonical() with no explicit mode must behave as STRICT.
    assert project_canonical([fact]) == []
    assert project_canonical([fact], mode=CanonicalReadMode.STRICT) == []


# ─── Test 7: no confidence promotion ────────────────────────────────────────────

@pytest.mark.parametrize("confidence", [0.0, 0.5, 0.99, 1.0])
def test_confidence_never_promotes_user_claimed_to_strict_canon(confidence):
    fact = _user_claimed_fact(confidence=confidence)
    assert is_strict_canonical(fact) is False


# ─── Test 8: no ESM-only promotion ──────────────────────────────────────────────

@pytest.mark.parametrize("epistemic_state", ["Validated", "Supported"])
def test_esm_state_alone_does_not_make_a_non_verified_fact_strict_canonical(
    epistemic_state,
):
    fact = _user_claimed_fact(epistemic_state=epistemic_state)
    assert is_strict_canonical(fact) is False


# ─── Positive ESM allowlist (STRICT_CANONICAL_ESM_STATES) ─────────────────────
# A blocklist-only design (exclude Contradicted/Deprecated/Collapsed, allow
# everything else) would let a VERIFIED-but-pre-canonical fact (Observed/
# Hypothesized/Supported), or one with a missing/unknown/malformed
# epistemic_state, slip through. STRICT_CANONICAL_ESM_STATES is a positive
# allowlist instead: only Validated / ImmutableCore qualify.

def test_strict_canonical_esm_states_is_exactly_validated_and_immutable_core():
    assert STRICT_CANONICAL_ESM_STATES == {"Validated", "ImmutableCore"}


@pytest.mark.parametrize("epistemic_state", ["Contradicted", "Deprecated", "Collapsed"])
def test_verified_truth_status_does_not_survive_a_non_canonical_esm_state(
    epistemic_state,
):
    """Regression for the exact scenario core/l3_graph.py's merge_fact() can
    produce: a fact contradicted/deprecated/collapsed AFTER being verified can
    still carry a STALE truth_status=VERIFIED (merge_fact does a partial dict
    update and core/reconcile.py's _sync_l3() merges via get_fact(), which
    never carries truth_status at all, so the earlier VERIFIED value survives
    untouched). epistemic_state must be checked independently of truth_status,
    not assumed to be implied by it."""
    fact = _verified_fact(epistemic_state=epistemic_state)
    assert is_strict_canonical(fact) is False


@pytest.mark.parametrize("epistemic_state", ["Observed", "Hypothesized", "Supported"])
def test_verified_truth_status_does_not_survive_a_pre_canonical_esm_state(
    epistemic_state,
):
    """A blocklist-only check would have missed this: these states are not in
    the old 'bad state' set, but they are pre-canonical/pending, not strict
    canon — a VERIFIED truth_status must not bypass the allowlist."""
    fact = _verified_fact(epistemic_state=epistemic_state)
    assert is_strict_canonical(fact) is False


def test_verified_truth_status_with_missing_esm_state_fails_closed():
    fact = _verified_fact()
    del fact["epistemic_state"]
    assert is_strict_canonical(fact) is False


def test_verified_truth_status_with_unknown_esm_state_string_fails_closed():
    fact = _verified_fact(epistemic_state="QuantumSuperposition")
    assert is_strict_canonical(fact) is False


@pytest.mark.parametrize("epistemic_state", [123, ["Validated"], {"state": "Validated"}, None])
def test_verified_truth_status_with_malformed_non_string_esm_state_fails_closed(
    epistemic_state,
):
    fact = _verified_fact(epistemic_state=epistemic_state)
    assert is_strict_canonical(fact) is False


def test_validated_esm_state_is_allowed():
    fact = _verified_fact(epistemic_state="Validated")
    assert is_strict_canonical(fact) is True


def test_immutable_core_esm_state_is_allowed():
    """Ring Zero / VALUES_CORE contract: a permanently entrenched fact is at
    least as canonical as Validated, not less — explicitly part of the
    allowlist, not merely "not excluded"."""
    fact = _verified_fact(epistemic_state="ImmutableCore")
    assert is_strict_canonical(fact) is True


# ─── Required identity/provenance fields ────────────────────────────────────────

@pytest.mark.parametrize("field", ["fact_id", "source", "claim"])
def test_strict_canonical_requires_non_empty_identity_and_provenance_fields(field):
    fact = _verified_fact()
    fact[field] = ""
    assert is_strict_canonical(fact) is False

    fact2 = _verified_fact()
    del fact2[field]
    assert is_strict_canonical(fact2) is False


# ─── Purity / no side effects ───────────────────────────────────────────────────

def test_is_strict_canonical_never_mutates_its_argument():
    fact = _verified_fact()
    original = dict(fact)
    is_strict_canonical(fact)
    assert fact == original


def test_project_canonical_preserves_input_order():
    facts = [_verified_fact(fact_id=f"v{i}") for i in range(5)]
    result = project_canonical(facts)
    assert [f["fact_id"] for f in result] == [f["fact_id"] for f in facts]


def test_project_canonical_rejects_unknown_mode():
    with pytest.raises(ValueError):
        project_canonical([_verified_fact()], mode="bogus")
