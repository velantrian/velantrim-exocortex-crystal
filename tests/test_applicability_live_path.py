"""Offline applicability tests: real SQLite L1/L3, cache clear, fresh query.

AC inputs are frozen copies of the existing synthetic audit, not new model runs
or revisions of its historical labels. Manual attribution is explicit below.
"""
import asyncio
from copy import deepcopy
from contextlib import closing
import json
from pathlib import Path
import sqlite3

import pytest

from core import evidence, memory, l3_graph
from core.applicability import _fact_covers_as_of
from core.ingest import ingest
from core.pipeline import build_facts_pack, generate_answer
from core.query_pipeline import query

NOW = "2026-11-08T10:00:00+01:00"


@pytest.fixture
def durable(monkeypatch, tmp_path):
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "sqlite")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "l3.db"))
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    l3_graph.reset_l3_graph()
    # Exercise applicability rather than hashing recall quality: include all
    # small-fixture candidates using the real configurable retrieval path.
    from core import retrieval_config
    config_path = tmp_path / "retrieval.json"
    config_path.write_text(json.dumps({"k": 20, "min_similarity": 0.0}))
    monkeypatch.setenv("VELANTRIM_RETRIEVAL_CONFIG", str(config_path))
    retrieval_config.reset_retrieval_config()
    return tmp_path


def admit(fid, claim, applicability, *, verified=True):
    result = ingest(claim, fact_id=fid, source="isolated-synthetic-fixture",
                    claim_type="WORLD_FACT", confidence=0.99,
                    source_status="EXTERNAL" if verified else "USER_REPORTED",
                    metadata={"applicability": applicability})
    assert result["accepted"]
    if verified:
        evidence.attach_evidence(fid, "file://synthetic-" + fid,
                                 source_text=claim, section="fixture")
    return result["fact"]


def reopen():
    memory._L0.clear()
    l3_graph.reset_l3_graph()


def dumps(durable):
    # Detect ALL durable changes, not only claim/verdict changes.
    result = []
    for path in (Path(memory.SQLITE_PATH), durable / "l3.db"):
        with closing(sqlite3.connect(path)) as conn:
            result.append(tuple(conn.iterdump()))
    return result


@pytest.mark.parametrize("values,allowed", [
    ({"primary_object": "L", "observed_at": NOW}, True),
    ({"primary_object": "L", "observed_at": "2026-10-08T10:00:00+02:00",
      "recorded_at": NOW}, False),
    ({"primary_object": "L2", "linked_objects": ["L"], "observed_at": NOW}, False),
    ({"primary_object": "L2", "linked_objects": ["L"],
      "status_applies_to": ["L"], "observed_at": NOW}, True),
    ({"observed_at": NOW}, False),
])
def test_real_store_cache_clear_fresh_retrieve_answer(durable, values, allowed):
    admit("saved", "Laboratory component ready", values)
    reopen()
    stored = memory.get_fact("saved")
    assert stored["metadata"]["applicability"] == values
    assert l3_graph.get_l3_graph().get_fact("saved")["metadata"]["applicability"] == values
    before = dumps(durable)
    result = query("Laboratory component ready", asked_object="L", as_of=NOW,
                   temporal_scope="current")
    assert (result["answer"] is not None) == allowed
    assert result["read_only"] is True
    if allowed:
        assert result["facts"][0]["observed_at"] == values["observed_at"]
        assert result["facts"][0]["primary_object"] == values["primary_object"]
        if "status_applies_to" in values:
            assert result["facts"][0]["status_applies_to"] == ["L"]
            assert result["facts"][0]["linked_objects"] == ["L"]
    else:
        assert result["facts"] == []
        if "recorded_at" in values:
            assert "current status is not established" in result["error"]
            assert result["applicability"]["historical_facts"][0]["observed_at"].startswith("2026-10-08")
        if "linked_objects" in values:
            assert result["applicability"]["context_relations"][0]["linked_objects"] == ["L"]
            assert not result["applicability"]["context_relations"][0]["status_transferred"]
    assert dumps(durable) == before
    assert memory.get_fact("saved") == stored
    assert l3_graph.get_l3_graph().get_fact("saved")["truth_status"] == "VERIFIED"


def test_build_store_then_real_reload_then_live_answer(durable):
    values = {"object": "wrapper", "primary_object": "L2", "linked_objects": ["L"],
              "status_applies_to": ["L"], "observed_at": NOW, "recorded_at": "2026-11-09",
              "valid_from": "2026-11-01", "valid_until": "2026-11-30"}
    item = dict(id="built", text="Laboratory inherited status", source="fixture", confidence=0.99,
                epistemic_state="Observed", claim_type="WORLD_FACT", source_status="EXTERNAL", **values)
    build_facts_pack([item], "Laboratory inherited status")
    memory._L0.clear()
    metadata = memory.get_fact("built")["metadata"]
    assert metadata["applicability"] == values
    # Real admission follows the real save; retrieval is never monkeypatched.
    result = ingest(item["text"], fact_id="built", source="fixture", confidence=0.99,
                    source_status="EXTERNAL", metadata=metadata)
    assert result["accepted"]
    evidence.attach_evidence("built", "file://built", source_text=item["text"], section="fixture")
    reopen()
    result = query(item["text"], asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] == item["text"]
    assert all(result["facts"][0][k] == v for k, v in values.items())


