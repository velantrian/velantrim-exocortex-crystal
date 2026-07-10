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


def test_run_result_facts_hide_internal_score_field():
    """The relevance rank (_score) is internal: the answer payload exposes the
    real fact fields but no underscore-prefixed keys."""
    from core.pipeline import run
    result = run("quantum entanglement")
    assert result["facts"]
    for f in result["facts"]:
        assert not any(k.startswith("_") for k in f), f
        assert f["fact_id"] and f["claim"]          # real fields still present


def test_blocked_result_facts_hide_internal_score_field(monkeypatch):
    """The blocked payload is cleaned the same way as the answer payload."""
    from core import pipeline
    monkeypatch.setattr(pipeline, "truth_gate", lambda fp, **k: (False, "nope"))
    result = pipeline.run("quantum entanglement")
    assert result["answer"] is None and result["facts"]
    for f in result["facts"]:
        assert not any(k.startswith("_") for k in f), f


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


# ─── L3 outbox (self-healing partial state) ───────────────────────────────────

def test_l3_outbox_self_heals_failed_merge(monkeypatch):
    """A failed L3 merge queues the fact; draining the outbox after the backend
    recovers lands the node in the canon — no manual re-run of the same query."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    from core.memory import pending_l3_writes

    graph = get_l3_graph()
    real_merge = graph.merge_fact
    monkeypatch.setattr(graph, "merge_fact",
                        lambda _f: (_ for _ in ()).throw(RuntimeError("L3 down")))

    blocked = pipeline.run("quantum entanglement")
    assert blocked["answer"] is None
    assert "L3 promotion failed" in blocked["error"]
    assert graph.all_facts() == []
    assert "f2" in pending_l3_writes()              # queued for retry

    monkeypatch.setattr(graph, "merge_fact", real_merge)   # backend recovers
    assert pipeline.drain_l3_outbox() >= 1
    assert pending_l3_writes() == []
    assert "f2" in {f["fact_id"] for f in graph.all_facts()}


def test_drain_l3_outbox_drops_stale_entry():
    """An outbox entry whose SQLite fact vanished is dropped, not retried forever."""
    from core import pipeline
    from core.memory import enqueue_l3_write, pending_l3_writes

    enqueue_l3_write("ghost")                       # never stored in SQLite
    assert pipeline.drain_l3_outbox() == 0
    assert pending_l3_writes() == []


def test_drain_l3_outbox_drops_non_validated_entry():
    """Outbox is for post-gate Validated merges only — Observed entries are dropped."""
    from core import pipeline
    from core.memory import store_fact, enqueue_l3_write, pending_l3_writes

    store_fact({"fact_id": "obs_q", "claim": "c", "source": "s",
                "epistemic_state": "Observed"})
    enqueue_l3_write("obs_q")
    assert pipeline.drain_l3_outbox() == 0
    assert pending_l3_writes() == []


def test_drain_l3_outbox_keeps_queue_when_backend_down(monkeypatch):
    """If the backend is still down during a drain, the entry stays queued."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    from core.memory import store_fact, enqueue_l3_write, pending_l3_writes

    store_fact({"fact_id": "q1", "claim": "c", "source": "s",
                "confidence": 0.8, "epistemic_state": "Validated"})
    enqueue_l3_write("q1")
    graph = get_l3_graph()
    monkeypatch.setattr(graph, "merge_fact",
                        lambda _f: (_ for _ in ()).throw(RuntimeError("down")))

    assert pipeline.drain_l3_outbox() == 0
    assert "q1" in pending_l3_writes()              # kept for retry


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


