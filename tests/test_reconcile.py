"""Tests for core/reconcile.py — truth maintenance (reinforce / supersede / contradict)."""
import pytest

from core.memory import store_fact, transition_esm, get_fact
from core.l3_graph import get_l3_graph
from core.compliance import restrict_processing
from core.reconcile import (
    reinforce,
    supersede,
    contradict,
    find_conflicts,
    fact_history,
    REL_SUPERSEDED_BY,
    REL_CONTRADICTS,
)


def _validated(fact_id, confidence=0.5, claim="c"):
    store_fact({"fact_id": fact_id, "claim": claim, "source": "s",
                "confidence": confidence})
    transition_esm(fact_id, "Validated")
    get_l3_graph().merge_fact(get_fact(fact_id))


# ─── reinforce ────────────────────────────────────────────────────────────────

def test_reinforce_raises_confidence_with_diminishing_returns():
    _validated("r1", confidence=0.5)
    c1 = reinforce("r1")
    c2 = reinforce("r1")
    assert 0.5 < c1 < c2
    assert (c1 - 0.5) > (c2 - c1)            # each repeat adds less
    assert get_fact("r1")["metadata"]["observations"] == 3


def test_reinforce_disagreement_lowers_confidence():
    _validated("r2", confidence=0.8)
    assert reinforce("r2", agreement=False) < 0.8


def test_reinforce_missing_fact_returns_none():
    assert reinforce("ghost") is None


def test_reinforce_syncs_confidence_into_l3():
    _validated("r3", confidence=0.5)
    new_conf = reinforce("r3")
    assert get_l3_graph().get_fact("r3")["confidence"] == new_conf


def test_reinforce_on_observed_does_not_merge_into_l3():
    """Observed facts must not enter L3 via reinforce() metadata sync."""
    store_fact({"fact_id": "obs_r", "claim": "pre-canonical", "source": "s",
                "confidence": 0.5})
    assert get_fact("obs_r")["epistemic_state"] == "Observed"
    new_conf = reinforce("obs_r")
    assert new_conf is not None
    assert get_l3_graph().get_fact("obs_r") is None


def test_reinforce_agreement_follows_exact_formula():
    """Pin the exact update rule (not just its direction):
    new_conf = round(conf + (1.0 - conf) / (obs + 1), 4). Consecutive calls
    walk observations 1 → 2 → 3, so an off-by-one in the denominator
    (obs + 1 → obs + 2) produces 0.6667 instead of 0.75 on the first call."""
    _validated("rf_agree", confidence=0.5)
    assert reinforce("rf_agree") == 0.75            # obs=1: 0.5 + 0.5/2
    assert reinforce("rf_agree") == 0.8333          # obs=2: 0.75 + 0.25/3
    assert reinforce("rf_agree") == 0.875           # obs=3: 0.8333 + 0.1667/4
    fact = get_fact("rf_agree")
    assert fact["confidence"] == 0.875
    assert fact["metadata"]["observations"] == 4


def test_reinforce_disagreement_follows_exact_formula():
    """Pin the exact decay rule: new_conf = round(conf * obs / (obs + 1), 4)."""
    _validated("rf_disagree", confidence=0.8)
    assert reinforce("rf_disagree", agreement=False) == 0.4      # obs=1: 0.8*1/2
    assert reinforce("rf_disagree", agreement=False) == 0.2667   # obs=2: 0.4*2/3
    assert reinforce("rf_disagree", agreement=False) == 0.2      # obs=3: 0.2667*3/4
    fact = get_fact("rf_disagree")
    assert fact["confidence"] == 0.2
    assert fact["metadata"]["observations"] == 4


# ─── supersede ──────────────────────────────────────────────────────────────

def test_supersede_deprecates_old_and_links_new():
    _validated("old", claim="earth is flat")
    new_id = supersede("old", {"fact_id": "new", "claim": "earth is round",
                               "source": "s", "confidence": 0.9})
    assert new_id == "new"
    assert get_fact("old")["epistemic_state"] == "Deprecated"
    assert get_fact("new")["epistemic_state"] == "Validated"
    neighbors = get_l3_graph().neighbors("old", rel_type=REL_SUPERSEDED_BY)
    assert "new" in {n["fact_id"] for n in neighbors}


