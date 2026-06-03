# core/pipeline.py
# Velantrim ExoCortex — Core Pipeline
# v8.7.0-sprint2
#
# Принцип: Graph = Truth · LLM = Language · Memory = Physiology
# Пайплайн: Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer
#
# Ретрив — векторный (косинус эмбеддингов) по сид-корпусу + recall из L3.
# Ответ — сменный Generator (extractive по умолчанию, опц. LLM). L3 — сменный
# backend (auto→LadybugDB / mock / neo4j). Полная архитектура L0–L6:
# docs/Velantrim_V8_Crystal_Sprint1_toc.md
#
# TODO (дальше):
#   - HybridRetriever: добавить graph-walk / PageRank поверх vector-recall
#   - ESM: полная матрица переходов + автоматические Supported/Hypothesized
#   - Первоклассные эпизодические узлы (Person/Place/Time) вместо props рёбер

import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from core.trace import build_trace, promote_trace, format_trace
from core.memory import (
    store_fact, get_fact, transition_esm, SUBJECTIVE_CLAIM_TYPES,
)
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder, cosine
from core.generation import get_generator
from core import metrics, adaptation

logger = logging.getLogger(__name__)

# ─── RETRIEVAL CORPUS (источник для retrieve, не L3) ──────────────────────────
# Это корпус для извлечения, не канонический граф. Канон L3 живёт в
# core/l3_graph.py и наполняется только после TruthGate (см. run, шаг 6).
# Прямой MERGE в L3 минуя TruthGate — архитектурный баг.
DATABASE = [
    {"id": "f1", "text": "Water boils at 100°C at sea level",     "source": "physics",    "confidence": 0.99},
    {"id": "f2", "text": "Quantum entanglement links particles",    "source": "physics",    "confidence": 0.85},
    {"id": "f3", "text": "Earth revolves around the Sun",          "source": "astronomy",  "confidence": 0.99},
    {"id": "f4", "text": "The human brain has ~86 billion neurons","source": "neuroscience","confidence": 0.90},
    {"id": "f5", "text": "DNA encodes genetic information",        "source": "biology",    "confidence": 0.99},
]


# ─── RETRIEVAL (vector / semantic) ────────────────────────────────────────────
# Косинусная близость эмбеддингов по ДВУМ источникам:
#   1) сид-корпус DATABASE — внешние факты «из коробки»;
#   2) канон L3 — то, что система уже выучила и провела через врата.
# Recall из L3 замыкает цикл «узнал → запомнил → вспомнил»: факты, принятые
# через ingest()/pipeline, становятся доступны для ответа. Дедуп по id.
# Эмбеддер сменный (core/embedding.py): дефолт HashingEmbedder, sbert опционально.
# Гибрид: vector-recall + multi-hop graph-walk (spreading activation / HippoRAG-lite).

# Порог отсечения шума от хэш-коллизий: ниже — не релевантно.
_RETRIEVAL_MIN_SIM = 0.05
# Damping активации на каждый хоп graph-walk (PageRank-распространение).
_GRAPH_WALK_DECAY = 0.5
# Глубина graph-walk (число хопов от vector-хитов).
_GRAPH_WALK_HOPS = 2


