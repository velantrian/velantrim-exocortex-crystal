# core/retrieval_config.py
# Velantrim ExoCortex — tunable retrieval configuration
#
# Retrieval used to be governed by module-level constants scattered across
# core/pipeline.py and core/l3_graph.py. This module centralizes them into a
# single validated, bounded config so operators can tune recall without
# editing source — while keeping the defaults bit-identical to the historical
# constants (backwards compatibility is a hard requirement).
#
# Design:
#   - stdlib-only leaf module: imports nothing from pipeline/l3_graph (they
#     import us), so there are no cycles.
#   - Bounded validation: every knob has a closed range; unknown keys raise
#     ValueError. A config file can therefore never push retrieval into a
#     pathological regime (k=10^6, negative decay, ...).
#   - Provenance: a config loaded from a file carries `source` and `saved_at`;
#     save_config() appends a content-free audit event (sha256 of the JSON,
#     never the values themselves — they may describe operational posture).
#   - Opt-in: with no VELANTRIM_RETRIEVAL_CONFIG env var the behaviour is
#     exactly the pre-config Crystal.

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

_ENV_VAR = "VELANTRIM_RETRIEVAL_CONFIG"

# Closed ranges for every tunable knob: (min, max, type).
# k is the only integer; everything else is a float weight/threshold.
_BOUNDS: Dict[str, Any] = {
    "k":                   (1,   50,  int),
    "min_similarity":      (0.0, 1.0, float),
    "graph_walk_hops":     (0,   5,   int),
    "graph_walk_decay":    (0.0, 1.0, float),
    "significance_weight": (0.0, 2.0, float),
}

_ALLOWED_SOURCES = ("default", "manual", "imported")

# Keys a config JSON may carry besides the knobs (provenance metadata).
_META_KEYS = ("_source", "_savedAt")


@dataclass(frozen=True)
class RetrievalConfig:
    """Validated retrieval knobs. Defaults == the historical constants."""
    k: int = 3                          # top-k returned by retrieve()
    min_similarity: float = 0.05        # cosine cutoff (hash-collision noise floor)
    graph_walk_hops: int = 2            # spreading-activation depth
    graph_walk_decay: float = 0.5       # activation damping per hop
    significance_weight: float = 0.5    # salience contribution in vector_search
    source: str = "default"             # default | manual | imported
    saved_at: Optional[str] = None      # ISO timestamp from the config file

    def __post_init__(self) -> None:
        for name, (lo, hi, typ) in _BOUNDS.items():
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"retrieval config: {name} must be a number, "
                                 f"got {value!r}")
            if typ is int and not isinstance(value, int):
                raise ValueError(f"retrieval config: {name} must be an integer, "
                                 f"got {value!r}")
            if not (lo <= value <= hi):
                raise ValueError(f"retrieval config: {name}={value!r} out of "
                                 f"range [{lo}, {hi}]")
        if self.source not in _ALLOWED_SOURCES:
            raise ValueError(f"retrieval config: source={self.source!r} must be "
                             f"one of {_ALLOWED_SOURCES}")

    def to_dict(self) -> Dict[str, Any]:
        """Knobs + provenance in the on-disk JSON shape."""
        out: Dict[str, Any] = {name: getattr(self, name) for name in _BOUNDS}
        out["_source"] = self.source
        if self.saved_at is not None:
            out["_savedAt"] = self.saved_at
        return out


DEFAULTS = RetrievalConfig()


def _from_dict(data: Dict[str, Any]) -> RetrievalConfig:
    if not isinstance(data, dict):
        raise ValueError("retrieval config: JSON root must be an object")
    unknown = [key for key in data if key not in _BOUNDS and key not in _META_KEYS]
    if unknown:
        raise ValueError(f"retrieval config: unknown keys {sorted(unknown)} "
                         f"(allowed: {sorted(_BOUNDS)})")
    kwargs: Dict[str, Any] = {name: data[name] for name in _BOUNDS if name in data}
    if "_source" in data:
        kwargs["source"] = data["_source"]
    if "_savedAt" in data:
        kwargs["saved_at"] = data["_savedAt"]
    return RetrievalConfig(**kwargs)


def load_config(path: str) -> RetrievalConfig:
    """Load + validate a config JSON. Raises ValueError on any bad content."""
    with open(path, encoding="utf-8") as fh:
        return _from_dict(json.load(fh))


def save_config(cfg: RetrievalConfig, path: str, *,
                source: str = "manual") -> Dict[str, Any]:
    """
    Persist a config to JSON and append a content-free audit event: the chain
    records THAT the retrieval posture changed (sha256, source, basename) —
    never the knob values themselves.
    """
    stamped = RetrievalConfig(**{
        **{name: getattr(cfg, name) for name in _BOUNDS},
        "source": source,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    })
    payload = json.dumps(stamped.to_dict(), ensure_ascii=False, sort_keys=True,
                         indent=2) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(payload)
    # Hash the EXACT bytes written, so `sha256sum <file>` matches the audit
    # event (the trailing newline is part of the file).
    sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    from core.audit import append_event  # lazy: keep this module a leaf
    receipt = append_event("retrieval_config_saved", None, {
        "sha256": sha,
        "source": source,
        "file": os.path.basename(path),
    })
    return {"path": path, "sha256": sha, "config": stamped.to_dict(),
            "audit_seq": receipt["seq"]}


_CONFIG: Optional[RetrievalConfig] = None


def get_retrieval_config() -> RetrievalConfig:
    """
    Config singleton. With VELANTRIM_RETRIEVAL_CONFIG set, loads (and caches)
    that JSON file; otherwise returns the historical defaults.
    """
    global _CONFIG
    if _CONFIG is None:
        path = os.environ.get(_ENV_VAR, "")
        _CONFIG = load_config(path) if path else DEFAULTS
    return _CONFIG


def reset_retrieval_config() -> None:
    """Reset the singleton (for tests / config reload)."""
    global _CONFIG
    _CONFIG = None