def test_retrieve_rrf_deduplicates_seed_and_l3_same_id(monkeypatch):
    """The same fact_id in seed and L3 rankings must appear once in results."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "1")
    g = get_l3_graph()
    g.merge_fact({"fact_id": "f2", "claim": "Quantum entanglement links particles",
                  "source": "physics", "confidence": 0.85,
                  "epistemic_state": "Validated"})
    hits = retrieve("quantum entanglement", k=10)
    assert sum(1 for h in hits if h["id"] == "f2") == 1


def test_retrieve_rrf_respects_top_k(monkeypatch):
    from core.pipeline import retrieve
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "1")
    hits = retrieve("DNA genetic information physics", k=2)
    assert len(hits) <= 2


def test_retrieve_rrf_excludes_restricted_l3_facts(monkeypatch):
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    g = get_l3_graph()
    g.merge_fact({"fact_id": "rstr", "claim": "Zorblax telemetry alpha signal",
                  "source": "s", "confidence": 0.95,
                  "epistemic_state": "Validated", "restricted": True})
    hits = retrieve("Zorblax telemetry alpha signal", k=5)
    assert "rstr" not in {h["id"] for h in hits}


def test_retrieve_rrf_order_is_stable_for_multi_ranking_overlap(monkeypatch):
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "1")
    g = get_l3_graph()
    g.merge_fact({"fact_id": "f2", "claim": "Quantum entanglement links particles",
                  "source": "physics", "confidence": 0.85,
                  "epistemic_state": "Validated"})
    ids_a = [h["id"] for h in retrieve("quantum entanglement", k=5)]
    ids_b = [h["id"] for h in retrieve("quantum entanglement", k=5)]
    assert ids_a == ids_b


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


def test_graph_walk_sums_activation_across_paths():
    """PageRank-style: a hub reachable from two vector hits accumulates more
    activation than a node reachable from only one."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    for fid, claim in [("A", "alpha topic"), ("B", "beta topic"),
                       ("hub", "shared concept"), ("X", "lonely note")]:
        g.merge_fact({"fact_id": fid, "claim": claim, "source": "s",
                      "confidence": 1.0, "epistemic_state": "Validated"})
    g.add_edge("A", "CO_OCCURRED", "hub", {})   # hub reached from both hits
    g.add_edge("B", "CO_OCCURRED", "hub", {})
    g.add_edge("A", "CO_OCCURRED", "X", {})     # X reached from one hit only

    hits = {h["id"]: h for h in retrieve("alpha beta", k=5)}
    assert hits["A"]["origin"] == "memory" and hits["B"]["origin"] == "memory"
    assert hits["hub"]["origin"] == "graph" and hits["X"]["origin"] == "graph"
    assert hits["hub"]["_score"] > hits["X"]["_score"]   # two paths > one


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


