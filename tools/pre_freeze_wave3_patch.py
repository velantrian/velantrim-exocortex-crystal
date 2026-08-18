from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {count}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_memory_schema() -> None:
    replace_once(
        "core/memory.py",
        '''        source_sha256 TEXT,\n        claim_sha256  TEXT NOT NULL,\n        created_at    TEXT NOT NULL\n''',
        '''        source_sha256 TEXT,\n        claim_sha256  TEXT NOT NULL,\n        lineage_id    TEXT,\n        independence_class TEXT NOT NULL DEFAULT 'UNKNOWN',\n        lineage_basis TEXT NOT NULL DEFAULT 'UNKNOWN',\n        created_at    TEXT NOT NULL\n''',
    )
    replace_once(
        "core/memory.py",
        '''_EVIDENCE_MIGRATIONS = [\n    ("section", "TEXT"),  # human-readable source location (heading/page/section)\n]\n''',
        '''_EVIDENCE_MIGRATIONS = [\n    ("section", "TEXT"),  # human-readable source location (heading/page/section)\n    ("lineage_id", "TEXT"),\n    ("independence_class", "TEXT NOT NULL DEFAULT 'UNKNOWN'"),\n    ("lineage_basis", "TEXT NOT NULL DEFAULT 'UNKNOWN'"),\n]\n''',
    )
    replace_once(
        "core/memory.py",
        '''# database. Version 1 covers the revision CAS token added in #244; version 2\n# adds durable audit/provenance chain checkpoints. Future schema changes must\n# increment this value.\n_SCHEMA_VERSION = 2\n''',
        '''# database. Version 1 covers the revision CAS token added in #244; version 2\n# adds durable audit/provenance chain checkpoints; version 3 adds unknown-by-default\n# evidence lineage metadata. Future schema changes must increment this value.\n_SCHEMA_VERSION = 3\n''',
    )


