from core.topic_facets import (
    TopicFacet,
    attach_facets,
    canonicalize_facets,
    filter_records,
    matches_facets,
    read_facets,
)


def test_topic_facet_normalizes_and_serializes():
    facet = TopicFacet("Machine Learning", 0.75, "model")
    assert facet.label == "machine-learning"
    assert facet.to_dict() == {
        "label": "machine-learning",
        "score": 0.75,
        "origin": "model",
    }


def test_canonicalization_prefers_score_then_curator_origin():
    facets = canonicalize_facets(
        [
            TopicFacet("ai", 0.4, "curator"),
            TopicFacet("ai", 0.9, "model"),
            TopicFacet("security", 0.8, "model"),
            TopicFacet("security", 0.8, "curator"),
        ]
    )
    assert facets == (
        TopicFacet("ai", 0.9, "model"),
        TopicFacet("security", 0.8, "curator"),
    )


def test_attach_facets_preserves_authority_fields_and_metadata():
    original = {
        "fact_id": "f1",
        "epistemic_state": "Validated",
        "truth_status": "grounded",
        "metadata": {"source_hash": "abc"},
    }
    updated = attach_facets(original, [TopicFacet("science")])
    assert updated["epistemic_state"] == "Validated"
    assert updated["truth_status"] == "grounded"
    assert updated["metadata"]["source_hash"] == "abc"
    assert read_facets(updated) == (TopicFacet("science"),)
    assert original["metadata"] == {"source_hash": "abc"}


def test_read_facets_ignores_malformed_entries():
    record = {
        "metadata": {
            "topic_facets": [
                {"label": "valid", "score": 0.5, "origin": "rule"},
                {"label": "INVALID LABEL!", "score": 0.5, "origin": "rule"},
                "not-a-record",
            ]
        }
    }
    assert read_facets(record) == (TopicFacet("valid", 0.5, "rule"),)


def test_matches_and_filters_are_advisory():
    records = [
        attach_facets({"fact_id": "a"}, [TopicFacet("ai", 0.9), TopicFacet("safety", 0.7)]),
        attach_facets({"fact_id": "b"}, [TopicFacet("biology", 1.0)]),
    ]
    assert matches_facets(records[0], all_of=["AI", "safety"], min_score=0.7)
    assert not matches_facets(records[0], all_of=["ai"], min_score=0.95)
    assert [item["fact_id"] for item in filter_records(records, any_of=["biology"])] == ["b"]