def test_graph_walk_does_not_propagate_through_truth_maintenance_edges():
    """Edge-type weighting: relevance spreads along an episodic CO_OCCURRED edge
    but NOT along a CONTRADICTS edge — even to a Validated node. A fact isn't
    'more relevant' because the vector hit contradicts it."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    for fid, claim in [("A", "sunlight energy"), ("assoc", "leaf cells"),
                       ("rival", "moonlight myth")]:
        g.merge_fact({"fact_id": fid, "claim": claim, "source": "s",
                      "confidence": 1.0, "epistemic_state": "Validated"})
    g.add_edge("A", "CO_OCCURRED", "assoc", {})   # association → propagates
    g.add_edge("A", "CONTRADICTS", "rival", {})   # truth-maintenance → does not

    ids = {h["id"] for h in retrieve("sunlight energy", k=5)}
    assert "A" in ids                              # direct vector hit
    assert "assoc" in ids                          # pulled in by association
    assert "rival" not in ids                      # contradiction does not spread


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


def test_collapsed_fact_skipped_in_promotion_not_enqueued():
    """Regression for Codex review #4: a fact already Collapsed in L1 must be
    silently skipped in the ESM promotion loop — its illegal transition must not
    fall into the broad L3 exception handler and must not be enqueued into the
    L3 outbox for drain_l3_outbox() to later merge into Canon."""
    from core.pipeline import run
    from core.memory import transition_esm, get_all_facts
    from core.queue import get_outbox_queue

    # First run: demo-seed facts land in L1 and are promoted to Validated.
    first = run("quantum entanglement")
    assert first.get("error") is None

    # Collapse one of the now-Validated facts (Validated → Collapsed is a
    # valid matrix step — this simulates curator-driven logical removal).
    validated = get_all_facts("Validated")
    assert validated, "expected at least one Validated fact after first run"
    target_id = validated[0]["fact_id"]
    assert transition_esm(target_id, "Collapsed") is True

    # Second run: the demo-seed re-surfaces the same fact as "Observed", but
    # L1 now has "Collapsed". The promotion guard must skip it silently —
    # the ValueError from transition_esm must NOT propagate to the broad L3
    # exception handler (which would enqueue the fact for drain_l3_outbox).
    # The pipeline may return "insufficient grounding" if all facts are now
    # terminal; that is correct behavior, not a promotion failure.
    second = run("quantum entanglement")
    error = second.get("error", "")
    assert "L3 promotion failed" not in error, (
        f"Collapsed fact triggered L3 outbox path: {error}"
    )
    assert target_id not in get_outbox_queue().pending(), (
        "Collapsed fact must not be enqueued in the L3 outbox"
    )


# ─── guardian ───────────────────────────────────────────────────────────────

def test_guardian_rejects_empty_facts():
    from core.pipeline import guardian
    ok, reason = guardian({"facts": []}, [{"fact_id": "x"}])
    assert ok is False and "empty" in reason


def test_guardian_rejects_empty_trace():
    from core.pipeline import guardian
    ok, reason = guardian({"facts": [{"fact_id": "x"}]}, [])
    assert ok is False and "Trace" in reason


def test_guardian_rejects_trace_fact_count_mismatch():
    from core.pipeline import guardian
    facts = {"facts": [{"fact_id": "a", "claim": "c", "source": "s", "confidence": 1},
                       {"fact_id": "b", "claim": "c", "source": "s", "confidence": 1}]}
    ok, reason = guardian(facts, [{"fact_id": "a"}])
    assert ok is False and "Mismatch" in reason


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
    assert ok is False and "threshold" in reason


# ─── type-aware truth_gate (modality axis) ──────────────────────────────────

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
    """Issue #63: truth status is source-aware — user-reported world claims are
    USER_CLAIMED, not VERIFIED; only externally sourced facts become VERIFIED."""
    from core.pipeline import _truth_status_for
    # External / derived sources → independently verified world knowledge
    assert _truth_status_for("WORLD_FACT", "EXTERNAL") == "VERIFIED"
    assert _truth_status_for("WORLD_FACT", "DERIVED") == "VERIFIED"
    assert _truth_status_for("WORLD_FACT", "OBSERVED") == "VERIFIED"
    # User-reported world claim → stored as recalled, not independently verified
    assert _truth_status_for("WORLD_FACT", "USER_REPORTED") == "USER_CLAIMED"
    # No source / unknown → unverified
    assert _truth_status_for("WORLD_FACT") == "UNVERIFIED"
    assert _truth_status_for("WORLD_FACT", None) == "UNVERIFIED"
    # Subjective and interpretive modalities are unaffected by source_status
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
    fact["truth_status"] = pipeline._truth_status_for(fact["claim_type"], fact.get("source_status"))

    assert fact["truth_status"] == "SUBJECTIVE"   # valid feeling…
    assert fact["claim_type"] != "WORLD_FACT"     # …but not a fact about the world


# ─── generate_answer fallback ─────────────────────────────────────────────────

def test_generate_answer_blocks_when_nothing_validated():
    """Issue #64: no Validated/Supported facts → insufficient grounding → block.
    A verifiable memory system must not answer from unvalidated material."""
    from core.pipeline import generate_answer
    pack = {"facts": [{"fact_id": "a", "claim": "raw", "source": "s",
                       "epistemic_state": "Observed"}]}
    out = generate_answer(pack, trace=[])
    assert out["answer"] is None
    assert out.get("error") is not None
    assert "grounding" in out["error"]
    assert out["total_facts"] == 0


# ─── CanonicalView strict grounding (core/canonical_view.py) ──────────────────

def _pack(*facts):
    return {"facts": list(facts), "query": "q", "total": len(facts)}


def test_generate_answer_blocks_on_user_claimed_facts_only():
    """A USER_CLAIMED WORLD_FACT reaching epistemic_state Validated must NOT
    ground a confident answer — the exact trust-boundary gap this PR closes.
    High confidence and epistemic_state=Validated must not change the result."""
    from core.pipeline import generate_answer
    pack = _pack({
        "fact_id": "u1", "claim": "My cat is the smartest animal alive",
        "source": "user", "claim_type": "WORLD_FACT",
        "source_status": "USER_REPORTED", "truth_status": "USER_CLAIMED",
        "epistemic_state": "Validated", "confidence": 1.0, "restricted": False,
    })
    out = generate_answer(pack, trace=[])
    assert out["answer"] is None
    assert "strict-canonical" in out["error"] or "VERIFIED" in out["error"]
    assert out["total_facts"] == 0
    assert out["facts"] == []


def test_generate_answer_grounds_only_the_verified_fact_from_a_mixed_pack():
    """Mixed candidate set: VERIFIED, USER_CLAIMED, Contradicted, restricted —
    only the VERIFIED, unrestricted, non-contradicted fact grounds the answer."""
    from core.pipeline import generate_answer
    verified = {
        "fact_id": "v1", "claim": "Verified claim", "source": "src",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "truth_status": "VERIFIED", "epistemic_state": "Validated",
        "confidence": 0.9, "restricted": False,
    }
    user_claimed = {**verified, "fact_id": "u1", "claim": "User claim",
                    "source_status": "USER_REPORTED", "truth_status": "USER_CLAIMED"}
    contradicted = {**verified, "fact_id": "c1", "epistemic_state": "Contradicted"}
    restricted = {**verified, "fact_id": "r1", "restricted": True}

    out = generate_answer(
        _pack(verified, user_claimed, contradicted, restricted), trace=[])

    assert out["answer"] is not None
    assert out["total_facts"] == 1
    assert [f["fact_id"] for f in out["facts"]] == ["v1"]


def test_run_refuses_when_retrieval_surfaces_only_user_claimed_material(monkeypatch):
    """End-to-end refusal (Test 6): when retrieve() finds only user-claimed /
    otherwise non-canonical material, run() must refuse (existing
    insufficient-evidence behavior), never hallucinate an answer from the
    excluded claims."""
    from core import pipeline
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [{
        "id": "u1", "text": "My cat is the smartest animal alive",
        "source": "user", "confidence": 1.0, "claim_type": "WORLD_FACT",
        "source_status": "USER_REPORTED", "significance": 0.5,
        "_score": 0.9, "epistemic_state": "Observed", "origin": "retrieval",
    }])
    result = pipeline.run("smartest animal")
    assert result["answer"] is None
    assert "insufficient grounding" in (result.get("error") or "")


def test_run_end_to_end_verified_grounding_trace_and_receipt_unaffected():
    """Regression pin (Test 9): a genuinely VERIFIED fact's trace, receipt and
    evidence-span behavior must be unchanged by CanonicalView strict grounding."""
    from core.ingest import ingest
    from core.pipeline import run
    from core import evidence, provenance

    fid = ingest("Argon is a noble gas",
                 source_status="EXTERNAL")["fact"]["fact_id"]
    evidence.attach_evidence(fid, "chem.md", source_kind="file")

    result = run("is argon a noble gas")
    assert result["answer"] is not None
    assert result["total_facts"] >= 1
    assert result["trace"]
    assert all(f["truth_status"] == "VERIFIED" for f in result["facts"])

    receipt = provenance.build_receipt(result)
    verified = provenance.verify_receipt(receipt, strict_provenance=True)
    assert verified["verified"] is True


# ─── Blocker 1 (#257 review): preserve authoritative L3 truth metadata ────────
# _from_node() must not fail-open default missing trust fields, and run()'s
# ESM-promotion loop must never recompute/overwrite an already-persisted L3
# verdict on ordinary recall (only on a genuinely new admission).

def _seed_l1_and_l3(fact_id, *, epistemic_state="Validated",
                    claim_type="WORLD_FACT", source_status="EXTERNAL",
                    confidence=0.9, l3_node=None):
    """Directly seed L1 (SQLite) + L3 (graph) as an already-canonical fact,
    bypassing ingest()/run()'s own admission — lets a test control exactly
    what the L3 node's persisted truth_status is (including a malformed/
    missing one) independent of what the pipeline would normally compute."""
    from core.memory import store_fact
    from core.l3_graph import get_l3_graph
    claim = f"claim text for {fact_id}"
    store_fact({
        "fact_id": fact_id, "claim": claim, "source": "seed",
        "confidence": confidence, "epistemic_state": epistemic_state,
        "claim_type": claim_type, "source_status": source_status,
        "significance": 0.5,
    })
    node = {"fact_id": fact_id, "claim": claim, "source": "seed",
            "confidence": confidence, "epistemic_state": epistemic_state,
            "claim_type": claim_type, "source_status": source_status}
    if l3_node:
        node.update(l3_node)
    get_l3_graph().merge_fact(node)
    return claim


def _retrieved_item(fact_id, claim, epistemic_state="Validated", **overrides):
    """A retrieve()-shaped item for the given already-seeded fact_id, as
    _from_node() would build it (used with a monkeypatched retrieve() to
    isolate run()'s own recall-vs-new-admission handling from real vector
    search/embedding mechanics)."""
    item = {
        "id": fact_id, "text": claim, "source": "seed", "confidence": 0.9,
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "significance": 0.5, "_score": 0.9, "epistemic_state": epistemic_state,
        "origin": "memory",
    }
    item.update(overrides)
    return item


def test_persisted_user_claimed_truth_status_survives_recall_never_becomes_verified(monkeypatch):
    from core import pipeline
    from core.l3_graph import get_l3_graph
    fid = "recall-user-claimed"
    claim = _seed_l1_and_l3(fid, source_status="USER_REPORTED",
                           l3_node={"truth_status": "USER_CLAIMED"})
    monkeypatch.setattr(pipeline, "retrieve",
                       lambda q, k=3: [_retrieved_item(fid, claim)])

    result = pipeline.run("q")

    assert get_l3_graph().get_fact(fid)["truth_status"] == "USER_CLAIMED"
    assert result["answer"] is None
    assert "insufficient grounding" in (result.get("error") or "")


def test_persisted_curator_override_truth_status_survives_recall_never_becomes_verified(monkeypatch):
    from core import pipeline
    from core.l3_graph import get_l3_graph
    fid = "recall-curator-override"
    claim = _seed_l1_and_l3(fid, l3_node={"truth_status": "CURATOR_OVERRIDE"})
    monkeypatch.setattr(pipeline, "retrieve",
                       lambda q, k=3: [_retrieved_item(fid, claim)])

    result = pipeline.run("q")

    assert get_l3_graph().get_fact(fid)["truth_status"] == "CURATOR_OVERRIDE"
    assert result["answer"] is None
    assert "insufficient grounding" in (result.get("error") or "")


def test_recall_of_l3_node_missing_truth_status_fails_closed_not_backfilled(monkeypatch):
    """A malformed/legacy L3 node that is already Validated but was NEVER
    assigned a truth_status must not have one invented for it on recall."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    fid = "recall-missing-truth-status"
    claim = _seed_l1_and_l3(fid)  # l3_node has no truth_status key at all
    monkeypatch.setattr(pipeline, "retrieve",
                       lambda q, k=3: [_retrieved_item(fid, claim)])

    result = pipeline.run("q")

    assert get_l3_graph().get_fact(fid).get("truth_status") is None
    assert result["answer"] is None
    assert "insufficient grounding" in (result.get("error") or "")


