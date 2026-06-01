# core/embedding.py
# Velantrim ExoCortex — Embedding Layer (сменная абстракция)
# v8.3.0-sprint2
#
# Назначение: превратить текст claim'а / запроса в вектор для семантического
# поиска (vector retrieval) — лекарство от «понимания по поверхностным токенам».
#
# Backend сменный:
#   HashingEmbedder (дефолт) — без зависимостей, детерминированный. Это НЕ
#     нейросемантика: признаки лексические (слова + char-триграммы) с удалением
#     стоп-слов. Чинит баг ранжирования по стоп-словам и даёт рабочий vector-
#     пайплайн. Для настоящей семантики ("Sun" ~ "solar") включай модель ниже.
#   SentenceTransformerEmbedder — реальные эмбеддинги (опц. зависимость,
#     ленивый импорт). Включается VELANTRIM_EMBEDDER=sbert.
#
# Важно: хэш стабильный (hashlib), а не встроенный hash() — иначе векторы
# не воспроизводятся между процессами и ломается персистентность в L3.

import hashlib
import math
import os
import re
from abc import ABC, abstractmethod
from typing import List, Optional

# Размерность вектора. Фиксирована: L3-граф хранит FLOAT[EMBED_DIM].
# Чем больше, тем реже коллизии хэш-трюка между разными словами (ценой размера).
# 2048 выбрано так, чтобы дефолтный демо-корпус был свободен от коллизий.
EMBED_DIM = 2048

# Небольшой стоп-лист: служебные слова, по которым нельзя ранжировать смысл.
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
    """Слова в нижнем регистре без стоп-слов."""
    return [w.lower() for w in _WORD_RE.findall(text)
            if w.lower() not in STOPWORDS]


def _stable_bucket(feature: str) -> tuple[int, float]:
    """
    Детерминированный (index, sign) для признака через md5.
    Хэширующий трюк со знаком уменьшает влияние коллизий.
    """
    h = hashlib.md5(feature.encode("utf-8")).digest()
    idx = int.from_bytes(h[:4], "big") % EMBED_DIM
    sign = 1.0 if (h[4] & 1) else -1.0
    return idx, sign


def cosine(a: List[float], b: List[float]) -> float:
    """Косинусная близость двух векторов (0.0 при нулевой норме)."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


# ─── ИНТЕРФЕЙС ────────────────────────────────────────────────────────────────

class Embedder(ABC):
    """Контракт эмбеддера: текст → вектор фиксированной размерности EMBED_DIM."""

    dim: int = EMBED_DIM

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Вектор длины self.dim, L2-нормализованный."""


# ─── HASHING EMBEDDER (дефолт, без зависимостей) ──────────────────────────────

class HashingEmbedder(Embedder):
    """
    Хэширующий эмбеддер: слова (без стоп-слов) → bag-of-words в EMBED_DIM со
    знаковым хэш-трюком, L2-нормализация. Детерминированный, офлайновый, без
    зависимостей. Лексический по природе (не нейросемантика): не свяжет
    "Sun"~"solar", но даёт честный косинусный поиск и убивает баг ранжирования
    по стоп-словам. Для настоящей семантики — VELANTRIM_EMBEDDER=sbert.

    Char-триграммы намеренно НЕ используются: они дают морфологическую
    устойчивость, но и заметный коллизионный шум между несвязанными текстами,
    из-за чего порог отсечения становится хрупким.
    """

    dim = EMBED_DIM

    def embed(self, text: str) -> List[float]:
        vec = [0.0] * EMBED_DIM
        words = _tokens(text)
        if not words:
            return vec  # нулевой вектор → косинус 0 со всем (напр. чистый стоп-запрос)

        for word in words:
            idx, sign = _stable_bucket(word)
            vec[idx] += sign

        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0.0:
            vec = [x / norm for x in vec]
        return vec


# ─── SENTENCE-TRANSFORMER EMBEDDER (опц. зависимость) ─────────────────────────

class SentenceTransformerEmbedder(Embedder):  # pragma: no cover
    """
    Реальные нейроэмбеддинги через sentence-transformers (опц. зависимость).
    Ленивый импорт; при отсутствии — понятный ImportError. Размерность модели
    приводится к EMBED_DIM (усечение/паддинг), чтобы совпасть со схемой L3.
    Исключено из coverage-гейта: CI не ставит модель; проверяется локально.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ImportError(
                "SentenceTransformerEmbedder требует 'sentence-transformers' "
                "(опц. зависимость). Дефолт — HashingEmbedder."
            ) from e
        self._model = SentenceTransformer(model_name)
        self.dim = EMBED_DIM

    def embed(self, text: str) -> List[float]:
        raw = self._model.encode(text or "", normalize_embeddings=True).tolist()
        if len(raw) >= EMBED_DIM:
            vec = raw[:EMBED_DIM]
        else:
            vec = raw + [0.0] * (EMBED_DIM - len(raw))
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0.0 else vec


# ─── ФАБРИКА / SINGLETON ──────────────────────────────────────────────────────

_EMBEDDERS = {
    "hashing": HashingEmbedder,
    "sbert": SentenceTransformerEmbedder,
}

_INSTANCE: Optional[Embedder] = None


def get_embedder(backend: Optional[str] = None) -> Embedder:
    """
    Singleton эмбеддера. Backend — аргументом или VELANTRIM_EMBEDDER
    (по умолчанию 'auto').

    Режимы:
      'auto'    — взять реальную модель (sbert), если установлена; иначе
                  откатиться на HashingEmbedder. Безопасный дефолт: где есть
                  sentence-transformers — настоящая семантика, где нет (напр. CI)
                  — детерминированный лексический поиск без зависимостей.
      'hashing' — всегда HashingEmbedder.
      'sbert'   — всегда нейроэмбеддинги (ImportError, если пакет не стоит).
    """
    global _INSTANCE
    if _INSTANCE is not None and backend is None:
        return _INSTANCE
    name = backend or os.environ.get("VELANTRIM_EMBEDDER", "auto")
    instance = _instantiate(name)
    if backend is None:
        _INSTANCE = instance
    return instance


def _instantiate(name: str) -> Embedder:
    if name == "auto":
        try:
            return SentenceTransformerEmbedder()
        except ImportError:
            return HashingEmbedder()
    if name not in _EMBEDDERS:
        raise ValueError(
            f"get_embedder: неизвестный backend '{name}'. "
            f"Доступно: {sorted(_EMBEDDERS) + ['auto']}"
        )
    return _EMBEDDERS[name]()


def reset_embedder() -> None:
    """Сбросить singleton (для тестов)."""
    global _INSTANCE
    _INSTANCE = None