def patch_evidence() -> None:
    replace_once(
        "core/evidence.py",
        "import hashlib\nimport uuid\n",
        "import hashlib\nimport re\nimport uuid\n",
    )
    replace_once(
        "core/evidence.py",
        '''from core import memory\n\n\ndef _now() -> str:\n''',
        '''from core import memory\n\n_LINEAGE_CLASSES = frozenset({"UNKNOWN", "SAME_LINEAGE", "INDEPENDENT_ASSERTED"})\n_LINEAGE_BASES = frozenset({"UNKNOWN", "CURATOR_ASSERTED", "PUBLISHER_DECLARED", "IMPORTER_DECLARED"})\n_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")\n\n\ndef _now() -> str:\n''',
    )
    replace_once(
        "core/evidence.py",
        '''    source_text: Optional[str] = None,\n    source_sha256: Optional[str] = None,\n) -> Dict[str, Any]:\n''',
        '''    source_text: Optional[str] = None,\n    source_sha256: Optional[str] = None,\n    lineage_id: Optional[str] = None,\n    independence_class: str = "UNKNOWN",\n    lineage_basis: str = "UNKNOWN",\n) -> Dict[str, Any]:\n''',
    )
    replace_once(
        "core/evidence.py",
        '''    if source_sha256 is None and source_text is not None:\n        source_sha256 = sha256(source_text)\n\n    row = {\n''',
        '''    if source_sha256 is None and source_text is not None:\n        source_sha256 = sha256(source_text)\n    if independence_class not in _LINEAGE_CLASSES:\n        raise ValueError(f"attach_evidence: invalid independence_class {independence_class!r}")\n    if lineage_basis not in _LINEAGE_BASES:\n        raise ValueError(f"attach_evidence: invalid lineage_basis {lineage_basis!r}")\n    if independence_class != "UNKNOWN" and not (isinstance(lineage_id, str) and lineage_id.strip()):\n        raise ValueError("attach_evidence: non-UNKNOWN independence requires lineage_id")\n    if independence_class != "UNKNOWN" and lineage_basis == "UNKNOWN":\n        raise ValueError("attach_evidence: non-UNKNOWN independence requires an assertion basis")\n\n    row = {\n''',
    )
    replace_once(
        "core/evidence.py",
        '''        "source_sha256": source_sha256,\n        "claim_sha256":  sha256(claim_text),\n        "created_at":    _now(),\n''',
        '''        "source_sha256": source_sha256,\n        "claim_sha256":  sha256(claim_text),\n        "lineage_id":    lineage_id.strip() if isinstance(lineage_id, str) and lineage_id.strip() else None,\n        "independence_class": independence_class,\n        "lineage_basis": lineage_basis,\n        "created_at":    _now(),\n''',
    )
    replace_once(
        "core/evidence.py",
        '''            "source_kind, chunk_id, section, span_start, span_end, source_sha256, "\n            "claim_sha256, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\n            (row["evidence_id"], row["fact_id"], row["source_uri"],\n             row["source_kind"], row["chunk_id"], row["section"],\n             row["span_start"], row["span_end"], row["source_sha256"],\n             row["claim_sha256"], row["created_at"]),\n''',
        '''            "source_kind, chunk_id, section, span_start, span_end, source_sha256, "\n            "claim_sha256, lineage_id, independence_class, lineage_basis, created_at) "\n            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",\n            (row["evidence_id"], row["fact_id"], row["source_uri"],\n             row["source_kind"], row["chunk_id"], row["section"],\n             row["span_start"], row["span_end"], row["source_sha256"],\n             row["claim_sha256"], row["lineage_id"], row["independence_class"],\n             row["lineage_basis"], row["created_at"]),\n''',
    )
    replace_once(
        "core/evidence.py",
        '''            "section, span_start, span_end, source_sha256, claim_sha256, created_at "\n''',
        '''            "section, span_start, span_end, source_sha256, claim_sha256, "\n            "lineage_id, independence_class, lineage_basis, created_at "\n''',
    )
    replace_once(
        "core/evidence.py",
        '''def has_evidence(fact_id: str) -> bool:\n    """True if at least one source-span evidence record is attached to the fact."""\n    return bool(evidence_for(fact_id))\n''',
        '''def has_evidence(fact_id: str) -> bool:\n    """True if at least one source-span evidence record is attached to the fact."""\n    return bool(evidence_for(fact_id))\n\n\ndef _valid_source_location(span: Dict[str, Any]) -> bool:\n    start, end = span.get("span_start"), span.get("span_end")\n    if isinstance(start, int) and not isinstance(start, bool) and isinstance(end, int) and not isinstance(end, bool):\n        return 0 <= start <= end\n    return bool(span.get("chunk_id") or span.get("section"))\n\n\ndef valid_evidence_for_grounding(fact_id: str) -> List[Dict[str, Any]]:\n    """Replayable evidence eligible for grant-profile strict factual grounding.\n\n    A source label is not enough: require a non-blank URI, sealed source digest,\n    current-claim binding, and a bounded source location. This is a read predicate;\n    it never promotes a fact or fabricates legacy spans.\n    """\n    fact = memory.get_fact(fact_id)\n    if fact is None or fact.get("restricted"):\n        return []\n    claim_digest = sha256(fact.get("claim", ""))\n    valid: List[Dict[str, Any]] = []\n    for span in evidence_for(fact_id):\n        uri = span.get("source_uri")\n        digest = span.get("source_sha256")\n        if not isinstance(uri, str) or not uri.strip():\n            continue\n        if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:\n            continue\n        if span.get("claim_sha256") != claim_digest:\n            continue\n        if not _valid_source_location(span):\n            continue\n        valid.append(span)\n    return valid\n\n\ndef has_valid_evidence_for_grounding(fact_id: str) -> bool:\n    return bool(valid_evidence_for_grounding(fact_id))\n\n\ndef lineage_metrics(fact_ids: List[str]) -> Dict[str, float | int]:\n    """Honest, unknown-preserving lineage coverage for a retrieved evidence set."""\n    rows = [span for fid in fact_ids for span in evidence_for(fid)]\n    total = len(rows)\n    if total == 0:\n        return {\n            "evidence_count": 0, "known_lineage_coverage": 0.0,\n            "same_lineage_duplicate_rate": 0.0, "unique_lineage_count": 0,\n            "independence_assertion_coverage": 0.0, "unknown_lineage_rate": 0.0,\n        }\n    known = [r for r in rows if r.get("lineage_id") and r.get("independence_class") != "UNKNOWN"]\n    independent = [r for r in rows if r.get("independence_class") == "INDEPENDENT_ASSERTED"]\n    unknown = [r for r in rows if r.get("independence_class") == "UNKNOWN"]\n    seen: set[str] = set()\n    duplicate = 0\n    for row in known:\n        lineage = row["lineage_id"]\n        if lineage in seen:\n            duplicate += 1\n        else:\n            seen.add(lineage)\n    return {\n        "evidence_count": total,\n        "known_lineage_coverage": len(known) / total,\n        "same_lineage_duplicate_rate": duplicate / total,\n        "unique_lineage_count": len(seen),\n        "independence_assertion_coverage": len(independent) / total,\n        "unknown_lineage_rate": len(unknown) / total,\n    }\n''',
    )


