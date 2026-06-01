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

class LadybugL3Graph(L3GraphBackend):  # pragma: no cover
    """
    Backend на LadybugDB — embedded, Cypher-совместимый преемник Kuzu
    (Kuzu заморожен окт.2025). Узлы Fact + обобщённые рёбра EDGE с типом-свойством.

    API верифицирован спайком (v0.17.0): Database/Connection, MERGE-upsert по
    PRIMARY KEY, REL-таблицы, vector index (INSTALL vector / CREATE_VECTOR_INDEX).

    `ladybug` — опциональная зависимость (нативный пакет + numpy). Импорт ленивый;
    при отсутствии — понятный ImportError. Дефолтный backend остаётся 'mock', а
    эти методы исключены из coverage-гейта (pragma), т.к. CI не ставит ladybug;
    поведение проверяется локально тестами под pytest.importorskip('ladybug').
    """

    # Колонки узла Fact, которые персистим (остальное — в metadata JSON).
    _COLS = [
        "fact_id", "claim", "source", "confidence", "epistemic_state",
        "claim_type", "source_status", "significance", "truth_status", "metadata",
    ]

    def __init__(self, db_path: str = "./data/velantrim_l3.lbug") -> None:
        try:
            import ladybug as lb
        except ImportError as e:
            raise ImportError(
                "LadybugDB backend требует пакет 'ladybug' (опциональная "
                "зависимость): pip install ladybug. Дефолт — backend='mock'."
            ) from e
        self._lb = lb
        self._db = lb.Database(db_path)
        self._conn = lb.Connection(self._db)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        for ddl in (
            "CREATE NODE TABLE Fact(fact_id STRING PRIMARY KEY, claim STRING, "
            "source STRING, confidence DOUBLE, epistemic_state STRING, "
            "claim_type STRING, source_status STRING, significance DOUBLE, "
            "truth_status STRING, metadata STRING)",
            "CREATE REL TABLE EDGE(FROM Fact TO Fact, rel_type STRING, props STRING)",
        ):
            try:
                self._conn.execute(ddl)
            except Exception:
                pass  # таблица уже существует — схема идемпотентна

    @staticmethod
    def _serialize(fact: Dict[str, Any]) -> Dict[str, Any]:
        # metadata кодируется base64: LadybugDB авто-парсит STRING вида {..}/[..]
        # как map/list и теряет JSON-кавычки, поэтому JSON прячем за base64.
        import json, base64
        out = {}
        for col in LadybugL3Graph._COLS:
            if col == "metadata":
                raw = json.dumps(fact.get("metadata", {})).encode("utf-8")
                out["metadata"] = base64.b64encode(raw).decode("ascii")
            elif col in fact:
                out[col] = fact[col]
        return out

    @staticmethod
    def _row_to_fact(row: list, cols: list) -> Dict[str, Any]:
        import json, base64
        d = dict(zip(cols, row))
        if "metadata" in d and isinstance(d["metadata"], str):
            try:
                d["metadata"] = json.loads(base64.b64decode(d["metadata"]))
            except (ValueError, TypeError):
                d["metadata"] = {}
        return {k: v for k, v in d.items() if v is not None}

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        fact_id = fact.get("fact_id")
        if not fact_id:
            raise ValueError("merge_fact: fact_id обязателен")
        params = self._serialize(fact)
        sets = [f"f.{c} = ${c}" for c in params if c != "fact_id"]
        cypher = "MERGE (f:Fact {fact_id: $fact_id})"
        if sets:
            cypher += " SET " + ", ".join(sets)
        self._conn.execute(cypher, params)

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"f.{c}" for c in cols)
        res = self._conn.execute(
            f"MATCH (f:Fact {{fact_id: $id}}) RETURN {ret}", {"id": fact_id})
        if not res.has_next():
            return None
        return self._row_to_fact(res.get_next(), cols)

    def all_facts(self) -> List[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"f.{c}" for c in cols)
        res = self._conn.execute(f"MATCH (f:Fact) RETURN {ret}")
        out = []
        while res.has_next():
            out.append(self._row_to_fact(res.get_next(), cols))
        return out

    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        import json
        self._conn.execute(
            "MATCH (a:Fact {fact_id: $s}), (b:Fact {fact_id: $d}) "
            "MERGE (a)-[e:EDGE {rel_type: $rt}]->(b) SET e.props = $p",
            {"s": src_id, "d": dst_id, "rt": rel_type, "p": json.dumps(props or {})})

    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"b.{c}" for c in cols)
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params: Dict[str, Any] = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        res = self._conn.execute(f"{cypher} RETURN {ret}", params)
        out = []
        while res.has_next():
            out.append(self._row_to_fact(res.get_next(), cols))
        return out


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
