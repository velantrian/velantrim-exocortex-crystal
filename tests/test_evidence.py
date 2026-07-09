"""Tests for the Evidence Span Store (core/evidence.py, WP1) and Receipt v2."""
import json

import pytest

from core import evidence, knowledge, provenance, memory
from core.ingest import ingest


# ─── attach / list ────────────────────────────────────────────────────────────

def test_attach_and_list_evidence():
    fid = ingest("The Earth orbits the Sun")["fact"]["fact_id"]
    row = evidence.attach_evidence(
        fid, "astro.md", source_kind="file", chunk_id="c1",
        span_start=10, span_end=42, source_text="...the Earth orbits the Sun...")
    assert row["evidence_id"].startswith("ev:")
    assert row["source_sha256"] == evidence.sha256("...the Earth orbits the Sun...")
    spans = evidence.evidence_for(fid)
    assert len(spans) == 1
    assert spans[0]["source_uri"] == "astro.md" and spans[0]["chunk_id"] == "c1"


def test_attach_unknown_fact_raises():
    with pytest.raises(ValueError):
        evidence.attach_evidence("does-not-exist", "x.txt")


def test_attach_defaults_claim_to_current_fact():
    fid = ingest("Gold is a metal")["fact"]["fact_id"]
    row = evidence.attach_evidence(fid, "chem.txt")
    assert row["claim_sha256"] == evidence.sha256("Gold is a metal")


# ─── verify / drift ─────────────────────────────────────────────────────────

def test_verify_evidence_ok():
    fid = ingest("Vienna is the capital of Austria")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "geo.txt")
    report = evidence.verify_evidence(fid)
    assert report and all(e["status"] == "ok" for e in report)


def test_verify_detects_modified_claim():
    fid = ingest("Water boils at 100C")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "phys.txt")
    memory.update_fact(fid, claim="Water boils at 90C now")
    report = evidence.verify_evidence(fid)
    assert report[0]["status"] == "modified"


def test_verify_detects_erased():
    # erase_fact() physically deletes evidence_spans (GDPR Art. 17), so a fully
    # erased fact has no spans left to replay — an empty report, not a
    # per-span "erased" status. (The "erased" branch in verify_evidence()
    # still exists for legacy data erased before this behavior shipped.)
    from core.erasure import erase_fact
    fid = ingest("Helium is a gas")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "chem.txt")
    erase_fact(fid, reason="test")
    assert evidence.verify_evidence(fid) == []


def test_verify_no_spans_is_empty():
    fid = ingest("Mercury is a planet")["fact"]["fact_id"]
    assert evidence.verify_evidence(fid) == []


# ─── span validation (#61) ────────────────────────────────────────────────────

def test_attach_rejects_inverted_span():
    fid = ingest("Saturn has rings")["fact"]["fact_id"]
    with pytest.raises(ValueError):
        evidence.attach_evidence(fid, "astro.md", span_start=50, span_end=10)


def test_attach_rejects_negative_span():
    fid = ingest("Jupiter is a planet")["fact"]["fact_id"]
    with pytest.raises(ValueError):
        evidence.attach_evidence(fid, "astro.md", span_start=-1, span_end=5)


def test_attach_rejects_half_span():
    fid = ingest("Neptune is blue")["fact"]["fact_id"]
    with pytest.raises(ValueError):
        evidence.attach_evidence(fid, "astro.md", span_start=10)


def test_attach_accepts_valid_span_and_section():
    fid = ingest("Mars is red")["fact"]["fact_id"]
    row = evidence.attach_evidence(
        fid, "astro.md", section="Chapter 2 — Planets",
        span_start=0, span_end=11)
    assert row["section"] == "Chapter 2 — Planets"
    spans = evidence.evidence_for(fid)
    assert spans[0]["section"] == "Chapter 2 — Planets"
    assert spans[0]["span_start"] == 0 and spans[0]["span_end"] == 11


# ─── stale source detection (#61) ─────────────────────────────────────────────

def test_verify_detects_stale_source():
    fid = ingest("The Alps are mountains")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "geo.md", source_text="The Alps are mountains.")
    # Source content changed since the span was sealed.
    report = evidence.verify_evidence(
        fid, current_sources={"geo.md": "The Alps were leveled."})
    assert report[0]["status"] == "stale_source"


def test_verify_source_unchanged_is_ok():
    fid = ingest("The Nile is a river")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "geo.md", source_text="The Nile is a river.")
    report = evidence.verify_evidence(
        fid, current_sources={"geo.md": "The Nile is a river."})
    assert report[0]["status"] == "ok"


