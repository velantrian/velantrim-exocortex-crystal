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
    hits = retrieve("the", k=2)               # common token, several matches
    assert len(hits) <= 2
    assert all(h["epistemic_state"] == "Observed" for h in hits)
    assert retrieve("zxqvbnmqwerty") == []


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
