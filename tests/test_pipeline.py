"""Smoke tests for the MVP pipeline."""
import pytest

# DB isolation is provided by the autouse `isolated_db` fixture in conftest.py.


def test_pipeline_happy_path():
    from core.pipeline import run
    result = run("quantum entanglement")
    assert result.get("answer") is not None
    assert "error" not in result or result.get("error") is None
    assert len(result["facts"]) > 0
    for f in result["facts"]:
        assert f["epistemic_state"] == "Validated"
        assert f["truth_status"] == "VERIFIED"


def test_validated_facts_are_merged_into_l3_graph():
    """The single entry into L3 is TruthGate: validated facts land in the graph."""
    from core.pipeline import run
    from core.l3_graph import get_l3_graph

    result = run("quantum entanglement")
    graph = get_l3_graph()
    graph_ids = {f["fact_id"] for f in graph.all_facts()}
    for f in result["facts"]:
        assert f["fact_id"] in graph_ids
        assert graph.get_fact(f["fact_id"])["truth_status"] == "VERIFIED"


def test_run_blocks_gracefully_when_l3_promotion_fails(monkeypatch):
    """L3 (canon) and SQLite (pending) have no shared transaction. A failed L3
    merge must surface as a blocked result, not a raw traceback — and the
    documented partial state holds: the fact is Validated in SQLite (re-run
    re-merges, MERGE is idempotent), the graph stays empty."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    from core.memory import get_fact

    graph = get_l3_graph()

    def boom(_fact):
        raise RuntimeError("L3 backend down")

    monkeypatch.setattr(graph, "merge_fact", boom)

    result = pipeline.run("quantum entanglement")
    assert result["answer"] is None
    assert "L3 promotion failed" in result["error"]
    # graph never received the node…
    assert graph.all_facts() == []
    # …but the SQLite-side ESM transition already happened (acceptable, idempotent).
    assert get_fact("f2")["epistemic_state"] == "Validated"


def test_blocked_pipeline_does_not_write_to_l3_graph():
    """A fact that never passes TruthGate must not appear in canonical L3."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    pipeline.run("zxqvbnmqwerty")  # empty retrieval → blocked before promotion
    assert get_l3_graph().all_facts() == []


# ─── episodic binding ─────────────────────────────────────────────────────────

def _two_retrieved():
    return [
        {"id": "f2", "text": "Quantum entanglement links particles",
         "source": "physics", "confidence": 0.85, "_score": 0.6,
         "epistemic_state": "Observed", "origin": "retrieval"},
        {"id": "f5", "text": "DNA encodes genetic information",
         "source": "biology", "confidence": 0.99, "_score": 0.5,
         "epistemic_state": "Observed", "origin": "retrieval"},
    ]


def test_run_links_co_recalled_facts_with_episode_context(monkeypatch):
    from core import pipeline
    from core.l3_graph import get_l3_graph

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())
    pipeline.run("two facts",
                 episode={"who": ["user"], "where": "lab", "when": "2026-06-01T17:00"})

    g = get_l3_graph()
    assert "f5" in {n["fact_id"] for n in g.neighbors("f2")}
    edge = next(e for e in g._edges if e[0] == "f2" and e[2] == "f5")
    assert edge[1] == "CO_OCCURRED"
    assert edge[3]["who"] == ["user"]
    assert edge[3]["where"] == "lab"
    assert edge[3]["when"] == "2026-06-01T17:00"


def test_recall_episode_reads_who_where_when(monkeypatch):
    """The episodic context written by _link_episode is now queryable."""
    from core import pipeline

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())
    pipeline.run("session topic",
                 episode={"who": ["user", "assistant"], "where": "chat",
                          "when": "2026-06-01"})

    episodes = pipeline.recall_episode("f2")
    assert episodes, "expected an episodic link from f2"
    ep = episodes[0]
    assert ep["with"] == "f5"
    assert ep["who"] == ["user", "assistant"]
    assert ep["where"] == "chat"
    assert ep["when"] == "2026-06-01"
    assert ep["query"] == "session topic"


def test_recall_episode_empty_for_unlinked_fact():
    from core.pipeline import recall_episode
    assert recall_episode("never-seen") == []


