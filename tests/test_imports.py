"""Tests for Import Sessions & Dry-run Review (core/imports.py, WP2)."""
import json

from core import imports, memory
from core.ingest import ingest, _fact_id, _legacy_fact_id
from core.compliance import is_restricted
from core.erasure import is_erased


# ─── Dry-run prediction (no writes) ───────────────────────────────────────────

def test_predict_accept_new_world_fact():
    res = imports.predict_claim("Saturn has visible rings")
    assert res["verdict"] == "accept" and res["claim_type"] == "WORLD_FACT"


def test_predict_blocked_low_confidence():
    res = imports.predict_claim("A doubtful world fact", confidence=0.0)
    assert res["verdict"] == "blocked" and res["reason"]


def test_predict_empty_is_blocked():
    assert imports.predict_claim("   ")["verdict"] == "blocked"


def test_predict_explicit_claim_type_override():
    # "I feel happy" classifies as EMOTION; forcing WORLD_FACT overrides it.
    res = imports.predict_claim("I feel happy about gravity", claim_type="WORLD_FACT")
    assert res["claim_type"] == "WORLD_FACT"


def test_predict_immune_blocked():
    from core import immune
    immune.record_threat("forbidden xyz pattern", severity=1.0)
    res = imports.predict_claim("forbidden xyz pattern")
    assert res["verdict"] == "blocked" and res["reason"].startswith("Immune")


def test_predict_duplicate_for_existing_validated():
    ingest("Gold is a metal")
    res = imports.predict_claim("Gold is a metal")
    assert res["verdict"] == "duplicate"


def test_predict_legacy_cross_variant_duplicate_without_writing_index():
    original = "I Prefer   Legacy Imports"
    legacy = _legacy_fact_id(original)
    normalized_id = _fact_id(original)
    assert legacy != normalized_id
    assert ingest(original, fact_id=legacy)["accepted"] is True

    # A dry run must find the same cross-variant legacy target as live ingest,
    # but must not create/backfill the persistent derived compatibility index.
    res = imports.predict_claim("i prefer legacy imports")
    assert res["verdict"] == "duplicate"
    assert res["fact_id"] == legacy
    assert memory.get_fact(normalized_id) is None

    with memory._db() as conn:
        table = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'normalized_ingest_index'"
        ).fetchone()
    assert table is None


def test_predict_conflict_against_canon():
    ingest("Water boils at 100 degrees Celsius")
    res = imports.predict_claim("Water boils at 50 degrees Celsius")
    assert res["verdict"] == "conflict"
    assert res["conflicts"]


def test_dry_run_writes_nothing():
    claim = "The Andromeda galaxy is approaching the Milky Way"
    before = memory.get_fact(_fact_id(claim))
    report = imports.dry_run_text(claim + "\n", fmt="txt", source="astro")
    assert before is None
    assert memory.get_fact(_fact_id(claim)) is None      # still not written
    assert report["dry_run"] is True
    assert report["total"] == 1 and report["would_accept"] == 1


def test_dry_run_file_fmt_without_dot(tmp_path):
    p = tmp_path / "kb.dat"
    p.write_text("Saturn has rings\n", encoding="utf-8")
    report = imports.dry_run_file(str(p), fmt="txt", source="planets")
    assert report["total"] == 1 and report["source"] == "planets"


def test_dry_run_file_unsupported_extension(tmp_path):
    import pytest
    p = tmp_path / "data.bin"
    p.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        imports.dry_run_file(str(p))


def test_dry_run_file_md(tmp_path):
    p = tmp_path / "kb.md"
    p.write_text("# Notes\n- Mercury is a planet.\n- A weak claim.\n", encoding="utf-8")
    report = imports.dry_run_file(str(p), source="lesson")
    assert report["dry_run"] is True and report["total"] == 2
    assert report["source"] == "lesson"
    # nothing persisted
    assert memory.get_fact(_fact_id("Mercury is a planet.")) is None


# ─── Real import with a session ───────────────────────────────────────────────

def test_import_file_records_session(tmp_path):
    p = tmp_path / "corpus.md"
    p.write_text("- The Moon orbits the Earth.\n- Stars emit light.\n", encoding="utf-8")
    rep = imports.import_file(str(p), source="astro-101")
    assert rep["accepted"] == 2
    sid = rep["session_id"]
    assert sid.startswith("imp:")
    assert set(imports.session_facts(sid)) == set(rep["fact_ids"])