def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Гибридный поиск: косинус эмбеддингов по сид-корпусу DATABASE и канону L3,
    затем 1-hop graph-walk — связанные в графе факты всплывают по ассоциации
    (spreading activation). Возвращает топ-k по score, дедуп по id.
    Корпус-факты приходят как Observed, recall из L3 — со своим ESM-состоянием.
    """
    embedder = get_embedder()
    graph = get_l3_graph()
    q_vec = embedder.embed(query)
    by_id: Dict[str, Dict[str, Any]] = {}

    def _offer(item: Dict[str, Any]) -> None:
        # Дедуп по id: один и тот же факт может быть и в корпусе, и в L3.
        prev = by_id.get(item["id"])
        if prev is None or item["_score"] > prev["_score"]:
            by_id[item["id"]] = item

    # Источник 1: сид-корпус (внешние факты, сырой вход → Observed).
    for item in DATABASE:
        sim = cosine(q_vec, embedder.embed(item["text"]))
        if sim < _RETRIEVAL_MIN_SIM:
            continue
        _offer({
            **item,
            "_score":          round(sim * item.get("confidence", 1.0), 4),
            "epistemic_state": "Observed",
            "origin":          "retrieval",
        })

    def _from_node(node: Dict[str, Any], score: float, origin: str) -> Dict[str, Any]:
        return {
            "id":              node["fact_id"],
            "text":            node.get("claim", ""),
            "source":          node.get("source", "memory"),
            "confidence":      node.get("confidence", 1.0),
            "claim_type":      node.get("claim_type", "WORLD_FACT"),
            "source_status":   node.get("source_status", "DERIVED"),
            "significance":    node.get("significance", 0.5),
            "_score":          round(score, 4),
            "epistemic_state": node.get("epistemic_state", "Validated"),
            "origin":          origin,
        }

    # Источник 2: каноническая память L3 (recall выученного).
    vector_hits = []
    for node in graph.vector_search(q_vec, k=k):
        sim = node.get("_relevance", 0.0)
        if sim < _RETRIEVAL_MIN_SIM:
            continue
        _offer(_from_node(node, sim * node.get("confidence", 1.0), "memory"))
        vector_hits.append(node)

    # Источник 3: multi-hop graph-walk от vector-хитов (ассоциативный recall).
    # Personalized PageRank (без итераций до сходимости): активация течёт от
    # vector-хитов по рёбрам, на каждом хопе умножаясь на damping и делясь между
    # исходящими соседями (по out-degree). Достижимое по НЕСКОЛЬКИМ путям
    # суммируется — хорошо связанные «хабы» поднимаются. Распространяют и
    # возвращаются только Validated; в seed-хиты активация не вливается (у них
    # авторитетный vector-скор). Глубина — _GRAPH_WALK_HOPS, damping <1 +
    # ограничение хопов гарантируют сходимость без раздувания на циклах.
    seeds = {hit["fact_id"] for hit in vector_hits}
    graph_score: Dict[str, float] = {}
    node_cache: Dict[str, Dict[str, Any]] = {}
    current = {
        hit["fact_id"]: hit.get("_relevance", 0.0) * hit.get("confidence", 1.0)
        for hit in vector_hits
    }
    for _hop in range(_GRAPH_WALK_HOPS):
        nxt: Dict[str, float] = {}
        for fid, act in current.items():
            valid = [n for n in graph.neighbors(fid)
                     if n.get("epistemic_state") == "Validated"]
            if not valid:
                continue
            share = act * _GRAPH_WALK_DECAY / len(valid)
            for neighbor in valid:
                nid = neighbor["fact_id"]
                if nid in seeds:
                    continue  # в vector-хиты активацию не вливаем
                nxt[nid] = nxt.get(nid, 0.0) + share
                node_cache[nid] = neighbor
        if not nxt:
            break
        for nid, val in nxt.items():
            graph_score[nid] = graph_score.get(nid, 0.0) + val
        current = nxt

    for nid, score in graph_score.items():
        _offer(_from_node(node_cache[nid], score, "graph"))

    return sorted(by_id.values(), key=lambda x: x["_score"], reverse=True)[:k]


# ─── FACTS PACK ───────────────────────────────────────────────────────────────

def build_facts_pack(
    retrieved: List[Dict[str, Any]],
    query: str,
) -> Dict[str, Any]:
    """
    Собрать FactsPack из retrieved фактов.
    Каждый факт сохраняется в L0/L1 память через store_fact().
    truth_status = UNVERIFIED до прохождения TruthGate.
    epistemic_state берётся из retrieve() — владелец начального ESM-состояния.
    """
    facts: List[Dict[str, Any]] = []

    for item in retrieved:
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue  # согласованно с build_trace: пропускаем без id

        fact = {
            "fact_id":         fact_id,
            "claim":           item["text"],
            "source":          item["source"],
            "confidence":      item["_score"],
            "epistemic_state": item["epistemic_state"],  # из retrieve(), не дублируем
            # retrieval-факты — утверждения о мире из внешнего источника.
            "claim_type":      item.get("claim_type", "WORLD_FACT"),
            "source_status":   item.get("source_status", "EXTERNAL"),
            "significance":    item.get("significance", 0.5),
            "truth_status":    "UNVERIFIED",
        }
        # L0/L1 сохранение
        store_fact(fact)

        facts.append(fact)

    facts.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "facts": facts,
        "query": query,
        "total": len(facts),
    }


# ─── GUARDIAN ─────────────────────────────────────────────────────────────────
# Структурная проверка — последний рубеж перед ответом.
# 0 токенов · синхронный · Fast Path.

def guardian(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> tuple[bool, Optional[str]]:
    """
    Проверяет структурную целостность FactsPack и Trace.
    Возвращает (passed: bool, reason: str | None).
    """
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "FactsPack пустой"
    if not trace:
        return False, "Trace пустой — провенанс отсутствует"
    if len(trace) < len(facts):
        return False, f"Несоответствие: {len(facts)} фактов, {len(trace)} trace-элементов"

    for fact in facts:
        if not fact.get("fact_id"):
            return False, f"Факт без fact_id: {fact}"
        if not fact.get("claim"):
            return False, f"Факт без claim: {fact['fact_id']}"
        if not fact.get("source"):
            return False, f"Факт без source: {fact['fact_id']}"
        if fact.get("confidence", 0) <= 0:
            return False, f"Нулевая confidence: {fact['fact_id']}"

    return True, None


# ─── TRUTH GATE ───────────────────────────────────────────────────────────────
# Единственный вход в L3 граф. Обход = архитектурный баг.
# TODO Sprint 2: полная ESM матрица переходов, Laplace confidence.

def truth_gate(
    facts_pack: Dict[str, Any],
    min_confidence: Optional[float] = None,
) -> tuple[bool, Optional[str]]:
    """
    Верифицирует факты перед записью в L3.
    min_confidence=None → адаптивный порог (epigenetic verification, RFC0071):
    после блокировок порог растёт (защитнее), при здоровом потоке — расслабляется.
    Возвращает (passed: bool, reason: str | None).

    Type-aware: ворота НЕ выбрасывают субъективное, но не дают ему
    маскироваться под факт о мире.
      - WORLD_FACT      → требует source + confidence ≥ порога.
      - субъективные    → проходят без доказательной планки (чувство реально
        (EMOTION, OPINION…)  как чувство), но не станут WORLD_FACT.
      - LLM_OUTPUT      → не может быть WORLD_FACT сам по себе.

    Переход фактов в ESM-состояние Validated выполняется вызывающей стороной
    (run()) при passed=True. truth_gate() только принимает решение о верификации.
    """
    if min_confidence is None:
        min_confidence = adaptation.verification_threshold()
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "Нет фактов для верификации"

    for fact in facts:
        if not fact.get("source"):
            return False, f"Факт без source: {fact.get('fact_id')}"

        claim_type = fact.get("claim_type", "WORLD_FACT")

        # LLM-вывод сам по себе не является фактом о внешнем мире.
        if claim_type == "WORLD_FACT" and fact.get("source_status") == "LLM_OUTPUT":
            return False, (
                f"LLM_OUTPUT не может быть WORLD_FACT без независимого источника: "
                f"{fact.get('fact_id')}"
            )

        # Субъективные утверждения валидны как опыт — без доказательной планки.
        if claim_type in SUBJECTIVE_CLAIM_TYPES:
            continue

        # WORLD_FACT и INTERPRETATION — требуют минимальной уверенности.
        if fact.get("confidence", 0) < min_confidence:
            return False, (
                f"Confidence {fact['confidence']} < порога {min_confidence}: "
                f"{fact.get('fact_id')}"
            )

    return True, None


def _truth_status_for(claim_type: str) -> str:
    """
    Истинностный статус по модальности утверждения.
    Значимость отделена от истины: всё валидируется как память,
    но WORLD_FACT — единственное, что становится VERIFIED.
    """
    if claim_type == "WORLD_FACT":
        return "VERIFIED"
    if claim_type == "INTERPRETATION":
        return "HYPOTHESIS"
    return "SUBJECTIVE"


# ─── GENERATION ───────────────────────────────────────────────────────────────
# Ответ формирует сменный Generator (core/generation.py): дефолт — extractive,
# опционально — LLM (Claude) с FactsPack в system. Граф остаётся источником истины.

def generate_answer(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Генерация ответа из верифицированных фактов через get_generator().
    Дефолт-backend extractive (склейка); LLM — через VELANTRIM_GENERATOR=anthropic.
    """
    validated_facts = [
        f for f in facts_pack["facts"]
        if f.get("epistemic_state") in {"Validated", "Supported"}
    ]
    if not validated_facts:
        logger.warning(
            "generate_answer: нет фактов в состоянии Validated/Supported — "
            "fallback на все %d факта(ов)",
            len(facts_pack["facts"]),
        )
        validated_facts = facts_pack["facts"]

    answer = get_generator().generate(facts_pack.get("query", ""), validated_facts)

    return {
        "answer":       answer,
        "facts":        validated_facts,
        "trace":        trace,
        "trace_fmt":    format_trace(trace),
        "total_facts":  len(validated_facts),
    }


