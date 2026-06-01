# core/l3_graph.py
# Velantrim ExoCortex — L3 Canonical Graph (адаптер)
# v8.2.0-sprint2
#
# Принцип: Graph = Truth. L3 — единственный источник канонической истины.
# Единственный вход в L3 — через TruthGate (см. pipeline.run). Прямой MERGE
# в граф минуя TruthGate — архитектурный баг.
#
# Слои памяти (физически разные ткани):
#   SQLite (core/memory.py) — L0/L1 + L2-pending: быстрая рабочая память «сейчас»,
#                             стадии ESM Observed/Hypothesized до врат.
#   L3 граф (этот модуль)   — канон после врат: узлы + рёбра (связи, эпизоды, схемы).
#
# Backend сменный. Дефолт — MockL3Graph (in-memory, без зависимостей).
# Прод-цель — LadybugDB: преемник Kuzu (Kuzu заморожен в окт. 2025 после
# поглощения Apple). LadybugDB — embedded, Cypher-совместимый, с vector index
# и full-text search. Cypher стандартный → backend остаётся переносимым.

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


# ─── ИНТЕРФЕЙС BACKEND ────────────────────────────────────────────────────────

class L3GraphBackend(ABC):
    """
    Минимальный контракт канонического графа L3.
    Все реализации (mock / LadybugDB) обязаны его соблюдать,
    чтобы backend можно было менять, не трогая pipeline.
    """

    @abstractmethod
    def merge_fact(self, fact: Dict[str, Any]) -> None:
        """Upsert канонического узла по fact_id. Идемпотентно."""

    @abstractmethod
    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Вернуть канонический узел по fact_id или None."""

    @abstractmethod
    def all_facts(self) -> List[Dict[str, Any]]:
        """Все канонические узлы графа."""

    @abstractmethod
    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Добавить направленное ребро src -[rel_type]-> dst."""

    @abstractmethod
    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Соседние узлы по исходящим рёбрам (опционально фильтр по типу)."""


# ─── MOCK BACKEND (in-memory, дефолт) ─────────────────────────────────────────

class MockL3Graph(L3GraphBackend):
    """
    In-memory реализация L3 без внешних зависимостей.
    Достаточна для тестов и MVP-пайплайна; повторяет семантику будущего
    LadybugDB (MERGE-узел, направленные рёбра), но без персистентности.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, Dict[str, Any]] = {}
        # ребро: (src_id, rel_type, dst_id, props)
        self._edges: List[tuple] = []

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        fact_id = fact.get("fact_id")
        if not fact_id:
            raise ValueError("merge_fact: fact_id обязателен")
        # MERGE: обновляем существующий узел, не плодим дубли.
        node = self._nodes.get(fact_id, {})
        node.update(fact)
        self._nodes[fact_id] = node

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        node = self._nodes.get(fact_id)
        return dict(node) if node is not None else None

    def all_facts(self) -> List[Dict[str, Any]]:
        return [dict(n) for n in self._nodes.values()]

    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        edge = (src_id, rel_type, dst_id, props or {})
        if edge not in self._edges:
            self._edges.append(edge)

    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for src, rel, dst, _ in self._edges:
            if src != fact_id:
                continue
            if rel_type is not None and rel != rel_type:
                continue
            node = self._nodes.get(dst)
            if node is not None:
                out.append(dict(node))
        return out

    def clear(self) -> None:
        """Сброс состояния (для тестов)."""
        self._nodes.clear()
        self._edges.clear()


# ─── LADYBUGDB BACKEND (слот под спайк) ───────────────────────────────────────

class LadybugL3Graph(L3GraphBackend):
    """
    Backend на LadybugDB (Cypher MERGE, vector index, full-text).

    Намеренно не реализован до спайка: API форка ещё не верифицирован в этом
    окружении. Слот существует и выбирается через VELANTRIM_L3_BACKEND=ladybug,
    но падает с явной ошибкой — чтобы не тащить непроверенный Cypher в прод.
    План спайка: поднять embedded LadybugDB, прогнать MERGE одного узла и
    vector index по claim'ам, затем заменить тело методов реальными запросами.
    """

    def __init__(self, db_path: str = "./data/velantrim_l3.ladybug") -> None:
        raise NotImplementedError(
            "LadybugDB backend ещё не реализован (ожидает спайк). "
            "Используй backend='mock' до завершения интеграции. "
            "См. ROADMAP: L3 граф на LadybugDB."
        )

    def merge_fact(self, fact): ...        # pragma: no cover
    def get_fact(self, fact_id): ...       # pragma: no cover
    def all_facts(self): ...               # pragma: no cover
    def add_edge(self, src_id, rel_type, dst_id, props=None): ...  # pragma: no cover
    def neighbors(self, fact_id, rel_type=None): ...               # pragma: no cover


# ─── ФАБРИКА / SINGLETON ──────────────────────────────────────────────────────

_BACKENDS = {
    "mock": MockL3Graph,
    "ladybug": LadybugL3Graph,
}

_INSTANCE: Optional[L3GraphBackend] = None


def get_l3_graph(backend: Optional[str] = None) -> L3GraphBackend:
    """
    Вернуть singleton L3-графа. Backend выбирается аргументом или
    переменной окружения VELANTRIM_L3_BACKEND (по умолчанию 'mock').
    """
    global _INSTANCE
    if _INSTANCE is not None and backend is None:
        return _INSTANCE

    name = backend or os.environ.get("VELANTRIM_L3_BACKEND", "mock")
    if name not in _BACKENDS:
        raise ValueError(
            f"get_l3_graph: неизвестный backend '{name}'. "
            f"Доступно: {sorted(_BACKENDS)}"
        )
    instance = _BACKENDS[name]()
    if backend is None:
        _INSTANCE = instance
    return instance


def reset_l3_graph() -> None:
    """Сбросить singleton (для тестов)."""
    global _INSTANCE
    _INSTANCE = None
