"""Tests for advisory, read-only multi-label topic facets."""

from dataclasses import FrozenInstanceError

import pytest

import core.topic_facets as topics


def test_builtin_taxonomy_is_valid_and_versioned():
    assert topics.validate_taxonomy() == {"valid": True, "errors": []}
    assert topics.TAXONOMY_VERSION == "2026-08-v1"
    assert topics.ASSIGNED_BY == "keyword-facet-v1"


@pytest.mark.parametrize(
    "taxonomy,needle",
    [
        ({}, "non-empty mapping"),
        ({"bad": {"term": 0.5}}, "invalid topic_id"),
        ({"good/topic": {}}, "non-empty mapping"),
        ({"good/topic": {" ": 0.5}}, "term must be"),
        ({"good/topic": {" AI ": 0.5, "ai": 0.7}}, "duplicate normalized term"),
        ({"good/topic": {"term": True}}, "invalid weight"),
        ({"good/topic": {"term": 0.0}}, "invalid weight"),
        ({"good/topic": {"term": 1.1}}, "invalid weight"),
        ({"good/topic": {"term": float("nan")}}, "invalid weight"),
    ],
)
def test_taxonomy_validation_reports_malformed_contracts(taxonomy, needle):
    report = topics.validate_taxonomy(taxonomy)
    assert report["valid"] is False
    assert needle in "\n".join(report["errors"])


def test_topic_facet_is_frozen_and_serializes_fresh_data():
    facet = topics.TopicFacet(
        topic_id="computing/artificial-intelligence",
        score=0.75,
        matched_terms=("ai", "machine learning"),
    )
    first = facet.to_dict()
    second = facet.to_dict()

    assert first == second
    assert first is not second
    assert first["status"] == "suggested"
    first["matched_terms"].append("mutated")
    assert second["matched_terms"] == ["ai", "machine learning"]
    assert facet.matched_terms == ("ai", "machine learning")
    with pytest.raises(FrozenInstanceError):
        facet.score = 1.0


@pytest.mark.parametrize(
    "kwargs,exc,needle",
    [
        ({"topic_id": " ", "score": 0.5, "matched_terms": ()}, ValueError, "topic_id"),
        ({"topic_id": "a/b", "score": True, "matched_terms": ()}, ValueError, "score"),
        ({"topic_id": "a/b", "score": -0.1, "matched_terms": ()}, ValueError, "score"),
        ({"topic_id": "a/b", "score": 1.1, "matched_terms": ()}, ValueError, "score"),
        ({"topic_id": "a/b", "score": float("inf"), "matched_terms": ()}, ValueError, "score"),
        ({"topic_id": "a/b", "score": 0.5, "matched_terms": []}, TypeError, "immutable tuple"),
        ({"topic_id": "a/b", "score": 0.5, "matched_terms": ("",)}, ValueError, "non-blank"),
        (
            {"topic_id": "a/b", "score": 0.5, "matched_terms": (), "assigned_by": " "},
            ValueError,
            "assigned_by",
        ),
        (
            {"topic_id": "a/b", "score": 0.5, "matched_terms": (), "taxonomy_version": " "},
            ValueError,
            "taxonomy_version",
        ),
        (
            {"topic_id": "a/b", "score": 0.5, "matched_terms": (), "status": " "},
            ValueError,
            "status",
        ),
    ],
)
def test_topic_facet_rejects_invalid_fields(kwargs, exc, needle):
    with pytest.raises(exc, match=needle):
        topics.TopicFacet(**kwargs)


def test_projection_is_immutable_explicitly_advisory_and_fresh():
    facet = topics.TopicFacet(topic_id="science/physics", score=0.8, matched_terms=("physics",))
    projection = topics.TopicProjection(facets=(facet,))

    rendered = projection.to_dict()
    assert rendered["authoritative"] is False
    assert rendered["writes_memory"] is False
    assert rendered["score_meaning"] == "topic_relevance_not_truth"
    rendered["facets"][0]["topic_id"] = "mutated"
    assert projection.facets[0].topic_id == "science/physics"

    with pytest.raises(TypeError, match="immutable tuple"):
        topics.TopicProjection(facets=[])
    with pytest.raises(ValueError, match="advisory and read-only"):
        topics.TopicProjection(facets=(), authoritative=True)
    with pytest.raises(ValueError, match="advisory and read-only"):
        topics.TopicProjection(facets=(), writes_memory=True)


