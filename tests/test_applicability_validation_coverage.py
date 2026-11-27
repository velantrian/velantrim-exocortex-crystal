"""Fail-closed public requests and substantive temporal boundary diagnostics."""
from copy import deepcopy
from datetime import date, datetime, timezone

import pytest

from core import applicability as a
from core import query_pipeline
from tests.test_applicability_live_path import NOW, admit, dumps, reopen
from tests.test_applicability_live_path import durable as durable  # pytest fixture registration
from tests.test_generate_answer_asked_object import _verified
from core.pipeline import generate_answer


@pytest.mark.parametrize("scope", ["curent", "currnet", "historical", "", " ", 1, False, [], {}])
def test_public_query_rejects_temporal_scope_typo_without_disabling_time_filter(durable, scope):
    admit("old", "Laboratory component ready", {"primary_object": "L", "observed_at": "2026-10-08"})
    reopen()
    before = dumps(durable)
    result = query_pipeline.query("Laboratory component ready", asked_object="L", as_of=NOW,
                                  temporal_scope=scope)
    assert result["answer"] is None
    assert result["reason_code"] == "invalid_applicability_request"
    assert "invalid temporal_scope" in result["error"]
    assert "unknown values cannot disable time filtering" in result["error"]
    assert dumps(durable) == before
    # The direct rendering boundary must not bypass the same validation.
    fact = _verified("old", "Old status", primary_object="L", observed_at="2026-10-08")
    result = generate_answer({"facts": [fact], "asked_object": "L", "as_of": NOW,
                              "temporal_scope": scope}, [])
    assert result["answer"] is None
    assert "invalid temporal_scope" in result["error"]


@pytest.mark.parametrize("asked", ["", " ", False, 5, [], {}])
def test_public_query_explains_invalid_asked_object_before_retrieval(asked, monkeypatch):
    def unexpected_retrieval(*args, **kwargs):
        pytest.fail("invalid applicability parameters must fail before retrieval")
    monkeypatch.setattr(query_pipeline, "_retrieve_read_only", unexpected_retrieval)
    result = query_pipeline.query("Laboratory status", asked_object=asked)
    assert result["answer"] is None
    assert result["error"] == "asked_object must be a non-empty object identifier"


@pytest.mark.parametrize("instant", [date(2026, 11, 8), datetime(2026, 11, 8, 10, tzinfo=timezone.utc),
                                     " 2026-11-08 "])
def test_covering_helper_accepts_explicit_native_dates_and_normalizes_strings(instant):
    fact = _verified("same", "Same observation", observed_at=instant)
    assert a._facts_covering_as_of([fact], instant, " current ") == [fact]
    assert a._parse_temporal_instant(instant)[1] == (instant if not isinstance(instant, str) else date(2026, 11, 8))


@pytest.mark.parametrize("instant", [None, "", " ", 5, "2026-02-30", "2026-11-08oops"])
def test_covering_helper_never_keeps_facts_on_missing_or_invalid_current_instant(instant):
    fact = _verified("old", "Old observation", observed_at="2026-10-08")
    assert a._facts_covering_as_of([fact], instant, "current") == []
    assert not a._fact_covers_as_of(fact, instant)


@pytest.mark.parametrize("scope", ["curent", False, ""])
def test_covering_helper_unknown_scope_cannot_bypass_filter(scope):
    fact = _verified("old", "Old observation", observed_at="2026-10-08")
    assert a._facts_covering_as_of([fact], NOW, scope) == []


@pytest.mark.parametrize("asked", [None, "", 5])
def test_object_helper_no_requested_identifier_preserves_copied_candidate_list(asked):
    facts = [_verified("legacy", "Legacy unscoped fact")]
    result = a._facts_applicable_to_asked_object(facts, asked)
    assert result == facts
    assert result is not facts


@pytest.mark.parametrize("left,right,order", [
    ("2026-11-07", "2026-11-08", -1),
    ("2026-11-08", "2026-11-08", 0),
    ("2026-11-09", "2026-11-08", 1),
])
def test_date_comparison_orders_observations_without_clipping(left, right, order):
    assert a._compare_temporals(a._parse_temporal_instant(left), a._parse_temporal_instant(right)) == order
    assert a._fact_covers_as_of({"observed_at": left}, right) is (order == 0)


