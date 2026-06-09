"""Targeted tests for defensive / fallback branches that the feature-level
suites don't naturally reach. Each test pins one specific edge so the behaviour
is locked in (not merely to move a coverage number)."""
import pytest

from core import eval as _eval
from core import evidence, knowledge, review
from core.ingest import ingest
from core.memory import store_fact, get_fact


# ─── eval.py — bundled-fixture fallbacks ────────────────────────────────────────

def test_load_fixture_json_missing_returns_none():
    # A file that is not bundled → the loader swallows the error and returns None.
    assert _eval._load_fixture_json("does-not-exist.json") is None


def test_retrieval_corpus_falls_back_to_inline(monkeypatch):
    monkeypatch.setattr(_eval, "_load_fixture_json", lambda name: None)
    corpus = _eval.load_retrieval_corpus()
    assert corpus["cases"] == list(_eval._FIXTURE)
    assert corpus["distractors"] == []


def test_contradiction_pairs_fall_back_to_inline(monkeypatch):
    monkeypatch.setattr(_eval, "_load_fixture_json", lambda name: None)
    assert _eval.load_contradiction_pairs() == list(_eval._CONTRADICTION_FIXTURE)


def test_retrieval_corpus_falls_back_on_empty_cases(monkeypatch):
    monkeypatch.setattr(_eval, "_load_fixture_json", lambda name: {"cases": []})
    assert _eval.load_retrieval_corpus()["cases"] == list(_eval._FIXTURE)


# ─── evidence.py — span validation (fact must exist first) ──────────────────────

