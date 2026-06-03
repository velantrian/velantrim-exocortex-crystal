"""Regression tests for the two bugs found in the code audit.

1. Recall must NOT erode a fact's canonical confidence (confidence vs _score
   conflation in build_facts_pack → merge_fact).
2. SleepCycle (consolidate) must decay facts produced by the ingest/run path,
   not only facts hand-merged with a created_at timestamp.

Both bugs passed the old suite because the conflated value was never asserted
and the consolidate test merged a full SQLite record by hand — a setup that
diverged from the real pipeline. These tests exercise the production path.
"""
from datetime import datetime, timedelta, timezone

from core.ingest import ingest
from core.pipeline import run, build_facts_pack
from core.consolidate import consolidate
from core.l3_graph import get_l3_graph


# ─── Bug 1: recall does not erode canonical confidence ────────────────────────

def test_build_facts_pack_keeps_confidence_distinct_from_score():
    """confidence is epistemic certainty, not the relevance rank (_score)."""
    pack = build_facts_pack(
        [{"id": "rc", "text": "Earth orbits the Sun", "source": "astro",
          "confidence": 0.9, "_score": 0.3, "epistemic_state": "Validated"}],
        "sun",
    )
    fact = pack["facts"][0]
    assert fact["confidence"] == 0.9      # certainty preserved …
    assert fact["_score"] == 0.3          # … rank kept separate


def test_repeated_recall_does_not_erode_canonical_confidence():
    """Recalling a fact across many queries must not shrink its L3 confidence.

    Old behaviour: each recall wrote sim×confidence back into the canon, so the
    node's confidence monotonically decayed every time it was answered."""
    res = ingest("Photosynthesis converts light into chemical energy",
                 confidence=0.8)
    fid = res["fact"]["fact_id"]
    graph = get_l3_graph()
    before = graph.get_fact(fid)["confidence"]

    for _ in range(3):
        run("photosynthesis light chemical energy")

    after = graph.get_fact(fid)["confidence"]
    assert after >= before  # recall never erodes certainty


# ─── Bug 2: SleepCycle decays facts from the ingest/run path ──────────────────

def test_consolidate_decays_facts_from_ingest_path():
    """A fact merged through ingest carries created_at into L3, so the decay
    cycle finds a baseline timestamp and actually runs (it never did before)."""
    res = ingest("Mount Everest is the tallest mountain on Earth",
                 confidence=0.8)
    fid = res["fact"]["fact_id"]
    graph = get_l3_graph()
    before = graph.get_fact(fid)["confidence"]

    future = datetime.now(timezone.utc) + timedelta(days=120)
    out = consolidate(now=future)

    after = graph.get_fact(fid)["confidence"]
    assert after < before          # the node decayed …
    assert out["decayed"] >= 1     # … and the cycle reported it