@pytest.mark.parametrize("empty", [None, "", " "])
def test_absent_validity_bounds_do_not_override_observation_and_probe_fallback(empty):
    fact = {"valid_from": empty, "valid_until": empty, "observed_at": empty, "date": "2026-11-08"}
    assert a._fact_covers_as_of(fact, "2026-11-08")
    assert not a._fact_covers_as_of(fact, "2026-11-09")


@pytest.mark.parametrize("values,instant,reason", [
    ({"valid_from": "bad"}, NOW, "invalid valid_from"),
    ({"valid_until": "bad"}, NOW, "invalid valid_until"),
    ({"valid_until": "2026-11-07"}, NOW, "validity expired before as_of"),
    ({"valid_from": "2026-11-09"}, NOW, "validity starts after as_of"),
    ({"valid_from": "2026-11-08T09:00:00"}, NOW, "validity interval/as_of timezone awareness differs"),
    ({"valid_until": "2026-11-09T10:00:00"}, NOW, "validity interval/as_of timezone awareness differs"),
    ({"observed_at": "not-an-instant"}, NOW, "invalid observation time"),
    ({"observed_at": "2026-11-08T10:00:00"}, NOW, "observation/as_of timezone awareness differs"),
    ({"observed_at": "2026-11-08T10:00:00+01:00"}, "2026-11-08", "instant observation cannot establish a whole queried date"),
    ({"valid_from": "2026-11-08T10:00:00+01:00"}, "2026-11-08", "validity starts after as_of (whole-day coverage required)"),
    ({"valid_until": "2026-11-08T10:00:00+01:00"}, "2026-11-08", "validity expired before as_of (whole-day coverage required)"),
])
def test_excluded_temporal_evidence_explains_actual_boundary_and_preserves_record(values, instant, reason):
    fact = _verified("boundary", "Laboratory status", primary_object="L", **values)
    before = deepcopy(fact)
    result = generate_answer({"facts": [fact], "asked_object": "L", "as_of": instant,
                              "temporal_scope": "current"}, [])
    assert result["answer"] is None
    assert result["applicability"]["exclusions"] == [{"fact_id": "boundary", "reason": reason}]
    assert "current status is not established" in result["error"]
    assert fact == before


def test_date_only_observation_same_day_not_silently_historical_at_midnight():
    fact = _verified("day", "Observed sometime that day", observed_at="2026-11-08")
    result = generate_answer({"facts": [fact], "as_of": NOW, "temporal_scope": "current"}, [])
    assert result["answer"] is None
    assert result["applicability"]["historical_facts"] == []
    assert "date-only observation" in result["error"]


@pytest.mark.parametrize("scope", ["current", "CURRENT", "Current", " current "])
def test_public_query_normalizes_current_case_variants_and_excludes_old_evidence(durable, scope):
    admit("old", "Laboratory component ready", {"primary_object": "L", "observed_at": "2026-10-08"})
    assert query_pipeline.query("Laboratory component ready", asked_object="L")["answer"] is not None
    filtered = query_pipeline.query("Laboratory component ready", asked_object="L", as_of=NOW,
                                    temporal_scope=scope)
    assert filtered["answer"] is None
    assert "current status is not established" in filtered["error"]


def test_embedding_no_applicability_preserves_unrelated_metadata_without_inventing_namespace():
    fact = {"claim": "Legacy fact", "metadata": {"lineage": {"source": "existing"}}}
    before = deepcopy(fact)
    a.embed(fact)
    assert fact == before
    assert "applicability" not in fact["metadata"]


def test_open_ended_validity_start_covers_later_instant_without_observation_expiry():
    fact = _verified("ongoing", "Ongoing explicitly declared validity", valid_from="2026-11-01")
    result = generate_answer({"facts": [fact], "as_of": NOW, "temporal_scope": "current"}, [])
    assert result["answer"] == fact["claim"]
    assert result["facts"][0]["valid_from"] == "2026-11-01"
    assert "uncertainty" not in result