def test_recall_by_entity_finds_facts_by_who_and_where(monkeypatch):
    from core import pipeline

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())
    pipeline.run("topic", episode={"who": ["alice"], "where": "lab"})

    assert pipeline.recall_by_entity(who="alice") == ["f2", "f5"]
    assert pipeline.recall_by_entity(where="lab") == ["f2", "f5"]
    assert pipeline.recall_by_entity(who="bob") == []
    assert pipeline.recall_by_entity() == []   # no criterion → nothing


def test_single_fact_recall_creates_no_episode_edge(monkeypatch):
    from core import pipeline
    from core.l3_graph import get_l3_graph

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved()[:1])
    pipeline.run("one fact")
    assert get_l3_graph()._edges == []


def test_link_episode_defaults_when_to_now_without_context():
    from core import pipeline
    from core.l3_graph import MockL3Graph

    g = MockL3Graph()
    facts = [{"fact_id": "a"}, {"fact_id": "b"}]
    pipeline._link_episode(g, facts, "q", episode=None)
    edge = next(e for e in g._edges if e[0] == "a")
    assert "when" in edge[3] and edge[3]["when"]      # auto-stamped
    assert "who" not in edge[3]                        # no context → no who/where


def test_pipeline_empty_retrieval_blocks():
    from core.pipeline import run
    result = run("zxqvbnmqwerty")   # matches nothing in DATABASE
    assert result.get("answer") is None
    assert "Retrieval" in result.get("error", "")


def test_trace_is_built_for_each_fact():
    from core.pipeline import run
    result = run("DNA")
    assert len(result["trace"]) == len(result["facts"])
    for el in result["trace"]:
        assert "fact_id" in el
        assert "epistemic_state" in el
        assert el["epistemic_state"] == "Validated"


# ─── helpers ──────────────────────────────────────────────────────────────────

def test_retrieve_respects_k_and_skips_non_matches():
    from core.pipeline import retrieve
    hits = retrieve("the", k=2)               # pure stopword query → nothing
    assert len(hits) <= 2
    assert all(h["epistemic_state"] == "Observed" for h in hits)
    assert retrieve("zxqvbnmqwerty") == []


def test_retrieve_is_semantic_not_stopword_matching():
    """Regression: 'Tell me about the Sun' must NOT pull the brain fact in via
    the shared stopword 'the' (the old BM25-lite bug)."""
    from core.pipeline import retrieve
    hits = retrieve("Tell me about the Sun")
    ids = [h["id"] for h in hits]
    assert "f3" in ids          # Earth revolves around the Sun
    assert "f4" not in ids      # The human brain ... (no longer a false match)


def test_retrieve_pure_stopword_query_returns_nothing():
    from core.pipeline import retrieve
    assert retrieve("how do you do") == []


def test_retrieve_graph_walk_surfaces_linked_facts():
    """A fact linked in the graph to a vector hit surfaces by association
    (spreading activation), even with no lexical overlap with the query."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    g.merge_fact({"fact_id": "A", "claim": "sunlight energy photosynthesis",
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated"})
    g.merge_fact({"fact_id": "B", "claim": "chlorophyll molecule structure",
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated"})
    g.add_edge("A", "CO_OCCURRED", "B", {})

    hits = {h["id"]: h for h in retrieve("sunlight energy")}
    assert hits["A"]["origin"] == "memory"        # direct vector hit
    assert hits["B"]["origin"] == "graph"         # pulled in via the edge
    assert hits["B"]["_score"] < hits["A"]["_score"]   # decayed by distance


def test_graph_walk_is_multi_hop_with_decay():
    """Activation spreads multiple hops, decaying each hop: A→B→C from a query
    that only matches A. C (2 hops out) ranks below B (1 hop) below A."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    for fid, claim in [("A", "sunlight energy"), ("B", "leaf cells"),
                       ("C", "soil minerals")]:
        g.merge_fact({"fact_id": fid, "claim": claim, "source": "s",
                      "confidence": 1.0, "epistemic_state": "Validated"})
    g.add_edge("A", "CO_OCCURRED", "B", {})
    g.add_edge("B", "CO_OCCURRED", "C", {})

    hits = {h["id"]: h for h in retrieve("sunlight energy", k=5)}
    assert hits["A"]["origin"] == "memory"
    assert hits["B"]["origin"] == "graph"
    assert hits["C"]["origin"] == "graph"          # reached 2 hops out
    assert hits["A"]["_score"] > hits["B"]["_score"] > hits["C"]["_score"]


