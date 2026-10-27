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
    merge must surface as a blocked result, not a raw traceback â€” and the
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
    # graph never received the nodeâ€¦
    assert graph.all_facts() == []
    # â€¦but the SQLite-side ESM transition already happened (acceptable, idempotent).
    assert get_fact("f2")["epistemic_state"] == "Validated"


def test_blocked_pipeline_does_not_write_to_l3_graph():
    """A fact that never passes TruthGate must not appear in canonical L3."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    pipeline.run("zxqvbnmqwerty")  # empty retrieval â†’ blocked before promotion
    assert get_l3_graph().all_facts() == []


# â”€â”€â”€ L3 outbox (self-healing partial state) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_l3_outbox_self_heals_failed_merge(monkeypatch):
    """A failed L3 merge queues the fact; draining the outbox after the backend
    recovers lands the node in the canon â€” no manual re-run of the same query."""
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
    """Outbox is for post-gate Validated merges only â€” Observed entries are dropped."""
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


# â”€â”€â”€ episodic binding â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _two_retrieved():
    # source_status=EXTERNAL/claim_type=WORLD_FACT (#257 corrective hardening):
    # episodic linking now only happens after a successful strict-grounded
    # answer, so these fixture facts must actually be admissible as VERIFIED,
    # not just merely present.
    return [
        {"id": "f2", "text": "Quantum entanglement links particles",
         "source": "physics", "confidence": 0.85, "_score": 0.6,
         "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
         "epistemic_state": "Observed", "origin": "retrieval"},
        {"id": "f5", "text": "DNA encodes genetic information",
         "source": "biology", "confidence": 0.99, "_score": 0.5,
         "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
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
    assert pipeline.recall_by_entity() == []   # no criterion â†’ nothing


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
    assert "who" not in edge[3]                        # no context â†’ no who/where


# â”€â”€â”€ Episodic-write contract (#257 corrective hardening, independent finding) â”€â”€
# Compatibility change: implicit co-recall graph linking is removed. Only an
# explicit `episode` argument, on a query whose answer actually grounds, may
# create episodic graph mutations (CO_OCCURRED edges, entity nodes/MENTIONS).

def test_implicit_co_recall_without_episode_creates_no_edges(monkeypatch):
    """Two fully strict-canonical, co-recalled facts with NO explicit episode
    must not create any CO_OCCURRED edge â€” implicit co-recall linking is
    removed."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())
    result = pipeline.run("two facts, no episode")

    assert result["answer"] is not None
    assert get_l3_graph()._edges == []


def test_blocked_query_with_explicit_episode_creates_no_edges(monkeypatch):
    """An explicit episode on a query that ultimately refuses (no
    strict-canonical facts) must not write any episodic edge."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    non_canonical = [
        {"id": "nc1", "text": "a user-claimed fact one",
         "source": "user", "confidence": 0.9, "_score": 0.6,
         "claim_type": "WORLD_FACT", "source_status": "USER_REPORTED",
         "epistemic_state": "Observed", "origin": "retrieval"},
        {"id": "nc2", "text": "a user-claimed fact two",
         "source": "user", "confidence": 0.9, "_score": 0.5,
         "claim_type": "WORLD_FACT", "source_status": "USER_REPORTED",
         "epistemic_state": "Observed", "origin": "retrieval"},
    ]
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: non_canonical)
    result = pipeline.run("blocked query", episode={"who": ["alice"], "where": "lab"})

    assert result["answer"] is None
    assert get_l3_graph()._edges == []
    assert get_l3_graph()._mentions == []


def test_explicit_episode_with_only_restricted_facts_creates_no_edges(monkeypatch):
    """Restricted facts are excluded from strict grounding; if that leaves
    nothing to ground, an explicit episode must still not write anything."""
    from core import pipeline
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    for fid in ("restricted-a", "restricted-b"):
        g.merge_fact({"fact_id": fid, "claim": f"a restricted claim {fid}",
                     "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
                     "source_status": "EXTERNAL", "epistemic_state": "Validated",
                     "truth_status": "VERIFIED", "restricted": True})

    items = [
        {"id": "restricted-a", "text": "a restricted claim restricted-a",
         "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
         "source_status": "EXTERNAL", "significance": 0.5, "_score": 0.9,
         "epistemic_state": "Validated", "origin": "memory"},
        {"id": "restricted-b", "text": "a restricted claim restricted-b",
         "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
         "source_status": "EXTERNAL", "significance": 0.5, "_score": 0.8,
         "epistemic_state": "Validated", "origin": "memory"},
    ]
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: items)
    result = pipeline.run("q", episode={"who": ["alice"]})

    assert result["answer"] is None
    assert get_l3_graph()._edges == []


def test_explicit_episode_with_mixed_facts_links_only_canonical(monkeypatch):
    """When only some retrieved facts ground the answer, episodic linking
    (edges and entity mentions) must cover only the used canonical facts, not
    the excluded non-canonical one."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    items = [
        {"id": "canon-a", "text": "a verified canonical claim a",
         "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
         "source_status": "EXTERNAL", "_score": 0.9,
         "epistemic_state": "Observed", "origin": "retrieval"},
        {"id": "canon-b", "text": "a verified canonical claim b",
         "source": "s", "confidence": 0.9, "claim_type": "WORLD_FACT",
         "source_status": "EXTERNAL", "_score": 0.8,
         "epistemic_state": "Observed", "origin": "retrieval"},
        {"id": "non-canon-c", "text": "a user-claimed non-canonical claim c",
         "source": "user", "confidence": 0.9, "claim_type": "WORLD_FACT",
         "source_status": "USER_REPORTED", "_score": 0.7,
         "epistemic_state": "Observed", "origin": "retrieval"},
    ]
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: items)
    result = pipeline.run("mixed facts", episode={"who": ["bob"]})

    assert result["answer"] is not None
    assert {f["fact_id"] for f in result["facts"]} == {"canon-a", "canon-b"}

    g = get_l3_graph()
    edge_pairs = {(e[0], e[2]) for e in g._edges}
    assert ("canon-a", "canon-b") in edge_pairs or ("canon-b", "canon-a") in edge_pairs
    for src, _, dst in [(e[0], e[1], e[2]) for e in g._edges]:
        assert "non-canon-c" not in (src, dst)
    mentioned_facts = {fid for fid, _eid, _rel in g._mentions}
    assert "non-canon-c" not in mentioned_facts
    assert {"canon-a", "canon-b"} <= mentioned_facts


def test_explicit_episode_success_links_once(monkeypatch):
    """A successful strict-grounded answer with an explicit episode must
    create exactly the expected CO_OCCURRED pair, not zero and not more than
    once."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())
    result = pipeline.run("two facts", episode={"who": ["carol"], "where": "office",
                                                 "when": "2026-07-11T10:00:00"})

    assert result["answer"] is not None
    g = get_l3_graph()
    co_occurred_edges = [e for e in g._edges if e[1] == "CO_OCCURRED"]
    assert len(co_occurred_edges) == 2  # undirected pair: f2->f5 and f5->f2


def test_repeated_identical_explicit_episode_creates_no_duplicate_edges(monkeypatch):
    """Calling run() twice with the SAME explicit episode context (including
    an explicit `when`) for the same facts must not create duplicate edges â€”
    add_edge is an idempotent MERGE keyed on (src, rel_type, dst, props)."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())
    episode = {"who": ["dave"], "where": "kitchen", "when": "2026-07-11T09:00:00"}

    pipeline.run("two facts", episode=dict(episode))
    pipeline.run("two facts", episode=dict(episode))

    g = get_l3_graph()
    co_occurred_edges = [e for e in g._edges if e[1] == "CO_OCCURRED"]
    assert len(co_occurred_edges) == 2  # not 4 â€” the repeat is not a duplicate


def test_episode_link_failure_after_grounded_answer_is_safe_and_observable(monkeypatch):
    """A backend failure while writing episodic links must not turn a
    correct, already-grounded answer into a failure, must not raise out of
    run(), and must be observable via a metric."""
    from core import pipeline
    from core import metrics

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _two_retrieved())

    def _boom(*a, **k):
        raise RuntimeError("simulated episodic backend failure")
    monkeypatch.setattr(pipeline, "_link_episode", _boom)

    before = metrics.value("episode_link.failed")
    result = pipeline.run("two facts", episode={"who": ["erin"]})  # must not raise

    assert result["answer"] is not None
    assert metrics.value("episode_link.failed") == before + 1


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


# â”€â”€â”€ helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_retrieve_respects_k_and_skips_non_matches():
    from core.pipeline import retrieve
    hits = retrieve("the", k=2)               # pure stopword query â†’ nothing
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
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
                  "restricted": False})
    g.merge_fact({"fact_id": "B", "claim": "chlorophyll molecule structure",
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
                  "restricted": False})
    g.add_edge("A", "CO_OCCURRED", "B", {})

    hits = {h["id"]: h for h in retrieve("sunlight energy")}
    assert hits["A"]["origin"] == "memory"        # direct vector hit
    assert hits["B"]["origin"] == "graph"         # pulled in via the edge
    assert hits["B"]["_score"] < hits["A"]["_score"]   # decayed by distance


def test_graph_walk_is_multi_hop_with_decay():
    """Activation spreads multiple hops, decaying each hop: Aâ†’Bâ†’C from a query
    that only matches A. C (2 hops out) ranks below B (1 hop) below A."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    for fid, claim in [("A", "sunlight energy"), ("B", "leaf cells"),
                       ("C", "soil minerals")]:
        g.merge_fact({"fact_id": fid, "claim": claim, "source": "s",
                      "confidence": 1.0, "epistemic_state": "Validated",
                      "restricted": False})
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
                      "confidence": 1.0, "epistemic_state": "Validated",
                      "restricted": False})
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
                  "confidence": 0.9, "epistemic_state": "Validated",
                  "restricted": False})
    g.merge_fact({"fact_id": "old", "claim": "outdated note", "source": "s",
                  "confidence": 0.9, "epistemic_state": "Deprecated"})
    g.add_edge("A", "SUPERSEDED_BY", "old", {})

    ids = {h["id"] for h in retrieve("sunlight energy")}
    assert "A" in ids and "old" not in ids        # stale neighbor not recalled


def test_graph_walk_does_not_propagate_through_truth_maintenance_edges():
    """Edge-type weighting: relevance spreads along an episodic CO_OCCURRED edge
    but NOT along a CONTRADICTS edge â€” even to a Validated node. A fact isn't
    'more relevant' because the vector hit contradicts it."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    for fid, claim in [("A", "sunlight energy"), ("assoc", "leaf cells"),
                       ("rival", "moonlight myth")]:
        g.merge_fact({"fact_id": fid, "claim": claim, "source": "s",
                      "confidence": 1.0, "epistemic_state": "Validated",
                      "restricted": False})
    g.add_edge("A", "CO_OCCURRED", "assoc", {})   # association â†’ propagates
    g.add_edge("A", "CONTRADICTS", "rival", {})   # truth-maintenance â†’ does not

    ids = {h["id"] for h in retrieve("sunlight energy", k=5)}
    assert "A" in ids                              # direct vector hit
    assert "assoc" in ids                          # pulled in by association
    assert "rival" not in ids                      # contradiction does not spread


