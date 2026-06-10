# core/salience.py
# Velantrim ExoCortex — utterance salience → significance
#
# A deterministic, stdlib-only port of Eiti's eitiCalcSalience: how loudly the
# user is signalling that an utterance matters. CAPS, exclamation marks and
# importance keywords (RU/EN) multiply a base score of 1.0, capped at 4.0.
#
# Boundary (audit constraint): salience feeds ONLY the `significance` ranking
# signal — never confidence, truth_status or epistemic_state. Significance is
# "how much this matters to recall", not "how true it is" (see
# l3_graph._salience_score and fractal.anchor_strength).
#
# Privacy: callers exposing explainability metadata must use marker CATEGORIES
# (the strings below) — matched raw phrases never leave this module.

import re
from typing import Dict, List

# Marker categories: fixed vocabulary, safe to store in fact metadata.
CAPS = "CAPS"
EXCLAMATION = "EXCLAMATION"
IMPORTANCE_RU = "IMPORTANCE_RU"
IMPORTANCE_EN = "IMPORTANCE_EN"

# Each category multiplies the base salience of 1.0 (Eiti heritage: CAPS ×1.5,
# "!" ×1.3, importance keywords ×1.4 — applied once per matched category).
_RULES = [
    (CAPS,          re.compile(r"[А-ЯЁA-Z]{3,}"),                          1.5),
    (EXCLAMATION,   re.compile(r"!"),                                      1.3),
    (IMPORTANCE_RU, re.compile(
        r"важно|критично|никогда|всегда|обязательно|запомни", re.I),       1.4),
    (IMPORTANCE_EN, re.compile(
        r"\b(important|critical|never|always|must|remember)\b", re.I),     1.4),
]

_CAP = 4.0


def analyze(text: str) -> Dict[str, object]:
    """
    {"salience": float, "markers": [categories], "significance": float}.

    Plain text → salience 1.0, no markers, significance exactly 0.5 (the
    historical default — backwards compatibility is a hard requirement).
    """
    score = 1.0
    markers: List[str] = []
    for category, pattern, factor in _RULES:
        if pattern.search(text or ""):
            score *= factor
            markers.append(category)
    score = min(score, _CAP)
    return {
        "salience": round(score, 4),
        "markers": markers,
        "significance": min(1.0, round(0.5 * score, 4)),
    }


def significance_for(text: str) -> float:
    """Significance ∈ [0.5, 1.0] for an utterance (0.5 = ordinary text)."""
    return analyze(text)["significance"]
