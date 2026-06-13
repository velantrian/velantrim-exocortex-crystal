# core/adapters/wikidata_adapter.py
# Velantrim ExoCortex — Wikidata knowledge adapter (grant WP4)
# v8.27.0-sprint6
#
# Fetches entity labels and descriptions from the Wikidata API for a list of
# Q-codes and converts them to claim dicts that core/knowledge.py can ingest.
#
# Input file format (.qids or .wikidata):
#   - Text file: one QID per line (e.g. "Q42\nQ937\n")
#     Lines starting with # are treated as comments and skipped.
#   - JSON array: ["Q42", "Q937"]
#
# Install: pip install "velantrim-exocortex-crystal[wikidata]"
from __future__ import annotations

from typing import Any, Dict, List

try:
    import requests as _requests
except ImportError as _exc:  # pragma: no cover - install hint when the extra is absent
    raise ImportError(
        "Wikidata adapter requires requests. "
        "Install with: pip install 'velantrim-exocortex-crystal[wikidata]'"
    ) from _exc

import json as _json

from core.adapters import register

_WIKIDATA_API = "https://www.wikidata.org/w/api.php"
_BATCH_SIZE = 50


def _read_qids(path: str) -> List[str]:
    """Read QIDs from a file; supports JSON array or one-per-line text format."""
    with open(path, encoding="utf-8") as fh:
        content = fh.read()

    stripped = content.strip()
    if stripped.endswith("]"):
        # JSON array format
        data = _json.loads(stripped)
        return [str(q).strip() for q in data if str(q).strip()]

    # Text format: one QID per line; skip empty lines and comments
    qids: List[str] = []
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            qids.append(line)
    return qids


def _fetch_entities(qids: List[str]) -> Dict[str, Any]:
    """Batch-fetch entity labels and descriptions from the Wikidata API.

    Processes QIDs in batches of _BATCH_SIZE (Wikidata API limit recommendation).
    Returns a merged dict of {qid: entity_data}.
    """
    all_entities: Dict[str, Any] = {}
    for i in range(0, len(qids), _BATCH_SIZE):
        batch = qids[i : i + _BATCH_SIZE]
        params = {
            "action": "wbgetentities",
            "ids": "|".join(batch),
            "props": "labels|descriptions",
            "languages": "en",
            "format": "json",
        }
        try:
            resp = _requests.get(_WIKIDATA_API, params=params, timeout=30)
        except _requests.exceptions.RequestException as exc:
            raise RuntimeError(
                f"Wikidata API request failed for batch {batch}: {exc}"
            ) from exc

        if resp.status_code != 200:
            raise RuntimeError(
                f"Wikidata API returned HTTP {resp.status_code} for batch {batch}"
            )

        data = resp.json()
        all_entities.update(data.get("entities", {}))

    return all_entities


def extract_wikidata_claims(path: str) -> List[Dict[str, Any]]:
    """Load a .qids / .wikidata file and return a list of claim dicts."""
    qids = _read_qids(path)

    # Deduplicate while preserving order
    seen: set = set()
    unique_qids: List[str] = []
    for q in qids:
        if q and q not in seen:
            seen.add(q)
            unique_qids.append(q)

    if not unique_qids:
        return []

    entities = _fetch_entities(unique_qids)

    results: List[Dict[str, Any]] = []
    for qid in unique_qids:
        entity = entities.get(qid, {})
        label_data = entity.get("labels", {}).get("en", {})
        label = label_data.get("value", "")
        if not label:
            continue  # skip entities with no English label
        desc_data = entity.get("descriptions", {}).get("en", {})
        description = desc_data.get("value", "")
        if description:
            claim = f"{label}: {description}"
        else:
            claim = label
        results.append({"claim": claim, "chunk_id": qid})

    return results


register("qids", extract_wikidata_claims)
register("wikidata", extract_wikidata_claims)