def test_recall_of_l3_node_with_unknown_truth_status_fails_closed(monkeypatch):
    from core import pipeline
    from core.l3_graph import get_l3_graph
    fid = "recall-unknown-truth-status"
    claim = _seed_l1_and_l3(fid, l3_node={"truth_status": "PROBABLY_TRUE"})
    monkeypatch.setattr(pipeline, "retrieve",
                       lambda q, k=3: [_retrieved_item(fid, claim)])

    result = pipeline.run("q")

    assert get_l3_graph().get_fact(fid)["truth_status"] == "PROBABLY_TRUE"  # untouched
    assert result["answer"] is None


def test_persisted_verified_fact_continues_to_answer_across_recall(monkeypatch):
    """Regression: a genuinely VERIFIED fact's verdict must also survive
    recall unchanged (not just the negative cases above)."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    fid = "recall-verified"
    claim = _seed_l1_and_l3(fid, l3_node={"truth_status": "VERIFIED"})
    monkeypatch.setattr(pipeline, "retrieve",
                       lambda q, k=3: [_retrieved_item(fid, claim)])

    result = pipeline.run("q")

    assert get_l3_graph().get_fact(fid)["truth_status"] == "VERIFIED"
    assert result["answer"] is not None
    assert [f["fact_id"] for f in result["facts"]] == [fid]


def test_retrieve_defaults_missing_epistemic_state_to_observed_not_validated():
    """_from_node() must not fail-open default a missing epistemic_state to
    'Validated' — a malformed/legacy L3 node must not be treated as
    already-canonical."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    get_l3_graph().merge_fact({
        "fact_id": "malformed-no-esm",
        "claim": "malformed node missing epistemic state entirely",
        "source": "s", "confidence": 0.9,
    })  # no epistemic_state key at all
    hits = {h["id"]: h for h in retrieve("malformed node missing epistemic state entirely")}
    assert hits["malformed-no-esm"]["epistemic_state"] == "Observed"