def test_graph_walk_does_not_propagate_to_node_stale_validated_in_l3_but_terminal_in_l1():
    """retrieve()'s graph-walk runs BEFORE run()'s later
    _reconcile_recalled_fact() ever executes, so a node whose L3 copy still
    reads epistemic_state='Validated' (stale) while its L1 record has
    already gone terminal (Collapsed/Contradicted/Deprecated) must not
    receive or pass on spreading-activation credit â€” the walk must consult
    L1 itself for terminal-state resurrection, not trust only the L3 node's
    own possibly-stale epistemic_state (#257 independent-review round)."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    g.merge_fact({"fact_id": "seed", "claim": "sunlight energy seed",
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
                  "restricted": False})
    _seed_l1_and_l3("stale-terminal", epistemic_state="Collapsed",
                     l3_node={"epistemic_state": "Validated", "restricted": False})
    g.add_edge("seed", "CO_OCCURRED", "stale-terminal", {})

    ids = {h["id"] for h in retrieve("sunlight energy seed", k=5)}
    assert "seed" in ids
    assert "stale-terminal" not in ids


def test_graph_walk_skips_confirmed_restricted_target():
    """A graph-walk target node whose `restricted` field is a CONFIRMED True
    must not receive or pass on activation (#257 independent-review round)."""
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    g.merge_fact({"fact_id": "seed2", "claim": "moonlight tide pattern",
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
                  "restricted": False})
    g.merge_fact({"fact_id": "confirmed-restricted", "claim": "tide chart neighbor",
                  "source": "s", "confidence": 0.9, "epistemic_state": "Validated",
                  "restricted": True})
    g.add_edge("seed2", "CO_OCCURRED", "confirmed-restricted", {})

    ids = {h["id"] for h in retrieve("moonlight tide pattern", k=5)}
    assert "seed2" in ids
    assert "confirmed-restricted" not in ids


def test_graph_walk_propagates_to_target_with_unknown_restricted_bit_and_no_l1_record():
    """A graph-walk target node whose `restricted` field is merely UNKNOWN
    (missing/malformed, e.g. an L3 backend like LadybugL3Graph that never
    persists this column at all) AND has no L1 record either must still be
    allowed to propagate â€” treating that structural absence as a confirmed
    restriction would make every such node permanently unreachable on a
    backend that simply cannot express this field. L1's own restricted flc^¸ãÛh‘éì¶»§q«^u…±”°Ì¹½‘”ˆ(€€€ÍÑ½É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰½±±…ÁÍ•‰ô¤(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%‰ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰=‰Í•ÉÙ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}Ý¡•¹}°Í}É•ÍÑÉ¥Ñ•‘}ÑÉÕ•}‰ÕÑ}ÑÉ…¹Í¥•¹Ñ}¥Ñ•µ}Í…åÍ}™…±Í”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰¸0Ì¹½‘”Ñ¡…Ð¥ÌÉ•ÍÑÉ¥Ñ•µÕÍÐ¹½Ð‰”É½Õ¹‘…‰±”©ÕÍÐ‰•…ÕÍ”Ñ¡”(€€€¥¸µ™±¥¡Ð¥Ñ•´€¡”¹œ¸™É½´„‘¥™™•É•¹ÐÉ•ÑÉ¥•Ù…°½É¥¥¸Í¡…É¥¹œÑ¡”Í…µ”(€€€™…Ñ}¥¤¹•Ù•È…ÉÉ¥•Ñ¡”É•ÍÑÉ¥Ñ¥½¸¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°ÌµÉ•ÍÑÉ¥Ñ•µÑÉ…¹Í¥•¹ÐµÍ…åÌµÕ¹É•ÍÑÉ¥Ñ•ˆ(€€€±…¥´€ô€‰„™…ÐÉ•ÍÑÉ¥Ñ•¥¸°ÌÉ•…±±•Ù¥„…¸¥Ñ•´Ý¥Ñ¡½ÕÐÑ¡”É•ÍÑÉ¥Ñ¥½¸ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆèQÉÕ•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}Ý¡•¹}°Å}É•ÍÑÉ¥Ñ•‘}ÑÉÕ•}°Í}É•Á½ÉÑÍ}™…±Í”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰Q¡”É•Ù•ÉÍ”‘¥É•Ñ¥½¸è0Ä…±É•…‘äµ…É­•Ñ¡”™…ÐÉ•ÍÑÉ¥Ñ•°‰ÕÐÑ¡”(€€€0Ì¹½‘”¡…Ì¹½Ð€¡å•Ð¤Íå¹•Ñ¡…ÐƒŠP‘•¹äµ‘½µ¥¹…¹Ð°¹½Ð€‰±…ÍÐÝÉ¥Ñ”(€€€Ý¥¹Ìˆ¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹µ•µ½Éä¥µÁ½ÉÐÍÑ½É•}™…Ð°Í•Ñ}É•ÍÑÉ¥Ñ•(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°ÄµÉ•ÍÑÉ¥Ñ•µ°ÌµÉ•Á½ÉÑÌµÕ¹É•ÍÑÉ¥Ñ•ˆ(€€€±…¥´€ô€‰„™…ÐÉ•ÍÑÉ¥Ñ•¥¸°Ä‰ÕÐ¹½Ðå•ÐÉ•™±•Ñ•½¸¥ÑÌ°Ì¹½‘”ˆ(€€€ÍÑ½É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•‰ô¤(€€€Í•Ñ}É•ÍÑÉ¥Ñ•¡™¥°QÉÕ”¤(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}…±±½ÝÍ}Ý¡•¹}°Í}É•ÍÑÉ¥Ñ•‘}Ù…±Õ•}¥Í}Õ¹­¹½Ý¹}ÑåÁ•}‰ÕÑ}°Å}½¹™¥ÉµÍ}™…±Í”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰µ…±™½Éµ•½Õ¹­¹½Ý¸É•ÍÑÉ¥Ñ•‘€Ù…±Õ”½¸Ñ¡”0Ì¹½‘”€¡¹½Ð„­¹½Ý¸(€€€€À¼Ä½‰½½°¤¥ÌU9-9=]8°¹½Ð„½¹™¥Éµ•QÉÕ”ƒŠP0ÄÌ½Ý¸½¹™¥Éµ•…±Í”(€€€€¡Íå¹•‰ä‰Õ¥±‘}™…ÑÍ}Á…¬ ¤¤µÕÍÐÉ½Õ¹¹½Éµ…±±äÉ…Ñ¡•ÈÑ¡…¸‰•¥¹œ(€€€½Ù•ÉÉ¥‘‘•¸‰ä…¸0ÌµÍ¥‘”Ù…±Õ”Ñ¡…Ð¥Í¸Ð¥ÑÍ•±˜„É•…°É•ÍÑÉ¥Ñ¥½¸(€€€€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€Ôì½ÉÉ•Ñ•™É½´Ñ¡”É½Õ¹´È¼ÌÙ•ÉÍ¥½¸(€€€½˜Ñ¡¥ÌÑ•ÍÐ°Ý¡¥ …ÍÍ•ÉÑ•Ñ¡”½ÁÁ½Í¥Ñ”‰•™½É”Ñ¡”1…‘å‰Õœµ‰É•…­¥¹œ(€€€½Ù•Èµ…ÁÁ±¥…Ñ¥½¸½˜‘•¹äµ‘½µ¥¹…¹”Ý…Ì¥‘•¹Ñ¥™¥•…¹™¥á•¤¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°ÌµÉ•ÍÑÉ¥Ñ•µÕ¹­¹½Ý¸µÑåÁ”ˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°ÌÉ•ÍÑÉ¥Ñ•™¥•±¥Ì„µ…±™½Éµ•Õ¹­¹½Ý¸Ù…±Õ”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè€‰å•Ì‰ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}…±±½ÝÍ}Ý¡•¹}‰½Ñ¡}É•ÁÉ•Í•¹Ñ…Ñ¥½¹Í}…É••}Õ¹É•ÍÑÉ¥Ñ•¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰I•É•ÍÍ¥½¸Õ…ÉèÑ¡”‘•¹äµ‘½µ¥¹…¹ÐÉ•½¹¥±¥…Ñ¥½¸µÕÍÐ¹½Ð(€€€½Ù•Èµ‰±½¬Ñ¡”½µµ½¸…Í”Ý¡•É”‰½Ñ Í¥‘•Ì…É•”Ñ¡”™…Ð¥Ì¹½Ð(€€€É•ÍÑÉ¥Ñ•¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰‰½Ñ µÍ¥‘•Ìµ…É•”µÕ¹É•ÍÑÉ¥Ñ•ˆ(€€€±…¥´€ô€‰„™…Ð‰½Ñ É•ÁÉ•Í•¹Ñ…Ñ¥½¹Ì…É•”¥Ì¹½ÐÉ•ÍÑÉ¥Ñ•ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}…±±½ÝÍ}Ý¡•¹}°Í}¹½‘•}¹•Ù•É}…ÉÉ¥•Í}…}É•ÍÑÉ¥Ñ•‘}™¥•±‘}…¹‘}°Å}½¹™¥ÉµÍ}™…±Í”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰Q¡”0ÄÍ¥‘”É•Á½ÉÑÌ„­¹½Ý¸°•áÁ±¥¥Ð…±Í”°…¹Ñ¡”Á¡åÍ¥…°0Ì¹½‘”(€€€¹•Ù•È…ÉÉ¥•Ì„É•ÍÑÉ¥Ñ•‘€™¥•±…Ð…±°€¡”¹œ¸1…‘å‰Õ0ÍÉ…Á °Ý¡½Í”(€€€Í¡•µ„‘½•Ì¹½ÐÑÉ…¬¥Ð¤¸5¥ÍÍ¥¹œ¥ÌU9-9=]8°¹½Ð„½¹™¥Éµ•QÉÕ”ƒŠP(€€€0ÄÌ½¹™¥Éµ•…±Í”µÕÍÐÉ½Õ¹Ñ¡”™…Ð¹½Éµ…±±äÉ…Ñ¡•ÈÑ¡…¸‰•¥¹œ(€€€½Ù•ÉÉ¥‘‘•¸‰äÑ¡”0Ì‰…­•¹ÌÍÑÉÕÑÕÉ…°¥¹…‰¥±¥ÑäÑ¼•áÁÉ•ÍÌÑ¡¥Ì(€€€™¥•±…Ð…±°€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€ÔèÑ¡”ÁÉ•Ù¥½ÕÌ(€€€™…¥°µ±½Í•Ù•ÉÍ¥½¸½˜Ñ¡¥ÌÑ•ÍÐµ…‘”•Ù•ÉäÉ•…±±•™…Ð½¸ÍÕ „(€€€‰…­•¹Á•Éµ…¹•¹Ñ±ä¹½¸µÉ½Õ¹‘…‰±”°Ý¡¥ ¥ÌÑ¡”•á…ÐÉ•É•ÍÍ¥½¸Ñ¡¥Ì(€€€É½Õ¹½ÉÉ•ÑÌƒŠPÍ•”Ñ¡”¥‘•¹Ñ¥…°™¥à…±É•…‘ä…ÁÁ±¥•Ñ¼Ñ¡”(€€€É•ÑÉ¥•Ù…°±…å•È¥¸É½Õ¹€Ð¤¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°Ìµ¹½‘”µ¹•Ù•Èµ¡…ÌµÉ•ÍÑÉ¥Ñ•µ™¥•±ˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°Ì‰…­•¹¹•Ù•ÈÉ•ÑÕÉ¹Ì„É•ÍÑÉ¥Ñ•™¥•±ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%‰ô¤(€€€€Œ¹¼€‰É•ÍÑÉ¥Ñ•ˆ­•ä…Ð…±°ƒŠPÍ¥µÕ±…Ñ•Ì„‰…­•¹Ý¡½Í”Á…å±½…Í¡•µ„(€€€€ŒÍ¥µÁ±ä‘½•Ì¹½Ð¥¹±Õ‘”Ñ¡”½±Õµ¸½™¥•±¸(€€€…ÍÍ•ÉÐ€‰É•ÍÑÉ¥Ñ•ˆ¹½Ð¥¸œ¹•Ñ}™…Ð¡™¥¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}…±±½ÝÍ}Ý¡•¹}‰½Ñ¡}Í¥‘•Í}…É•}­¹½Ý¹}ÍÅ±¥Ñ•}é•É¼¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰0ÄÉ•ÍÑÉ¥Ñ•ôÀ…¹Ñ¡”0Ì¹½‘”Ì½Ý¸É•ÍÑÉ¥Ñ•ôÀ€¡‰½Ñ „É•…°¥¹Ð(€€€™É½´„­¹½Ý¸…‘…ÁÑ•È‰½Õ¹‘…Éä°¹½Ð™±½…Ð½‰½½°¤µÕÍÐÉ½Õ¹¹½Éµ…±±ä¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰‰½Ñ µÍ¥‘•Ìµ­¹½Ý¸µÍÅ±¥Ñ”µé•É¼ˆ(€€€±…¥´€ô€‰„™…Ð‰½Ñ ÍÑ½É•ÌÉ•Á½ÉÐ…ÌÉ•ÍÑÉ¥Ñ•¥¹Ñ••Èé•É¼ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè€Áô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}Ý¡•¹}°Í}É•Á½ÉÑÍ}­¹½Ý¹}ÍÅ±¥Ñ•}½¹”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰0ÄÉ•ÍÑÉ¥Ñ•ôÀ‰ÕÐÑ¡”0Ì¹½‘”Ì½Ý¸É•ÍÑÉ¥Ñ•ôÄ€¡‰½Ñ É•…°¥¹ÑÌ(€€€™É½´„­¹½Ý¸…‘…ÁÑ•È‰½Õ¹‘…Éä¤ƒŠP‘•¹äµ‘½µ¥¹…¹ÐÍÑ¥±°‰±½­Ì¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°Ìµ­¹½Ý¸µÍÅ±¥Ñ”µ½¹”ˆ(€€€±…¥´€ô€‰„™…Ð°ÌÉ•Á½ÉÑÌ…ÌÉ•ÍÑÉ¥Ñ•¥¹Ñ••È½¹”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè€Åô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}½¹}Õ¹É•Í½±Ù…‰±•}¹½¹}Ñ•Éµ¥¹…±}•Á¥ÍÑ•µ¥}ÍÑ…Ñ•}‘¥Í…É••µ•¹Ð¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰0ÄÍ¡½ÝÌY…±¥‘…Ñ•°Ñ¡”0Ì¹½‘”Í¡½ÝÌ%µµÕÑ…‰±•½É”ƒŠP¥¹‘¥Ù¥‘Õ…±±ä‰½Ñ (€€€…É”ÍÑÉ¥Ðµ…¹½¹¥…°ÍÑ…Ñ•Ì°‰ÕÐ…¸Õ¹É•Í½±Ù…‰±”‘¥Í…É••µ•¹Ð‰•ÑÝ••¸Ñ¡”(€€€ÑÝ¼É•ÁÉ•Í•¹Ñ…Ñ¥½¹ÌµÕÍÐ™…¥°±½Í•€¡MQ=I}MQQ}=91%P¤°¹½ÐÍ¥±•¹Ñ±ä(€€€ÁÉ•™•È•¥Ñ¡•ÈÍ¥‘”¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹µ•µ½Éä¥µÁ½ÉÐÍÑ½É•}™…Ð(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰Õ¹É•Í½±Ù…‰±”µÍÑ…Ñ”µ‘¥Í…É••µ•¹Ðˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°Ä…¹°ÌÙ¥•ÝÌ½˜•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‘¥Í…É•”ˆ(€€€ÍÑ½É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•‰ô¤(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰%µµÕÑ…‰±•½É”ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%‰ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰=‰Í•ÉÙ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}É•½¹¥±¥…Ñ¥½¹}‘½•Í}¹½Ñ}µÕÑ…Ñ•}Á•ÉÍ¥ÍÑ•‘}ÍÑ…Ñ”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰I•…±°É•½¹¥±¥…Ñ¥½¸¥ÌÉ•…µ½¹±äèÉ•Á•…Ñ•É•…±°½˜„½¹™±¥Ñ¥¹œ(€€€™…ÐµÕÍÐ¹•Ù•ÈÝÉ¥Ñ”‰…¬Ñ¼0Ä½È0ÌƒŠPÑ¡”Ñ•Éµ¥¹…°ÍÑ…Ñ”ÍÑ…åÌ•á…Ñ±ä(€€€…ÌÁ•ÉÍ¥ÍÑ•½¸‰½Ñ Í¥‘•Ì¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹µ•µ½Éä¥µÁ½ÉÐÍÑ½É•}™…Ð°•Ñ}™…Ð(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰É•Á•…Ñ•µÉ•…±°µ¹¼µµÕÑ…Ñ¥½¸ˆ(€€€±…¥´€ô€‰„™…ÐÉ•…±±•ÑÝ¥”µÕÍÐ¹½Ð¡…Ù”¥ÑÌÁ•ÉÍ¥ÍÑ•ÍÑ…Ñ”¡…¹•‰äÉ•…±°ˆ(€€€ÍÑ½É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰½±±…ÁÍ•‰ô¤(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%‰ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰=‰Í•ÉÙ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€Á¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤(€€€Á¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐ•Ñ}™…Ð¡™¥¥l‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‰t€ôô€‰½±±…ÁÍ•ˆ(€€€…ÍÍ•ÉÐœ¹•Ñ}™…Ð¡™¥¥l‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‰t€ôô€‰Y…±¥‘…Ñ•ˆ(()‘•˜Ñ•ÍÑ}É•…±±}ÕÍ•Í}°Í}É•½É‘}±…¥µ}…¹‘}Í½ÕÉ•}¹½Ñ}ÑÉ…¹Í¥•¹Ñ}¥Ñ•´¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰Q¡”Á¡åÍ¥…°0Ì¹½‘”¥ÌÑ¡”Í¥¹±”…ÕÑ¡½É¥Ñ…Ñ¥Ù”É•½É™½È¥ÑÌ(€€€™…Ñ}¥ƒŠP„ÑÉ…¹Í¥•¹ÐÉ•ÑÉ¥•Ù•¥Ñ•´Ì±…¥´½Í½ÕÉ”€¡”¹œ¸„‘¥™™•É•¹Ð(€€€É•ÑÉ¥•Ù…°½É¥¥¸½¥¹¥‘•¹Ñ…±±äÍ¡…É¥¹œÑ¡¥Ì™…Ñ}¥¤µÕÍÐ¹½Ð½Ù•ÉÉ¥‘”(€€€¥Ð¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°Ìµ…ÕÑ¡½É¥Ñ…Ñ¥Ù”µ±…¥´µ…¹µÍ½ÕÉ”ˆ(€€€É•…±}±…¥´€ô€‰Ñ¡”É•…°…¹½¹¥…°±…¥´Á•ÉÍ¥ÍÑ•¥¸°Ìˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆèÉ•…±}±…¥´°€‰Í½ÕÉ”ˆè€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ°(€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€À¸ä°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè€‰„‘¥™™•É•¹Ð¹½¸µ…¹½¹¥…°±…¥´™É½´…¹½Ñ¡•ÈÉ•ÑÉ¥•Ù…°½É¥¥¸ˆ°(€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Õ¹ÑÉÕÍÑ•µ½Ñ¡•Èµ½É¥¥¸ˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰™…ÑÌ‰ulÁul‰±…¥´‰t€ôôÉ•…±}±…¥´(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰™…ÑÌ‰ulÁul‰Í½ÕÉ”‰t€ôô€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ(()‘•˜Ñ•ÍÑ}É•…±±}É•½¹¥±¥…Ñ¥½¹}Íå¹Í}ÑÉ…•}Í½ÕÉ•}¹½Ñ}©ÕÍÑ}•Á¥ÍÑ•µ¥}ÍÑ…Ñ”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰•¹•É…Ñ•}…¹ÍÝ•È ¤ÌÍÕ•ÍÌÁ…Ñ ÁÉÕ¹•Ñ¡”ÑÉ…”Ñ¼É½Õ¹‘¥¹œ™…ÑÌ(€€€…¹Íå¹••Á¥ÍÑ•µ¥}ÍÑ…Ñ”°‰ÕÐ¹½ÐÍ½ÕÉ”ƒŠPÍ¼…™Ñ•È(€€€}É•½¹¥±•}É•…±±•‘}™…Ð ¤É•Á±…•ÌÑ¡”¥¸µ™±¥¡Ð™…ÐÌÍ½ÕÉ”Ý¥Ñ Ñ¡”(€€€0Ìµ…ÕÑ¡½É¥Ñ…Ñ¥Ù”Ù…±Õ”°Ñ¡”ÑÉ…”€¡‰Õ¥±Ð•…É±¥•È‰ä‰Õ¥±‘}ÑÉ…”¡É•ÑÉ¥•Ù•¤(€€€™É½´Ñ¡”ÁÉ”µÉ•½¹¥±¥…Ñ¥½¸ÑÉ…¹Í¥•¹Ð¥Ñ•´¤ÍÑ¥±°¥Ñ•Ñ¡”ÝÉ½¹œÍ½ÕÉ”°(€€€•Ù•¸Ñ¡½Õ É•ÍÕ±Ñl‰™…ÑÌ‰t½ÉÉ•Ñ±äÍ¡½Ý•Ñ¡”0ÌÍ½ÕÉ”€ ŒÈÔÜ(€€€¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€È¤¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰ÑÉ…”µÍ½ÕÉ”µÍå¹Œˆ(€€€É•…±}±…¥´€ô€‰Ñ¡”É•…°…¹½¹¥…°±…¥´Á•ÉÍ¥ÍÑ•¥¸°Ì™½ÈÑÉ…”Íå¹Œˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆèÉ•…±}±…¥´°€‰Í½ÕÉ”ˆè€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ°(€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€À¸ä°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè€‰„‘¥™™•É•¹Ð¹½¸µ…¹½¹¥…°±…¥´™½ÈÑÉ…”Íå¹Œˆ°(€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Õ¹ÑÉÕÍÑ•µ½Ñ¡•Èµ½É¥¥¸ˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰™…ÑÌ‰ulÁul‰Í½ÕÉ”‰t€ôô€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰ÑÉ…”‰ulÁul‰Í½ÕÉ”‰t€ôô€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ(€€€…ÍÍ•ÉÐ€‰Õ¹ÑÉÕÍÑ•µ½Ñ¡•Èµ½É¥¥¸ˆ¹½Ð¥¸É•ÍÕ±Ñl‰ÑÉ…•}™µÐ‰t(()‘•˜Ñ•ÍÑ}É•…±±}É•½¹¥±¥…Ñ¥½¹}É•Íå¹Í}°Å}±…¥µ}…¹‘}Í½ÕÉ•}…™Ñ•É}Á½±±ÕÑ¥½¸¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰‰Õ¥±‘}™…ÑÍ}Á…¬ ¤Á•ÉÍ¥ÍÑÌÑ¡”ÁÉ”µÉ•½¹¥±¥…Ñ¥½¸ÑÉ…¹Í¥•¹Ð¥Ñ•´Ñ¼(€€€0ÄÙ¥„ÍÑ½É•}™…Ð ¤‰•™½É”}É•½¹¥±•}É•…±±•‘}™…Ð ¤•Ù•ÈÉÕ¹Ì¸%˜Ñ¡”(€€€ÑÉ…¹Í¥•¹Ð¥Ñ•´Ì±…¥´½Í½ÕÉ”‘¥Í…É••Ý¥Ñ Ñ¡”0ÌÉ•½É°0Ä¥Ì±•™Ð(€€€¡½±‘¥¹œÑ¡”]I=9Ù…±Õ”•Ù•¸Ñ¡½Õ Ñ¡¥Ì…¹ÍÝ•È¥ÑÍ•±˜É½Õ¹‘Ì½ÉÉ•Ñ±ä(€€€½¸0ÌƒŠPÁ½±±ÕÑ¥¹œ™ÕÑÕÉ”µ•µ½Éä¹•Ñ}™…Ð ¤É•…‘Ì…¹ÁÉ½Ù•¹…¹”É••¥ÁÐ(€€€Ù•É¥™¥…Ñ¥½¸¸}É•½¹¥±•}É•…±±•‘}™…Ð ¤µÕÍÐÉ”µÍå¹Œ0Ä‰…¬Ñ¼Ñ¡”(€€€…ÕÑ¡½É¥Ñ…Ñ¥Ù”0ÌÙ…±Õ”€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€È¤¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€™É½´½É”¹µ•µ½Éä¥µÁ½ÉÐ•Ñ}™…Ð(€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°ÄµÉ•Íå¹Œµ…™Ñ•ÈµÁ½±±ÕÑ¥½¸ˆ(€€€É•…±}±…¥´€ô€‰Ñ¡”É•…°…¹½¹¥…°±…¥´Á•ÉÍ¥ÍÑ•¥¸°Ì™½È°ÄÉ•Íå¹Œˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆèÉ•…±}±…¥´°€‰Í½ÕÉ”ˆè€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ°(€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€À¸ä°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè€‰„‘¥™™•É•¹Ð¹½¸µ…¹½¹¥…°±…¥´™½È°ÄÉ•Íå¹Œˆ°(€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Õ¹ÑÉÕÍÑ•µ½Ñ¡•Èµ½É¥¥¸ˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(€€€°Å}…™Ñ•È€ô•Ñ}™…Ð¡™¥¤(€€€…ÍÍ•ÉÐ°Å}…™Ñ•Él‰±…¥´‰t€ôôÉ•…±}±…¥´(€€€…ÍÍ•ÉÐ°Å}…™Ñ•Él‰Í½ÕÉ”‰t€ôô€‰ÑÉÕÍÑ•µ°ÌµÍ½ÕÉ”ˆ(((ŒƒŠRŠRŠR I•…±°µ•Ñ…‘…Ñ„µ½¹™±¥ÐÉ•½¹¥±¥…Ñ¥½¸€ ŒÈÔÜ½ÉÉ•Ñ¥Ù”°™½±±½ÜµÕÀ¤ƒŠRŠRŠRŠRŠRŠR (ŒÑÉÕÑ¡}ÍÑ…ÑÕÌ¥ÌÑ…­•¸™É½´Ñ¡”0Ì¹½‘”ìÍ¥±•¹Ñ±äÑ…­¥¹œ(Œ½¹™¥‘•¹”½±…¥µ}ÑåÁ”½Í½ÕÉ•}ÍÑ…ÑÕÌ™É½´„%I9P€¡ÑÉ…¹Í¥•¹Ð¤(ŒÉ•ÁÉ•Í•¹Ñ…Ñ¥½¸Ý¥Ñ¡½ÕÐ¡•­¥¹œÑ¡•ä…É•”¥ÌÑ¡”Í…µ”¡å‰É¥µÉ•½É(Œ…¹Ñ¤µÁ…ÑÑ•É¸ƒŠP„É•…°‘¥Í…É••µ•¹ÐµÕÍÐ™…¥°±½Í•°¹½ÐÁ¥¬„Í¥‘”¸()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}Ý¡•¹}°Í}½¹™¥‘•¹•}‘¥Í…É••Í}Ý¥Ñ¡}ÑÉ…¹Í¥•¹Ñ}¥Ñ•´¡µ½¹­•åÁ…Ñ ¤è(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°Ìµ½¹™¥‘•¹”µ‘¥Í…É••Ìˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°Ì…¹ÑÉ…¹Í¥•¹Ð½¹™¥‘•¹”Ù…±Õ•Ì‘¥Í…É•”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸äÔ°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸È°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}Ý¡•¹}°Í}±…¥µ}ÑåÁ•}‘¥Í…É••Í}Ý¥Ñ¡}ÑÉ…¹Í¥•¹Ñ}¥Ñ•´¡µ½¹­•åÁ…Ñ ¤è(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°Ìµ±…¥´µÑåÁ”µ‘¥Í…É••Ìˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°Ì…¹ÑÉ…¹Í¥•¹Ð±…¥µ}ÑåÁ”Ù…±Õ•Ì‘¥Í…É•”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰=A%9%=8ˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}‰±½­Í}Ý¡•¹}°Í}Í½ÕÉ•}ÍÑ…ÑÕÍ}‘¥Í…É••Í}Ý¥Ñ¡}ÑÉ…¹Í¥•¹Ñ}¥Ñ•´¡µ½¹­•åÁ…Ñ ¤è(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰°ÌµÍ½ÕÉ”µÍÑ…ÑÕÌµ‘¥Í…É••Ìˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°Ì…¹ÑÉ…¹Í¥•¹ÐÍ½ÕÉ•}ÍÑ…ÑÕÌÙ…±Õ•Ì‘¥Í…É•”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰UMI}IA=IQˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}ÍÕ••‘Í}Ý¡•¹}™Õ±±}ÑÉÕÍÑ}µ•Ñ…‘…Ñ…}µ…Ñ¡•Ì¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰I•É•ÍÍ¥½¸Õ…ÉèÑ¡”µ•Ñ…‘…Ñ„µ½¹™±¥Ð¡•¬µÕÍÐ¹½Ð½Ù•Èµ‰±½¬Ñ¡”(€€€½µµ½¸…Í”Ý¡•É”½¹™¥‘•¹”½±…¥µ}ÑåÁ”½Í½ÕÉ•}ÍÑ…ÑÕÌ•¹Õ¥¹•±ä…É•”(€€€‰•ÑÝ••¸Ñ¡”ÑÉ…¹Í¥•¹Ð¥Ñ•´…¹Ñ¡”Á¡åÍ¥…°0Ì¹½‘”¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰™Õ±°µÑÉÕÍÐµµ•Ñ…‘…Ñ„µµ…Ñ¡•Ìˆ(€€€±…¥´€ô€‰„™…ÐÝ¡½Í”°Ì…¹ÑÉ…¹Í¥•¹Ðµ•Ñ…‘…Ñ„™Õ±±ä…É•”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(()‘•˜Ñ•ÍÑ}É•…±±}É•½¹¥±¥…Ñ¥½¹}É½Õ¹‘Í}‰½Ñ¡}™…ÑÍ}Ù¥…}É•…±}É•ÑÉ¥•Ù…±}Á…Ñ  ¤è(€€€€ˆˆ‰±°½Ñ¡•ÈÉ•…±°µÉ•½¹¥±¥…Ñ¥½¸Ñ•ÍÑÌ¥¸Ñ¡¥Ìµ½‘Õ±”µ½¹­•åÁ…Ñ (€€€É•ÑÉ¥•Ù” ¤Ý¥Ñ „Íå¹Ñ¡•Ñ¥Œ¥Ñ•´°‰åÁ…ÍÍ¥¹œÑ¡”É•…°Ù•Ñ½ÈµÍ•…É €¬(€€€É…Á µÝ…±¬µ•¡…¹¥Ì•¹Ñ¥É•±ä¸Q¡¥Ì¥ÌÑ¡”½¹”É•½¹¥±¥…Ñ¥½¸Ñ•ÍÐÑ¡…Ð(€€€‘É¥Ù•Ì}É•½¹¥±•}É•…±±•‘}™…Ð ¤Ñ¡É½Õ Ñ¡”…ÑÕ…°É•ÑÉ¥•Ù” ¤Á¥Á•±¥¹”(€€€™½ÈÑÝ¼…±É•…‘äµ…¹½¹¥…°™…ÑÌÑ¡…Ð…É”‰½Ñ ‘¥É•ÐÙ•Ñ½È¡¥ÑÌ9(€€€±¥¹­•Ñ¼•… ½Ñ¡•È¥¸Ñ¡”É…Á ƒŠPÙ•É¥™å¥¹œÑ¡”É•…±°Á…Ñ ÍÑ¥±°(€€€É½Õ¹‘Ì½ÉÉ•Ñ±ä•¹µÑ¼µ•¹Ý¡•¸„™…Ð¥ÌÉ•…¡•‰äµ½É”Ñ¡…¸½¹”(€€€É•ÑÉ¥•Ù…°Í½ÕÉ”…Ð½¹”°¹½Ð©ÕÍÐÙ¥„…¸¥¹©•Ñ•¥Ñ•´¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÉÕ¸(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰É•½¸µÉ•…°µÁ…Ñ µ„ˆ°(€€€€€€€€€€€€€€€€€‰±…¥´ˆè€‰…±Á¡„Ñ½Á¥ŒÉ•½¹¥±¥…Ñ¥½¸É•…°Á…Ñ ¡•¬ˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰É•½¸µÉ•…°µÁ…Ñ µˆˆ°(€€€€€€€€€€€€€€€€€‰±…¥´ˆè€‰‰•Ñ„Ñ½Á¥ŒÉ•½¹¥±¥…Ñ¥½¸É•…°Á…Ñ ¡•¬ˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤(€€€œ¹…‘‘}•‘” ‰É•½¸µÉ•…°µÁ…Ñ µ„ˆ°€‰=}=UIIˆ°€‰É•½¸µÉ•…°µÁ…Ñ µˆˆ°íô¤((€€€É•ÍÕ±Ð€ôÉÕ¸ ‰…±Á¡„Ñ½Á¥Œ‰•Ñ„Ñ½Á¥ŒÉ•½¹¥±¥…Ñ¥½¸É•…°Á…Ñ ¡•¬ˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(€€€…ÍÍ•ÉÐí™l‰™…Ñ}¥‰t™½È˜¥¸É•ÍÕ±Ñl‰™…ÑÌ‰uô€ôôì(€€€€€€€€‰É•½¸µÉ•…°µÁ…Ñ µ„ˆ°€‰É•½¸µÉ•…°µÁ…Ñ µˆ‰ô(((ŒƒŠRŠRŠR 	±½­•È€È€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ì¤è¹¼Íå¹Ñ¡•Í¥é•ÁÉ½Ù•¹…¹”½½¹™¥‘•¹”ƒŠRŠRŠRŠR ()‘•˜Ñ•ÍÑ}Ù•É¥™¥•‘}Ù…±¥‘…Ñ•‘}°Í}¹½‘•}µ¥ÍÍ¥¹}Í½ÕÉ•}‰±½­Í}Ù¥…}Õ…É‘¥…¸ ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÉÕ¸(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€±…¥´€ô€‰„Ù•É¥™¥•±…¥´µ¥ÍÍ¥¹œ¥ÑÌÍ½ÕÉ”™¥•±•¹Ñ¥É•±ä™½ÈÕ…É‘¥…¸ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰µ¥ÍÍ¥¹œµÍ½ÕÉ”µÙ•É¥™¥•ˆ°€‰±…¥´ˆè±…¥´°(€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤€€Œ¹¼€‰Í½ÕÉ”ˆ­•ä…Ð…±°((€€€É•ÍÕ±Ð€ôÉÕ¸¡±…¥´¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐ€‰Õ…É‘¥…¸ˆ¥¸€¡É•ÍÕ±Ð¹•Ð ‰•ÉÉ½Èˆ¤½È€ˆˆ¤(()‘•˜Ñ•ÍÑ}Ù•É¥™¥•‘}Ù…±¥‘…Ñ•‘}°Í}¹½‘•}µ¥ÍÍ¥¹}½¹™¥‘•¹•}‰±½­Í}Ù¥…}Õ…É‘¥…¸ ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÉÕ¸(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€±…¥´€ô€‰„Ù•É¥™¥•±…¥´µ¥ÍÍ¥¹œ¥ÑÌ½¹™¥‘•¹”™¥•±•¹Ñ¥É•±ä™½ÈÕ…É‘¥…¸ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰µ¥ÍÍ¥¹œµ½¹™¥‘•¹”µÙ•É¥™¥•ˆ°€‰±…¥´ˆè±…¥´°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤€€Œ¹¼€‰½¹™¥‘•¹”ˆ­•ä…Ð…±°((€€€É•ÍÕ±Ð€ôÉÕ¸¡±…¥´¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐ€‰Õ…É‘¥…¸ˆ¥¸€¡É•ÍÕ±Ð¹•Ð ‰•ÉÉ½Èˆ¤½È€ˆˆ¤(()‘•˜Ñ•ÍÑ}µ…±™½Éµ•‘}Í½ÕÉ•}…¹‘}½¹™¥‘•¹•}ÑåÁ•Í}™…¥±}±½Í•‘}Ý¥Ñ¡½ÕÑ}É…Í¡¥¹œ ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÉÕ¸(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€±…¥´€ô€‰„±…¥´Ý¥Ñ µ…±™½Éµ•Í½ÕÉ”…¹½¹™¥‘•¹”ÑåÁ•Ì™½ÈÕ…É‘¥…¸ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰µ…±™½Éµ•µÑåÁ•Ìˆ°€‰±…¥´ˆè±…¥´°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ”ˆèl‰¹½Ðˆ°€‰„ˆ°€‰ÍÑÉ¥¹œ‰t°€‰½¹™¥‘•¹”ˆè€‰¹½Ðµ„µ¹Õµ‰•Èˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€É•ÍÕ±Ð€ôÉÕ¸¡±…¥´¤€€ŒµÕÍÐ¹½ÐÉ…¥Í”((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐ€‰Õ…É‘¥…¸ˆ¥¸€¡É•ÍÕ±Ð¹•Ð ‰•ÉÉ½Èˆ¤½È€ˆˆ¤(()‘•˜Ñ•ÍÑ}Ù…±¥‘}Á•ÉÍ¥ÍÑ•‘}Í½ÕÉ•}…¹‘}½¹™¥‘•¹•}É•µ…¥¹}Õ¹…™™•Ñ• ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÉÕ¸(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€±…¥´€ô€‰„™Õ±±äÙ…±¥Ù•É¥™¥•±…¥´…‰½ÕÐÁÉ½Á•É±äÍ½ÕÉ•Ý¥‘•ÑÌˆ(€€€€Œ±…¥µ}ÑåÁ”½Í½ÕÉ•}ÍÑ…ÑÕÌµÕÍÐ…ÑÕ…±±äÍÕÁÁ½ÉÐ„YI%%Ù•É‘¥Ð(€€€€Œ€ ŒÈÔÜ½ÉÉ•Ñ¥Ù”¡…É‘•¹¥¹œè…¹½¹¥…±Y¥•Ü¹½Ü™…¥±Ì±½Í•½¸„(€€€€ŒYI%%±…‰•°Ñ¡”ÝÉ¥Ñ”µÑ¥µ”Á½±¥ä½Õ±¹•Ù•È¡…Ù”ÁÉ½‘Õ•™½ÈÑ¡”(€€€€Œ™…ÐÌ±…¥µ}ÑåÁ”½Í½ÕÉ•}ÍÑ…ÑÕÌ½µ‰¥¹…Ñ¥½¸¤ƒŠP„€‰™Õ±±äÙ…±¥ˆ™¥áÑÕÉ”(€€€€Œ¹••‘Ì½¹Í¥ÍÑ•¹Ðµ•Ñ…‘…Ñ„°¹½Ð©ÕÍÐ„‰…É”ÑÉÕÑ¡}ÍÑ…ÑÕÌ¸(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰Ù…±¥µÙ•É¥™¥•ˆ°€‰±…¥´ˆè±…¥´°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰ÑÉÕÍÑ•µÍ½ÕÉ”ˆ°€‰½¹™¥‘•¹”ˆè€À¸äÔ°(€€€€€€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€É•ÍÕ±Ð€ôÉÕ¸¡±…¥´¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰™…ÑÌ‰ulÁul‰Í½ÕÉ”‰t€ôô€‰ÑÉÕÍÑ•µÍ½ÕÉ”ˆ(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰™…ÑÌ‰ulÁul‰½¹™¥‘•¹”‰t€ôôÁåÑ•ÍÐ¹…ÁÁÉ½à À¸äÔ¤(((ŒƒŠRŠRŠR 	±½­•È€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ð¤è¹½¸µ™¥¹¥Ñ”½¹™¥‘•¹”µÕÍÐ™…¥°±½Í•ƒŠRŠRŠRŠR (Œ™±½…Ð ‰¹…¸ˆ¤½™±½…Ð ‰¥¹˜ˆ¤‰½Ñ ½¹Ù•ÉÐÝ¥Ñ¡½ÕÐÉ…¥Í¥¹œ°‰ÕÐ9…8½µÁ…É•Ì(Œ…±Í”……¥¹ÍÐ•Ù•ÉäÉ•±…Ñ¥½¹…°½Á•É…Ñ½È€ ø°€ðô°€ð¤ƒŠP„É…Üà€ø€Á€€¼(Œà€ðô€Á€€¼à€ðÑ¡É•Í¡½±‘€¡•¬Í¥±•¹Ñ±ä±•ÑÌ¥ÐÑ¡É½Õ ¥¹ÍÑ•…½˜(ŒÉ•©•Ñ¥¹œ¥Ð°…¹€­%¹™¥¹¥Ñä±•¥Ñ¥µ…Ñ•±äÍ…Ñ¥Í™¥•Ì•Ù•Éä€‰½¹™¥‘•¹”€øô(ŒÑ¡É•Í¡½±ˆ¡•¬Ñ¡•É”¥Ì¸()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰É…Üˆ°l(€€€™±½…Ð ‰¹…¸ˆ¤°€‰9…8ˆ°€‰¹…¸ˆ°(€€€™±½…Ð ‰¥¹˜ˆ¤°€‰%¹™¥¹¥Ñäˆ°€‰¥¹˜ˆ°(€€€™±½…Ð ˆµ¥¹˜ˆ¤°€ˆµ%¹™¥¹¥Ñäˆ°€ˆµ¥¹˜ˆ°)t¤)‘•˜Ñ•ÍÑ}Í…™•}½¹™¥‘•¹•}É•©•ÑÍ}…±±}¹½¹}™¥¹¥Ñ•}™½ÉµÌ¡É…Ü¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}Í…™•}½¹™¥‘•¹”(€€€…ÍÍ•ÉÐ}Í…™•}½¹™¥‘•¹”¡É…Ü¤€ôô€À¸À(()‘•˜Ñ•ÍÑ}Í…™•}½¹™¥‘•¹•}…•ÁÑÍ}Ù…±¥‘}™¥¹¥Ñ•}Ù…±Õ” ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}Í…™•}½¹™¥‘•¹”(€€€…ÍÍ•ÉÐ}Í…™•}½¹™¥‘•¹” À¸ä¤€ôôÁåÑ•ÍÐ¹…ÁÁÉ½à À¸ä¤(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰É…Üˆ°l´À¸Ô°€Ä¸Ô°€ÄÀÀ¸Át¤)‘•˜Ñ•ÍÑ}Í…™•}½¹™¥‘•¹•}É•©•ÑÍ}½ÕÑ}½™}‘½µ…¥¹}Ù…±Õ•Ì¡É…Ü¤è(€€€€ˆˆ‰Q¡”…¹½¹¥…°½¹™¥‘•¹”‘½µ…¥¸¥ÌlÀ¸À°€Ä¸Át€¡Í¡•µ…Ì½™…Ð¹Í¡•µ„¹©Í½¸è(€€€µ¥¹¥µÕ´€À¸À°µ…á¥µÕ´€Ä¸Àì½É”½…Á¤¹ÁäÌ%¹•ÍÑI•ÅÕ•ÍÐè¥•±¡”ôÀ¸À°(€€€±”ôÄ¸À¤¤ƒŠP„Ù…±Õ”½ÕÑÍ¥‘”¥Ð¥Ìµ…±™½Éµ•°¹½Ðµ•É•±ä€‰Ù•Éä½¹™¥‘•¹Ðˆ¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}Í…™•}½¹™¥‘•¹”(€€€…ÍÍ•ÉÐ}Í…™•}½¹™¥‘•¹”¡É…Ü¤€ôô€À¸À(((ŒƒŠRŠRŠR ½ÉÉ•Ñ¥Ù”¡…É‘•¹¥¹œ€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ô¤èÉ•©•ÐÍÑÉ¥¹œ½¹™¥‘•¹•Ì(Œ‰•™½É”½•É¥½¸ƒŠP„Á•ÉÍ¥ÍÑ•¹Õµ•É¥ŒÍÑÉ¥¹œµÕÍÐ¹½Ð‰”¹½Éµ…±¥é•¥¹Ñ¼(ŒÑÉÕÍÑ•µ•Ñ…‘…Ñ„©ÕÍÐ‰•…ÕÍ”™±½…Ð ¤¡…ÁÁ•¹ÌÑ¼…•ÁÐ¥Ð¸()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰É…Üˆ°lˆÀ¸äˆ°€ˆÄˆ°€ˆÄ¸Àˆ°€ˆÀˆ°€ˆÀ¸À‰t¤)‘•˜Ñ•ÍÑ}Í…™•}½¹™¥‘•¹•}É•©•ÑÍ}Ù…±¥‘}±½½­¥¹}¹Õµ•É¥}ÍÑÉ¥¹Ì¡É…Ü¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}Í…™•}½¹™¥‘•¹”(€€€…ÍÍ•ÉÐ}Í…™•}½¹™¥‘•¹”¡É…Ü¤€ôô€À¸À(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰É…Üˆ°mQÉÕ”°…±Í•t¤)‘•˜Ñ•ÍÑ}Í…™•}½¹™¥‘•¹•}É•©•ÑÍ}‰½½°¡É…Ü¤è(€€€€ˆˆ‰‰½½°¥Ì…¸¥¹ÐÍÕ‰±…ÍÌ¥¸AåÑ¡½¸ƒŠPQÉÕ”½…±Í”µÕÍÐ¹½ÐÍ¥±•¹Ñ±ä(€€€½•É”Ñ¼€Ä¸À¼À¸À½¹™¥‘•¹”¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}Í…™•}½¹™¥‘•¹”(€€€…ÍÍ•ÉÐ}Í…™•}½¹™¥‘•¹”¡É…Ü¤€ôô€À¸À(()‘•˜Ñ•ÍÑ}Í…™•}½¹™¥‘•¹•}™…¥±Í}±½Í•‘}½¹}½Ù•ÉÍ¥é•‘}¥¹Ñ••É}Ý¥Ñ¡½ÕÑ}É…Í¡¥¹œ ¤è(€€€€ˆˆ‰™±½…Ð¡Ù…±Õ”¤¥ÑÍ•±˜É…¥Í•Ì=Ù•É™±½ÝÉÉ½È™½È„É•…°¥¹ÐÑ½¼±…É”Ñ¼(€€€½¹Ù•ÉÐÑ¼„™±½…Ð€¡”¹œ¸€ÄÀ¨¨ÄÀÀÀ¤ƒŠPµÕÍÐ™…¥°±½Í•Ñ¼Ñ¡”‘•™…Õ±Ð°(€€€¹½ÐÉ…Í •Ù•Éä…±±•È½˜Ñ¡¥ÌÁ•ÉÙ…Í¥Ù•±äµÕÍ•¡•±Á•È€¡Õ…É‘¥…¸°(€€€É•ÑÉ¥•Ù” ¤ÌÍ½É¥¹œ°}™…Ñ}µ•Ñ…‘…Ñ…}½¹™±¥ÑÌ°€¸¸¸¤€ ŒÈÔÜ(€€€¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€Ô¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}Í…™•}½¹™¥‘•¹”(€€€…ÍÍ•ÉÐ}Í…™•}½¹™¥‘•¹” ÄÀ¨¨ÄÀÀÀ¤€ôô€À¸À(((ŒƒŠRŠRŠR ¥É•ÐÕ¹¥Ð½Ù•É…”™½ÈÑ¡”É•…±°µÉ•½¹¥±¥…Ñ¥½¸¡•±Á•ÉÌƒŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠR ()‘•˜Ñ•ÍÑ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ñ}…•ÁÑÍ}­¹½Ý¹}ÍÅ±¥Ñ•}…‘…ÁÑ•É}Ù…±Õ•Ì ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð(€€€…ÍÍ•ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð À¤¥Ì…±Í”(€€€…ÍÍ•ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð Ä¤¥ÌQÉÕ”(€€€…ÍÍ•ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð¡QÉÕ”¤¥ÌQÉÕ”(€€€…ÍÍ•ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð¡…±Í”¤¥Ì…±Í”(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰‰…ˆ°l(€€€9½¹”°€€€€€€Œµ¥ÍÍ¥¹œƒŠP…¸Õ¹ÍÕÁÁ½ÉÑ•‰…­•¹…Á…‰¥±¥Ñä°¹½Ð„­¹½Ý¸…±Í”(€€€€È°€´Ä°€€€€€Œ½ÕÐµ½˜µÉ…¹”¥¹Ð(€€€€À¸À°€Ä¸À°€€Œ™±½…ÐƒŠPµÕÍÐ¹½Ð½µÁ…É”•ÅÕ…°Ñ¼¥¹Ð€À¼Ä¡•É”(€€€€‰å•Ìˆ°€ˆÄˆ°€ˆÀˆ°€‰ÑÉÕ”ˆ°€‰™…±Í”ˆ°(€€€mt°íô°)t¤)‘•˜Ñ•ÍÑ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ñ}ÑÉ•…ÑÍ}½Ñ¡•É}Ù…±Õ•Í}…Í}Õ¹­¹½Ý¸¡‰…¤è(€€€€ˆˆ‰=¹±ä‰½½°½È„É•…°¥¹Ð€À¼Ä™É½´„­¹½Ý¸…‘…ÁÑ•È‰½Õ¹‘…Éä¹½Éµ…±¥é”¸(€€€Ù•ÉåÑ¡¥¹œ•±Í”ƒŠP¥¹±Õ‘¥¹œ„µ¥ÍÍ¥¹œÙ…±Õ”°Ý¡¥ µ…äµ•…¸…¸(€€€Õ¹ÍÕÁÁ½ÉÑ•‰…­•¹…Á…‰¥±¥Ñä€¡”¹œ¸1…‘å‰Õ0ÍÉ…Á ¹}=1L¡…Ì¹¼(€€€€‰É•ÍÑÉ¥Ñ•ˆ½±Õµ¸…Ð…±°¤É…Ñ¡•ÈÑ¡…¸„•¹Õ¥¹”…±Í”ƒŠP¥ÌU9-9=]8¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð(€€€…ÍÍ•ÉÐ}¹½Éµ…±¥é•}É•ÍÑÉ¥Ñ•‘}‰¥Ð¡‰…¤¥Ì9½¹”(()‘•˜Ñ•ÍÑ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•‘}‘•¹å}‘½µ¥¹…¹Ñ}µ…ÑÉ¥à ¤è(€€€€ˆˆ‰}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡™…Ñ}É•ÍÑÉ¥Ñ•°°Í}É•ÍÑÉ¥Ñ•¤¥Ì…Íåµµ•ÑÉ¥Œ(€€€€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€Ô¤è™…Ñ}É•ÍÑÉ¥Ñ•¥Ì…±É•…‘ä0ÄÌ(€€€½¹™¥Éµ•°…ÕÑ¡½É¥Ñ…Ñ¥Ù”Ù…±Õ”‰äÑ¡”Ñ¥µ”Ñ¡¥ÌÉÕ¹Ì€¡Íå¹•‰ä(€€€‰Õ¥±‘}™…ÑÍ}Á…¬ ¤¤°Í¼„µ•É•±äµU9-9=]8½µ…±™½Éµ•½µ¥ÍÍ¥¹œ0Ì™¥•±(€€€µÕÍÐ9=P½Ù•ÉÉ¥‘”…¸0Äµ½¹™¥Éµ•…±Í”ƒŠP½¹±ä„=9%I5QÉÕ”™É½´(€€€•¥Ñ¡•ÈÍ¥‘”‰±½­Ì¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡…±Í”°…±Í”¤¥Ì…±Í”(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡QÉÕ”°…±Í”¤¥ÌQÉÕ”(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡…±Í”°QÉÕ”¤¥ÌQÉÕ”(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡QÉÕ”°QÉÕ”¤¥ÌQÉÕ”(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡…±Í”°€‰µ…±™½Éµ•ˆ¤¥Ì…±Í”€€Œ0Ä…±Í”Ý¥¹Ìì0Ì¹½Ð½¹™¥Éµ•QÉÕ”(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡…±Í”°9½¹”¤¥Ì…±Í”€€€€€€€€€Œ0Ä…±Í”Ý¥¹Ììµ¥ÍÍ¥¹œ0Ì™¥•±¥Ì¹½Ð½¹™¥Éµ•QÉÕ”(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ•¡9½¹”°9½¹”¤¥ÌQÉÕ”€€€€€€€€€€€Œ™…Ñ}É•ÍÑÉ¥Ñ•¥ÑÍ•±˜U9-9=]8ƒŠH™…¥°±½Í•‘•™•¹Í¥Ù•±ä(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}É•ÍÑÉ¥Ñ• ‰µ…±™½Éµ•ˆ°…±Í”¤¥ÌQÉÕ”€€€Œ™…Ñ}É•ÍÑÉ¥Ñ•¥ÑÍ•±˜µ…±™½Éµ•ƒŠH™…¥°±½Í•‘•™•¹Í¥Ù•±ä(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰‰…‘}™…Ñ}¥ˆ°ml‰„ˆ°€‰±¥ÍÐ‰t°ì‰„ˆè€‰‘¥Ð‰ô°€ÄÈÌ°9½¹•t¤)‘•˜Ñ•ÍÑ}°Å}Ñ•Éµ¥¹…±}ÍÑ…Ñ•}‰±½­Í}™…¥±Í}±½Í•‘}Ñ½}™…±Í•}½¹}µ…±™½Éµ•‘}™…Ñ}¥¡‰…‘}™…Ñ}¥¤è(€€€€ˆˆ‰µ…±™½Éµ•€¡¹½¸µÍÑÉ¥¹œ¤™…Ñ}¥ƒŠP”¹œ¸™É½´„½ÉÉÕÁÑ•É…Á µÝ…±¬(€€€¹½‘”ƒŠPµÕÍÐ¹½Ð‰”±½½­•ÕÀ¥¸0Ä…Ð…±°ìÑ¡”¡•±Á•ÈµÕÍÐ™…¥°±½Í•(€€€Ñ¼…±Í”€¡‘½•Ì¹½Ð…‘‘¥Ñ¥½¹…±±ä‰±½¬¤É…Ñ¡•ÈÑ¡…¸É…¥Í”½Èµ¥Í‰•¡…Ù”(€€€€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹€È¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}°Å}Ñ•Éµ¥¹…±}ÍÑ…Ñ•}‰±½­Ì(€€€…ÍÍ•ÉÐ}°Å}Ñ•Éµ¥¹…±}ÍÑ…Ñ•}‰±½­Ì¡‰…‘}™…Ñ}¥¤¥Ì…±Í”(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰‰…‘}™…Ñ}¥ˆ°ml‰„ˆ°€‰±¥ÍÐ‰t°ì‰„ˆè€‰‘¥Ð‰ô°€ÄÈÌ°9½¹•t¤)‘•˜Ñ•ÍÑ}°Å}É•ÍÑÉ¥Ñ•‘}‰±½­Í}™…¥±Í}±½Í•‘}Ñ½}™…±Í•}½¹}µ…±™½Éµ•‘}™…Ñ}¥¡‰…‘}™…Ñ}¥¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}°Å}É•ÍÑÉ¥Ñ•‘}‰±½­Ì(€€€…ÍÍ•ÉÐ}°Å}É•ÍÑÉ¥Ñ•‘}‰±½­Ì¡‰…‘}™…Ñ}¥¤¥Ì…±Í”(()‘•˜Ñ•ÍÑ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ•}µ…ÑÉ¥à ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ”°MQ=I}MQQ}=91%P(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ” ‰½±±…ÁÍ•ˆ°€‰Y…±¥‘…Ñ•ˆ¤€ôô€‰½±±…ÁÍ•ˆ(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ” ‰Y…±¥‘…Ñ•ˆ°€‰½±±…ÁÍ•ˆ¤€ôô€‰½±±…ÁÍ•ˆ(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ” ‰½¹ÑÉ…‘¥Ñ•ˆ°€‰Y…±¥‘…Ñ•ˆ¤€ôô€‰½¹ÑÉ…‘¥Ñ•ˆ(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ” ‰Y…±¥‘…Ñ•ˆ°€‰•ÁÉ•…Ñ•ˆ¤€ôô€‰•ÁÉ•…Ñ•ˆ(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ” ‰Y…±¥‘…Ñ•ˆ°€‰Y…±¥‘…Ñ•ˆ¤€ôô€‰Y…±¥‘…Ñ•ˆ(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ” ‰Y…±¥‘…Ñ•ˆ°€‰%µµÕÑ…‰±•½É”ˆ¤€ôôMQ=I}MQQ}=91%P(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰™…Ñ}ÍÑ…Ñ”±°Í}ÍÑ…Ñ”ˆ°l(€€€€¡l‰½±±…ÁÍ•‰t°€‰Y…±¥‘…Ñ•ˆ¤°(€€€€ ‰Y…±¥‘…Ñ•ˆ°l‰½±±…ÁÍ•‰t¤°(€€€€¡ì‰Ìˆè€‰½±±…ÁÍ•‰ô°€‰Y…±¥‘…Ñ•ˆ¤°)t¤)‘•˜Ñ•ÍÑ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ•}Õ¹¡…Í¡…‰±•}ÍÑ…Ñ•}™…¥±Í}±½Í•‘}Ý¥Ñ¡½ÕÑ}É…Í¡¥¹œ (€€€™…Ñ}ÍÑ…Ñ”°°Í}ÍÑ…Ñ”°(¤è(€€€€ˆˆ‰¸Õ¹¡…Í¡…‰±”™…Ñ}ÍÑ…Ñ”½°Í}ÍÑ…Ñ”€¡”¹œ¸„½ÉÉÕÁÑ•¹½‘”Ì±¥ÍÐ½‘¥Ð(€€€•Á¥ÍÑ•µ¥}ÍÑ…Ñ”¤µÕÍÐ¹½ÐÉ…¥Í”QåÁ•ÉÉ½È½ÕÐ½˜Ñ¡”Ñ•Éµ¥¹…°µÍÑ…Ñ”(€€€µ•µ‰•ÉÍ¡¥À¡•¬ƒŠP¥ÐµÕÍÐ™…±°Ñ¡É½Õ Ñ¼Ñ¡”•ÅÕ…±¥Ñä½‘¥Í…É••µ•¹Ð(€€€Á…Ñ ±¥­”…¹ä½Ñ¡•È¹½¸µÑ•Éµ¥¹…°Ù…±Õ”€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•ÜÉ½Õ¹¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ”°MQ=I}MQQ}=91%P(€€€…ÍÍ•ÉÐ}•™™•Ñ¥Ù•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ”¡™…Ñ}ÍÑ…Ñ”°°Í}ÍÑ…Ñ”¤€ôôMQ=I}MQQ}=91%P(()‘•˜Ñ•ÍÑ}Ù•É¥™¥•‘}Ù…±¥‘…Ñ•‘}°Í}¹½‘•}Ý¥Ñ¡}¹Õµ•É¥}ÍÑÉ¥¹}½¹™¥‘•¹•}‰±½­•¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰É•…±±•0Ì¹½‘”ÍÑ½É¥¹œ½¹™¥‘•¹”…Ì„¹Õµ•É¥ŒÍÑÉ¥¹œ€¡”¹œ¸™É½´„(€€€±•…ä½½ÉÉÕÁÑ•ÝÉ¥Ñ”¤µÕÍÐ¹½ÐÉ½Õ¹…¸…¹ÍÝ•ÈƒŠPÑ¡”½•É¥½¸¥¸(€€€}Í…™•}½¹™¥‘•¹”µÕÍÐÉ•©•ÐÑ¡”ÝÉ½¹œÑåÁ”‰•™½É”½¹Ù•ÉÑ¥¹œ¥Ð°¹½Ð(€€€¹½Éµ…±¥é”¥Ð¥¹Ñ¼„Ù…±¥™±½…Ð€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ô¤¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰ÍÑÉ¥¹œµ½¹™¥‘•¹”µ¹½‘”ˆ(€€€±…¥´€ô€‰„±…¥´Ý¡½Í”Á•ÉÍ¥ÍÑ•½¹™¥‘•¹”¥Ì„¹Õµ•É¥ŒÍÑÉ¥¹œˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°(€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€ˆÀ¸äˆ°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%‰ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€ˆÀ¸äˆ°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰É…Üˆ°m™±½…Ð ‰¹…¸ˆ¤°™±½…Ð ‰¥¹˜ˆ¤°™±½…Ð ˆµ¥¹˜ˆ¤°(€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€€‰9…8ˆ°€‰%¹™¥¹¥Ñäˆ°€‰¹½Ðµ„µ¹Õµ‰•Èˆ°l‰à‰ut¤)‘•˜Ñ•ÍÑ}Õ…É‘¥…¹}‰±½­Í}¹½¹}™¥¹¥Ñ•}½É}µ…±™½Éµ•‘}½¹™¥‘•¹•}Ý¥Ñ¡½ÕÑ}É…Í¡¥¹œ¡É…Ü¤è(€€€€ˆˆ‰Õ…É‘¥…¸µÕÍÐÉ•©•Ð¹½¸µ™¥¹¥Ñ”½µ…±™½Éµ•½¹™¥‘•¹”¥ÑÍ•±˜ƒŠP¹½Ð(€€€µ•É•±äÑÉÕÍÐÑ¡…Ð„…±±•È…±É•…‘äÍ…¹¥Ñ¥é•¥ÐƒŠP…¹µÕÍÐ¹•Ù•ÈÉ…Í (€€€½µÁÕÑ¥¹œÑ¡”‘¥…¹½ÍÑ¥Œ€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ð¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÕ…É‘¥…¹}‘¥…¹½Í”°UI%9}YI%Q}	1=,(€€€™…ÑÌ€ôì‰™…ÑÌˆèmì‰™…Ñ}¥ˆè€‰„ˆ°€‰±…¥´ˆè€‰Œˆ°€‰Í½ÕÉ”ˆè€‰Ìˆ°(€€€€€€€€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆèÉ…Ýõuô(€€€‘¥…œ€ôÕ…É‘¥…¹}‘¥…¹½Í”¡™…ÑÌ°mì‰™…Ñ}¥ˆè€‰„‰õt¤(€€€…ÍÍ•ÉÐ‘¥…l‰Ù•É‘¥Ð‰t€ôôUI%9}YI%Q}	1=,(€€€…ÍÍ•ÉÐ‘¥…l‰¡•­Ì‰ul‰…±±}¡…Ù•}Á½Í¥Ñ¥Ù•}½¹™¥‘•¹”‰t¥Ì…±Í”(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰É…Ý}½¹™¥‘•¹”ˆ°l(€€€™±½…Ð ‰¹…¸ˆ¤°™±½…Ð ‰¥¹˜ˆ¤°™±½…Ð ˆµ¥¹˜ˆ¤°€‰9…8ˆ°€‰¹½Ðµ„µ¹Õµ‰•Èˆ°l‰à‰t°)t¤)‘•˜Ñ•ÍÑ}Ù•É¥™¥•‘}Ù…±¥‘…Ñ•‘}°Í}¹½‘•}Ý¥Ñ¡}¹½¹}™¥¹¥Ñ•}½¹™¥‘•¹•}¹½}…¹ÍÝ•É}¹½}É…Í ¡É…Ý}½¹™¥‘•¹”¤è(€€€€ˆˆ‰µ…±™½Éµ•½¹½¸µ™¥¹¥Ñ”YI%%€¬Y…±¥‘…Ñ•0Ì¹½‘”µÕÍÐÁÉ½‘Õ”¹¼(€€€…¹ÍÝ•È…¹µÕÍÐ¹½ÐÉ…Í Ñ¡”Á¥Á•±¥¹”€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ð¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐÉÕ¸(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€±…¥´€ô˜‰„Ù•É¥™¥•±…¥´Ý¥Ñ ¹½¸™¥¹¥Ñ”½¹™¥‘•¹”íÉ…Ý}½¹™¥‘•¹”…Éôˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè€‰¹½¸µ™¥¹¥Ñ”µ½¹™¥‘•¹”ˆ°€‰±…¥´ˆè±…¥´°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆèÉ…Ý}½¹™¥‘•¹”°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°(€€€€€€€€€€€€€€€€€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€É•ÍÕ±Ð€ôÉÕ¸¡±…¥´¤€€ŒµÕÍÐ¹½ÐÉ…¥Í”((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐ€‰Õ…É‘¥…¸ˆ¥¸€¡É•ÍÕ±Ð¹•Ð ‰•ÉÉ½Èˆ¤½È€ˆˆ¤(((ŒƒŠRŠRŠR QÉ…”µ•Ñ…‘…Ñ„½¹Í¥ÍÑ•¹ä€ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ì¤ƒŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠR ()‘•˜Ñ•ÍÑ}ÑÉ…•}•Á¥ÍÑ•µ¥}ÍÑ…Ñ•}µ…Ñ¡•Í}™…Ñ}•Á¥ÍÑ•µ¥}ÍÑ…Ñ•}™½É}ÍÕ•ÍÍ™Õ±}…¹ÍÝ•È¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰½È„ÍÕ•ÍÍ™Õ°ÍÑÉ¥Ð…¹ÍÝ•È°•Ù•ÉäÑÉ…”•±•µ•¹ÐÌ•Á¥ÍÑ•µ¥}ÍÑ…Ñ”(€€€µÕÍÐµ…Ñ ¥ÑÌ½ÉÉ•ÍÁ½¹‘¥¹œ™…ÐÌI0•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ƒŠPÉÕ¸ ¤Ì(€€€‰±…¹­•ÐÁÉ½µ½Ñ•}ÑÉ…”¡ÑÉ…”°€‰Y…±¥‘…Ñ•ˆ¤…±°µÕÍÐ¹½ÐÍÕÉÙ¥Ù”¥¹Ñ¼Ñ¡”(€€€™¥¹…°ÑÉ…”™½È„™…ÐÝ¡½Í”…ÑÕ…°ÍÑ…Ñ”¥ÌÍ½µ•Ñ¡¥¹œ•±Í”€¡¡•É”è(€€€%µµÕÑ…‰±•½É”¤¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰¥µµÕÑ…‰±”µ½É”µÉ½Õ¹‘¥¹œµ™…Ðˆ(€€€±…¥´€ô€‰…¸¥µµÕÑ…‰±”½É”É½Õ¹‘¥¹œ™…Ð…‰½ÕÐÉ¥¹œé•É¼Ù…±Õ•Ìˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°(€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰%µµÕÑ…‰±•½É”ˆ°(€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%ˆ°€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°(€€€€€€€€€€€€€€€€€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°€‰É•ÍÑÉ¥Ñ•ˆè…±Í•ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰%µµÕÑ…‰±•½É”ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì¹½Ð9½¹”(€€€…ÍÍ•ÉÐm™l‰™…Ñ}¥‰t™½È˜¥¸É•ÍÕ±Ñl‰™…ÑÌ‰ut€ôôm™¥‘t(€€€…ÍÍ•ÉÐmÑl‰™…Ñ}¥‰t™½ÈÐ¥¸É•ÍÕ±Ñl‰ÑÉ…”‰ut€ôôm™¥‘t(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰™…ÑÌ‰ulÁul‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‰t€ôô€‰%µµÕÑ…‰±•½É”ˆ(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰ÑÉ…”‰ulÁul‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‰t€ôô€‰%µµÕÑ…‰±•½É”ˆ(()‘•˜Ñ•ÍÑ}É•™ÕÍ…±}ÑÉ…•}‘½•Í}¹½Ñ}É•Á½ÉÑ}…}™…±Í•}Ù…±¥‘…Ñ•‘}ÍÑ…Ñ”¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆˆ ŒÈÔÜÉ•Ù¥•ÜÉ½Õ¹€Ô¤]¡•¸•¹•É…Ñ•}…¹ÍÝ•È ¤É•™ÕÍ•Ì‰•…ÕÍ”…±°(€€€…¹‘¥‘…Ñ•Ì…É”¹½¸µ…¹½¹¥…°°Ñ¡”É•ÑÕÉ¹•ÑÉ…”µÕÍÐ¹½Ð±…¥´(€€€€‰Y…±¥‘…Ñ•ˆ™½È„™…ÐÑ¡”É•…±°‰É…¹ ‘•±¥‰•É…Ñ•±ä±•™ÐÕ¹¡…¹•(€€€€¡¡•É”èMÕÁÁ½ÉÑ•€¼UIQ=I}=YII%¤ƒŠP„‰±½­•É•ÍÁ½¹Í”µÕÍÐ¹•Ù•È(€€€±½½¬±¥­”Ù…±¥‘…Ñ¥½¸¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€™É½´½É”¹°Í}É…Á ¥µÁ½ÉÐ•Ñ}°Í}É…Á (€€€œ€ô•Ñ}°Í}É…Á  ¤(€€€™¥€ô€‰ÕÉ…Ñ½Èµ½Ù•ÉÉ¥‘”µÍÕÁÁ½ÉÑ•µÉ•™ÕÍ…°µÑÉ…”ˆ(€€€±…¥´€ô€‰„ÕÉ…Ñ½Èµ½Ù•ÉÉ¥‘”±…¥´Ñ¡…ÐµÕÍÐ¹½ÐÉ•Á½ÉÐ„Ù…±¥‘…Ñ•ÑÉ…”ˆ(€€€œ¹µ•É•}™…Ð¡ì‰™…Ñ}¥ˆè™¥°€‰±…¥´ˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰MÕÁÁ½ÉÑ•ˆ°€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰UIQ=I}=YII%‰ô¤((€€€¥Ñ•´€ôì‰¥ˆè™¥°€‰Ñ•áÐˆè±…¥´°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰½¹™¥‘•¹”ˆè€À¸ä°(€€€€€€€€€€€€‰±…¥µ}ÑåÁ”ˆè€‰]=I1}Pˆ°€‰Í½ÕÉ•}ÍÑ…ÑÕÌˆè€‰aQI90ˆ°(€€€€€€€€€€€€‰Í¥¹¥™¥…¹”ˆè€À¸Ô°€‰}Í½É”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰MÕÁÁ½ÉÑ•ˆ°(€€€€€€€€€€€€‰½É¥¥¸ˆè€‰µ•µ½Éä‰ô(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰É•ÑÉ¥•Ù”ˆ°±…µ‰‘„Ä°¬ôÌèm¥Ñ•µt¤((€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰Äˆ¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰ÑÉ…”‰t°€‰É•™ÕÍ…°µÕÍÐÍÑ¥±°…ÉÉä„ÑÉ…”™½È‘¥…¹½ÍÑ¥Ìˆ(€€€™½ÈÐ¥¸É•ÍÕ±Ñl‰ÑÉ…”‰tè(€€€€€€€…ÍÍ•ÉÐÐ¹•Ð ‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆ¤€„ô€‰Y…±¥‘…Ñ•ˆ(()‘•˜Ñ•ÍÑ}É•™ÕÍ…±}ÑÉ…•}Õ¹µ…Ñ¡•‘}•¹ÑÉå}‘½•Í}¹½Ñ}É•Á½ÉÑ}™…±Í•}Ù…±¥‘…Ñ•‘}ÍÑ…Ñ” ¤è(€€€€ˆˆ‰ÑÉ…”•¹ÑÉäÝ¥Ñ ¹¼½ÉÉ•ÍÁ½¹‘¥¹œ™…Ð¥¸™…ÑÍ}Á…¬€¡Õ¹µ…Ñ¡•½È(€€€µ…±™½Éµ•¤µÕÍÐ¹½Ð‰”±•™Ð…ÉÉå¥¹œ„ÍÑ…±”‰±…¹­•ÐµÁÉ½µ½Ñ•(€€€€‰Y…±¥‘…Ñ•ˆÍÑ…Ñ”•¥Ñ¡•ÈƒŠPÑ¡•É”¥Ì¹½Ñ¡¥¹œÑ¼Ù•É¥™ä¥Ð……¥¹ÍÐ°Í¼¥Ð(€€€µÕÍÐ¹½ÐÍ¥±•¹Ñ±ä­••À±½½­¥¹œÙ…±¥‘…Ñ•€ ŒÈÔÜ½ÉÉ•Ñ¥Ù”¡…É‘•¹¥¹œ°(€€€™½±±½ÜµÕÀ¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ•¹•É…Ñ•}…¹ÍÝ•È(€€€™…ÑÍ}Á…¬€ôì‰™…ÑÌˆèmt°€‰ÅÕ•Éäˆè€‰Äˆ°€‰Ñ½Ñ…°ˆè€Áô(€€€ÑÉ…”€ômì‰™…Ñ}¥ˆè€‰½ÉÁ¡…¸µ¹½Ðµ¥¸µ™…ÑÌµÁ…¬ˆ°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•‰õt((€€€É•ÍÕ±Ð€ô•¹•É…Ñ•}…¹ÍÝ•È¡™…ÑÍ}Á…¬°ÑÉ…”¤((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰ÑÉ…”‰ulÁul‰™…Ñ}¥‰t€ôô€‰½ÉÁ¡…¸µ¹½Ðµ¥¸µ™…ÑÌµÁ…¬ˆ(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰ÑÉ…”‰ulÁul‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‰t€„ô€‰Y…±¥‘…Ñ•ˆ(()ÁåÑ•ÍÐ¹µ…É¬¹Á…É…µ•ÑÉ¥é” ‰‰…‘}™…Ñ}¥ˆ°ml‰„ˆ°€‰±¥ÍÐ‰t°ì‰„ˆè€‰‘¥Ð‰õt¤)‘•˜Ñ•ÍÑ}É•™ÕÍ…±}ÑÉ…•}Õ¹¡…Í¡…‰±•}™…Ñ}¥‘}™…¥±Í}±½Í•‘}Ý¥Ñ¡½ÕÑ}É…Í¡¥¹œ¡‰…‘}™…Ñ}¥¤è(€€€€ˆˆ‰‘¥É•Ð•¹•É…Ñ•}…¹ÍÝ•È ¤…±±•È…¸Á…ÍÌ„™…ÐÝ¡½Í”™…Ñ}¥¥Ì…¸(€€€Õ¹¡…Í¡…‰±”±¥ÍÐ½‘¥ÐƒŠP…¹½¹¥…±Y¥•Ü½ÉÉ•Ñ±äÉ•©•ÑÌ¥Ð…Ì¹½¸´(€€€…¹½¹¥…°€¡¹½Ð„Ù…±¥¥‘•¹Ñ¥Ñä™¥•±¤°‰ÕÐÑ¡”É•™ÕÍ…°µÁ…Ñ ÑÉ…”µÍå¹Œ(€€€‘¥Ð½µÁÉ•¡•¹Í¥½¸µÕÍÐ¹½ÐÉ…Í ÑÉå¥¹œÑ¼ÕÍ”¥Ð…Ì„‘¥Ð­•ä¥¹ÍÑ•…(€€€½˜É•…¡¥¹œÑ¡”¥¹Ñ•¹‘•™…¥°µ±½Í•É•™ÕÍ…°€ ŒÈÔÜ¥¹‘•Á•¹‘•¹ÐµÉ•Ù¥•Ü(€€€É½Õ¹€È¤¸ˆˆˆ(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ•¹•É…Ñ•}…¹ÍÝ•È(€€€™…ÑÍ}Á…¬€ôì(€€€€€€€€‰™…ÑÌˆèmì‰™…Ñ}¥ˆè‰…‘}™…Ñ}¥°€‰±…¥´ˆè€‰Œˆ°€‰Í½ÕÉ”ˆè€‰Ìˆ°(€€€€€€€€€€€€€€€€€€€‰½¹™¥‘•¹”ˆè€À¸ä°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•ˆ°(€€€€€€€€€€€€€€€€€€€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆè€‰YI%%‰õt°(€€€€€€€€‰ÅÕ•Éäˆè€‰Äˆ°€‰Ñ½Ñ…°ˆè€Ä°(€€€ô(€€€ÑÉ…”€ômì‰™…Ñ}¥ˆè‰…‘}™…Ñ}¥°€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰Y…±¥‘…Ñ•‰õt((€€€É•ÍÕ±Ð€ô•¹•É…Ñ•}…¹ÍÝ•È¡™…ÑÍ}Á…¬°ÑÉ…”¤€€ŒµÕÍÐ¹½ÐÉ…¥Í”((€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰ÑÉ…”‰ulÁul‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”‰t€„ô€‰Y…±¥‘…Ñ•ˆ(((ŒƒŠRŠRŠR ‘•µ¼Í••½ÁÐµ¥¸€¡¥ÍÍÕ”€ŒØÔ¤ƒŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠR ()‘•˜Ñ•ÍÑ}ÁÉ½‘ÕÑ¥½¹}‘•™…Õ±Ñ}¡…Í}¹½}Í••‘}½ÉÁÕÌ¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰%ÍÍÕ”€ŒØÔèÝ¥Ñ¡½ÕÐY19QI%5}5=}MôÄÑ¡”É•ÑÉ¥•Ù…°½ÉÁÕÌ¥Ì•µÁÑä¸(€€€±°™…ÑÌµÕÍÐ•¹Ñ•ÈÑ¡É½Õ ¥¹•ÍÐ ¤ìÑ¡”ÁÉ½‘ÕÑ¥½¸Á¥Á•±¥¹”¥Ì±•…¸¸ˆˆˆ(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ•¹Ø ‰Y19QI%5}5=}Mˆ°€ˆÀˆ¤(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}±½…‘}‘•µ½}Í••(€€€…ÍÍ•ÉÐ}±½…‘}‘•µ½}Í•• ¤€ôômt(()‘•˜Ñ•ÍÑ}‘•µ½}Í••‘}•¹…‰±•‘}É•ÑÕÉ¹Í}™¥Ù•}™…ÑÌ¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰]¥Ñ Y19QI%5}5=}MôÄÑ¡”Í••½ÉÁÕÌÉ•ÑÕÉ¹ÌÑ¡”ÕÉ…Ñ•™…ÑÌ¸ˆˆˆ(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ•¹Ø ‰Y19QI%5}5=}Mˆ°€ˆÄˆ¤(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ}±½…‘}‘•µ½}Í••(€€€™…ÑÌ€ô}±½…‘}‘•µ½}Í•• ¤(€€€…ÍÍ•ÉÐ±•¸¡™…ÑÌ¤€ôô€Ô(€€€…ÍÍ•ÉÐ…±°¡˜¹•Ð ‰Í½ÕÉ•}ÍÑ…ÑÕÌˆ¤€ôô€‰aQI90ˆ™½È˜¥¸™…ÑÌ¤(((ŒƒŠRŠRŠR ‰Õ¥±‘}™…ÑÍ}Á…¬ƒŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠR ()‘•˜Ñ•ÍÑ}‰Õ¥±‘}™…ÑÍ}Á…­}Í­¥ÁÍ}¥Ñ•µÍ}Ý¥Ñ¡½ÕÑ}¥ ¤è(€€€™É½´½É”¹Á¥Á•±¥¹”¥µÁ½ÉÐ‰Õ¥±‘}™…ÑÍ}Á…¬(€€€Á…¬€ô‰Õ¥±‘}™…ÑÍ}Á…¬ (€€€€€€€mì‰Ñ•áÐˆè€‰¹¼¥ˆ°€‰Í½ÕÉ”ˆè€‰Ìˆ°€‰}Í½É”ˆè€À¸Ô°(€€€€€€€€€€‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆè€‰=‰Í•ÉÙ•‰õt°(€€€€€€€€‰Äˆ°(€€€€¤(€€€…ÍÍ•ÉÐÁ…­l‰™…ÑÌ‰t€ôômt(€€€…ÍÍ•ÉÐÁ…­l‰Ñ½Ñ…°‰t€ôô€À(((ŒƒŠRŠRŠR ÉÕ¸ ¤‰±½¬Á…Ñ¡Ì€¡Õ…É‘¥…¸€¼ÑÉÕÑ¡}…Ñ”É•©•Ñ¥½¸¤ƒŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠRŠR ()‘•˜Ñ•ÍÑ}ÉÕ¹}‰±½­Í}Ý¡•¹}Õ…É‘¥…¹}™…¥±Ì¡µ½¹­•åÁ…Ñ ¤è(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰Õ…É‘¥…¸ˆ°±…µ‰‘„™À°ÑÈè€¡…±Í”°€‰‰½½´ˆ¤¤(€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰ÅÕ…¹ÑÕ´•¹Ñ…¹±•µ•¹Ðˆ¤(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐ€‰Õ…É‘¥…¸è‰½½´ˆ¥¸É•ÍÕ±Ñl‰•ÉÉ½È‰t(()‘•˜Ñ•ÍÑ}ÉÕ¹}‰±½­Í}Ý¡•¹}ÑÉÕÑ¡}…Ñ•}™…¥±Ì¡µ½¹­•åÁ…Ñ ¤è(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰ÑÉÕÑ¡}…Ñ”ˆ°±…µ‰‘„™À°€¨©¬è€¡…±Í”°€‰¹½Á”ˆ¤¤(€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰9ˆ¤(€€€…ÍÍ•ÉÐÉ•ÍÕ±Ñl‰…¹ÍÝ•È‰t¥Ì9½¹”(€€€…ÍÍ•ÉÐ€‰QÉÕÑ¡…Ñ”è¹½Á”ˆ¥¸É•ÍÕ±Ñl‰•ÉÉ½È‰t(()‘•˜Ñ•ÍÑ}Á¥Á•±¥¹•}Í­¥ÁÍ}°Í}µ•É•}½¹}…Í}µ¥ÍÌ¡µ½¹­•åÁ…Ñ ¤è(€€€€ˆˆ‰%˜ÑÉ…¹Í¥Ñ¥½¹}•Í´É•Á½ÉÑÌ„Lµ¥ÍÌ‘ÕÉ¥¹œÁÉ½µ½Ñ¥½¸°Ñ¡”Á¥Á•±¥¹”Í­¥ÁÌ(€€€µ•É¥¹œÑ¡…Ð™…Ð¥¹Ñ¼Ñ¡”…¹½¸€¡¹¼ÍÑ…±”ÁÉ½µ½Ñ¥½¸¤¥¹ÍÑ•…½˜½¹Ñ¥¹Õ¥¹œÑ¼(€€€„ÍÕ•ÍÌµ•É”¸•™•¹Í”µ¥¸µ‘•ÁÑ °¹½Ð„™Õ±°…Ñ½µ¥¥ÑäÕ…É…¹Ñ•”¸ˆˆˆ(€€€™É½´½É”¥µÁ½ÉÐÁ¥Á•±¥¹”(€€€µ½¹­•åÁ…Ñ ¹Í•Ñ…ÑÑÈ¡Á¥Á•±¥¹”°€‰ÑÉ…¹Í¥Ñ¥½¹}•Í´ˆ°±…µ‰‘„€©„°€¨©¬è…±Í”¤(€€€É•ÍÕ±Ð€ôÁ¥Á•±¥¹”¹ÉÕ¸ ‰9ˆ¤(€€€€ŒQ¡”ÉÕ¸½µÁ±•Ñ•ÌÝ¥Ñ¡½ÕÐÉ…Í¡¥¹œì…¹ä™…ÐÑ¡…Ð¡¥ÐÑ¡”Lµ¥ÍÌÝ…Ì(€€€€ŒÍ­¥ÁÁ•‰•™½É”¥ÑÌÑÉÕÑ¡}ÍÑ…ÑÕÌÝ…ÌÍ•Ð€¼‰•™½É”Ñ¡”0Ìµ•É”¸(€€€…ÍÍ•ÉÐ¥Í¥¹ÍÑ…¹”¡É•ÍÕ±Ð°‘¥Ð¤(€€€…ÍÍ•ÉÐ€‰…¹ÍÝ•Èˆ¥¸É•ÍÕ±Ð(€€€™½È˜¥¸É•ÍÕ±Ð¹•Ð ‰™…ÑÌˆ°mt¤è(€€€€€€€¥˜˜¹•Ð ‰•Á¥ÍÑ•µ¥}ÍÑ…Ñ”ˆ¤€„ô€‰Y…±¥‘…Ñ•ˆè(€€€€€€€€€€€…ÍÍ•ÉÐ€‰ÑÉÕÑ¡}ÍÑ…ÑÕÌˆ¹½Ð¥¸˜(