@pytest.mark.parametrize("as_of", [None, "", "2026-11-08oops", "2026-02-30", 123])
def test_current_missing_invalid_as_of_explains_even_without_memory(durable, as_of):
    result = query("What is the current state?", temporal_scope="current", as_of=as_of)
    assert result["answer"] is None
    assert result["reason_code"] == "invalid_applicability_request"
    assert "requires a valid explicit as_of" in result["error"]
    from core.pipeline import run
    legacy = run("What is the current state?", temporal_scope="current", as_of=as_of)
    assert legacy["answer"] is None
    assert "requires a valid explicit as_of" in legacy["error"]


@pytest.mark.parametrize("extra", [
    {"observed_at": "2026-11-08T23:00:00+01:00"},
    {"valid_from": "2026-11-08T00:00:00+01:00", "valid_until": "2026-11-08T01:00:00+01:00"},
    {"recorded_at": NOW}, {"created_at": NOW}, {"updated_at": NOW},
    {"observed_at": "2026-10-08", "recorded_at": NOW},
    {"observed_at": "2026-11-08"},
])
def test_live_later_expired_write_only_old_or_date_only_not_current(durable, extra):
    # created_at/updated_at are actual storage columns, not part of applicability.
    values = {k: v for k, v in extra.items() if k not in ("created_at", "updated_at")}
    admit("counterexample", "Laboratory component status", {"primary_object": "L", **values})
    reopen()
    result = query("Laboratory component status", asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] is None
    assert "current status is not established" in result["error"]


@pytest.mark.parametrize("extra,as_of,allowed", [
    ({"observed_at": "2026-11-08T09:00:00Z"}, NOW, True),
    ({"observed_at": "2026-11-08T10:00:00"}, NOW, False),
    ({"valid_from": "2026-11-08", "valid_until": "2026-11-08"}, "2026-11-08T23:59:59+01:00", True),
    ({"valid_from": "2026-11-08T00:00:00+01:00", "valid_until": "2026-11-08"}, "2026-11-08", True),
    ({"valid_from": "2026-11-08T01:00:00+01:00", "valid_until": "2026-11-08"}, "2026-11-08", False),
    ({"valid_from": "2026-11-08T00:00:00+01:00", "valid_until": "2026-11-08T23:59:59.999999+01:00"}, "2026-11-08", True),
    ({"valid_from": "2026-11-09", "valid_until": "2026-11-08"}, NOW, False),
    ({"valid_until": "not a date"}, NOW, False),
])
def test_new_precision_boundary_cases(extra, as_of, allowed):
    assert _fact_covers_as_of(extra, as_of) is allowed


@pytest.mark.parametrize("primary", [None, "", [], {}, 7])
def test_malformed_primary_never_falls_back_or_accepts_transfer(primary):
    from tests.test_generate_answer_asked_object import _verified, _pack
    fact = _verified("bad", "A label is not grounds", object="L", primary_object=primary,
                     status_applies_to=["L"])
    result = generate_answer(_pack(fact, asked_object="L"), [])
    assert result["answer"] is None
    assert "object belonging not established" in result["error"]


def test_arbitrary_applicability_label_cannot_verify_user_report(durable):
    admit("user", "Laboratory component ready", {"primary_object": "L", "observed_at": NOW,
          "status_applies_to": ["L"], "truth_status": "VERIFIED"}, verified=False)
    result = query("Laboratory component ready", asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] is None
    assert l3_graph.get_l3_graph().get_fact("user")["truth_status"] == "USER_CLAIMED"


def test_removing_evidence_still_blocks_correct_applicability(durable):
    admit("no-evidence", "Laboratory component ready", {"primary_object": "L", "observed_at": NOW})
    with memory._db() as conn:
        conn.execute("DELETE FROM evidence_spans")
    result = query("Laboratory component ready", asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] is None
    assert result["reason_code"] == "insufficient_grounding_missing_verified_evidence"


def test_restricted_record_cannot_leak_into_exclusion_or_history(durable):
    from core.compliance import restrict_processing
    admit("secret", "Laboratory secret status", {"primary_object": "L2", "observed_at": "2026-10-08"})
    restrict_processing("secret")
    result = query("Laboratory secret status", asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] is None
    assert "Laboratory secret status" not in json.dumps(result.get("applicability", {}))