def patch_query_grounding() -> None:
    replace_once(
        "core/query_pipeline.py",
        "from core.embedding import get_embedder\n",
        "from core.embedding import get_embedder\nfrom core.evidence import has_valid_evidence_for_grounding\n",
    )
    replace_once(
        "core/query_pipeline.py",
        '''    facts = _resolve_retrieval_hits(retrieved)\n    if not facts:\n        return _blocked(\n            "Insufficient grounding: retrieval found no existing graph facts.",\n            query_text,\n            reason_code="no_canonical_retrieval_results",\n            episode_requested=episode is not None,\n            retrieval=legacy,\n        )\n\n    config_id = _retrieval_config_id()\n''',
        '''    facts = _resolve_retrieval_hits(retrieved)\n    if not facts:\n        return _blocked(\n            "Insufficient grounding: retrieval found no existing graph facts.",\n            query_text,\n            reason_code="no_canonical_retrieval_results",\n            episode_requested=episode is not None,\n            retrieval=legacy,\n        )\n\n    if _grant_profile_enabled():\n        verified_before = [f for f in facts if f.get("truth_status") == "VERIFIED"]\n        facts = [\n            f for f in facts\n            if f.get("truth_status") != "VERIFIED"\n            or has_valid_evidence_for_grounding(f["fact_id"])\n        ]\n        if verified_before and not any(f.get("truth_status") == "VERIFIED" for f in facts):\n            return _blocked(\n                "Insufficient grounding: VERIFIED facts lack valid replayable evidence spans.",\n                query_text,\n                reason_code="insufficient_grounding_missing_verified_evidence",\n                episode_requested=episode is not None,\n                retrieval=legacy,\n            )\n\n    config_id = _retrieval_config_id()\n''',
    )


def patch_reconcile() -> None:
    replace_once("core/reconcile.py", "import logging\n", "import logging\nimport os\n")
    replace_once(
        "core/reconcile.py",
        '''def reinforce(fact_id: str, agreement: bool = True) -> Optional[float]:\n''',
        '''def reinforce(\n    fact_id: str,\n    agreement: bool = True,\n    *,\n    lineage_id: Optional[str] = None,\n) -> Optional[float]:\n''',
    )
    replace_once(
        "core/reconcile.py",
        '''    agreement=False → confidence *= obs / (obs + 1)               — decaying decline.\n    The observation counter is stored in metadata['observations'].\n    """\n    for attempt in range(_CAS_MAX_ATTEMPTS):\n''',
        '''    agreement=False → confidence *= obs / (obs + 1)               — decaying decline.\n    The observation counter is stored in metadata['observations'].\n\n    ``lineage_id`` identifies the evidence family that caused this explicit\n    reinforcement. In the grant profile it is mandatory. Reusing an already\n    counted lineage is idempotent: it cannot increase observations or confidence.\n    Outside the grant profile a missing lineage remains backward-compatible but\n    is recorded as UNKNOWN rather than being represented as independent evidence.\n    """\n    normalized_lineage = lineage_id.strip() if isinstance(lineage_id, str) and lineage_id.strip() else None\n    grant_profile = os.environ.get("VELANTRIM_RELEASE_PROFILE", "").strip().casefold() == "grant"\n    if grant_profile and normalized_lineage is None:\n        raise ValueError("reinforce: grant profile requires lineage_id")\n\n    for attempt in range(_CAS_MAX_ATTEMPTS):\n''',
    )
    replace_once(
        "core/reconcile.py",
        '''        meta = dict(fact.get("metadata") or {})\n        obs = int(meta.get("observations", 1))\n        conf = float(fact.get("confidence", 0.5))\n\n        if agreement:\n''',
        '''        meta = dict(fact.get("metadata") or {})\n        counted_lineages = {\n            value for value in (meta.get("reinforcement_lineages") or [])\n            if isinstance(value, str) and value\n        }\n        if normalized_lineage is not None and normalized_lineage in counted_lineages:\n            return float(fact.get("confidence", 0.5))\n\n        obs = int(meta.get("observations", 1))\n        conf = float(fact.get("confidence", 0.5))\n\n        if agreement:\n''',
    )
    replace_once(
        "core/reconcile.py",
        '''        meta["observations"] = obs + 1\n        meta["last_consolidated"] = _now()  # reinforcement resets the decay clock\n''',
        '''        meta["observations"] = obs + 1\n        if normalized_lineage is not None:\n            counted_lineages.add(normalized_lineage)\n            meta["reinforcement_lineages"] = sorted(counted_lineages)\n            meta["last_reinforcement_lineage"] = normalized_lineage\n        else:\n            meta["reinforcement_lineage_status"] = "UNKNOWN"\n        meta["last_consolidated"] = _now()  # reinforcement resets the decay clock\n''',
    )


