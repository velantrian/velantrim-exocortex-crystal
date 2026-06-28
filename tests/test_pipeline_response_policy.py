"""Read-path integration tests for response_policy metadata in pipeline answers."""


def test_run_exposes_response_policy_metadata():
    from core.pipeline import run

    result = run("quantum entanglement")

    assert result.get("answer") is not None
    assert result["facts"]
    assert result["response_policy"]

    fact_ids = {f["fact_id"] for f in result["facts"]}
    policy_ids = {p["fact_id"] for p in result["response_policy"]}
    assert policy_ids == fact_ids

    first = result["response_policy"][0]
    assert first["action"] == "ASSERT"
    assert first["requires_citation"] is True
    assert "reason" in first


def test_generate_answer_exposes_hedge_for_supported_fact():
    from core.pipeline import generate_answer

    facts_pack = {
        "query": "supported claim",
        "facts": [
            {
                "fact_id": "s1",
                "claim": "Supported claims should be phrased cautiously.",
                "source": "unit-test",
                "confidence": 0.8,
                "epistemic_state": "Supported",
                "claim_type": "WORLD_FACT",
                "source_status": "EXTERNAL",
                "truth_status": "VERIFIED",
            }
        ],
    }

    result = generate_answer(facts_pack, trace=[])

    assert result["answer"] is not None
    assert result["response_policy"] == [
        {
            "fact_id": "s1",
            "action": "HEDGE",
            "reason": "Supporting evidence exists but not yet fully validated by TruthGate.",
            "requires_citation": False,
        }
    ]


def test_blocked_result_has_empty_response_policy(monkeypatch):
    from core import pipeline

    monkeypatch.setattr(pipeline, "truth_gate", lambda fp, **k: (False, "blocked"))
    result = pipeline.run("quantum entanglement")

    assert result["answer"] is None
    assert result["response_policy"] == []
