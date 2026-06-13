# core/embedding.py
# Velantrim ExoCortex — Embedding Layer (pluggable abstraction)
#
# Purpose: turn the text of a claim / query into a vector for semantic search
# (vector retrieval) — a cure for "understanding via surface tokens".
#
# Pluggable backend:
#   HashingEmbedder (default) — dependency-free, deterministic. This is NOT
#     neural semantics: the features are lexical (words + char trigrams) with
#     stop-word removal. It fixes the stop-word ranking bug and gives a working
#     vector pipeline. For real semantics ("Sun" ~ "solar") enable the model below.
#   SentenceTransformerEmbedder — real embeddings (optional dependency,
#     lazy import). Enabled with VELANTRIM_EMBEDDER=sbert.
#
# ⚠️ Do not mix embedders on a single persistent L3 store: vectors from hashing
# and sbert are not cosine-comparable. Pick one backend per store. (The full
# guard — embedder tag on the node + check at search time — is deferred, see ROADMAP.)
#
# Important: the hash is stable (hashlib), not the built-in hash() — otherwise the
# vectors would not reproduce across processes and L3 persistence would break.

import hashlib
import logging
import math
import os
import re
from abc import ABC, abstractmethod
from typing import List, Optional

from core._registry import BackendRegistry

logger = logging.getLogger(__name__)


class EmbedderMismatchError(Exception):
    """Raised (strict mode) when a store's vectors were built with a different
    embedder than the active one — their cosine similarities are meaningless."""

# Vector dimensionality. Fixed: the L3 graph stores FLOAT[EMBED_DIM].
# The larger it is, the rarer the hashing-trick collisions between different words
# (at the cost of size). 2048 is chosen so the default demo corpus is collision-free.
EMBED_DIM = 2048

# A small stop list: function words that cannot be used to rank meaning.
STOPWORDS = {
    "a", "an", "the", "of", "to", "in", "on", "at", "is", "are", "am", "be",
    "was", "were", "and", "or", "but", "if", "then", "this", "that", "these",
    "those", "it", "its", "as", "by", "for", "with", "about", "into", "from",
    "me", "my", "you", "your", "i", "we", "us", "he", "she", "they", "them",
    "tell", "how", "what", "why", "when", "where", "who", "does", "do", "did",
    "can", "could", "would", "should", "will", "has", "have", "had",
}

_WORD_RE = re.compile(r"[a-zа-я0-9]+", re.IGNORECASE)


def _tokens(text: str) -> List[str]:
    """Lowercased words without stop words."""
    return [w.lower() for w in _WORD_RE.findall(text)
            if w.lower() not in STOPWORDS]


def _stable_bucket(feature: str) -> tuple[int, float]:
    """
    Deterministic (index, sign) for a feature via md5.
    The signed hashing trick reduces the impact of collisions.
    """
    h = hashlib.md5(feature.encode("utf-8"), usedforsecurity=False).digest()
    idx = int.from_bytes(h[:4], "big") % EMBED_DIM
    sign = 1.0 if (h[4] & 1) else -1.0
    return idx, sign


def cosine(a: List[float], b: List[float]) -> float:
    """Cosine similarity of two vectors (0.0 when the norm is zero)."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


# ─── INTERFACE ────────────────────────────────────────────────────────────────

class Embedder(ABC):
    """Embedder contract: text → vector of fixed dimensionality EMBED_DIM."""

    dim: int = EMBED_DIM
    # Stable embedder identifier: everything that makes vectors NOT comparable by
    # cosine (family, model, dimensionality). Stored on nodes/store to guard
    # against mixing embedders (assert_compatible_embedder).
    id: str = "embedder"

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Vector of length self.dim, L2-normalized."""


# ─── HASHING EMBEDDER (default, dependency-free) ──────────────────────────────