# ─── EPISODIC BINDING ─────────────────────────────────────────────────────────
# Эпизодическая память: «что-где-когда-с-кем». Факты, вспомненные вместе,
# связываются в L3 ненаправленной парой рёбер CO_OCCURRED с контекстом эпизода.
# Рёбра соединяют уже валидированные узлы — это не обход TruthGate (тот сторожит
# только вход факта-узла в канон).

_EPISODE_REL = "CO_OCCURRED"


def _entity_refs(episode: Dict[str, Any]) -> List[tuple]:
    """Сущности эпизода → [(entity_id, kind, label)] для who/where."""
    refs = []
    for name in (episode.get("who") or []):
        refs.append((f"who:{name}", "person", name))
    where = episode.get("where")
    if where is not None:
        refs.append((f"where:{where}", "place", where))
    return refs


def _link_episode(
    graph,
    facts: List[Dict[str, Any]],
    query: str,
    episode: Optional[Dict[str, Any]],
) -> None:
    """Связать со-вспомненные факты эпизодом: who/where → entity-узлы (для любого
    числа фактов) + ребро CO_OCCURRED между парами (минимум два факта)."""
    ids = [f["fact_id"] for f in facts]
    episode = episode or {}

    # Первоклассные entity-узлы who/where: каждый факт упоминает сущность.
    for entity_id, kind, label in _entity_refs(episode):
        graph.merge_entity(entity_id, kind, label)
        for fid in ids:
            graph.link_fact_to_entity(fid, entity_id)

    if len(ids) < 2:
        return  # эпизодическое ребро нужно минимум двум фактам

    props: Dict[str, Any] = {
        "query": query,
        "when": episode.get("when") or datetime.now(timezone.utc).isoformat(),
    }
    for key in ("who", "where", "event"):
        if episode.get(key) is not None:
            props[key] = episode[key]

    # Цепочка соседних пар (а не все пары) — O(n) связок, достаточно для эпизода.
    for a, b in zip(ids, ids[1:]):
        graph.add_edge(a, _EPISODE_REL, b, props)
        graph.add_edge(b, _EPISODE_REL, a, props)