def test_supersede_requires_new_fact_id():
    with pytest.raises(ValueError, match="fact_id"):
        supersede("old", {"claim": "no id"})


def test_supersede_rejects_zero_confidence_new_fact():
    # #70: a supersession may not inject an unvalidated world fact into L3.
    _validated("old", claim="earth is flat")
    with pytest.raises(ValueError, match="TruthGate"):
        supersede("old", {"fact_id": "ungated", "claim": "earth is round",
                          "source": "s", "confidence": 0.0})  # Guardian blocks zero confidence
    assert get_fact("ungated")["epistemic_state"] == "Observed"  # never reached L3
    assert get_fact("old")["epistemic_state"] == "Validated"     # old untouched


def test_supersede_rejects_llm_output_as_world_fact():
    # #70: LLM_OUTPUT cannot become a WORLD_FACT through supersession either.
    _validated("old2", claim="the sky is green")
    with pytest.raises(ValueError, match="TruthGate"):
        supersede("old2", {"fact_id": "llm", "claim": "the sky is blue",
                           "source": "model", "confidence": 0.9,
                           "claim_type": "WORLD_FACT", "source_status": "LLM_OUTPUT"})
    assert get_fact("llm")["epistemic_state"] == "Observed"


def test_supersede_enforce_gate_false_skips_gate():
    # Reserved escape hatch for already-gated callers stays available.
    _validated("old3", claim="earth is flat")
    new_id = supersede("old3", {"fact_id": "trusted", "claim": "earth is round"},
                       enforce_gate=False)
    assert new_id == "trusted"
    assert get_fact("trusted")["epistemic_state"] == "Validated"


# ─── contradict ─────────────────────────────────────────────────────────────

def test_contradict_marks_validated_fact_and_adds_edge():
    _validated("c1")
    changed = contradict("c1", "source_fact")
    assert changed is True
    assert get_fact("c1")["epistemic_state"] == "Contradicted"
    g = get_l3_graph()
    assert any(e[0] == "c1" and e[1] == REL_CONTRADICTS and e[2] == "source_fact"
               for e in g._edges)


def test_contradict_non_validated_adds_edge_without_state_change():
    store_fact({"fact_id": "obs", "claim": "c", "source": "s"})  # stays Observed
    get_l3_graph().merge_fact(get_fact("obs"))
    changed = contradict("obs", "src")
    assert changed is False
    assert get_fact("obs")["epistemic_state"] == "Observed"
    assert any(e[0] == "obs" and e[1] == REL_CONTRADICTS for e in get_l3_graph()._edges)


# ─── fact_history (truth provenance) ──────────────────────────────────────────

def test_fact_history_tracks_supersede_both_directions():
    _validated("old", claim="earth is flat")
    supersede("old", {"fact_id": "new", "claim": "earth is round",
                      "source": "s", "confidence": 0.9})
    assert fact_history("old")["superseded_by"] == ["new"]
    assert fact_history("new")["supersedes"] == ["old"]


def test_fact_history_tracks_contradiction_both_directions():
    _validated("claim_x")
    contradict("claim_x", "evidence_y")
    assert fact_history("claim_x")["contradicts"] == ["evidence_y"]
    # the contradicting source sees it from the other side
    assert "claim_x" in fact_history("evidence_y")["contradicted_by"]


def test_fact_history_empty_for_isolated_fact():
    _validated("solo")
    assert fact_history("solo") == {
        "superseded_by": [], "supersedes": [], "contradicts": [], "contradicted_by": []}


# ─── find_conflicts ───────────────────────────────────────────────────────────

def _validated_worldfact(fact_id, claim):
    store_fact({"fact_id": fact_id, "claim": claim, "source": "s",
                "confidence": 0.9, "claim_type": "WORLD_FACT"})
    transition_esm(fact_id, "Validated")
    get_l3_graph().merge_fact(get_fact(fact_id))


def test_find_conflicts_surfaces_near_but_different_canonical_fact():
    _validated_worldfact("cap1", "The capital of Australia is Sydney")
    hits = find_conflicts("The capital of Australia is Canberra")
    assert "cap1" in {h["fact_id"] for h in hits}


