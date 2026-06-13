# core/adapters/yaml_adapter.py
# Velantrim ExoCortex — YAML knowledge adapter (grant WP4)
#
# Parses YAML files into claim dicts that core/knowledge.py can ingest.
# Supported top-level shapes (mirrors the JSON shapes in _normalise_records):
#
#   list of strings:       ["Water boils at 100 °C", "Gold is a metal"]
#   list of dicts:         [{claim: "...", confidence: 0.9, claim_type: WORLD_FACT}]
#   dict with claims key:  {description: "...", claims: [...]}
#   single mapping:        {claim: "...", confidence: 0.9}
#
# Install: pip install "velantrim-exocortex-crystal[yaml]"
from __future__ import annotations

from typing import Any, Dict, List

try:
    import yaml as _yaml
except ImportError as _exc:  # pragma: no cover - install hint when the extra is absent
    raise ImportError(
        "YAML adapter requires PyYAML. "
        'Install with: pip install "velantrim-exocortex-crystal[yaml]"'
    ) from _exc

from core.adapters import register


# ─── Normalisation (mirrors knowledge._normalise_records, no cross-import) ───

def _norm(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, str):
        return [{"claim": data}] if data.strip() else []
    if isinstance(data, dict):
        if "claims" in data:
            return _norm(data["claims"])
        if "claim" in data:
            rec: Dict[str, Any] = {"claim": str(data["claim"]).strip()}
            for k in ("confidence", "significance", "claim_type"):
                if data.get(k) is not None:
                    rec[k] = data[k]
            return [rec] if rec["claim"] else []
        return []
    if isinstance(data, list):
        out: List[Dict[str, Any]] = []
        for item in data:
            out.extend(_norm(item))
        return out
    return []


def extract_yaml_claims(path: str) -> List[Dict[str, Any]]:
    """Load a YAML file and return a list of claim dicts."""
    with open(path, encoding="utf-8") as fh:
        data = _yaml.safe_load(fh)
    return _norm(data if data is not None else [])


register("yaml", extract_yaml_claims)
register("yml", extract_yaml_claims)
