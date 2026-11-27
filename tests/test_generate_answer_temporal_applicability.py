"""Temporal applicability in generate_answer (as_of + temporal_scope)."""
from core.pipeline import (
    generate_answer,
    _lift_applicability,
    build_facts_pack,
)
from core.applicability import _facts_covering_as_of, _fact_covers_as_of, _parse_temporal_instant
from datetime import date


def _verified(fact_id, claim, **extra):
    fact = {
        "fact_id": fact_id,
        "claim": claim,
        "source": f"independent-source:{fact_id}",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "epistemic_state": "Validated",
        "confidence": 1.0,
        "restricted": False,
    }
    fact.update(extra)
    return fact


def _pack(*facts, asked_object=None, as_of=None, temporal_scope=None, query="q"):
    pack = {"facts": list(facts), "query": query, "total": len(facts)}
    if asked_object is not None:
        pack["asked_object"] = asked_object
    if as_of is not None:
        pack["as_of"] = as_of
    if temporal_scope is not None:
        pack["temporal_scope"] = temporal_scope
    return pack


def test_no_temporal_params_keeps_old_observation():
    old = _verified("e1", "L in progress", object="L", primary_object="L", observed_at="2026-10-08")
    out = generate_answer(_pack(old, asked_object="L"), trace=[])
    assert out["answer"] == "L in progress"
    assert [f["fact_id"] for f in out["facts"]] == ["e1"]


def test_current_scope_without_as_of_explains_required_parameter():
    old = _verified("e1", "L in progress", observed_at="2026-10-08")
    out = generate_answer(_pack(old, temporal_scope="current"), trace=[])
    assert out["answer"] is None
    assert "requires a valid explicit as_of" in out["error"]


def test_as_of_without_current_scope_is_noop():
    old = _verified("e1", "L in progress", observed_at="2026-10-08")
    out = generate_answer(_pack(old, as_of="2026-11-08"), trace=[])
    assert out["answer"] == "L in progress"


