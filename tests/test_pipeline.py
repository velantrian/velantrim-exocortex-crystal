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


def test_blocked_pipeline_does_not_write_to_l3_graph():
    """A fact that never passes TruthGate must not appear in canonical L3."""
    from core import pipeline
    from core.l3_graph import get_l3_graph

    pipeline.run("zxqvbnmqwerty")  # empty retrieval → blocked before promotion
    assert get_l3_graph().all_facts() == []


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

def test_tokenize_lowercases_and_strips_punctuation():
    from core.pipeline import tokenize
    assert tokenize("Hello, WORLD! (DNA)") == ["hello", "world", "dna"]


def test_normalize_score_clamps_and_guards_zero_max():
    from core.pipeline import normalize_score
    assert normalize_score(5, 0) == 0.0       # guard against div-by-zero
    assert normalize_score(2, 4) == 0.5
    assert normalize_score(10, 4) == 1.0      # clamped to 1.0


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
