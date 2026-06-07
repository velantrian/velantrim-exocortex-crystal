"""Tests for the Fractal Memory Layer (core/fractal.py, RFC0070)."""
from datetime import datetime, timedelta, timezone

import pytest

from core import fractal
from core.fractal import SHORT, MEDIUM, LONG, CORE
from core.memory import store_fact, transition_esm, get_fact, update_fact
from core.l3_graph import get_l3_graph


def _canon(fact_id, *, confidence=0.6, significance=0.5, observations=1,
           scale=None, age_days=0):
    """A Validated L3 fact with controlled anchoring inputs."""
    store_fact({"fact_id": fact_id, "claim": f"claim {fact_id}", "source": "s",
                "confidence": confidence, "significance": significance})
    transition_esm(fact_id, "Validated")
    meta = {"observations": observations}
    if scale is not None:
        meta["fractal_scale"] = scale
    if age_days:
        meta["last_consolidated"] = (
            datetime.now(timezone.utc) - timedelta(days=age_days)).isoformat()
    update_fact(fact_id, metadata=meta)
    get_l3_graph().merge_fact(get_fact(fact_id))


# ─── Pure scoring / banding ───────────────────────────────────────────────────

def test_anchor_strength_bounds_and_drivers():
    weak = {"significance": 0.0, "confidence": 0.0, "metadata": {"observations": 1}}
    strong = {"significance": 1.0, "confidence": 1.0, "metadata": {"observations": 50}}
    assert fractal.anchor_strength(weak) == 0.0
    assert 0.95 <= fractal.anchor_strength(strong) <= 1.0
    # each driver raises strength monotonically
    base = fractal.anchor_strength({"significance": 0.5, "confidence": 0.5,
                                    "metadata": {"observations": 1}})
    more_sig = fractal.anchor_strength({"significance": 0.9, "confidence": 0.5,
                                        "metadata": {"observations": 1}})
    more_obs = fractal.anchor_strength({"significance": 0.5, "confidence": 0.5,
                                        "metadata": {"observations": 10}})
    assert more_sig > base and more_obs > base


def test_scale_for_strength_bands():
    assert fractal.scale_for_strength(0.90) == CORE
    assert fractal.scale_for_strength(0.60) == LONG
    assert fractal.scale_for_strength(0.40) == MEDIUM
    assert fractal.scale_for_strength(0.10) == SHORT
    assert fractal.scale_for_strength(0.0) == SHORT


def test_capacities_are_fractal_halving():
    assert fractal.capacities(1024) == {SHORT: 1024, MEDIUM: 512, LONG: 256, CORE: 128}
    assert fractal.capacities(8) == {SHORT: 8, MEDIUM: 4, LONG: 2, CORE: 1}


def test_base_capacity_falls_back_on_malformed_env(monkeypatch):
    monkeypatch.setenv("VELANTRIM_FRACTAL_BASE", "not-a-number")
    assert fractal.capacities()[SHORT] == 1024   # default base


def test_protection_and_anchored():
    assert fractal.protection_factor(SHORT) == 1.0
    assert fractal.protection_factor(MEDIUM) == 2.0
    assert fractal.protection_factor(LONG) == 4.0
    assert fractal.protection_factor(CORE) == float("inf")
    assert fractal.protection_factor(None) == 1.0   # unanchored → no change
    assert fractal.is_anchored(CORE) and not fractal.is_anchored(LONG)


# ─── reanchor over the canon ──────────────────────────────────────────────────

def test_reanchor_assigns_scales_and_persists():
    _canon("weak", significance=0.0, confidence=0.0, observations=1)        # SHORT
    _canon("mid",  significance=0.5, confidence=0.6, observations=1)        # MEDIUM
    _canon("deep", significance=1.0, confidence=1.0, observations=20)       # CORE
    res = fractal.reanchor()
    assert res["assigned"][CORE] == 1
    assert get_fact("deep")["metadata"]["fractal_scale"] == CORE
    assert get_fact("weak")["metadata"]["fractal_scale"] == SHORT
    # stronger facts sit in deeper scales
    order = {SHORT: 0, MEDIUM: 1, LONG: 2, CORE: 3}
    s_weak = order[get_fact("weak")["metadata"]["fractal_scale"]]
    s_deep = order[get_fact("deep")["metadata"]["fractal_scale"]]
    assert s_deep > s_weak