def write_wave3_tests() -> None:
    (ROOT / "tests/test_pre_freeze_wave3.py").write_text('''from __future__ import annotations\n\nimport pytest\n\nfrom core import embedding, evidence, query_pipeline, reconcile\nfrom core.l3_graph import MockL3Graph\nfrom core.memory import get_fact, store_fact, transition_esm\n\n\ndef _stored_verified(fid="f1", claim="alpha beta", source="file://source.txt"):\n    store_fact({\n        "fact_id": fid, "claim": claim, "source": source, "confidence": 0.9,\n        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",\n    })\n    transition_esm(fid, "Validated")\n    return get_fact(fid)\n\n\ndef test_valid_grounding_evidence_requires_digest_claim_binding_and_location():\n    fact = _stored_verified()\n    evidence.attach_evidence(\n        fact["fact_id"], "file://source.txt", source_text="source content",\n        span_start=0, span_end=6,\n    )\n    assert evidence.has_valid_evidence_for_grounding(fact["fact_id"])\n\n\ndef test_bare_source_label_or_unsealed_evidence_is_not_grant_grounding():\n    fact = _stored_verified("f2")\n    evidence.attach_evidence(fact["fact_id"], "file://source.txt", span_start=0, span_end=6)\n    assert not evidence.has_valid_evidence_for_grounding(fact["fact_id"])\n\n\ndef test_lineage_defaults_unknown_and_metrics_do_not_infer_independence():\n    fact = _stored_verified("f3")\n    evidence.attach_evidence(\n        fact["fact_id"], "file://a", source_text="a", span_start=0, span_end=1,\n    )\n    evidence.attach_evidence(\n        fact["fact_id"], "file://b", source_text="b", span_start=0, span_end=1,\n        lineage_id="family:1", independence_class="SAME_LINEAGE",\n        lineage_basis="IMPORTER_DECLARED",\n    )\n    rows = evidence.evidence_for(fact["fact_id"])\n    assert rows[0]["independence_class"] == "UNKNOWN"\n    metrics = evidence.lineage_metrics([fact["fact_id"]])\n    assert metrics["unknown_lineage_rate"] == pytest.approx(0.5)\n    assert metrics["independence_assertion_coverage"] == 0.0\n\n\ndef test_reinforce_same_lineage_is_idempotent():\n    _stored_verified("f4")\n    first = reconcile.reinforce("f4", lineage_id="family:one")\n    after_first = get_fact("f4")["metadata"]["observations"]\n    second = reconcile.reinforce("f4", lineage_id="family:one")\n    assert second == first\n    assert get_fact("f4")["metadata"]["observations"] == after_first\n    assert get_fact("f4")["metadata"]["reinforcement_lineages"] == ["family:one"]\n\n\ndef test_grant_profile_reinforce_requires_lineage(monkeypatch):\n    _stored_verified("f5")\n    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")\n    with pytest.raises(ValueError, match="requires lineage_id"):\n        reconcile.reinforce("f5")\n\n\ndef test_grant_query_refuses_verified_fact_without_valid_span(monkeypatch):\n    fact = _stored_verified("f6", claim="grant alpha")\n    graph = MockL3Graph()\n    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")\n    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")\n    embedding.reset_embedder()\n    node = dict(fact)\n    node["truth_status"] = "VERIFIED"\n    graph.merge_fact(node)\n    graph.set_embedder_fingerprint(embedding.get_embedder().id)\n    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)\n    monkeypatch.setattr("core.pipeline.get_l3_graph", lambda: graph)\n\n    result = query_pipeline.query("grant alpha")\n    assert result["answer"] is None\n    assert result["reason_code"] == "insufficient_grounding_missing_verified_evidence"\n\n    evidence.attach_evidence(\n        "f6", "file://grant.txt", source_text="grant source", span_start=0, span_end=5,\n    )\n    result = query_pipeline.query("grant alpha")\n    assert result["answer"] is not None\n''', encoding="utf-8")


def main() -> None:
    patch_memory_schema()
    patch_evidence()
    patch_query_grounding()
    patch_reconcile()
    write_wave3_tests()


if __name__ == "__main__":
    main()
