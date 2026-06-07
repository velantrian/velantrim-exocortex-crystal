"""Tests for Memory Volition (core/volition.py, RFC0065)."""
import json
from datetime import datetime, timezone

import pytest

from core import volition
from core.memory import store_fact, transition_esm, get_fact, update_fact
from core.l3_graph import get_l3_graph


def _canon(fid, *, confidence=0.6, significance=0.5, observations=1, last=None):
    store_fact({"fact_id": fid, "claim": f"claim {fid}", "source": "s",
                "confidence": confidence, "significance": significance})
    transition_esm(fid, "Validated")
    meta = {"observations": observations}
    if last:
        meta["last_consolidated"] = last
    update_fact(fid, metadata=meta)
    get_l3_graph().merge_fact(get_fact(fid))


def _coactivate(fid, n):
    g = get_l3_graph()
    for i in range(n):
        g.add_edge(fid, "CO_OCCURRED", f"{fid}_n{i}", {"when": f"t{i}"})


# ─── Salience ─────────────────────────────────────────────────────────────────

def test_salience_bounds():
    _canon("low", confidence=0.0, significance=0.0, observations=1)
    _canon("high", confidence=1.0, significance=1.0, observations=50)
    _coactivate("high", 5)
    assert volition.volition_salience(get_fact("low")) == 0.0
    assert volition.volition_salience(get_fact("high")) >= 0.95


def test_salience_drivers_monotonic():
    _canon("base", confidence=0.5, significance=0.5, observations=1)
    _canon("sig", confidence=0.5, significance=1.0, observations=1)
    _canon("obs", confidence=0.5, significance=0.5, observations=20)
    base = volition.volition_salience(get_fact("base"))
    assert volition.volition_salience(get_fact("sig")) > base
    assert volition.volition_salience(get_fact("obs")) > base


def test_coactivation_norm_env_fallback(monkeypatch):
    monkeypatch.setenv("VELANTRIM_VOLITION_COACT_NORM", "not-a-float")
    _canon("c", confidence=0.5, significance=0.5)
    _coactivate("c", 10)
    # falls back to default norm (5) → co-activation term saturates at 0.15
    assert volition.volition_salience(get_fact("c")) == round(
        0.40 * 0.5 + 0.25 * 0.5 + 0.0 + 0.15, 4)


# ─── Voluntary write (through the gates) ──────────────────────────────────────

def test_write_voluntary_passes_gate_and_is_tagged():
    res = volition.write_voluntary("The Pacific is the largest ocean")
    assert res["accepted"] is True and res["volition"] is True
    fid = res["fact"]["fact_id"]
    assert get_fact(fid)["metadata"]["volition"] is True
    assert res["fact"]["claim_type"] == "WORLD_FACT"


def test_write_voluntary_can_be_blocked_like_any_write():
    res = volition.write_voluntary("dubious self-claim", confidence=0.0)
    assert res["accepted"] is False and res["volition"] is True
    assert "reason" in res
    assert get_l3_graph().get_fact(res["fact"]["fact_id"]) is None


# ─── Focus & rehearsal (VolitionWorker) ───────────────────────────────────────

def test_focus_ranks_and_limits():
    _canon("weak", confidence=0.0, significance=0.0)
    _canon("strong", confidence=1.0, significance=1.0, observations=20)
    focus = volition.volition_focus(k=1)
    assert len(focus) == 1 and focus[0]["fact_id"] == "strong"


def test_focus_ignores_non_validated_facts():
    _canon("good", confidence=0.6, significance=0.6)
    # an Observed (non-canonical) fact must not enter the attention set
    store_fact({"fact_id": "obs", "claim": "c", "source": "s", "confidence": 0.9})
    get_l3_graph().merge_fact(get_fact("obs"))
    ids = [f["fact_id"] for f in volition.volition_focus()]
    assert ids == ["good"]


def test_volition_cycle_rehearses_without_faking_evidence():
    old = "2000-01-01T00:00:00+00:00"
    _canon("s1", confidence=0.8, significance=1.0, observations=10, last=old)
    _canon("s2", confidence=0.7, significance=0.9, observations=5, last=old)
    now = datetime.now(timezone.utc)
    res = volition.volition_cycle(k=5, now=now)
    assert set(res["focused"]) == {"s1", "s2"}
    for fid, conf in (("s1", 0.8), ("s2", 0.7)):
        f = get_fact(fid)
        assert f["metadata"]["last_consolidated"] == now.isoformat()  # clock refreshed
        assert f["metadata"]["volition_rehearsed_at"] == now.isoformat()
        assert f["confidence"] == conf                                # evidence untouched


def test_volition_cycle_protects_from_decay():
    # A rehearsed fact should not decay on the next SleepCycle at the rehearsal
    # instant (its clock was just reset).
    from core.consolidate import consolidate
    _canon("keep", confidence=0.8, significance=0.0,
           last="2000-01-01T00:00:00+00:00")
    now = datetime.now(timezone.utc)
    volition.volition_cycle(k=5, now=now)
    consolidate(now=now)
    assert get_fact("keep")["confidence"] == 0.8


def test_volition_report():
    _canon("a", confidence=0.6, significance=0.6)
    volition.write_voluntary("Mount Everest is the tallest mountain")
    rep = volition.volition_report()
    assert rep["voluntary"] == 1
    assert rep["total"] == 2
    assert rep["focus"]


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_volition_roundtrip(capsys):
    from core.cli import main

    assert main(["volition-write", "The Nile is a river in Africa"]) == 0
    w = json.loads(capsys.readouterr().out.strip())
    assert w["accepted"] is True and w["volition"] is True

    assert main(["volition-focus"]) == 0
    assert json.loads(capsys.readouterr().out.strip())               # non-empty

    assert main(["volition-cycle"]) == 0
    assert "focused" in json.loads(capsys.readouterr().out.strip())

    assert main(["volition-report"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["voluntary"] == 1