def test_find_conflicts_excludes_self_exact_repeat_and_unrelated():
    _validated_worldfact("cap1", "The capital of Australia is Sydney")
    _validated_worldfact("bee1", "Bees communicate through waggle dance")
    # exact repeat of cap1 → reinforcement, not a conflict; self excluded by id;
    # unrelated bee fact below threshold.
    hits = find_conflicts("The capital of Australia is Sydney", fact_id="cap1")
    assert hits == []


def test_find_conflicts_ignores_subjective_claims():
    store_fact({"fact_id": "emo1", "claim": "I feel the capital is wrong",
                "source": "user", "confidence": 0.9, "claim_type": "EMOTION"})
    transition_esm("emo1", "Validated")
    get_l3_graph().merge_fact(get_fact("emo1"))
    # an EMOTION node is never a world-fact conflict candidate
    assert find_conflicts("the capital is wrong") == []


def test_find_conflicts_excludes_restricted_facts():
    """GDPR Art. 18: a fact under processing restriction must never surface as
    a conflict candidate, even when semantically close to the query claim.
    find_conflicts() is exposed read-only via the MCP `find_conflicts` tool, so
    this also closes that leak path (see core/reconcile.py:249)."""
    _validated_worldfact("cap_restricted", "The capital of Australia is Sydney")
    restrict_processing("cap_restricted", reason="dispute")
    hits = find_conflicts("The capital of Australia is Canberra")
    assert "cap_restricted" not in {h["fact_id"] for h in hits}


def test_find_conflicts_still_returns_unrestricted_candidate():
    """Restriction filtering must not over-filter: an unrestricted validated
    WORLD_FACT in the same candidate set is still surfaced as a conflict."""
    _validated_worldfact("cap_restricted2", "The capital of Australia is Sydney")
    restrict_processing("cap_restricted2", reason="dispute")
    _validated_worldfact("cap_open", "The capital of Australia is Perth")
    hits = find_conflicts("The capital of Australia is Canberra")
    ids = {h["fact_id"] for h in hits}
    assert "cap_restricted2" not in ids
    assert "cap_open" in ids


def test_find_conflicts_excludes_restricted_even_when_node_lacks_the_flag():
    """Regression for a Codex P1 finding: LadybugL3Graph._COLS is a fixed
    typed-column list that omits `restricted`, so its vector_search()/get_fact()
    nodes never carry the flag even when the underlying fact IS restricted.
    find_conflicts() must not trust node.get("restricted") alone — it has to
    fall back to core.memory.get_fact() (always has the flag, L1-backed,
    backend-independent). Simulate the gap directly on the in-memory mock by
    stripping `restricted` from the L3 node after merge, exactly as a
    fixed-column backend would."""
    _validated_worldfact("cap_restricted3", "The capital of Freldania is Sunmere")
    restrict_processing("cap_restricted3", reason="dispute")
    get_l3_graph()._nodes["cap_restricted3"].pop("restricted", None)
    hits = find_conflicts("The capital of Freldania is Rivenholt")
    assert "cap_restricted3" not in {h["fact_id"] for h in hits}


def test_find_conflicts_overfetches_so_restricted_top_k_does_not_hide_others():
    """A restricted candidate can occupy a raw top-k vector_search slot; without
    overfetching beyond k, filtering it out would silently return fewer than k
    real conflicts (or none) even though an unrestricted one qualifies. Rank the
    restricted fact strictly first via significance, then ask for only k=1."""
    store_fact({"fact_id": "cap_restricted4", "claim": "The capital of Meridia is Ashfall",
                "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
                "significance": 0.9})
    transition_esm("cap_restricted4", "Validated")
    get_l3_graph().merge_fact(get_fact("cap_restricted4"))
    restrict_processing("cap_restricted4", reason="dispute")

    store_fact({"fact_id": "cap_open2", "claim": "The capital of Meridia is Brightholm",
                "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
                "significance": 0.5})
    transition_esm("cap_open2", "Validated")
    get_l3_graph().merge_fact(get_fact("cap_open2"))

    hits = find_conflicts("The capital of Meridia is Stonegate", k=1)
    ids = {h["fact_id"] for h in hits}
    assert "cap_restricted4" not in ids
    assert "cap_open2" in ids
    assert len(hits) == 1