def test_retrieve_defaults_missing_source_status_to_unknown_not_derived():
    """_from_node() must not fail-open default a missing source_status to
    'DERIVED' (a privileged, verification-implying value)."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    get_l3_graph().merge_fact({
        "fact_id": "malformed-no-ss",
        "claim": "malformed node missing source status field entirely",
        "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
    })  # no source_status key at all
    hits = {h["id"]: h for h in retrieve("malformed node missing source status field entirely")}
    assert hits["malformed-no-ss"]["source_status"] == "UNKNOWN"


def test_retrieve_propagates_persisted_truth_status_from_l3_node():
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    get_l3_graph().merge_fact({
        "fact_id": "persisted-curator-override",
        "claim": "a curator overridden claim about widgets and gadgets",
        "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
        "truth_status": "CURATOR_OVERRIDE",
    })
    hits = {h["id"]: h for h in retrieve("a curator overridden claim about widgets and gadgets")}
    assert hits["persisted-curator-override"]["truth_status"] == "CURATOR_OVERRIDE"


def test_retrieve_missing_truth_status_on_l3_node_surfaces_as_none():
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    get_l3_graph().merge_fact({
        "fact_id": "no-truth-status",
        "claim": "a node with absolutely no truth status field present",
        "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
    })
    hits = {h["id"]: h for h in retrieve("a node with absolutely no truth status field present")}
    assert hits["no-truth-status"]["truth_status"] is None


def test_new_admission_with_missing_source_status_stays_unverified_not_verified(monkeypatch):
    """A genuinely new candidate (no existing L3 node for this fact_id — see
    test_genuinely_new_candidate_still_follows_truth_gate_admission_path for
    the physical-presence check this relies on) missing source_status, and
    promoted this round via the normal admission path, must compute
    truth_status=UNVERIFIED (the safe UNKNOWN default), never VERIFIED (the
    old fail-open DERIVED default) and must not crash."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    assert g.get_fact("pending-no-ss") is None  # genuinely new to L3
    item = {
        "id": "pending-no-ss",
        "text": "a pending world fact missing source status entirely",
        "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
        "significance": 0.5, "_score": 0.9, "epistemic_state": "Observed",
        "origin": "memory",
    }  # no source_status key at all
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is None
    node = g.get_fact("pending-no-ss")
    assert node["epistemic_state"] == "Validated"   # promoted this round (new admission)
    assert node["truth_status"] == "UNVERIFIED"     # never silently VERIFIED


