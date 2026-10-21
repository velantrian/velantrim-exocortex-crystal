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


def test_write_voluntary_declares_source_status_explicitly(monkeypatch):
    """write_voluntary() must explicitly pass a system-declared source_status
    to ingest(), not rely on classify_claim()'s user-oriented fallback —
    otherwise a self-authored fact silently inherits whatever the classifier
    assigns to ordinary user text (fragile: any change to classify_claim's
    default would silently change what a voluntary write is attributed to).
    """
    from core import ingest as ingest_mod
    monkeypatch.setattr(ingest_mod, "classify_claim",
                        lambda utterance: ("WORLD_FACT", "OBSERVED"))
    res = volition.write_voluntary("Self-authored claim for this test")
    assert res["accepted"] is True
    assert res["fact"]["source_status"] == "SYSTEM_AUTHORED"


def test_write_voluntary_is_never_user_reported_nor_verified(monkeypatch):
    """A self-authored write must never be attributed to the user
    (USER_REPORTED) nor become VERIFIED — even if the user-utterance
    classifier would label the text as a privileged/external source."""
    from core import ingest as ingest_mod
    for fallback in ("USER_REPORTED", "OBSERVED", "EXTERNAL", "DERIVED"):
        monkeypatch.setattr(ingest_mod, "classify_claim",
                            lambda utterance, _s=fallback: ("WORLD_FACT", _s))
        res = volition.write_voluntary(f"Self-authored claim via {fallback}")
        fact = res["fact"]
        assert fact["source_status"] != "USER_REPORTED"
        assert fact.get("truth_status") != "VERIFIED"


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


# ─── Recall must not erase stored metadata (audit finding #1) ─────────────────

def test_recall_preserves_system_authorship_metadata(monkeypatch):
    """A normal pipeline recall (build_facts_pack → store_fact) must not wipe
    the stored metadata of a system-authored fact: before the fix every query
    rewrote L1 metadata as {}, dropping metadata.volition so the fact no
    longer showed up as voluntary."""
    from core.pipeline import run
    from core.memory import _L0
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")  # recall only our own fact
    claim = "The Pacific is the largest ocean"
    res = volition.write_voluntary(claim)
    assert res["accepted"] is True
    fid = res["fact"]["fact_id"]
    assert volition.volition_report()["voluntary"] == 1

    out = run(claim)
    assert fid in [t["fact_id"] for t in out["trace"]]  # the query really recalled it

    _L0.clear()  # read the persisted L1 row, not the L0 cache
    stored = get_fact(fid)
    assert stored["metadata"].get("volition") is True
    assert stored["source_status"] == "SYSTEM_AUTHORED"
    assert volition.volition_report()["voluntary"] == 1


def test_recall_preserves_occurrence_metadata(monkeypatch):
    """Occurrence/lineage metadata (occurrences, sources_seen) survives a recall."""
    from core.pipeline import run
    from core.memory import _L0
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")  # recall only our own fact
    from core.reconcile import record_occurrence
    claim = "Water boils at 100 degrees Celsius at sea level"
    res = volition.write_voluntary(claim)
    fid = res["fact"]["fact_id"]
    assert record_occurrence(fid, source="user") == 2
    before = get_fact(fid)["metadata"]
    assert before["occurrences"] == 2 and "user" in before["sources_seen"]

    out = run(claim)
    assert fid in [t["fact_id"] for t in out["trace"]]  # the query really recalled it

    _L0.clear()
    after = get_fact(fid)["metadata"]
    assert after["occurrences"] == 2
    assert after["sources_seen"] == before["sources_seen"]
    assert after.get("volition") is True


def test_store_fact_preserve_metadata_only_affects_existing_rows():
    """preserve_metadata keeps an existing row's metadata but a brand-new row
    still takes the incoming metadata; the default overwrite is unchanged."""
    from core.memory import _L0
    store_fact({"fact_id": "pm-new", "claim": "c", "source": "s",
                "metadata": {"k": 1}}, preserve_metadata=True)
    assert get_fact("pm-new")["metadata"] == {"k": 1}
    store_fact({"fact_id": "pm-new", "claim": "c", "source": "s"},
               preserve_metadata=True)
    assert get_fact("pm-new")["metadata"] == {"k": 1}  # L0
    _L0.clear()
    assert get_fact("pm-new")["metadata"] == {"k": 1}  # L1
    store_fact({"fact_id": "pm-new", "claim": "c", "source": "s"})
    _L0.clear()
    assert get_fact("pm-new")["metadata"] == {}         # default: overwrite
