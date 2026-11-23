"""Regression: ingest() result must not share nested objects with L0.

transition_esm_if_unchanged() caches the refreshed record in L0 and returns
it to ingest(), which hands it out as result["fact"]. A shallow copy kept the
metadata dict shared, so mutating the ingest result changed later get_fact()
reads without any write.
"""
from core import ingest, memory


def test_ingest_result_metadata_not_shared_with_l0():
    result = ingest.ingest("Вода кипит при 100 градусах по Цельсию.")
    assert result["accepted"] is True
    fact = result["fact"]
    fid = fact["fact_id"]
    cached = memory._L0.get(fid)
    assert cached is not None
    assert fact is not cached
    assert fact["metadata"] is not cached["metadata"]

    fact["metadata"]["restricted"] = True
    assert "restricted" not in memory.get_fact(fid)["metadata"]
