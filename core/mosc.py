# core/mosc.py
# Velantrim ExoCortex — MOSC advisory claim-type classifier
#
# MOSC (Memory-Oriented Semantic Classifier) suggests a claim_type for an
# utterance from weighted RU/EN keywords. It is ADVISORY by design:
#
#   - classify() returns None below threshold — the historical regex fallback
#     in core/ingest.classify_claim() then decides;
#   - it runs BEFORE the gates and only proposes a modality label; it never
#     writes to L3, never touches truth_status or epistemic_state;
#   - WORLD_FACT is never suggested — it stays the fallback default, so MOSC
#     can only move an utterance toward the subjective/interpretive types,
#     which face the SAME TruthGate rules as before.
#
# Weights ship as package data (core/_mosc/claim_keywords.json). An operator
# may override them via VELANTRIM_MOSC_PATH; such an override is recorded in
# the audit chain as a content-free sha256 event, so weight changes are
# tamper-evident without copying keyword lists (which an operator may consider
# operational posture) into the log.

import hashlib
import json
import os
import re
from importlib import resources
from typing import Any, Dict, List, Optional, Tuple

from core.memory import CLAIM_TYPES

_ENV_VAR = "VELANTRIM_MOSC_PATH"
_PKG = "core._mosc"
_DEFAULT_NAME = "claim_keywords.json"

# Deterministic tie-break, mirroring the historical regex marker order
# (specific → general). Unlisted types sort after these, alphabetically.
_TIE_ORDER = ["EMOTION", "OPINION", "GOAL", "PREFERENCE", "INTERPRETATION"]


def _validate(data: Any) -> Dict[str, Any]:
    """Validate a weights document; ValueError on any structural problem."""
    if not isinstance(data, dict) or not isinstance(data.get("keywords"), dict) \
            or not data["keywords"]:
        raise ValueError("mosc: weights JSON must be an object with a "
                         "non-empty 'keywords' mapping")
    threshold = data.get("threshold", 0.6)
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) \
            or not (0.0 < threshold <= 5.0):
        raise ValueError(f"mosc: threshold={threshold!r} must be a number "
                         f"in (0, 5]")
    for keyword, mapping in data["keywords"].items():
        if not isinstance(keyword, str) or not keyword.strip():
            raise ValueError(f"mosc: empty keyword {keyword!r}")
        if not isinstance(mapping, dict) or not mapping:
            raise ValueError(f"mosc: keyword {keyword!r} must map to "
                             f"{{claim_type: weight}}")
        for claim_type, weight in mapping.items():
            if claim_type not in CLAIM_TYPES:
                raise ValueError(f"mosc: keyword {keyword!r} names invalid "
                                 f"claim_type {claim_type!r} "
                                 f"(allowed: {sorted(CLAIM_TYPES)})")
            if isinstance(weight, bool) or not isinstance(weight, (int, float)) \
                    or not (0.0 < weight <= 1.0):
                raise ValueError(f"mosc: keyword {keyword!r} weight {weight!r} "
                                 f"must be in (0, 1]")
    return data


class Mosc:
    """Validated keyword weights + deterministic scoring."""

    def __init__(self, raw_text: str, source: str) -> None:
        data = _validate(json.loads(raw_text))
        self.source = source                      # 'package' or the env path
        self.sha256 = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        self.threshold: float = float(data["threshold"])
        self.version = data.get("version")
        self.keywords: Dict[str, Dict[str, float]] = data["keywords"]
        # Single words match on word boundaries; keywords with a space match
        # as substrings (allows RU stems like 'я чувству' → 'я чувствую').
        self._patterns: List[Tuple[re.Pattern, Dict[str, float]]] = [
            (re.compile(re.escape(kw) if " " in kw else rf"\b{re.escape(kw)}\b",
                        re.IGNORECASE),
             mapping)
            for kw, mapping in self.keywords.items()
        ]

    def score(self, text: str) -> Dict[str, float]:
        """Summed keyword weights per claim type (only matched types appear)."""
        scores: Dict[str, float] = {}
        for pattern, mapping in self._patterns:
            if pattern.search(text or ""):
                for claim_type, weight in mapping.items():
                    scores[claim_type] = round(
                        scores.get(claim_type, 0.0) + weight, 6)
        return scores

    def _best(self, text: str) -> Tuple[Optional[str], float, Dict[str, float]]:
        scores = self.score(text)
        if not scores:
            return None, 0.0, scores

        def rank(ct: str) -> Tuple[float, int, str]:
            tie = _TIE_ORDER.index(ct) if ct in _TIE_ORDER else len(_TIE_ORDER)
            return (-scores[ct], tie, ct)

        best = sorted(scores, key=rank)[0]
        return best, scores[best], scores

    def classify(self, text: str) -> Optional[str]:
        """Suggested claim_type, or None below threshold (caller falls back)."""
        best, best_score, _ = self._best(text)
        return best if best is not None and best_score >= self.threshold else None


_MOSC: Optional[Mosc] = None


def _load() -> Mosc:
    path = os.environ.get(_ENV_VAR, "")
    if path:
        with open(path, encoding="utf-8") as fh:
            mosc = Mosc(fh.read(), source=path)
        _audit_override(mosc)
        return mosc
    raw = resources.files(_PKG).joinpath(_DEFAULT_NAME).read_text(encoding="utf-8")
    return Mosc(raw, source="package")


def _audit_override(mosc: Mosc) -> None:
    """Record an operator weights override in the audit chain — content-free
    (sha256 + counts), and only when the hash differs from the last recorded
    one, so re-loading the same file does not spam the log. The bundled
    package defaults are not audited: they are part of the released code."""
    from core.audit import append_event, audit_log
    last = None
    for entry in audit_log():
        if entry["event"] == "mosc_weights_loaded":
            last = entry["detail"].get("sha256")
    if last == mosc.sha256:
        return
    append_event("mosc_weights_loaded", None, {
        "sha256": mosc.sha256,
        "source": "env_override",
        "keywords": len(mosc.keywords),
        "threshold": mosc.threshold,
    })


def get_mosc() -> Mosc:
    """MOSC singleton (package weights, or VELANTRIM_MOSC_PATH override)."""
    global _MOSC
    if _MOSC is None:
        _MOSC = _load()
    return _MOSC


def reset_mosc() -> None:
    """Reset the singleton (for tests / weight reload)."""
    global _MOSC
    _MOSC = None


def classify(text: str) -> Optional[str]:
    """Advisory claim_type suggestion; None below threshold."""
    return get_mosc().classify(text)


def classify_detailed(text: str) -> Dict[str, Any]:
    """
    Diagnostic path (tests / CLI): how the suggestion was made.

    {"method": "mosc" | "fallback", "score": float,
     "matched_categories": {claim_type: score}, "claim_type": str}

    "fallback" means MOSC abstained and the regex classifier decided.
    """
    mosc = get_mosc()
    best, best_score, scores = mosc._best(text)
    if best is not None and best_score >= mosc.threshold:
        return {"method": "mosc", "score": best_score,
                "matched_categories": scores, "claim_type": best}
    from core.ingest import _regex_classify
    return {"method": "fallback", "score": best_score,
            "matched_categories": scores, "claim_type": _regex_classify(text)}


def report() -> Dict[str, Any]:
    """Active weights provenance: source, sha256, counts (content-free)."""
    mosc = get_mosc()
    return {"source": mosc.source, "sha256": mosc.sha256,
            "version": mosc.version, "threshold": mosc.threshold,
            "keywords": len(mosc.keywords)}