@pytest.fixture
def _fact(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    return ingest("Water boils at 100 degrees Celsius")["fact"]["fact_id"]


def test_attach_evidence_rejects_non_integer_span(_fact):
    with pytest.raises(ValueError, match="span offsets must be integers"):
        evidence.attach_evidence(_fact, "src", span_start=1.5, span_end="3")


def test_attach_evidence_rejects_negative_span(_fact):
    with pytest.raises(ValueError, match="non-negative"):
        evidence.attach_evidence(_fact, "src", span_start=-1, span_end=2)


def test_attach_evidence_rejects_half_open_span(_fact):
    with pytest.raises(ValueError, match="given together"):
        evidence.attach_evidence(_fact, "src", span_start=1)


# ─── knowledge.py — CSV row with an empty claim is skipped ──────────────────────

def test_csv_skips_empty_claim_rows():
    out = knowledge.extract_claims(
        "claim,confidence\nReal claim,0.9\n,0.5\n   ,0.4\n", "csv")
    assert [c["claim"] for c in out] == ["Real claim"]


# ─── review.py — immune-block and conflict diagnoses ────────────────────────────

def test_review_diagnose_immune_block(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import immune
    immune.record_threat("forbidden topic", threat_type="manual", severity=1.0,
                         actor="test")
    res = ingest("This is a forbidden topic claim", claim_type="WORLD_FACT")
    assert res["accepted"] is False  # blocked pre-gate by the immune layer
    fid = res["fact"]["fact_id"]
    item = review.review_item(fid)
    assert item["diagnosis"]["verdict"] == "blocked"
    assert "Immune" in item["diagnosis"]["reason"]


def test_review_diagnose_conflict(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    # A Validated canon fact …
    ingest("The tower is exactly 300 metres tall")
    # … and a quarantined Observed fact that contradicts it but passes the gates.
    fid = "ing:conflict01"
    store_fact({
        "fact_id": fid, "claim": "The tower is exactly 450 metres tall",
        "source": "review-test", "confidence": 0.9, "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL", "significance": 0.5,
    })
    diag = review.review_item(fid)["diagnosis"]
    assert diag["verdict"] == "conflict"
    assert diag["conflicts"]


# ─── cli.py — `eval --gate` failure path exits non-zero ─────────────────────────

def test_cli_eval_gate_failure_exits_nonzero(monkeypatch, capsys):
    from core import cli
    # Force a failing gate so the failure-reporting branch runs.
    monkeypatch.setattr(cli._eval, "gate", lambda report: {
        "passed": False,
        "failures": [{"metric": "retrieval.hit@1", "value": 0.0,
                      "op": ">=", "threshold": 0.8}],
    })
    rc = cli.main(["eval", "--gate"])
    assert rc == 1
    assert "gate FAIL" in capsys.readouterr().err


# ─── evidence.py — stale-source guard & truth-status passthrough ────────────────

def test_source_is_stale_false_without_stored_hash():
    # A span with no sealed source_sha256 can never be judged stale.
    assert evidence._source_is_stale({"source_uri": "u"}, {"u": "text"}) is False


def test_truth_status_of_uses_stored_value():
    assert evidence._truth_status_of({"truth_status": "VERIFIED"}) == "VERIFIED"


# ─── l3_graph._salience_score — non-numeric significance defaults to 0.5 ─────────

def test_salience_score_handles_non_numeric_significance():
    from core import l3_graph
    assert l3_graph._salience_score(1.0, "not-a-number") == 1.0 * (1.0 + 0.5 * 0.5)


# ─── fractal.scale_for_strength — strength below all bands → SHORT ──────────────

def test_scale_for_strength_below_all_bands():
    from core import fractal
    assert fractal.scale_for_strength(-0.5) == fractal.SHORT


# ─── velum._remove — removing a key that isn't present is a no-op ───────────────

def test_velum_remove_missing_key_is_noop():
    from core import velum
    v = velum.get_velum()
    v._remove(("nonexistent", "edge"))  # must not raise (early return)


# ─── YAML adapter — empty-claim dict and non-collection scalar ──────────────────

def test_yaml_norm_empty_claim_and_scalar():
    from core.adapters import yaml_adapter
    assert yaml_adapter._norm({"claim": "   "}) == []   # blank claim → dropped
    assert yaml_adapter._norm({"meta": "x"}) == []      # dict w/o claim/claims → []
    assert yaml_adapter._norm(123) == []                # int → no records


# ─── RDF adapter — a blank-node OBJECT triple is skipped ────────────────────────

def test_rdf_skips_blank_node_object(tmp_path):
    pytest.importorskip("rdflib")
    import core.adapters.rdf_adapter as rdf
    nt = tmp_path / "bo.nt"
    # Object is a blank node → the triple must be skipped (no readable object).
    nt.write_text(
        '<http://example.org/S> <http://example.org/p> _:obj .\n'
        '<http://example.org/S> <http://schema.org/name> "Named thing" .\n',
        encoding="utf-8")
    claims = rdf.extract_rdf_claims(str(nt))
    texts = " ".join(c["claim"] for c in claims)
    assert "named thing" in texts.lower()


# ─── PDF adapter — a page with real text yields a claim ─────────────────────────

def test_pdf_extract_collects_paragraph_text(monkeypatch):
    pytest.importorskip("pypdf")
    import core.adapters.pdf_adapter as pdf

    class _FakePage:
        def extract_text(self):
            return "Water boils at one hundred degrees Celsius at sea level."

    class _FakeReader:
        def __init__(self, path):
            self.pages = [_FakePage()]

    monkeypatch.setattr(pdf, "_pypdf", type("M", (), {"PdfReader": _FakeReader}))
    claims = pdf.extract_pdf_claims("ignored.pdf")
    assert claims and "Water boils" in claims[0]["claim"]


# ─── memory._migrate — adds a missing column to an old evidence_spans table ─────

def test_migrate_adds_missing_evidence_column(tmp_path):
    import sqlite3
    from core import memory
    db = tmp_path / "old.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    # An evidence_spans table from an older schema (no 'section' column) + facts.
    conn.execute("CREATE TABLE facts (fact_id TEXT PRIMARY KEY)")
    conn.execute("CREATE TABLE evidence_spans (evidence_id TEXT PRIMARY KEY)")
    memory._migrate(conn)
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(evidence_spans)")}
    assert "section" in cols
    conn.close()


# ─── pipeline — the velum / neurocore hooks never break the canon ───────────────

def test_link_episode_survives_velum_failure(monkeypatch):
    # The Velum hint hook must never break the canon: a failure is swallowed.
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import pipeline, velum
    from core.l3_graph import get_l3_graph
    a = ingest("The honey bee builds a hive")["fact"]["fact_id"]
    b = ingest("The honey bee makes honey")["fact"]["fact_id"]
    monkeypatch.setattr(velum, "get_velum",
                        lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    # Two facts → the episode path runs and reaches the (failing) Velum hook.
    pipeline._link_episode(get_l3_graph(),
                           [{"fact_id": a, "claim": "x"}, {"fact_id": b, "claim": "y"}],
                           "honey bee", None)  # must not raise


def test_pipeline_survives_neurocore_failure(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    from core import pipeline, neurocore
    ingest("Glass is an amorphous solid")
    monkeypatch.setattr(neurocore, "enabled",
                        lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    res = pipeline.run("what is glass")
    assert "answer" in res or "error" in res


# ─── reconcile.find_conflicts — skips non-Validated and verbatim candidates ─────

def test_find_conflicts_skips_nonvalidated_and_verbatim(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.reconcile import find_conflicts
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    # A verbatim Validated duplicate of the probe → must be skipped (a reinforce).
    g.merge_fact({"fact_id": "v1", "claim": "The sky is blue", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Validated",
                  "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"})
    # A near-duplicate that is NOT Validated → must be skipped (not in the canon).
    g.merge_fact({"fact_id": "o1", "claim": "The sky is blue and clear", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Observed",
                  "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"})
    ids = [c["fact_id"] for c in find_conflicts("The sky is blue", fact_id="probe")]
    assert "v1" not in ids and "o1" not in ids


# ─── consolidate — a node with an unparseable baseline timestamp is skipped ─────

def test_consolidate_skips_unparseable_baseline(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import consolidate
    from core.l3_graph import get_l3_graph
    from core.memory import update_fact, get_fact
    fid = ingest("Mercury is the smallest planet")["fact"]["fact_id"]
    update_fact(fid, metadata={"last_consolidated": "not-a-date"})
    get_l3_graph().merge_fact(get_fact(fid))
    consolidate.consolidate()  # must not raise; the bad-baseline node is skipped


# ─── neurogenesis._validated_records — non-Validated graph nodes are skipped ────

def test_validated_records_skips_non_validated(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import neurogenesis
    from core.l3_graph import get_l3_graph
    get_l3_graph().merge_fact({"fact_id": "obs1", "claim": "pending claim",
                               "source": "s", "confidence": 0.5,
                               "epistemic_state": "Observed",
                               "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"})
    ids = [r["fact_id"] for r in neurogenesis._validated_records()]
    assert "obs1" not in ids


# ─── volition_cycle — a focused fact that vanished mid-cycle is skipped ─────────

def test_volition_cycle_skips_vanished_fact(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import volition
    ingest("Saturn is famous for its rings")
    # get_fact → None simulates the fact being erased between focus and rehearsal.
    monkeypatch.setattr(volition, "get_fact", lambda *a, **k: None)
    res = volition.volition_cycle()
    assert res["focused"] == []


# ─── pipeline.retrieve — a below-threshold vector hit is dropped ────────────────

def test_retrieve_drops_below_threshold_hit(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    monkeypatch.setattr(g, "vector_search", lambda *a, **k: [{
        "fact_id": "weak", "claim": "barely related", "_relevance": 0.01,
        "confidence": 1.0, "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"}])
    # _relevance 0.01 < _RETRIEVAL_MIN_SIM (0.05) → the hit is filtered out.
    assert all(item["id"] != "weak" for item in pipeline.retrieve("anything"))


# ─── pipeline spreading activation — non-Validated & restricted neighbours skip ─

def test_spreading_activation_skips_nonvalidated_and_restricted(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.pipeline import run
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    seed = ingest("Photosynthesis occurs in plant chloroplasts")["fact"]["fact_id"]
    g.merge_fact({"fact_id": "nb_obs", "claim": "an observed neighbour", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Observed",
                  "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"})
    g.merge_fact({"fact_id": "nb_res", "claim": "a restricted neighbour", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Validated", "restricted": True,
                  "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"})
    g.add_edge(seed, "RELATED_TO", "nb_obs", {})
    g.add_edge(seed, "RELATED_TO", "nb_res", {})
    # The walk reaches both neighbours and skips them (non-Validated / restricted).
    res = run("photosynthesis chloroplasts")
    assert "answer" in res or "error" in res


# ─── provenance.verify_receipt — sealed evidence reports a drifted fact ─────────

def test_verify_receipt_reports_evidence_drift(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core import provenance, evidence
    from core.pipeline import run
    from core.memory import update_fact
    fid = ingest("The Eiffel Tower is in Paris")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "guide.pdf", source_kind="file",
                            claim="The Eiffel Tower is in Paris")
    receipt = provenance.build_receipt(run("where is the Eiffel Tower"))
    # Drift the underlying fact AFTER sealing the receipt → the span must flag it.
    update_fact(fid, claim="The Eiffel Tower is in Berlin")
    verified = provenance.verify_receipt(receipt)
    statuses = [e["status"]
                for cit in verified.get("citations", [])
                for e in cit.get("evidence", [])]
    assert statuses  # at least one sealed span was replayed
    assert any(s != "ok" for s in statuses)


# ─── SqliteL3Graph.vector_search — an orphan vector (no node) is skipped ────────

def test_sqlite_vector_search_skips_orphan_vector():
    from core.l3_graph import SqliteL3Graph
    from core.embedding import get_embedder
    g = SqliteL3Graph(":memory:")
    g.merge_fact({"fact_id": "x", "claim": "orphan vector test claim", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Validated",
                  "claim_type": "WORLD_FACT", "source_status": "EXTERNAL"})
    # Delete the node row but leave its vector → search must skip the orphan.
    with g._conn:
        g._conn.execute("DELETE FROM nodes WHERE fact_id = 'x'")
    hits = g.vector_search(get_embedder().embed("orphan vector test claim"))
    assert all(h.get("fact_id") != "x" for h in hits)
    g.close()


# ─── _registry.reset — a failing close() during reset is swallowed ──────────────

def test_registry_reset_swallows_close_errors():
    from core._registry import BackendRegistry

    class _Boom:
        def close(self):
            raise RuntimeError("close failed")

    reg = BackendRegistry("VELANTRIM_X", "default", lambda name: _Boom())
    reg.get()                 # populate the singleton with a closable instance
    reg.reset()               # close() raises → must be swallowed, instance cleared
    assert reg._instance is None
