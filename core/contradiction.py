# core/contradiction.py
# Velantrim ExoCortex — Contradiction Detection (immune layer)
#
# find_conflicts() surfaces canonical facts that are semantically CLOSE to a new
# claim — but closeness alone cannot tell a *contradiction* ("water boils at
# 100°C" vs "water does NOT boil at 100°C") from a *refinement* ("…at sea level").
# This module adds a deterministic, dependency-free classifier that turns a
# similarity candidate into one of:
#
#   CONTRADICTION — same subject, opposite assertion (negation / antonym / number)
#   REFINEMENT    — same subject, same polarity (a duplicate or a more specific form)
#   RELATED       — topically near but no contradiction signal
#
# It is deliberately HIGH-PRECISION over high-recall: it only calls CONTRADICTION
# when (a) the two claims share enough content to be about the same thing AND
# (b) there is an explicit polarity signal. This keeps the immune response from
# firing on mere topical overlap — the long-standing concern in reconcile.py.
#
# Three orthogonal, explainable signals (stdlib only, no NLI model):
#   negation — exactly one claim carries a negation cue (not/no/n't/never/без/не…)
#   antonym  — the claims differ by a known antonym pair (hot/cold, rises/falls…)
#   numeric  — same wording but a differing key number (100°C vs 90°C)

import re
from typing import Dict, Any, Optional, Set, List

# Kinds
CONTRADICTION = "CONTRADICTION"
REFINEMENT = "REFINEMENT"
RELATED = "RELATED"

# A claim must share at least this fraction of content tokens with the other to
# be judged "about the same thing" (Jaccard over content words). Kept modest
# because in a tight antonym pair ("market is open/closed") the differing word
# is the only signal, so the subject overlap is structurally small.
_MIN_CONTENT_OVERLAP = 0.3

# Negation cues (EN + RU). 'not'/'no'/'never'… and the contracted n't (handled separately).
_NEGATIONS = {
    "not", "no", "never", "none", "cannot", "without", "nor", "neither",
    "isnt", "arent", "wasnt", "werent", "dont", "doesnt", "didnt", "wont",
    "cant", "couldnt", "shouldnt", "wouldnt", "havent", "hasnt", "hadnt",
    "не", "нет", "ни", "без", "никогда", "нельзя",
}

# Tokens with no discriminating content — ignored when measuring "same subject".
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "of", "in", "on", "at", "to", "for", "and", "or", "as", "by", "that",
    "this", "it", "its", "with", "from", "has", "have", "had", "does", "do",
    "did", "will", "would", "can", "could", "should", "than", "then",
    "которая", "это", "и", "в", "на", "с", "по",
}

# Symmetric antonym pairs → expanded into a lookup map both ways.
_ANTONYM_PAIRS = [
    ("hot", "cold"), ("increase", "decrease"), ("increases", "decreases"),
    ("rise", "fall"), ("rises", "falls"), ("rising", "falling"),
    ("increasing", "decreasing"), ("growing", "shrinking"),
    ("up", "down"), ("true", "false"), ("alive", "dead"), ("open", "closed"),
    ("before", "after"), ("more", "less"), ("high", "low"), ("higher", "lower"),
    ("positive", "negative"), ("accept", "reject"), ("enable", "disable"),
    ("enabled", "disabled"), ("on", "off"), ("win", "lose"), ("won", "lost"),
    ("present", "absent"), ("possible", "impossible"), ("safe", "unsafe"),
    ("legal", "illegal"), ("valid", "invalid"), ("expand", "contract"),
    ("faster", "slower"), ("larger", "smaller"), ("bigger", "smaller"),
    ("warm", "cool"), ("good", "bad"), ("start", "stop"), ("begins", "ends"),
    ("heavy", "light"), ("heavier", "lighter"),
    ("fast", "slow"), ("wide", "narrow"), ("thick", "thin"),
    ("tall", "short"), ("young", "old"), ("cheap", "expensive"),
    ("strong", "weak"), ("hard", "soft"), ("rough", "smooth"),
    ("dark", "bright"), ("dirty", "clean"), ("sick", "healthy"),
    ("rich", "poor"), ("happy", "sad"), ("easy", "difficult"),
    ("simple", "complex"), ("beautiful", "ugly"), ("quiet", "loud"),
]
_ANTONYMS: Dict[str, Set[str]] = {}
for _a, _b in _ANTONYM_PAIRS:
    _ANTONYMS.setdefault(_a, set()).add(_b)
    _ANTONYMS.setdefault(_b, set()).add(_a)