def test_import_file_explicit_session_id(tmp_path):
    p = tmp_path / "c.txt"
    p.write_text("Helium is a noble gas\n", encoding="utf-8")
    rep = imports.import_file(str(p), session_id="imp:fixed1")
    assert rep["session_id"] == "imp:fixed1"
    assert imports.session_facts("imp:fixed1") == rep["fact_ids"]


def test_duplicate_import_session_does_not_own_preexisting_fact(tmp_path):
    """A session that only re-imports an already-canonical claim must not be
    able to erase/restrict the fact a DIFFERENT, earlier session created.

    Regression for: ingest_claims() recorded every accepted fact_id in
    `fact_ids`, including duplicate hits of pre-existing facts, so
    _record_session() enrolled a fact into a session that never created it —
    a later erase_session()/restrict_session() on that session then deleted a
    fact owned by an unrelated import.
    """
    p = tmp_path / "c.txt"
    p.write_text("Water boils at 100 degrees Celsius at sea level.\n", encoding="utf-8")

    rep_a = imports.import_file(str(p), source="doc_a")
    assert rep_a["accepted"] == 1
    assert rep_a["duplicates"] == 0
    fid = rep_a["fact_ids"][0]

    # Re-import of the SAME claim text: accepted-but-duplicate, zero NEW facts.
    rep_b = imports.import_file(str(p), source="doc_b")
    assert rep_b["accepted"] == 1
    assert rep_b["duplicates"] == 1
    assert rep_b["fact_ids"] == [fid]        # reporting still shows the hit
    assert rep_b["new_fact_ids"] == []       # but session B created nothing

    assert imports.session_facts(rep_b["session_id"]) == []
    assert imports.session_facts(rep_a["session_id"]) == [fid]

    e = imports.erase_session(rep_b["session_id"])
    assert e == {"session_id": rep_b["session_id"], "facts": 0, "erased": 0}
    assert not is_erased(fid)
    assert memory.get_fact(fid) is not None  # session A's fact survives


def test_restrict_and_erase_session(tmp_path):
    p = tmp_path / "c.txt"
    p.write_text("Neon glows orange\nArgon is inert\n", encoding="utf-8")
    rep = imports.import_file(str(p), session_id="imp:batch")
    fids = rep["fact_ids"]

    r = imports.restrict_session("imp:batch")
    assert r["restricted"] == len(fids)
    assert all(is_restricted(fid) for fid in fids)

    e = imports.erase_session("imp:batch")
    assert e["erased"] == len(fids)
    assert all(is_erased(fid) for fid in fids)
    # GDPR Art. 17: erase_session() erases through erase_fact(), which now
    # also cleans up each fact's import_sessions row(s) — no dangling
    # session_id/source pointer survives the batch erasure.
    assert imports.session_facts("imp:batch") == []


def test_dry_run_via_import_file(tmp_path):
    p = tmp_path / "c.txt"
    p.write_text("Titan is a moon of Saturn\n", encoding="utf-8")
    rep = imports.import_file(str(p), dry_run=True)
    assert rep["dry_run"] is True
    assert memory.get_fact(_fact_id("Titan is a moon of Saturn")) is None


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_learn_dry_run(tmp_path, capsys):
    from core.cli import main
    p = tmp_path / "k.md"
    p.write_text("- Jupiter is a gas giant.\n", encoding="utf-8")
    assert main(["learn", str(p), "--dry-run", "--source", "astro"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["dry_run"] is True and rep["would_accept"] == 1


def test_cli_session_restrict(tmp_path, capsys):
    from core.cli import main
    p = tmp_path / "k.txt"
    p.write_text("Xenon is a noble gas\n", encoding="utf-8")
    assert main(["learn", str(p), "--session", "imp:restrict"]) == 0
    capsys.readouterr()
    assert main(["session-restrict", "imp:restrict"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["restricted"] == 1


def test_cli_session_lifecycle(tmp_path, capsys):
    from core.cli import main
    p = tmp_path / "k.txt"
    p.write_text("Krypton is a noble gas\n", encoding="utf-8")
    assert main(["learn", str(p), "--session", "imp:cli"]) == 0
    capsys.readouterr()
    assert main(["import-session", "imp:cli"]) == 0
    fids = json.loads(capsys.readouterr().out.strip())
    assert len(fids) == 1
    assert main(["session-erase", "imp:cli"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["erased"] == 1
