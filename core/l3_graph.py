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

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from core._registry import BackendRegistry

logger = logging.getLogger(__name__)

# Вклад значимости (salience) в ранжирование vector_search: итоговый скор =
# близость × (1 + W × significance). Релевантность доминирует, значимость
# поднимает важные воспоминания при близких косинусах. significance ≠ truth.
_SIGNIFICANCE_WEIGHT = 0.5


def _salience_score(similarity: float, significance: Any) -> float:
    """Близость, усиленная значимостью узла (по умолчанию significance=0.5)."""
    try:
        sig = float(significance)
    except (TypeError, ValueError):
        sig = 0.5
    return similarity * (1.0 + _SIGNIFICANCE_WEIGHT * sig)


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

    @abstractmethod
    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Исходящие рёбра факта вместе с их props (в отличие от neighbors,
        который отдаёт только узлы). Элемент: {rel_type, target, props}.
        Нужен, чтобы читать эпизодический контекст who/where/when из рёбер.
        """

    @abstractmethod
    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Входящие рёбра факта (зеркало get_edges). Элемент: {rel_type, source,
        props}. Нужен для обратных запросов: чем факт заменён / что его
        опровергает / что на него ссылается.
        """

    @abstractmethod
    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Семантический поиск по эмбеддингам узлов.
        Возвращает до k фактов, отсортированных по убыванию близости;
        каждый дополнен полем '_score' (косинусная близость).
        """

    # ─── Эпизодические entity-узлы (Person/Place/Time как первоклассные узлы) ──
    @abstractmethod
    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        """Upsert entity-узла (kind: person/place/time). Идемпотентно."""

    @abstractmethod
    def link_fact_to_entity(
        self, fact_id: str, entity_id: str, rel: str = "MENTIONS",
    ) -> None:
        """Связать факт с entity-узлом (факт упоминает сущность)."""

    @abstractmethod
    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        """Факты, связанные с entity-узлом (обратный обход MENTIONS)."""


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
        # эмбеддинги узлов для vector_search (отдельно от данных узла)
        self._vectors: Dict[str, List[float]] = {}
        # entity-узлы и связи факт→сущность (отдельно от Fact-пространства)
        self._entities: Dict[str, Dict[str, Any]] = {}
        self._mentions: List[tuple] = []  # (fact_id, entity_id, rel)

    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        self._entities[entity_id] = {
            "entity_id": entity_id, "kind": kind, "label": label}

    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        edge = (fact_id, entity_id, rel)
        if edge not in self._mentions:
            self._mentions.append(edge)

    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        ids = [fid for fid, eid, _ in self._mentions if eid == entity_id]
        return [dict(self._nodes[fid]) for fid in ids if fid in self._nodes]

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        fact_id = fact.get("fact_id")
        if not fact_id:
            raise ValueError("merge_fact: fact_id обязателен")
        # MERGE: обновляем существующий узел, не плодим дубли.
        node = self._nodes.get(fact_id, {})
        node.update(fact)
        self._nodes[fact_id] = node
        # Эмбеддинг claim'а для семантического поиска.
        claim = node.get("claim")
        if claim:
            from core.embedding import get_embedder
            self._vectors[fact_id] = get_embedder().embed(claim)

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

    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        from core.embedding import cosine
        scored = []
        for fact_id, vec in self._vectors.items():
            sim = cosine(query_vector, vec)
            if sim <= 0.0:
                continue
            node = dict(self._nodes[fact_id])
            node["_relevance"] = round(sim, 6)
            node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
            scored.append(node)
        scored.sort(key=lambda n: n["_score"], reverse=True)
        return scored[:k]

    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for src, rel, dst, props in self._edges:
            if src != fact_id:
                continue
            if rel_type is not None and rel != rel_type:
                continue
            out.append({"rel_type": rel, "target": dst, "props": dict(props)})
        return out

    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for src, rel, dst, props in self._edges:
            if dst != fact_id:
                continue
            if rel_type is not None and rel != rel_type:
                continue
            out.append({"rel_type": rel, "source": src, "props": dict(props)})
        return out

    def clear(self) -> None:
        """Сброс состояния (для тестов)."""
        self._nodes.clear()
        self._edges.clear()
        self._vectors.clear()
        self._entities.clear()
        self._mentions.clear()


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

    def __init__(self, db_path: Optional[str] = None) -> None:
        import os
        # Путь персистентной БД настраивается через VELANTRIM_L3_PATH; БД
        # переживает перезапуски (в отличие от in-memory mock-дефолта).
        if db_path is None:
            db_path = os.environ.get("VELANTRIM_L3_PATH", "./data/velantrim_l3.lbug")
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
        from core.embedding import EMBED_DIM
        try:
            self._conn.execute("INSTALL vector; LOAD vector;")
        except Exception:
            pass  # расширение уже установлено/загружено
        for ddl in (
            f"CREATE NODE TABLE Fact(fact_id STRING PRIMARY KEY, claim STRING, "
            f"source STRING, confidence DOUBLE, epistemic_state STRING, "
            f"claim_type STRING, source_status STRING, significance DOUBLE, "
            f"truth_status STRING, metadata STRING, embedding FLOAT[{EMBED_DIM}])",
            "CREATE REL TABLE EDGE(FROM Fact TO Fact, rel_type STRING, props STRING)",
            "CREATE NODE TABLE Entity(entity_id STRING PRIMARY KEY, kind STRING, label STRING)",
            "CREATE REL TABLE MENTIONS(FROM Fact TO Entity, rel STRING)",
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
        # Эмбеддинг claim'а в FLOAT[]-колонку для нативного vector index.
        claim = fact.get("claim")
        if claim:
            from core.embedding import get_embedder
            params["embedding"] = get_embedder().embed(claim)
            sets.append("f.embedding = $embedding")
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
        import json, base64
        # props в base64 по той же причине, что и metadata (см. _serialize).
        payload = base64.b64encode(json.dumps(props or {}).encode("utf-8")).decode("ascii")
        self._conn.execute(
            "MATCH (a:Fact {fact_id: $s}), (b:Fact {fact_id: $d}) "
            "MERGE (a)-[e:EDGE {rel_type: $rt}]->(b) SET e.props = $p",
            {"s": src_id, "d": dst_id, "rt": rel_type, "p": payload})

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

    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        import json, base64
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params: Dict[str, Any] = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        res = self._conn.execute(
            f"{cypher} RETURN e.rel_type, b.fact_id, e.props", params)
        out = []
        while res.has_next():
            rel, target, raw = res.get_next()
            try:
                props = json.loads(base64.b64decode(raw)) if raw else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": rel, "target": target, "props": props})
        return out

    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        import json, base64
        cypher = "MATCH (a:Fact)-[e:EDGE]->(b:Fact {fact_id: $id})"
        params: Dict[str, Any] = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        res = self._conn.execute(
            f"{cypher} RETURN e.rel_type, a.fact_id, e.props", params)
        out = []
        while res.has_next():
            rel, source, raw = res.get_next()
            try:
                props = json.loads(base64.b64decode(raw)) if raw else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": rel, "source": source, "props": props})
        return out

    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        self._conn.execute(
            "MERGE (e:Entity {entity_id: $id}) SET e.kind = $kind, e.label = $label",
            {"id": entity_id, "kind": kind, "label": label})

    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        self._conn.execute(
            "MATCH (f:Fact {fact_id: $f}), (e:Entity {entity_id: $e}) "
            "MERGE (f)-[m:MENTIONS {rel: $rel}]->(e)",
            {"f": fact_id, "e": entity_id, "rel": rel})

    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"f.{c}" for c in cols)
        res = self._conn.execute(
            f"MATCH (f:Fact)-[:MENTIONS]->(e:Entity {{entity_id: $id}}) RETURN {ret}",
            {"id": entity_id})
        out = []
        while res.has_next():
            out.append(self._row_to_fact(res.get_next(), cols))
        return out

    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        # Индекс создаём один раз: спайк подтвердил, что строки, добавленные
        # ПОСЛЕ создания, видны поиску — дорогой DROP+CREATE на каждый запрос не
        # нужен. Повторный CREATE → "already exists" → глотаем.
        try:
            self._conn.execute("CALL CREATE_VECTOR_INDEX('Fact', 'fact_vec', 'embedding')")
        except Exception:
            pass  # индекс уже есть, либо строк с эмбеддингом ещё нет
        # Берём с запасом (k*3), затем пере-ранжируем по значимости, чтобы
        # salient-воспоминание не выпало из top-k при близких косинусах.
        # distance — косинусное расстояние (0 = точно).
        try:
            res = self._conn.execute(
                "CALL QUERY_VECTOR_INDEX('Fact', 'fact_vec', $q, $k) "
                "RETURN node.fact_id, distance",
                {"q": query_vector, "k": max(k * 3, k)})
        except Exception:
            return []  # индекса нет (пустой граф) — искать не по чему
        out = []
        while res.has_next():
            fact_id, distance = res.get_next()
            node = self.get_fact(fact_id)
            if node is not None:
                sim = 1.0 - distance  # близость ≈ 1 - косинусное расстояние
                node["_relevance"] = round(sim, 6)
                node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
                out.append(node)
        out.sort(key=lambda n: n["_score"], reverse=True)
        return out[:k]


# ─── NEO4J BACKEND (опциональная альтернатива) ────────────────────────────────

class Neo4jL3Graph(L3GraphBackend):  # pragma: no cover
    """
    Backend на Neo4j (опциональная альтернатива LadybugDB). Стандартный Cypher
    через neo4j-драйвер; конфиг — NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD /
    NEO4J_DATABASE. metadata и props рёбер хранятся JSON-строкой (Neo4j не
    допускает вложенных map в свойствах); embedding — массив float.

    `neo4j` — опциональная зависимость (ленивый импорт). vector_search считает
    косинус на стороне Python (версионно-независимо, без vector-index Neo4j).

    Сетевой бэкенд: требует запущенного сервера Neo4j. В этом окружении сервера
    нет, поэтому класс исключён из coverage-гейта; Cypher повторяет проверенный
    в спайке LadybugL3Graph (MERGE/MATCH-семантика идентична).
    """

    def __init__(self) -> None:
        import os
        try:
            from neo4j import GraphDatabase
        except ImportError as e:
            raise ImportError(
                "Neo4j backend требует пакет 'neo4j' (опциональная зависимость): "
                "pip install neo4j. Дефолт — backend='auto' (LadybugDB/mock)."
            ) from e
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "neo4j")
        self._db = os.environ.get("NEO4J_DATABASE", "neo4j")
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._driver.execute_query(
            "CREATE CONSTRAINT fact_id IF NOT EXISTS "
            "FOR (f:Fact) REQUIRE f.fact_id IS UNIQUE",
            database_=self._db)

    def _run(self, cypher: str, **params):
        records, _, _ = self._driver.execute_query(
            cypher, database_=self._db, **params)
        return records

    @staticmethod
    def _props(fact: Dict[str, Any]) -> Dict[str, Any]:
        import json
        out = {}
        for k, v in fact.items():
            if k.startswith("_"):
                continue
            out[k] = json.dumps(v) if k == "metadata" else v
        return out

    @staticmethod
    def _node(props: Dict[str, Any]) -> Dict[str, Any]:
        import json
        d = dict(props)
        if isinstance(d.get("metadata"), str):
            try:
                d["metadata"] = json.loads(d["metadata"])
            except (ValueError, TypeError):
                d["metadata"] = {}
        d.pop("embedding", None)
        return d

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        if not fact.get("fact_id"):
            raise ValueError("merge_fact: fact_id обязателен")
        props = self._props(fact)
        if fact.get("claim"):
            from core.embedding import get_embedder
            props["embedding"] = get_embedder().embed(fact["claim"])
        self._run("MERGE (f:Fact {fact_id: $id}) SET f += $props",
                  id=fact["fact_id"], props=props)

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        rows = self._run(
            "MATCH (f:Fact {fact_id: $id}) RETURN properties(f) AS p", id=fact_id)
        return self._node(rows[0]["p"]) if rows else None

    def all_facts(self) -> List[Dict[str, Any]]:
        rows = self._run("MATCH (f:Fact) RETURN properties(f) AS p")
        return [self._node(r["p"]) for r in rows]

    def add_edge(self, src_id, rel_type, dst_id, props=None) -> None:
        import json
        self._run(
            "MATCH (a:Fact {fact_id: $s}), (b:Fact {fact_id: $d}) "
            "MERGE (a)-[e:EDGE {rel_type: $rt}]->(b) SET e.props = $p",
            s=src_id, d=dst_id, rt=rel_type, p=json.dumps(props or {}))

    def neighbors(self, fact_id, rel_type=None) -> List[Dict[str, Any]]:
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        rows = self._run(cypher + " RETURN properties(b) AS p", **params)
        return [self._node(r["p"]) for r in rows]

    def get_edges(self, fact_id, rel_type=None) -> List[Dict[str, Any]]:
        import json
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        rows = self._run(
            cypher + " RETURN e.rel_type AS rt, b.fact_id AS t, e.props AS p", **params)
        out = []
        for r in rows:
            try:
                props = json.loads(r["p"]) if r["p"] else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": r["rt"], "target": r["t"], "props": props})
        return out

    def incoming_edges(self, fact_id, rel_type=None) -> List[Dict[str, Any]]:
        import json
        cypher = "MATCH (a:Fact)-[e:EDGE]->(b:Fact {fact_id: $id})"
        params = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        rows = self._run(
            cypher + " RETURN e.rel_type AS rt, a.fact_id AS s, e.props AS p", **params)
        out = []
        for r in rows:
            try:
                props = json.loads(r["p"]) if r["p"] else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": r["rt"], "source": r["s"], "props": props})
        return out

    def merge_entity(self, entity_id, kind, label) -> None:
        self._run("MERGE (e:Entity {entity_id: $id}) SET e.kind = $k, e.label = $l",
                  id=entity_id, k=kind, l=label)

    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        self._run(
            "MATCH (f:Fact {fact_id: $f}), (e:Entity {entity_id: $e}) "
            "MERGE (f)-[m:MENTIONS {rel: $rel}]->(e)",
            f=fact_id, e=entity_id, rel=rel)

    def facts_for_entity(self, entity_id) -> List[Dict[str, Any]]:
        rows = self._run(
            "MATCH (f:Fact)-[:MENTIONS]->(e:Entity {entity_id: $id}) "
            "RETURN properties(f) AS p", id=entity_id)
        return [self._node(r["p"]) for r in rows]

    def vector_search(self, query_vector, k=5) -> List[Dict[str, Any]]:
        from core.embedding import cosine
        rows = self._run(
            "MATCH (f:Fact) WHERE f.embedding IS NOT NULL "
            "RETURN f.fact_id AS id, f.embedding AS v")
        scored = []
        for r in rows:
            sim = cosine(query_vector, r["v"])
            if sim <= 0.0:
                continue
            node = self.get_fact(r["id"])
            if node is None:
                continue
            node["_relevance"] = round(sim, 6)
            node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
            scored.append(node)
        scored.sort(key=lambda n: n["_score"], reverse=True)
        return scored[:k]


# ─── ФАБРИКА / SINGLETON ──────────────────────────────────────────────────────

_BACKENDS = {
    "mock": MockL3Graph,        # in-memory, без зависимостей (dev / CI)
    "ladybug": LadybugL3Graph,  # рекомендуемый прод-дефолт (преемник Kuzu)
    "neo4j": Neo4jL3Graph,      # опциональная альтернатива (нужен сервер)
}


def _make(name: str) -> L3GraphBackend:
    if name == "auto":
        # Прод-дефолт: LadybugDB, если доступен; иначе — mock (CI / без зависимостей).
        try:
            return LadybugL3Graph()
        except Exception as e:  # noqa: BLE001 — любой сбой инициализации → откат
            logger.warning(
                "auto L3: LadybugDB недоступен (%s), откат на in-memory mock",
                type(e).__name__,
            )
            return MockL3Graph()
    if name not in _BACKENDS:
        raise ValueError(
            f"get_l3_graph: неизвестный backend '{name}'. "
            f"Доступно: {sorted(_BACKENDS) + ['auto']}"
        )
    return _BACKENDS[name]()


_REGISTRY = BackendRegistry("VELANTRIM_L3_BACKEND", "auto", _make)


def get_l3_graph(backend: Optional[str] = None) -> L3GraphBackend:
    """
    Вернуть singleton L3-графа. Backend — аргументом или VELANTRIM_L3_BACKEND.

    Режимы:
      'auto' (дефолт) — LadybugDB, если установлен (рекомендуемый прод-движок,
                        преемник Kuzu); иначе in-memory mock без зависимостей.
      'ladybug'       — всегда LadybugDB (ImportError, если пакета нет).
      'neo4j'         — опциональная альтернатива (нужен запущенный сервер).
      'mock'          — всегда in-memory (dev / CI).
    """
    return _REGISTRY.get(backend)


def reset_l3_graph() -> None:
    """Сбросить singleton (для тестов)."""
    _REGISTRY.reset()