class HashingEmbedder(Embedder):
    """
    Hashing embedder: words (without stop words) → bag-of-words in EMBED_DIM with
    a signed hashing trick, L2-normalized. Deterministic, offline, dependency-
    free. Lexical by nature (not neural semantics): it will not link
    "Sun"~"solar", but it gives an honest cosine search and kills the stop-word
    ranking bug. For real semantics — VELANTRIM_EMBEDDER=sbert.

    Char trigrams are intentionally NOT used: they provide morphological
    robustness, but also noticeable collision noise between unrelated texts,
    which makes the cutoff threshold fragile.
    """

    dim = EMBED_DIM
    id = f"hashing-{EMBED_DIM}"

    def embed(self, text: str) -> List[float]:
        vec = [0.0] * EMBED_DIM
        words = _tokens(text)
        if not words:
            return vec  # zero vector → cosine 0 with everything (e.g. a pure stop-word query)

        for word in words:
            idx, sign = _stable_bucket(word)
            vec[idx] += sign

        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0.0:
            vec = [x / norm for x in vec]
        return vec


# ─── TRIGRAM HASHING EMBEDDER (opt-in, morphology-tolerant) ───────────────────

# Russian function words, used by the trigram embedder only: the word-level
# HashingEmbedder is frozen (same id ⇒ same vectors — the mismatch guard cannot
# see a drift behind an unchanged id), so its stop list must not change either.
STOPWORDS_RU = {
    "и", "в", "во", "не", "на", "с", "со", "что", "как", "это", "этот", "эта",
    "то", "та", "но", "а", "по", "к", "у", "о", "об", "от", "до", "из", "за",
    "для", "же", "ли", "бы", "был", "была", "было", "были", "есть", "я", "ты",
    "он", "она", "оно", "они", "мы", "вы", "мне", "меня", "его", "её", "их",
    "там", "тут", "где", "когда", "почему", "зачем", "какой", "какая", "какие",
}


class TrigramHashingEmbedder(Embedder):
    """
    Character-trigram hashing embedder (opt-in: VELANTRIM_EMBEDDER=hashing-trigram).

    Each token (stop words removed, RU+EN lists) is padded and split into char
    trigrams — "москва" → ^мо мос оск скв ква ва$ — hashed with the same signed
    trick as HashingEmbedder. Tokens shorter than 3 chars contribute whole.
    Shared trigrams survive typos and Russian morphology ("сталица"~"столица",
    "москве"~"москва"), where whole-word hashing yields cosine ≈ 0. The flip
    side is collision noise between unrelated short/noisy texts, so this stays
    opt-in and the English CI gate keeps the word-level default.

    ⚠️ Vectors are NOT comparable with HashingEmbedder's: switching an existing
    L3 store to trigram requires re-embedding/rebuilding it (the embedder
    mismatch guard enforces this — see assert_compatible_embedder).
    """

    dim = EMBED_DIM
    id = f"hashing-trigram-{EMBED_DIM}"

    def _features(self, text: str) -> List[str]:
        feats: List[str] = []
        for word in _WORD_RE.findall(text):
            word = word.lower()
            if word in STOPWORDS or word in STOPWORDS_RU:
                continue
            if len(word) < 3:
                feats.append(word)
                continue
            padded = f"^{word}$"
            feats.extend(padded[i:i + 3] for i in range(len(padded) - 2))
        return feats

    def embed(self, text: str) -> List[float]:
        vec = [0.0] * EMBED_DIM
        feats = self._features(text)
        if not feats:
            return vec
        for feat in feats:
            idx, sign = _stable_bucket(feat)
            vec[idx] += sign
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0.0:
            vec = [x / norm for x in vec]
        return vec


# ─── SENTENCE-TRANSFORMER EMBEDDER (optional dependency) ──────────────────────

