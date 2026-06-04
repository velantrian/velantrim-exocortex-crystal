"""Tests for core/contradiction.py — deterministic contradiction classifier."""
import json

import pytest

from core import contradiction as C
from core.contradiction import CONTRADICTION, REFINEMENT, RELATED


# ─── polarity ─────────────────────────────────────────────────────────────────

def test_polarity_affirmative_vs_negated():
    assert C.polarity("Water boils at 100 degrees") == 0
    assert C.polarity("Water does not boil at 100 degrees") == 1
    assert C.polarity("It isn't raining") == 1
    # double negation cancels (parity)
    assert C.polarity("not never wrong") == 0


# ─── negation signal ──────────────────────────────────────────────────────────

def test_negation_contradiction():
    v = C.classify("The vaccine is effective",
                   "The vaccine is not effective")
    assert v["kind"] == CONTRADICTION
    assert v["signal"] == "negation"


def test_same_polarity_same_subject_is_refinement():
    v = C.classify("Water boils at 100 degrees",
                   "Water boils at 100 degrees at sea level")
    assert v["kind"] == REFINEMENT


# ─── antonym signal ───────────────────────────────────────────────────────────

def test_antonym_contradiction():
    v = C.classify("Interest rates will rise next year",
                   "Interest rates will fall next year")
    assert v["kind"] == CONTRADICTION
    assert v["signal"].startswith("antonym:")


def test_antonym_true_false():
    assert C.is_contradiction("The claim is true", "The claim is false")


# ─── numeric signal ───────────────────────────────────────────────────────────

def test_numeric_contradiction():
    v = C.classify("The tower is 324 meters tall",
                   "The tower is 300 meters tall")
    assert v["kind"] == CONTRADICTION
    assert v["signal"] == "numeric"


def test_same_number_no_numeric_conflict():
    v = C.classify("The tower is 324 meters tall",
                   "The tower stands 324 meters in height")
    assert v["kind"] != CONTRADICTION or v["signal"] != "numeric"


# ─── same-subject gate (precision) ────────────────────────────────────────────

def test_unrelated_claims_are_related_not_contradiction():
    # Opposite polarity but different subjects → must NOT fire (low overlap).
    v = C.classify("The Eiffel Tower is in Paris",
                   "Quantum computers are not widely available")
    assert v["kind"] == RELATED
    assert v["signal"] is None


def test_topical_overlap_without_signal_is_related():
    v = C.classify("The brain has many neurons",
                   "The brain processes information")
    assert v["kind"] in (RELATED, REFINEMENT)
    assert v["signal"] is None


def test_no_content_tokens_is_related():
    # A claim made only of stopwords/numbers has no content set → no verdict.
    v = C.classify("the is at of", "42 100")
    assert v["kind"] == RELATED
    assert v["content_overlap"] == 0.0


def test_classify_is_order_independent():
    a = "The market is open"
    b = "The market is closed"
    assert C.classify(a, b)["kind"] == C.classify(b, a)["kind"] == CONTRADICTION


# ─── integration: find_conflicts now classifies ───────────────────────────────

def _validated_worldfact(fact_id, claim):
    from core.memory import store_fact, transition_esm, get_fact
    from core.l3_graph import get_l3_graph
    store_fact({"fact_id": fact_id, "claim": claim, "source": "s",
                "confidence": 0.9, "claim_type": "WORLD_FACT"})
    transition_esm(fact_id, "Validated")
    get_l3_graph().merge_fact(get_fact(fact_id))


def test_find_conflicts_labels_kind():
    from core.reconcile import find_conflicts
    _validated_worldfact("v1", "The vaccine is effective against the virus")
    hits = find_conflicts("The vaccine is not effective against the virus")
    match = [h for h in hits if h["fact_id"] == "v1"]
    assert match and match[0]["kind"] == CONTRADICTION
    assert match[0]["signal"] == "negation"


# ─── integration: ingest auto-contradict (opt-in) ─────────────────────────────

def test_ingest_no_auto_action_by_default(monkeypatch):
    from core.ingest import ingest
    monkeypatch.delenv("VELANTRIM_AUTO_CONTRADICT", raising=False)
    ingest("Sea levels are rising globally")
    res = ingest("Sea levels are falling globally")
    # conflict surfaced & classified, but no automatic edge written
    assert "auto_contradicted" not in res
    if "conflicts" in res:
        assert any(c["kind"] == CONTRADICTION for c in res["conflicts"])


def test_ingest_auto_contradict_links_edge(monkeypatch):
    from core.ingest import ingest
    from core.reconcile import fact_history
    monkeypatch.setenv("VELANTRIM_AUTO_CONTRADICT", "1")
    r1 = ingest("Global temperatures are increasing")
    r2 = ingest("Global temperatures are decreasing")
    assert r2.get("auto_contradicted"), "expected an auto CONTRADICTS link"
    new_id = r2["fact"]["fact_id"]
    # The new fact records an outgoing CONTRADICTS edge to the prior one.
    assert r1["fact"]["fact_id"] in fact_history(new_id)["contradicts"]


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_conflicts(capsys):
    from core.cli import main
    _validated_worldfact("cli1", "The bridge can hold 40 tons")
    assert main(["conflicts", "The bridge can hold 80 tons"]) == 0
    hits = json.loads(capsys.readouterr().out.strip())
    match = [h for h in hits if h["fact_id"] == "cli1"]
    assert match and match[0]["kind"] == CONTRADICTION
    assert match[0]["signal"] == "numeric"