def test_verify_source_not_supplied_is_not_rechecked():
    fid = ingest("The Sahara is a desert")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "geo.md", source_text="The Sahara is a desert.")
    # No current_sources for this uri → span is not re-hashed, stays ok.
    report = evidence.verify_evidence(fid, current_sources={"other.md": "x"})
    assert report[0]["status"] == "ok"


# ─── provenance-coverage guard (#61) ──────────────────────────────────────────

def test_provenance_gap_for_verified_fact_without_evidence():
    # An EXTERNAL world fact is promoted to VERIFIED but carries no evidence span.
    res = ingest("Lisbon is in Portugal", source_status="EXTERNAL")
    fid = res["fact"]["fact_id"]
    assert res["fact"]["truth_status"] == "VERIFIED"
    assert evidence.provenance_gaps([fid]) == [fid]


def test_no_provenance_gap_once_evidence_attached():
    res = ingest("Madrid is in Spain", source_status="EXTERNAL")
    fid = res["fact"]["fact_id"]
    evidence.attach_evidence(fid, "geo.md", source_text="Madrid is in Spain.")
    assert evidence.provenance_gaps([fid]) == []


def test_user_claimed_fact_is_not_a_provenance_gap():
    # USER_REPORTED world facts are USER_CLAIMED, not VERIFIED — no evidence required.
    res = ingest("My cat is named Mittens", source_status="USER_REPORTED")
    fid = res["fact"]["fact_id"]
    assert res["fact"]["truth_status"] != "VERIFIED"
    assert evidence.provenance_gaps([fid]) == []


# ─── knowledge ingestion attaches evidence ────────────────────────────────────

def test_learn_attaches_source_evidence(tmp_path):
    p = tmp_path / "astro.md"
    p.write_text("# Astronomy\n- The Moon orbits the Earth.\n", encoding="utf-8")
    rep = knowledge.ingest_file(str(p), source="astro-101")
    assert rep["accepted"] == 1
    spans = evidence.evidence_for(rep["fact_ids"][0])
    assert len(spans) == 1
    assert spans[0]["source_uri"] == "astro-101"
    assert spans[0]["source_kind"] == "file"
    assert spans[0]["source_sha256"]   # content hash recorded


def test_ingest_claims_can_disable_evidence():
    rep = knowledge.ingest_claims(
        [{"claim": "Saturn has rings"}], source="s", attach_evidence=False)
    assert evidence.evidence_for(rep["fact_ids"][0]) == []


# ─── Receipt v2: evidence sealed into citations + replay ──────────────────────

def _answer_with_evidence():
    fid = ingest("Jupiter is the largest planet")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "planets.md", source_kind="file")
    from core.pipeline import run
    return run("which is the largest planet")


def test_receipt_v2_version_and_embeds_evidence():
    assert provenance.RECEIPT_VERSION == 2
    receipt = provenance.build_receipt(_answer_with_evidence())
    cited = [c for c in receipt["citations"] if c.get("evidence")]
    assert cited, "expected at least one citation carrying evidence"
    assert cited[0]["evidence"][0]["source_uri"] == "planets.md"


def test_receipt_v2_fresh_evidence_verifies():
    receipt = provenance.build_receipt(_answer_with_evidence())
    report = provenance.verify_receipt(receipt)
    assert report["verified"] is True
    ev_cits = [c for c in report["citations"] if c.get("evidence")]
    assert ev_cits and all(e["status"] == "ok" for e in ev_cits[0]["evidence"])


def test_receipt_v2_detects_removed_evidence():
    res = _answer_with_evidence()
    receipt = provenance.build_receipt(res)
    # Drop the evidence row directly to simulate a removed source link.
    fid = receipt["citations"][0]["fact_id"]
    with memory._db() as conn:
        conn.execute("DELETE FROM evidence_spans WHERE fact_id = ?", (fid,))
    report = provenance.verify_receipt(receipt)
    statuses = {c["status"] for c in report["citations"]}
    assert "evidence_missing" in statuses
    assert report["verified"] is False


def test_evidence_free_citation_keeps_v1_shape():
    # A receipt over facts without evidence must keep the original 5-key citation.
    ingest("A plain fact about salt")
    from core.pipeline import run
    receipt = provenance.build_receipt(run("salt"))
    for cit in receipt["citations"]:
        assert "evidence" not in cit
        assert set(cit) == {"fact_id", "claim_sha256", "source",
                            "epistemic_state", "truth_status"}


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_evidence_list_and_verify(capsys):
    from core.cli import main
    fid = ingest("Neon is a noble gas")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "chem.txt")
    assert main(["evidence", fid]) == 0
    rows = json.loads(capsys.readouterr().out.strip())
    assert rows[0]["source_uri"] == "chem.txt"
    assert main(["evidence", fid, "--verify"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep[0]["status"] == "ok"