def test_query_does_not_trust_retrieval_wrapper_labels(durable, monkeypatch):
    from core import query_pipeline
    admit("wrapped", "Laboratory component ready", {"primary_object": "L2", "observed_at": NOW})
    monkeypatch.setattr(query_pipeline, "_retrieve_read_only", lambda q: [
        {"id": "wrapped", "primary_object": "L", "status_applies_to": ["L"], "observed_at": NOW}])
    result = query("Laboratory component ready", asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] is None


def test_l1_l3_disagreement_cannot_broaden_applicability(durable):
    admit("disputed", "Laboratory component ready", {"primary_object": "L2", "observed_at": NOW})
    stored = memory.get_fact("disputed")
    metadata = deepcopy(stored["metadata"])
    metadata["applicability"]["primary_object"] = "L"
    memory.update_fact("disputed", metadata=metadata)
    result = query("Laboratory component ready", asked_object="L", as_of=NOW, temporal_scope="current")
    assert result["answer"] is None
    assert "object belonging not established" in result["error"]


def ac_fixture(case):
    return json.loads((Path(__file__).parent / "fixtures" / "applicability" / (case + ".json")).read_text())


def load_ac_into_store(case, asked):
    data = ac_fixture(case)
    for index, record in enumerate(data["records"]):
        # Manual writer attribution from attached-document lineage, NOT NLP.
        primary = asked
        if case == "AC03" and index in (1, 3):
            primary = "R-14"
        if case == "AC07" and index in (1, 2):
            primary = "L2"
        # Assistant suggestions/assertions have no independent admission authority.
        verified = not ((case == "AC06" and index == 2) or (case == "AC08" and index == 1))
        from datetime import datetime
        from zoneinfo import ZoneInfo
        observed = datetime.strptime(record["time"].replace(" Europe/Berlin", ""), "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Europe/Berlin")).isoformat()
        # Render the record's declared wrapper object as a heading so the
        # offline word-hashing retriever sees its identifier (no new claim).
        claim = asked + ": " + record["statement"] + (" " + record["caveats"] if record["caveats"] else "")
        admit(case + "-" + str(index), claim, {"object": asked, "primary_object": primary,
              "observed_at": observed}, verified=verified)
    return data


@pytest.mark.parametrize("case,asked,as_of,admitted_ids", [
    ("AC03", "R-41", "2026-11-06T13:45:00+01:00", {"AC03-2"}),
    ("AC06", "M", "2026-11-08T09:30:00+01:00", {"AC06-1"}),
    ("AC07", "L", NOW, set()),
    ("AC08", "выбор способа упаковки", None, {"AC08-0"}),
])
def test_actual_ac_fixtures_through_durable_live_query(durable, case, asked, as_of, admitted_ids):
    data = load_ac_into_store(case, asked)
    reopen()
    before = dumps(durable)
    result = query(data["question"], asked_object=asked, as_of=as_of,
                   temporal_scope="current" if as_of else None)
    assert {f["fact_id"] for f in result["facts"]} == admitted_ids
    if case == "AC07":
        assert result["answer"] is None
        assert "current status is not established" in result["error"]
        assert result["applicability"]["historical_facts"][0]["observed_at"].startswith("2026-10-08")
    else:
        assert result["answer"] is not None
        assert "current status is not established" not in result["answer"]
    if case == "AC08":
        assert "журнал неполон" in result["answer"]
        assert "Уже согласовали" not in result["answer"]
        assert "решения не было" not in result["answer"].lower()
    assert dumps(durable) == before


def test_http_and_async_explicit_parameters_reach_live_filter(durable, monkeypatch):
    from core import aio
    from core.api import create_app
    from fastapi.testclient import TestClient
    admit("http", "Laboratory component ready", {"primary_object": "L2", "observed_at": NOW})
    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    client = TestClient(create_app())
    result = client.post("/ask", json={"query": "Laboratory component ready", "asked_object": "L",
                         "as_of": NOW, "temporal_scope": "current"}).json()
    assert result["answer"] is None
    assert "primary object differs" in result["error"]
    receipt = client.get("/receipt", params={"q": "Laboratory component ready", "asked_object": "L",
                         "as_of": NOW, "temporal_scope": "current"})
    assert receipt.status_code == 422
    assert client.get("/receipt", params={"q": "Laboratory component ready", "asked_object": "L2",
                      "as_of": NOW, "temporal_scope": "current"}).status_code == 200
    result = asyncio.run(aio.arun("Laboratory component ready", asked_object="L2", as_of=NOW, temporal_scope="current"))
    assert result["answer"] == "Laboratory component ready"


def test_cli_parameters_reach_live_filter(durable, capsys):
    from core.cli import main
    admit("cli", "Laboratory component ready", {"primary_object": "L2", "observed_at": NOW})
    main(["ask", "Laboratory component ready", "--asked-object", "L", "--as-of", NOW, "--temporal-scope", "current"])
    assert "primary object differs" in capsys.readouterr().out