# ─── Blocker 3 (#257 review): facts/trace/metrics consistency ─────────────────

def test_run_trace_contains_only_grounded_fact_ids_from_a_mixed_recall(monkeypatch):
    """set(result.facts.fact_id) == set(result.trace.fact_id) for a successful
    strict answer, even when retrieve() surfaces additional non-canonical
    candidates alongside the grounding fact."""
    from core import pipeline
    verified_fid = "mixed-verified"
    user_claimed_fid = "mixed-user-claimed"
    v_claim = _seed_l1_and_l3(verified_fid, l3_node={"truth_status": "VERIFIED"})
    u_claim = _seed_l1_and_l3(user_claimed_fid, source_status="USER_REPORTED",
                             l3_node={"truth_status": "USER_CLAIMED"})
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [
        _retrieved_item(verified_fid, v_claim),
        _retrieved_item(user_claimed_fid, u_claim),
    ])

    result = pipeline.run("q")

    assert result["answer"] is not None
    fact_ids = {f["fact_id"] for f in result["facts"]}
    trace_ids = {t["fact_id"] for t in result["trace"]}
    assert fact_ids == trace_ids == {verified_fid}


def test_strict_refusal_does_not_increment_query_answered_or_record_success(monkeypatch):
    from core import pipeline, metrics, adaptation
    metrics.reset()
    calls = {"success": 0, "block": 0}
    monkeypatch.setattr(adaptation, "record_success", lambda: calls.__setitem__("success", calls["success"] + 1))
    monkeypatch.setattr(adaptation, "record_block", lambda: calls.__setitem__("block", calls["block"] + 1))
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [{
        "id": "u1", "text": "My cat is the smartest animal alive",
        "source": "user", "confidence": 1.0, "claim_type": "WORLD_FACT",
        "source_status": "USER_REPORTED", "significance": 0.5,
        "_score": 0.9, "epistemic_state": "Observed", "origin": "retrieval",
    }])

    result = pipeline.run("smartest animal")

    assert result["answer"] is None
    assert metrics.value("query.answered") == 0
    assert metrics.value("query.blocked") == 1
    assert calls["success"] == 0
    assert calls["block"] == 1


def test_successful_verified_answer_still_records_success_and_answered_metrics(monkeypatch):
    from core import pipeline, metrics, adaptation
    from core.ingest import ingest
    ingest("Xenon is a noble gas", source_status="EXTERNAL")  # setup, before spying

    metrics.reset()
    calls = {"success": 0, "block": 0}
    monkeypatch.setattr(adaptation, "record_success", lambda: calls.__setitem__("success", calls["success"] + 1))
    monkeypatch.setattr(adaptation, "record_block", lambda: calls.__setitem__("block", calls["block"] + 1))

    result = pipeline.run("is xenon a noble gas")

    assert result["answer"] is not None
    assert metrics.value("query.answered") == 1
    assert metrics.value("query.blocked") == 0
    assert calls["success"] == 1
    assert calls["block"] == 0


# ─── Blocker 1 round 3 (#257 review): admission decision keys off physical ────
# L3 presence, not ESM state. An L3 node that already exists — legitimately
# pending, or with a missing/malformed epistemic_state on a corrupted/legacy
# record — is an ordinary recall, never a new admission, regardless of what
# epistemic_state the retrieved item/L1 row shows.

