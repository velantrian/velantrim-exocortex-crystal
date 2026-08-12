import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs" / "architecture" / "READER_RC8_RETRIEVAL_DECISION.md"
CORPUS = ROOT / "eval" / "reader_rc8_retrieval_adversarial.jsonl"

ALLOWED_REVIEW_CLASSES = {
    "SAME_PROPOSITION_CANDIDATE",
    "PARAPHRASE_CANDIDATE",
    "RELATED_CLAIM",
    "SAME_TOPIC",
    "POSSIBLE_CONTRADICTION",
    "MERELY_SIMILAR",
}

REQUIRED_STRATA = {
    "normalized_variant",
    "close_paraphrase",
    "low_lexical_overlap_paraphrase",
    "cross_lingual_paraphrase",
    "same_topic_different_claim",
    "same_entity_unrelated_predicate",
    "negation_flip",
    "modality_change",
    "quantifier_change",
    "temporal_change",
    "attribution_trap",
    "quotation_endorsement_trap",
    "exception_vs_contradiction",
    "homonym_entity_collision",
    "boilerplate_overlap",
    "numeric_threshold_change",
    "unit_conversion_equivalent",
    "jurisdiction_change",
    "conditional_scope",
}


def _cases():
    return [json.loads(line) for line in CORPUS.read_text(encoding="utf-8").splitlines() if line]


def test_rc8_decision_preserves_authority_and_storage_boundaries():
    text = DECISION.read_text(encoding="utf-8")
    normalized_lines = {" ".join(line.split()) for line in text.splitlines()}

    for invariant in (
        "retrieval match != evidence",
        "similarity != identity",
        "repetition != corroboration",
        "cross-document candidate != Canon relation",
        "candidate discovery != candidate adjudication",
    ):
        assert invariant in normalized_lines

    for marker in (
        "dedicated_reader_core=false",
        "PostgreSQL/pgvector",
        "active=false",
        "Semantic/hybrid retrieval may be compared later",
        "deterministic lexical Reader candidate-discovery baseline + benchmark runner",
        "#155",
        "#165",
        "#214",
    ):
        assert marker in text


def test_rc8_adversarial_corpus_is_bounded_unique_and_complete():
    cases = _cases()
    assert len(cases) == 20
    assert len({case["case_id"] for case in cases}) == len(cases)
    assert REQUIRED_STRATA <= {case["stratum"] for case in cases}
    assert {case["expected_review_class"] for case in cases} == ALLOWED_REVIEW_CLASSES
    for case in cases:
        assert set(case) == {
            "case_id",
            "stratum",
            "left",
            "right",
            "expected_review_class",
            "note",
        }
        assert case["case_id"].startswith("rc8-")
        assert case["left"].strip()
        assert case["right"].strip()
        assert case["note"].strip()


def test_rc8_corpus_contains_hard_identity_traps():
    by_stratum = {case["stratum"]: case for case in _cases()}
    assert by_stratum["negation_flip"]["expected_review_class"] == "POSSIBLE_CONTRADICTION"
    assert by_stratum["homonym_entity_collision"]["expected_review_class"] == "MERELY_SIMILAR"
    assert by_stratum["same_topic_different_claim"]["expected_review_class"] == "SAME_TOPIC"
    assert by_stratum["cross_lingual_paraphrase"]["expected_review_class"] == "PARAPHRASE_CANDIDATE"
    assert by_stratum["attribution_trap"]["expected_review_class"] == "RELATED_CLAIM"