class SentenceTransformerEmbedder(Embedder):  # pragma: no cover
    """
    Real neural embeddings via sentence-transformers (optional dependency).
    Lazy import; if missing — a clear ImportError. The model's dimensionality is
    coerced to EMBED_DIM (truncation/padding) to match the L3 schema.
    Excluded from the coverage gate: CI does not install the model; checked locally.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ImportError(
                "SentenceTransformerEmbedder requires 'sentence-transformers' "
                "(optional dependency). The default is HashingEmbedder."
            ) from e
        self._model = SentenceTransformer(model_name)
        self.dim = EMBED_DIM
        self.id = f"sbert-{model_name}-{EMBED_DIM}"

    def embed(self, text: str) -> List[float]:
        raw = self._model.encode(text or "", normalize_embeddings=True).tolist()
        if len(raw) >= EMBED_DIM:
            vec = raw[:EMBED_DIM]
        else:
            vec = raw + [0.0] * (EMBED_DIM - len(raw))
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0.0 else vec


# ─── FACTORY / SINGLETON ──────────────────────────────────────────────────────

_EMBEDDERS = {
    "hashing": HashingEmbedder,
    "hashing-trigram": TrigramHashingEmbedder,
    "sbert": SentenceTransformerEmbedder,
}


def _make(name: str) -> Embedder:
    if name == "auto":
        try:
            return SentenceTransformerEmbedder()
        except Exception as e:  # noqa: BLE001 — any load failure → fallback
            # Not only ImportError: the model may fail to download (offline / HF down).
            # The default must degrade rather than crash the pipeline.
            logger.warning(
                "auto embedder: sbert unavailable (%s), falling back to HashingEmbedder",
                type(e).__name__,
            )
            return HashingEmbedder()
    if name not in _EMBEDDERS:
        raise ValueError(
            f"get_embedder: unknown backend '{name}'. "
            f"Available: {sorted(_EMBEDDERS) + ['auto']}"
        )
    return _EMBEDDERS[name]()


_REGISTRY = BackendRegistry("VELANTRIM_EMBEDDER", "auto", _make)


def get_embedder(backend: Optional[str] = None) -> Embedder:
    """
    Embedder singleton. Backend — via argument or VELANTRIM_EMBEDDER
    (default 'auto').

    Modes:
      'auto'    — use the real model (sbert) if available; on ANY load failure
                  (package not installed, model not downloadable) — fall back to
                  HashingEmbedder. A safe default: where sbert is present — real
                  semantics, otherwise — deterministic lexical search.
      'hashing' — always HashingEmbedder.
      'sbert'   — always neural embeddings (ImportError if the package is missing).
    """
    return _REGISTRY.get(backend)


def reset_embedder() -> None:
    """Reset the singleton (for tests)."""
    _REGISTRY.reset()


# ─── EMBEDDER-MISMATCH GUARD ──────────────────────────────────────────────────
# Vectors from hashing and sbert are NOT cosine-comparable (see module header). On
# a persistent L3 store, swapping the embedder silently breaks vector_search
# ranking — the most invisible class of bugs (the results just slowly degrade). The
# guard stamps the embedder id onto the store on first use and warns loudly
# (or fails in strict mode) on any subsequent mismatch.

_STRICT_ENV = "VELANTRIM_EMBEDDER_STRICT"


def assert_compatible_embedder(graph) -> None:
    """
    Check the active embedder against the one the L3 store was built with.

    graph must support embedder_fingerprint()/set_embedder_fingerprint()
    (see L3GraphBackend). The first call records the fingerprint; afterwards, on a
    mismatch — a warning, and with VELANTRIM_EMBEDDER_STRICT=1 — EmbedderMismatchError.
    """
    active = get_embedder().id
    stored = graph.embedder_fingerprint()
    if stored is None:
        graph.set_embedder_fingerprint(active)
        return
    if stored == active:
        return
    msg = (
        f"L3 store was built with embedder '{stored}' but the active embedder is "
        f"'{active}'; their vectors are not cosine-comparable, so vector_search "
        f"ranking is unreliable. Pin one embedder per store (VELANTRIM_EMBEDDER) "
        f"or rebuild the store."
    )
    if os.environ.get(_STRICT_ENV, "").lower() in ("1", "true", "yes"):
        raise EmbedderMismatchError(msg)
    logger.warning(msg)