def test_existing_l3_node_user_claimed_external_missing_esm_refused_and_unchanged(monkeypatch):
    """Blocker 1 test 1: an existing L3 node with truth_status=USER_CLAIMED,
    source_status=EXTERNAL, and a MISSING epistemic_state must be treated as
    an ordinary recall (not a new admission) — run() must refuse and leave
    the node completely unchanged. This is the exact exploit path from the
    review: a missing epistemic_state used to make _from_node() default to
    "Observed", which made run() (wrongly, keying off ESM state) treat this
    as a new admission, transition it to Validated, and recompute
    truth_status=VERIFIED from source_status=EXTERNAL — silently overwriting
    the real USER_CLAIMED verdict."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "exploit-user-claimed-external"
    claim = "an exploit scenario claim about widgets and gizmos"
    g.merge_fact({"fact_id": fid, "claim": claim, "source": "s", "confidence": 0.9,
                 "source_status": "EXTERNAL", "truth_status": "USER_CLAIMED"})
    # no epistemic_state key at all on the L3 node
    before = dict(g.get_fact(fid))

    item = {"id": fid, "text": claim, "source": "s", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
            "significance": 0.5, "_score": 0.9, "epistemic_state": "Observed",
            "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is None
    assert "insufficient grounding" in (result.get("error") or "")
    assert g.get_fact(fid) == before  # completely unchanged


def test_existing_l3_node_curator_override_supported_remains_unchanged_and_excluded(monkeypatch):
    """Blocker 1 test 2: an existing L3 node with truth_status=CURATOR_OVERRIDE,
    epistemic_state=Supported must remain exactly that and be excluded from
    strict grounding — never auto-promoted or recomputed."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "exploit-curator-override-supported"
    claim = "an exploit scenario claim about gadgets and thingamajigs"
    g.merge_fact({"fact_id": fid, "claim": claim, "source": "s", "confidence": 0.9,
                 "epistemic_state": "Supported", "truth_status": "CURATOR_OVERRIDE"})
    before = dict(g.get_fact(fid))

    item = {"id": fid, "text": claim, "source": "s", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
            "significance": 0.5, "_score": 0.9, "epistemic_state": "Supported",
            "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is None
    after = g.get_fact(fid)
    assert after == before
    assert after["truth_status"] == "CURATOR_OVERRIDE"
    assert after["epistemic_state"] == "Supported"


def test_existing_l3_node_verified_observed_fails_closed_not_promoted(monkeypatch):
    """Blocker 1 test 3: an existing L3 node with truth_status=VERIFIED,
    epistemic_state=Observed must fail closed (Observed is pre-canonical, not
    in the strict ESM allowlist) and must NOT be promoted to Validated merely
    by a query touching it."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "exploit-verified-observed"
    claim = "an exploit scenario claim about doohickeys and contraptions"
    g.merge_fact({"fact_id": fid, "claim": claim, "source": "s", "confidence": 0.9,
                 "epistemic_state": "Observed", "truth_status": "VERIFIED"})

    item = {"id": fid, "text": claim, "source": "s", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
            "significance": 0.5, "_score": 0.9, "epistemic_state": "Observed",
            "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is None
    after = g.get_fact(fid)
    assert after["epistemic_state"] == "Observed"   # never auto-promoted
    assert after["truth_status"] == "VERIFIED"       # untouched


def test_genuinely_new_candidate_still_follows_truth_gate_admission_path(monkeypatch):
    """Blocker 1 test 4: a fact_id with NO existing L3 node is a genuinely new
    admission and must still follow the normal ESM-transition +
    _truth_status_for() path."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "genuinely-new-candidate"
    assert g.get_fact(fid) is None
    item = {"id": fid, "text": "a genuinely new claim about sprockets and cogs",
            "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL", "significance": 0.5, "_score": 0.9,
            "epistemic_state": "Observed", "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is not None
    after = g.get_fact(fid)
    assert after["epistemic_state"] == "Validated"
    assert after["truth_status"] == "VERIFIED"


def test_new_admission_with_non_promotable_state_is_skipped_not_merged(monkeypatch):
    """A fact_id genuinely new to L3 (never merged) but arriving with a
    non-promotable epistemic_state (e.g. Collapsed) must be skipped, not
    force-promoted or merged — the pre-existing terminal-state guard, now
    reachable only via the genuinely-new-admission branch (#257 review round
    3: an L3-existing fact takes the "not new admission" branch and never
    reaches this check at all)."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "new-but-collapsed"
    assert g.get_fact(fid) is None
    item = {"id": fid, "text": "a fact that arrives already collapsed and new to l3",
            "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL", "significance": 0.5, "_score": 0.9,
            "epistemic_state": "Collapsed", "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is None
    assert g.get_fact(fid) is None  # never merged


def test_l1_validated_l3_missing_outbox_recovery_self_heals_correctly(monkeypatch):
    """Blocker 1 test 5: a fact already Validated in L1 but missing from L3
    (simulating a prior merge failure) must still be recognized as a
    genuinely new L3 admission (no existing node to preserve) and self-heal
    with a freshly computed truth_status — the outbox-recovery path must
    keep working, not be mistaken for "not a new admission"."""
    from core import pipeline
    from core.memory import store_fact
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "outbox-recovery-candidate"
    claim = "an outbox recovery claim about widgets that never reached L3"
    store_fact({"fact_id": fid, "claim": claim, "source": "s", "confidence": 0.9,
               "epistemic_state": "Validated", "claim_type": "WORLD_FACT",
               "source_status": "EXTERNAL", "significance": 0.5})
    assert g.get_fact(fid) is None  # L3 merge never happened (simulated failure)

    item = {"id": fid, "text": claim, "source": "s", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
            "significance": 0.5, "_score": 0.9, "epistemic_state": "Validated",
            "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is not None
    after = g.get_fact(fid)
    assert after is not None            # self-healed: now merged
    assert after["truth_status"] == "VERIFIED"


# ─── Blocker 2 (#257 review round 3): no synthesized provenance/confidence ────

def test_verified_validated_l3_node_missing_source_blocks_via_guardian():
    from core.pipeline import run
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    claim = "a verified claim missing its source field entirely for guardian"
    g.merge_fact({"fact_id": "missing-source-verified", "claim": claim,
                 "confidence": 0.9, "epistemic_state": "Validated",
                 "truth_status": "VERIFIED"})  # no "source" key at all

    result = run(claim)

    assert result["answer"] is None
    assert "Guardian" in (result.get("error") or "")


def test_verified_validated_l3_node_missing_confidence_blocks_via_guardian():
    from core.pipeline import run
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    claim = "a verified claim missing its confidence field entirely for guardian"
    g.merge_fact({"fact_id": "missing-confidence-verified", "claim": claim,
                 "source": "s", "epistemic_state": "Validated",
                 "truth_status": "VERIFIED"})  # no "confidence" key at all

    result = run(claim)

    assert result["answer"] is None
    assert "Guardian" in (result.get("error") or "")


def test_malformed_source_and_confidence_types_fail_closed_without_crashing():
    from core.pipeline import run
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    claim = "a claim with malformed source and confidence types for guardian"
    g.merge_fact({"fact_id": "malformed-types", "claim": claim,
                 "source": ["not", "a", "string"], "confidence": "not-a-number",
                 "epistemic_state": "Validated", "truth_status": "VERIFIED"})

    result = run(claim)  # must not raise

    assert result["answer"] is None
    assert "Guardian" in (result.get("error") or "")


def test_valid_persisted_source_and_confidence_remain_unaffected():
    from core.pipeline import run
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    claim = "a fully valid verified claim about properly sourced widgets"
    g.merge_fact({"fact_id": "valid-verified", "claim": claim,
                 "source": "trusted-source", "confidence": 0.95,
                 "epistemic_state": "Validated", "truth_status": "VERIFIED"})

    result = run(claim)

    assert result["answer"] is not None
    assert result["facts"][0]["source"] == "trusted-source"
    assert result["facts"][0]["confidence"] == pytest.approx(0.95)


# ─── Trace metadata consistency (#257 review round 3) ─────────────────────────

def test_trace_epistemic_state_matches_fact_epistemic_state_for_successful_answer(monkeypatch):
    """For a successful strict answer, every trace element's epistemic_state
    must match its corresponding fact's REAL epistemic_state — run()'s
    blanket promote_trace(trace, "Validated") call must not survive into the
    final trace for a fact whose actual state is something else (here:
    ImmutableCore)."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    fid = "immutable-core-grounding-fact"
    claim = "an immutable core grounding fact about ring zero values"
    g.merge_fact({"fact_id": fid, "claim": claim, "source": "s",
                 "confidence": 0.9, "epistemic_state": "ImmutableCore",
                 "truth_status": "VERIFIED"})

    item = {"id": fid, "text": claim, "source": "s", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
            "significance": 0.5, "_score": 0.9, "epistemic_state": "ImmutableCore",
            "origin": "memory"}
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: [item])

    result = pipeline.run("q")

    assert result["answer"] is not None
    assert [f["fact_id"] for f in result["facts"]] == [fid]
    assert [t["fact_id"] for t in result["trace"]] == [fid]
    assert result["facts"][0]["epistemic_state"] == "ImmutableCore"
    assert result["trace"][0]["epistemic_state"] == "ImmutableCore"


# ─── demo seed opt-in (issue #65) ─────────────────────────────────────────────

def test_production_default_has_no_seed_corpus(monkeypatch):
    """Issue #65: without VELANTRIM_DEMO_SEED=1 the retrieval corpus is empty.
    All facts must enter through ingest(); the production pipeline is clean."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.pipeline import _load_demo_seed
    assert _load_demo_seed() == []


def test_demo_seed_enabled_returns_five_facts(monkeypatch):
    """With VELANTRIM_DEMO_SEED=1 the seed corpus returns the curated facts."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "1")
    from core.pipeline import _load_demo_seed
    facts = _load_demo_seed()
    assert len(facts) == 5
    assert all(f.get("source_status") == "EXTERNAL" for f in facts)


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


def test_pipeline_skips_l3_merge_on_cas_miss(monkeypatch):
    """If transition_esm reports a CAS miss during promotion, the pipeline skips
    merging that fact into the canon (no stale promotion) instead of continuing to
    a success merge. Defense-in-depth, not a full atomicity guarantee."""
    from core import pipeline
    monkeypatch.setattr(pipeline, "transition_esm", lambda *a, **k: False)
    result = pipeline.run("DNA")
    # The run completes without crashing; any fact that hit the CAS miss was
    # skipped before its truth_status was set / before the L3 merge.
    assert isinstance(result, dict)
    assert "answer" in result
    for f in result.get("facts", []):
        if f.get("epistemic_state") != "Validated":
            assert "truth_status" not in f
