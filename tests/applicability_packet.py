"""Reproduce the offline scenario packet: python -m tests.applicability_packet.

Uses the same isolated SQLite setup as pytest. This is not a model evaluation
and does not rewrite any historical experiment result or rubric label.
"""
import json
from pathlib import Path
import tempfile
from pytest import MonkeyPatch
from tests.conftest import isolated_db
from tests.test_applicability_live_path import (
    durable, admit, reopen, load_ac_into_store, NOW,
)
from core.query_pipeline import query


def summarize(question, result):
    return {"question": question,
            "admitted_grounds": [{"fact_id": f["fact_id"], "claim": f["claim"]} for f in result["facts"]],
            "exclusions": result.get("applicability", {}).get("exclusions", []),
            "historical_evidence": result.get("applicability", {}).get("historical_facts", []),
            "context_relations": result.get("applicability", {}).get("context_relations", []),
            "answer": result["answer"], "uncertainty": result.get("uncertainty"),
            "error": result.get("error")}


def isolated_case(callback):
    with tempfile.TemporaryDirectory(prefix="crystal-applicability-") as path, MonkeyPatch.context() as patch:
        setup = isolated_db.__wrapped__(patch, Path(path))
        next(setup)
        try:
            durable.__wrapped__(patch, Path(path))
            return callback()
        finally:
            next(setup, None)


def ac(case, asked, as_of):
    data = load_ac_into_store(case, asked)
    reopen()
    result = query(data["question"], asked_object=asked, as_of=as_of,
                   temporal_scope="current" if as_of else None)
    row = summarize(data["question"], result)
    row["pre_applicability_exclusions"] = (
        [{"fact_id": "AC06-2", "reason": "USER_CLAIMED, not strict-canonical"}] if case == "AC06" else
        [{"fact_id": "AC08-1", "reason": "USER_CLAIMED, not strict-canonical"}] if case == "AC08" else [])
    return row


def simple(case):
    values = {"primary_object": "L", "observed_at": NOW}
    if case == "foreign":
        values["primary_object"] = "L2"
    if case == "old":
        values.update(observed_at="2026-10-08T10:00:00+02:00", recorded_at=NOW)
    if case == "later":
        values["observed_at"] = "2026-11-08T23:00:00+01:00"
    if case == "linked":
        values.update(primary_object="L2", linked_objects=["L"])
    admit(case, "Laboratory component ready", values)
    reopen()
    question = "Laboratory component status: what is L's current state?"
    return summarize(question, query(question, asked_object="L", as_of=NOW, temporal_scope="current"))


def packet():
    result = {}
    for case, asked, instant in [("AC03", "R-41", "2026-11-06T13:45:00+01:00"),
                                 ("AC06", "M", "2026-11-08T09:30:00+01:00"),
                                 ("AC07", "L", NOW), ("AC08", "выбор способа упаковки", None)]:
        result[case] = isolated_case(lambda: ac(case, asked, instant))
    for case in ["fresh", "foreign", "old", "later", "linked"]:
        result[case] = isolated_case(lambda: simple(case))
    result["incomplete_journal"] = result["AC08"]
    return result


if __name__ == "__main__":
    print(json.dumps(packet(), ensure_ascii=False, indent=2))