def test_classifier_returns_deterministic_multilabel_english_projection():
    text = (
        "AI, machine learning and an LLM are used in software code with an API "
        "and database, while security privacy and GDPR remain explicit."
    )
    first = topics.classify_topics(text)
    second = topics.classify_topics(text)

    assert first == second
    ids = [facet.topic_id for facet in first.facets]
    assert ids == [
        "computing/software-engineering",
        "computing/security-privacy",
        "computing/artificial-intelligence",
    ]
    assert all(0.0 <= facet.score <= 1.0 for facet in first.facets)
    assert "machine learning" in first.facets[2].matched_terms
    assert first.to_dict()["authoritative"] is False


def test_classifier_handles_russian_topics_and_max_facets():
    projection = topics.classify_topics(
        "Медицина изучает болезнь, лечение и вакцину. Экология, климат, вода и засуха важны.",
        max_facets=1,
    )
    assert len(projection.facets) == 1
    assert projection.facets[0].topic_id in {
        "health/medicine",
        "environment/climate-water",
    }


def test_classifier_abstains_for_empty_unknown_or_zero_limit_input():
    assert topics.classify_topics(None).facets == ()
    assert topics.classify_topics(123).facets == ()
    assert topics.classify_topics("unrelated zephyr glyph").facets == ()
    assert topics.classify_topics("AI machine learning LLM", max_facets=0).facets == ()


@pytest.mark.parametrize("max_facets", [True, -1, 1.5])
def test_classifier_rejects_invalid_max_facets(max_facets):
    with pytest.raises(ValueError, match="max_facets"):
        topics.classify_topics("text", max_facets=max_facets)


@pytest.mark.parametrize("min_score", [True, -0.1, 1.1, float("nan"), "0.5"])
def test_classifier_rejects_invalid_min_score(min_score):
    with pytest.raises(ValueError, match="min_score"):
        topics.classify_topics("text", min_score=min_score)


def test_classifier_rejects_invalid_custom_taxonomy():
    with pytest.raises(ValueError, match="invalid topic taxonomy"):
        topics.classify_topics("text", taxonomy={"invalid": {"term": 0.5}})


def test_classifier_custom_taxonomy_has_stable_tie_order_and_phrase_boundaries():
    taxonomy = {
        "z/topic": {"machine learning": 1.0},
        "a/topic": {"machine learning": 1.0},
        "word/topic": {"ai": 1.0},
    }
    projection = topics.classify_topics(
        "Machine learning is explicit; said is not the token AI.",
        taxonomy=taxonomy,
        min_score=0.0,
    )
    assert [facet.topic_id for facet in projection.facets] == [
        "a/topic",
        "word/topic",
        "z/topic",
    ]
    assert projection.facets[1].matched_terms == ("ai",)

    no_substring = topics.classify_topics(
        "The word said contains letters but no standalone acronym.",
        taxonomy={"word/topic": {"ai": 1.0}},
        min_score=0.0,
    )
    assert no_substring.facets == ()


def test_min_score_filters_low_coverage_without_relabeling_score():
    taxonomy = {"custom/topic": {"strong": 1.0, "other": 1.0, "third": 1.0}}
    low = topics.classify_topics("strong", taxonomy=taxonomy, min_score=0.5)
    assert low.facets == ()
    kept = topics.classify_topics("strong other", taxonomy=taxonomy, min_score=0.5)
    assert len(kept.facets) == 1
    assert kept.facets[0].score == pytest.approx(0.716667)


def test_fact_projection_returns_copies_and_never_mutates_inputs():
    facts = [
        {"fact_id": "f1", "claim": "AI machine learning LLM", "truth_status": "UNVERIFIED"},
        {"fact_id": "f2", "claim": "unknown text", "truth_status": "VERIFIED"},
    ]
    original = [dict(fact) for fact in facts]

    result = topics.project_fact_topics(facts, min_score=0.0)

    assert facts == original
    assert result[0] is not facts[0]
    assert result[0]["truth_status"] == "UNVERIFIED"
    assert result[0]["topic_projection"]["writes_memory"] is False
    assert result[1]["topic_projection"]["facets"] == []


def test_fact_projection_supports_another_text_field_and_rejects_bad_input():
    result = topics.project_fact_topics(
        [{"fact_id": "f", "summary": "physics quantum energy"}],
        text_field="summary",
        min_score=0.0,
    )
    assert result[0]["topic_projection"]["facets"][0]["topic_id"] == "science/physics"

    with pytest.raises(ValueError, match="text_field"):
        topics.project_fact_topics([], text_field=" ")
    with pytest.raises(TypeError, match="every fact"):
        topics.project_fact_topics(["not-a-fact"])