def _tokens(text: str) -> List[str]:
    """Lowercase word tokens; contractions like don't → dont so cues match."""
    cleaned = text.lower().replace("’", "'").replace("'", "")
    return re.findall(r"[a-zа-я0-9]+", cleaned)


def _numbers(text: str) -> Set[str]:
    """Numeric literals (ints/decimals) appearing in the text."""
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def polarity(text: str) -> int:
    """0 if the claim is affirmative, 1 if negated (parity of negation cues)."""
    count = sum(1 for t in _tokens(text) if t in _NEGATIONS)
    return count % 2


def _is_number(token: str) -> bool:
    """True for a bare integer or decimal (e.g. '100', '90.5'). Numbers are
    handled by the dedicated numeric signal, so they are not discriminating
    content tokens — dropping integers but keeping decimals would skew overlap."""
    try:
        float(token)
        return True
    except ValueError:
        return False


def _content(tokens: List[str]) -> Set[str]:
    """Discriminating tokens: drop stopwords, negation cues and bare numbers."""
    return {
        t for t in tokens
        if t not in _STOPWORDS and t not in _NEGATIONS and not _is_number(t)
    }


def _overlap(a: Set[str], b: Set[str]) -> float:
    """Jaccard overlap of two content-token sets."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def classify(
    claim_a: str,
    claim_b: str,
    *,
    similarity: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Classify the relationship between two claims (order-independent).

    Returns:
      kind            — CONTRADICTION / REFINEMENT / RELATED
      signal          — the deciding signal ("negation"/"antonym:x↔y"/"numeric"), or None
      content_overlap — Jaccard overlap of content tokens (same-subject proxy)
      similarity      — the embedding similarity passed in (echoed back), or None
    """
    ta, tb = _tokens(claim_a), _tokens(claim_b)
    ca, cb = _content(ta), _content(tb)
    overlap = round(_overlap(ca, cb), 4)

    result = {
        "kind": RELATED,
        "signal": None,
        "content_overlap": overlap,
        "similarity": similarity,
    }

    # Same-subject gate: without enough shared content, withhold any verdict.
    if overlap < _MIN_CONTENT_OVERLAP:
        return result

    # Signal 1 — antonym pair across the two claims (subject shared by overlap gate).
    for tok in ca:
        hit = _ANTONYMS.get(tok, set()) & cb
        if hit:
            result["kind"] = CONTRADICTION
            result["signal"] = f"antonym:{tok}↔{sorted(hit)[0]}"
            return result

    # Signal 2 — negation polarity mismatch (one negated, one not).
    if polarity(claim_a) != polarity(claim_b):
        result["kind"] = CONTRADICTION
        result["signal"] = "negation"
        return result

    # Signal 3 — same wording but a differing key number (e.g. 100 vs 90).
    na, nb = _numbers(claim_a), _numbers(claim_b)
    if na and nb and na != nb and overlap >= _MIN_CONTENT_OVERLAP:
        result["kind"] = CONTRADICTION
        result["signal"] = "numeric"
        return result

    # Same subject, same polarity, no antonym/number clash → a refinement/duplicate.
    result["kind"] = REFINEMENT
    return result


def is_contradiction(claim_a: str, claim_b: str, **kw) -> bool:
    """Convenience boolean wrapper around classify()."""
    return classify(claim_a, claim_b, **kw)["kind"] == CONTRADICTION