def recall_episode(fact_id: str) -> List[Dict[str, Any]]:
    """
    Эпизодический recall: с какими фактами и в каком контексте (who/where/when/
    query) данный факт вспоминался вместе. Читает рёбра CO_OCCURRED — делает
    эпизодические данные, которые писал _link_episode, запрашиваемыми.
    """
    out: List[Dict[str, Any]] = []
    for edge in get_l3_graph().get_edges(fact_id, _EPISODE_REL):
        props = edge.get("props", {})
        out.append({
            "with":  edge["target"],
            "who":   props.get("who"),
            "where": props.get("where"),
            "when":  props.get("when"),
            "query": props.get("query"),
        })
    return out


def recall_by_entity(
    *, who: Optional[str] = None, where: Optional[str] = None,
) -> List[str]:
    """
    Recall по сущности: id фактов, упоминающих person/place. Прямой обратный
    обход первоклассных entity-узлов (facts_for_entity), а не скан рёбер.
    who/where задаются объединением (union).
    """
    if who is None and where is None:
        return []
    graph = get_l3_graph()
    matched = set()
    if who is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"who:{who}"))
    if where is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"where:{where}"))
    return sorted(matched)


# ─── MAIN PIPELINE ────────────────────────────────────────────────────────────

def run(query: str, episode: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Полный пайплайн Velantrim:
    Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer

    Принцип: Trace → Validation → Answer.
    Не наоборот.

    episode — необязательный контекст эпизода (who / where / when / event):
    факты, вспомненные вместе, связываются в L3 эпизодическим ребром.
    """
    metrics.incr("query.total")
    # 1. Retrieval
    retrieved = retrieve(query)
    if not retrieved:
        return _blocked("Retrieval вернул 0 результатов.", query)

    # 2. FactsPack
    facts_pack = build_facts_pack(retrieved, query)

    # 3. Trace
    trace = build_trace(retrieved)

    # 4. Guardian (структурная проверка)
    guardian_ok, guardian_reason = guardian(facts_pack, trace)
    if not guardian_ok:
        adaptation.record_block()   # стресс → растёт verification (RFC0071)
        return _blocked(f"Guardian: {guardian_reason}", query, facts_pack, trace)

    # 5. TruthGate (верификация)
    gate_ok, gate_reason = truth_gate(facts_pack)
    if not gate_ok:
        adaptation.record_block()
        return _blocked(f"TruthGate: {gate_reason}", query, facts_pack, trace)

    # 6. ESM: перевести факты и trace в Validated через transition_esm (единственный путь).
    #    truth_status выставляется по claim_type: VERIFIED только для WORLD_FACT,
    #    субъективное валидируется как опыт (Validated), но истиной о мире не становится.
    #
    #    Cross-store нюанс: SQLite (pending) и L3 (канон) — два хранилища без общей
    #    транзакции. Сбой записи в L3 ловим и возвращаем _blocked, а не роняем
    #    пайплайн трейсбеком. Частичное состояние допустимо: SQLite-факт может
    #    остаться Validated без узла в L3 — merge_fact идемпотентен, повторный
    #    прогон до-мержит. Источник истины — граф, SQLite лишь pending-кэш.
    graph = get_l3_graph()
    try:
        for fact in facts_pack["facts"]:
            # Recall-факт из L3 уже Validated — повторный переход недопустим в
            # ESM-матрице, поэтому переводим только ещё не валидированные.
            if fact.get("epistemic_state") != "Validated":
                transition_esm(fact["fact_id"], "Validated")
                updated = get_fact(fact["fact_id"])
                if updated:
                    fact["epistemic_state"] = updated["epistemic_state"]
            fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"))
            # Единственный вход в L3: канонический MERGE строго после TruthGate.
            graph.merge_fact(fact)
        # 6b. Эпизодическая связка: факты, вспомненные в одном запросе, связаны.
        _link_episode(graph, facts_pack["facts"], query, episode)
    except Exception as e:  # noqa: BLE001 — сбой L3 не должен ронять пайплайн
        logger.error("L3-промоция не удалась: %s", e)
        adaptation.record_block()
        return _blocked(f"L3 promotion failed: {e}", query, facts_pack, trace)

    promote_trace(trace, "Validated")

    # 7. Generate
    metrics.incr("query.answered")
    adaptation.record_success()     # здоровый исход → порог расслабляется
    return generate_answer(facts_pack, trace)


def _blocked(
    reason: str,
    query: str,
    facts_pack: Optional[Dict] = None,
    trace: Optional[List] = None,
) -> Dict[str, Any]:
    """Стандартный ответ при блокировке пайплайна."""
    metrics.incr("query.blocked")
    return {
        "error":  reason,
        "answer": None,
        "query":  query,
        "facts":  facts_pack.get("facts", []) if facts_pack else [],
        "trace":  trace or [],
    }


# ─── TEST ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    queries = [
        "What is quantum entanglement?",
        "How does DNA work?",
        "Tell me about the Sun",
    ]
    for q in queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {q}")
        result = run(q)
        print(f"ANSWER: {result.get('answer', 'BLOCKED')}")
        if result.get("error"):
            print(f"ERROR:  {result['error']}")
        if result.get("trace_fmt"):
            print(result["trace_fmt"])