def test_reanchor_is_idempotent():
    _canon("a", significance=1.0, confidence=1.0, observations=20)
    first = fractal.reanchor()
    second = fractal.reanchor()
    assert first["reanchored"] >= 1
    assert second["reanchored"] == 0   # already at scale → nothing rewritten


def test_reanchor_capacity_spills_down(monkeypatch):
    # base=8 → CORE capacity 1, LONG capacity 2. Three CORE-band facts → only the
    # strongest stays CORE; the rest spill down to LONG (never deleted).
    monkeypatch.setenv("VELANTRIM_FRACTAL_BASE", "8")
    _canon("c1", significance=1.0, confidence=1.0, observations=20)   # strongest
    _canon("c2", significance=1.0, confidence=0.95, observations=20)
    _canon("c3", significance=1.0, confidence=0.90, observations=20)
    res = fractal.reanchor()
    assert res["capacities"][CORE] == 1
    assert res["assigned"][CORE] == 1
    assert res["assigned"][LONG] == 2
    # nothing lost — all three are still anchored somewhere
    assert res["assigned"][CORE] + res["assigned"][LONG] == 3


# ─── SleepCycle integration (anti-catastrophic-forgetting) ────────────────────

def test_core_anchor_is_exempt_from_decay():
    from core.consolidate import consolidate
    _canon("anchored", confidence=0.8, significance=0.0, scale=CORE, age_days=400)
    consolidate()
    assert get_fact("anchored")["confidence"] == 0.8          # protected, no drift
    # the clock still advances so a later demotion can't cause a one-shot drop
    assert get_fact("anchored")["metadata"]["last_consolidated"]


def test_deeper_scale_decays_slower():
    from core.consolidate import consolidate
    _canon("short", confidence=0.8, significance=0.0, scale=SHORT, age_days=30)
    _canon("long",  confidence=0.8, significance=0.0, scale=LONG,  age_days=30)
    consolidate()
    assert get_fact("long")["confidence"] > get_fact("short")["confidence"]


def test_unanchored_facts_decay_as_before():
    # Regression: a fact with no fractal_scale must decay exactly as the pre-RFC0070
    # SleepCycle did (protection 1.0).
    from core.consolidate import consolidate
    _canon("plain", confidence=0.8, significance=0.0, age_days=30)   # one half-life
    consolidate()
    assert get_fact("plain")["confidence"] < 0.8


# ─── reporting / listing ──────────────────────────────────────────────────────

def test_fractal_report_and_anchors():
    _canon("r1", significance=1.0, confidence=1.0, observations=20)   # CORE
    _canon("r2", significance=0.0, confidence=0.0, observations=1)    # SHORT
    fractal.reanchor()
    rep = fractal.fractal_report()
    assert rep["depth"] == 4
    assert rep["anchored_total"] == 2
    assert rep["by_scale"][CORE] == 1
    core_only = fractal.anchors(CORE)
    assert len(core_only) == 1 and core_only[0]["fact_id"] == "r1"
    # full listing is strongest-first
    everything = fractal.anchors()
    assert [a["fact_id"] for a in everything] == ["r1", "r2"]


def test_report_counts_unanchored_and_skips_non_validated():
    # A Validated fact that has not been reanchored yet → counted as unanchored.
    _canon("pending_anchor", significance=0.5, confidence=0.6)
    # A non-Validated (Observed) fact is ignored by the fractal layer entirely.
    store_fact({"fact_id": "obs", "claim": "c", "source": "s", "confidence": 0.6})
    get_l3_graph().merge_fact(get_fact("obs"))
    rep = fractal.fractal_report()
    assert rep["unanchored"] == 1
    assert rep["anchored_total"] == 0
    assert all(a["fact_id"] != "obs" for a in fractal.anchors())


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_fractal_roundtrip(capsys):
    import json
    from core.cli import main
    _canon("cli_core", significance=1.0, confidence=1.0, observations=20)

    assert main(["fractal-reanchor"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["assigned"][CORE] == 1

    assert main(["fractal-report"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["anchored_total"] == 1

    assert main(["fractal-anchors", "--scale", "CORE"]) == 0
    hits = json.loads(capsys.readouterr().out.strip())
    assert hits and hits[0]["fact_id"] == "cli_core"