def test_older_observation_excluded_for_current_as_of():
    old = _verified("e1", "L in progress", observed_at="2026-10-08")
    out = generate_answer(
        _pack(old, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]
    assert out["facts"] == []
    assert old["truth_status"] == "VERIFIED"


def test_same_day_observation_included():
    same = _verified("e1", "L in progress today", observed_at="2026-11-08")
    out = generate_answer(
        _pack(same, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] == "L in progress today"
    assert [f["fact_id"] for f in out["facts"]] == ["e1"]


def test_datetime_observation_does_not_cover_date_only_as_of():
    same = _verified(
        "e1",
        "observed that day",
        observed_at="2026-11-08T10:00:00+01:00",
    )
    out = generate_answer(
        _pack(same, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_matching_datetime_observation_included():
    same = _verified(
        "e1",
        "observed that moment",
        observed_at="2026-11-08T10:00:00+01:00",
    )
    out = generate_answer(
        _pack(same, as_of="2026-11-08T10:00:00+01:00", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] == "observed that moment"


def test_equal_instants_across_timezones_are_included():
    same = _verified(
        "e1",
        "same instant",
        observed_at="2026-11-08T10:00:00+01:00",
    )
    assert _fact_covers_as_of(same, "2026-11-08T09:00:00+00:00") is True


def test_interval_covering_as_of_included():
    covering = _verified(
        "e1",
        "status valid through November",
        observed_at="2026-10-08",
        valid_from="2026-10-01",
        valid_until="2026-11-30",
    )
    out = generate_answer(
        _pack(covering, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] == "status valid through November"


def test_interval_not_covering_as_of_excluded():
    ended = _verified(
        "e1",
        "status ended in October",
        valid_from="2026-10-01",
        valid_until="2026-10-31",
    )
    out = generate_answer(
        _pack(ended, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_missing_timestamp_not_used_as_current_grounding():
    bare = _verified("e1", "undated claim")
    assert "observed_at" not in bare
    out = generate_answer(
        _pack(bare, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_created_at_is_not_evidence_time():
    storage_only = _verified(
        "e1",
        "write time is not observation",
        created_at="2026-11-08T12:00:00+01:00",
        updated_at="2026-11-08T12:00:00+01:00",
    )
    out = generate_answer(
        _pack(storage_only, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_created_at_does_not_override_older_observation():
    mixed = _verified(
        "e1",
        "old observation",
        observed_at="2026-10-08",
        created_at="2026-11-08T12:00:00+01:00",
        updated_at="2026-11-08T12:00:00+01:00",
    )
    assert _fact_covers_as_of(mixed, date(2026, 11, 8)) is False
    out = generate_answer(
        _pack(mixed, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None


def test_recorded_at_is_not_used_as_observation_time():
    fact = _verified("e1", "recorded same day", recorded_at="2026-11-08")
    out = generate_answer(
        _pack(fact, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_today_write_about_october_event_is_not_current_evidence():
    fact = _verified(
        "e1",
        "October state recorded today",
        observed_at="2026-10-08",
        recorded_at="2026-11-08",
    )
    assert _fact_covers_as_of(fact, "2026-11-08") is False
    out = generate_answer(
        _pack(fact, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]
    assert fact["truth_status"] == "VERIFIED"


def test_probe_date_used_when_no_observed_or_recorded():
    fact = _verified("e1", "probe date same day", date="2026-11-08")
    out = generate_answer(
        _pack(fact, as_of="2026-11-08", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] == "probe date same day"


def test_ac07_object_then_time_reports_uncertainty():
    old_l = _verified(
        "e1",
        "L in progress",
        object="L",
        primary_object="L",
        observed_at="2026-10-08",
    )
    l2 = _verified(
        "e2",
        "ready",
        object="L",
        primary_object="L2",
        observed_at="2026-11-08",
    )
    summary = _verified(
        "e3",
        "repeats readiness",
        object="L",
        primary_object="L2",
        observed_at="2026-11-08",
    )
    out = generate_answer(
        _pack(
            old_l,
            l2,
            summary,
            asked_object="L",
            as_of="2026-11-08",
            temporal_scope="current",
        ),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]
    assert "ready" not in (out.get("answer") or "")
    assert "in progress" not in (out.get("answer") or "")


def test_object_filter_unchanged_without_time():
    old_l = _verified("e1", "L in progress", object="L", primary_object="L", observed_at="2026-10-08")
    l2 = _verified("e2", "ready", object="L", primary_object="L2", observed_at="2026-11-08")
    out = generate_answer(_pack(old_l, l2, asked_object="L"), trace=[])
    assert out["answer"] == "L in progress"
    assert [f["fact_id"] for f in out["facts"]] == ["e1"]


def _retrieved_l_pair():
    return [
        {
            "id": "e1",
            "text": "L in progress",
            "source": "card-l",
            "confidence": 0.9,
            "_score": 0.8,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "epistemic_state": "Observed",
            "origin": "retrieval",
            "object": "L",
            "primary_object": "L",
            "observed_at": "2026-10-08",
        },
        {
            "id": "e2",
            "text": "ready",
            "source": "card-l2",
            "confidence": 0.95,
            "_score": 0.7,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "epistemic_state": "Observed",
            "origin": "retrieval",
            "object": "L",
            "primary_object": "L2",
            "observed_at": "2026-11-08",
        },
    ]


def test_run_without_time_keeps_old_l_card(monkeypatch):
    from core import pipeline

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _retrieved_l_pair())
    out = pipeline.run("Какой статус детали L сегодня?", asked_object="L")
    assert out["answer"] == "L in progress"
    assert [f["fact_id"] for f in out["facts"]] == ["e1"]


def test_run_forwards_as_of_and_temporal_scope(monkeypatch):
    from core import pipeline

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _retrieved_l_pair())
    out = pipeline.run(
        "Какой статус детали L сегодня?",
        asked_object="L",
        as_of="2026-11-08",
        temporal_scope="current",
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_run_includes_same_day_observation(monkeypatch):
    from core import pipeline

    items = _retrieved_l_pair()
    items[0] = dict(items[0], observed_at="2026-11-08", text="L in progress today")
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: items)
    out = pipeline.run(
        "Какой статус детали L сегодня?",
        asked_object="L",
        as_of="2026-11-08",
        temporal_scope="current",
    )
    assert out["answer"] == "L in progress today"
    assert [f["fact_id"] for f in out["facts"]] == ["e1"]


def test_covering_helper_noops_without_current_scope():
    old = _verified("e1", "old", observed_at="2026-10-08")
    kept = _facts_covering_as_of([old], "2026-11-08", None)
    assert kept == [old]

def test_observation_at_2300_does_not_cover_0900_same_day():
    fact = _verified("e1", "seen at 23:00", observed_at="2026-11-08T23:00:00+01:00")
    assert _fact_covers_as_of(fact, "2026-11-08T09:00:00+01:00") is False
    out = generate_answer(
        _pack(fact, as_of="2026-11-08T09:00:00+01:00", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_interval_ending_at_0100_does_not_cover_2300_same_day():
    fact = _verified(
        "e1",
        "ended at 01:00",
        valid_from="2026-11-08T00:00:00+01:00",
        valid_until="2026-11-08T01:00:00+01:00",
    )
    assert _fact_covers_as_of(fact, "2026-11-08T23:00:00+01:00") is False
    out = generate_answer(
        _pack(fact, as_of="2026-11-08T23:00:00+01:00", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_date_only_observation_does_not_cover_datetime_as_of():
    fact = _verified("e1", "seen that day", observed_at="2026-11-08")
    assert _fact_covers_as_of(fact, "2026-11-08T09:00:00+01:00") is False


def test_invalid_as_of_oops_is_rejected():
    assert _parse_temporal_instant("2026-11-08oops") is None
    fact = _verified("e1", "L in progress today", observed_at="2026-11-08")
    out = generate_answer(
        _pack(fact, as_of="2026-11-08oops", temporal_scope="current"),
        trace=[],
    )
    assert out["answer"] is None
    assert "current status is not established" in out["error"]


def test_applicability_survives_store_clear_cache_and_reload():
    from core import memory

    item = {
        "id": "persist-l",
        "text": "L in progress",
        "source": "card-l",
        "confidence": 0.9,
        "_score": 0.8,
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "epistemic_state": "Observed",
        "origin": "retrieval",
        "object": "L",
        "primary_object": "L",
        "observed_at": "2026-10-08",
        "valid_from": "2026-10-01",
        "recorded_at": "2026-11-08",
    }
    pack = build_facts_pack([item], "q", asked_object="L")
    fact = pack["facts"][0]
    stored_in_pack = fact["metadata"]["applicability"]
    assert stored_in_pack["primary_object"] == "L"
    assert stored_in_pack["object"] == "L"
    assert stored_in_pack["observed_at"] == "2026-10-08"
    assert stored_in_pack["valid_from"] == "2026-10-01"
    assert stored_in_pack["recorded_at"] == "2026-11-08"

    memory._L0.clear()
    reloaded = memory.get_fact("persist-l")
    assert reloaded is not None
    assert reloaded.get("primary_object") is None
    assert reloaded.get("observed_at") is None
    stored = reloaded["metadata"]["applicability"]
    assert stored["primary_object"] == "L"
    assert stored["object"] == "L"
    assert stored["observed_at"] == "2026-10-08"
    assert stored["valid_from"] == "2026-10-01"
    assert stored["recorded_at"] == "2026-11-08"

    lifted = {}
    _lift_applicability(lifted, reloaded)
    assert lifted["primary_object"] == "L"
    assert lifted["observed_at"] == "2026-10-08"
    assert lifted["recorded_at"] == "2026-11-08"