def test_graph_walk_skips_deprecated_neighbors():
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    g.merge_fact({"fact_id": "A", "claim": "sunlight energy", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Validated"})
    g.merge_fact({"fact_id": "old", "claim": "outdated note", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Deprecated"})
    g.add_edge("A", "SUPERSEDED_BY", "old", {})

    ids = {h["id"] for h in retrieve("sunlight energy")}
    assert "A" in ids and "old" not in ids        # stale neighbor not recalled


def test_retrieve_recalls_facts_learned_via_ingest():
    """Closing the loop: a fact accepted through ingest() lands in L3 and is
    then recallable by retrieve() (origin='memory'), not just the seed corpus."""
    from core.ingest import ingest
    from core.pipeline import retrieve

    ingest("Photosynthesis converts sunlight into energy")  # → canonical L3
    hits = retrieve("sunlight energy")

    recalled = [h for h in hits if h["origin"] == "memory"]
    assert recalled, "expected a recall from L3 memory"
    assert any("Photosynthesis" in h["text"] for h in recalled)


def test_rerun_recalls_validated_fact_without_esm_error():
    """A second run of the same query recalls the now-Validated L3 fact; the
    promotion loop must not try to re-transition it (Validated→Validated is
    illegal in the ESM matrix)."""
    from core.pipeline import run

    first = run("quantum entanglement")
    assert first["answer"] is not None

    second = run("quantum entanglement")
    assert second.get("error") is None
    assert second["answer"] is not None


# ─── guardian ───────────────────────────────────────────────────────────────

def test_guardian_rejects_empty_facts():
    from core.pipeline import guardian
    ok, reason = guardian({"facts": []}, [{"fact_id": "x"}])
    assert ok is False and "пустой" in reason


def test_guardian_rejects_empty_trace():
    from core.pipeline import guardian
    ok, reason = guardian({"facts": [{"fact_id": "x"}]}, [])
    assert ok is False and "Trace" in reason


def test_guardian_rejects_trace_fact_count_mismatch():
    from core.pipeline import guardian
    facts = {"facts": [{"fact_id": "a", "claim": "c", "source": "s", "confidence": 1},
                       {"fact_id": "b", "claim": "c", "source": "s", "confidence": 1}]}
    ok, reason = guardian(facts, [{"fact_id": "a"}])
    assert ok is False and "Несоответствие" in reason


@pytest.mark.parametrize("bad_fact, needle", [
    ({"fact_id": "", "claim": "c", "source": "s", "confidence": 1}, "fact_id"),
    ({"fact_id": "a", "claim": "", "source": "s", "confidence": 1}, "claim"),
    ({"fact_id": "a", "claim": "c", "source": "", "confidence": 1}, "source"),
    ({"fact_id": "a", "claim": "c", "source": "s", "confidence": 0}, "confidence"),
])
def test_guardian_field_level_rejections(bad_fact, needle):
    from core.pipeline import guardian
    ok, reason = guardian({"facts": [bad_fact]}, [{"fact_id": "a"}])
    assert ok is False and needle in reason


def test_guardian_accepts_well_formed_pack():
    from core.pipeline import guardian
    facts = {"facts": [{"fact_id": "a", "claim": "c", "source": "s", "confidence": 0.9}]}
    ok, reason = guardian(facts, [{"fact_id": "a"}])
    assert ok is True and reason is None


# ─── truth_gate ─────────────────────────────────────────────────────────────

def test_truth_gate_rejects_empty():
    from core.pipeline import truth_gate
    ok, reason = truth_gate({"facts": []})
    assert ok is False


def test_truth_gate_rejects_missing_source():
    from core.pipeline import truth_gate
    ok, reason = truth_gate({"facts": [{"fact_id": "a", "confidence": 0.9}]})
    assert ok is False and "source" in reason


def test_truth_gate_rejects_below_threshold():
    from core.pipeline import truth_gate
    ok, reason = truth_gate(
        {"facts": [{"fact_id": "a", "source": "s", "confidence": 0.01}]},
        min_confidence=0.05,
    )
    assert ok is False and "порога" in reason


# ─── type-aware truth_gate (ось модальности) ──────────────────────────────────

def test_truth_gate_passes_subjective_without_confidence_threshold():
    """A feeling is real as a feeling: EMOTION passes even at low confidence."""
    from core.pipeline import truth_gate
    ok, reason = truth_gate(
        {"facts": [{"fact_id": "e", "source": "user", "confidence": 0.0,
                    "claim_type": "EMOTION", "source_status": "USER_REPORTED"}]},
        min_confidence=0.05,
    )
    assert ok is True and reason is None


def test_truth_gate_blocks_llm_output_as_world_fact():
    """LLM output can never be a world fact by itself."""
    from core.pipeline import truth_gate
    ok, reason = truth_gate(
        {"facts": [{"fact_id": "h", "source": "model", "confidence": 0.9,
                    "claim_type": "WORLD_FACT", "source_status": "LLM_OUTPUT"}]},
    )
    assert ok is False and "LLM_OUTPUT" in reason


def test_truth_status_reflects_claim_type():
    """Promotion must label subjective claims SUBJECTIVE, not VERIFIED."""
    from core.pipeline import _truth_status_for
    assert _truth_status_for("WORLD_FACT") == "VERIFIED"
    assert _truth_status_for("EMOTION") == "SUBJECTIVE"
    assert _truth_status_for("USER_EXPERIENCE") == "SUBJECTIVE"
    assert _truth_status_for("INTERPRETATION") == "HYPOTHESIS"


def test_canonical_emotion_is_validated_but_not_world_fact():
    """ChatGPT's canonical case: 'felt anxious talking to X' is a valid
    experience (Validated) but must never become a verified world fact."""
    from core import pipeline, memory

    pack = {
        "facts": [{
            "fact_id": "anx1",
            "claim": "Пользователь почувствовал тревогу при разговоре с X",
            "source": "chat",
            "confidence": 0.9,
            "epistemic_state": "Observed",
            "claim_type": "EMOTION",
            "source_status": "USER_REPORTED",
            "significance": 0.7,
        }],
        "query": "q",
        "total": 1,
    }
    memory.store_fact(pack["facts"][0])

    ok, _ = pipeline.truth_gate(pack)
    assert ok is True

    fact = pack["facts"][0]
    memory.transition_esm(fact["fact_id"], "Validated")
    fact["truth_status"] = pipeline._truth_status_for(fact["claim_type"])

    assert fact["truth_status"] == "SUBJECTIVE"   # valid feeling…
    assert fact["claim_type"] != "WORLD_FACT"     # …but not a fact about the world


# ─── generate_answer fallback ─────────────────────────────────────────────────

def test_generate_answer_falls_back_when_nothing_validated():
    from core.pipeline import generate_answer
    pack = {"facts": [{"fact_id": "a", "claim": "raw", "source": "s",
                       "epistemic_state": "Observed"}]}
    out = generate_answer(pack, trace=[])
    # No Validated/Supported facts → fall back to all facts rather than empty.
    assert out["total_facts"] == 1
    assert "raw" in out["answer"]


# ─── build_facts_pack ─────────────────────────────────────────────────────────

def test_build_facts_pack_skips_items_without_id():
    from core.pipeline import build_facts_pack
    pack = build_facts_pack(
        [{"text": "no id", "source": "s", "_score": 0.5,
          "epistemic_state": "Observed"}],
        "q",
    )
    assert pack["facts"] == []
    assert pack["total"] == 0


# ─── run() block paths (guardian / truth_gate rejection) ──────────────────────

def test_run_blocks_when_guardian_fails(monkeypatch):
    from core import pipeline
    monkeypatch.setattr(pipeline, "guardian", lambda fp, tr: (False, "boom"))
    result = pipeline.run("quantum entanglement")
    assert result["answer"] is None
    assert "Guardian: boom" in result["error"]


def test_run_blocks_when_truth_gate_fails(monkeypatch):
    from core import pipeline
    monkeypatch.setattr(pipeline, "truth_gate", lambda fp, **k: (False, "nope"))
    result = pipeline.run("DNA")
    assert result["answer"] is None
    assert "TruthGate: nope" in result["error"]
