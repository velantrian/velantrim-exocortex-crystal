# core/pipeline.py
# Velantrim ExoCortex — Core Pipeline
# v8.0.2-sprint1
#
# Принцип: Graph = Truth · LLM = Language · Memory = Physiology
# Пайплайн: Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer
#
# Текущий уровень: MVP (L0/L1 память, BM25-lite retrieval).
# Полная архитектура L0–L6: docs/Velantrim_V8_Crystal_Sprint1_toc.md
#
# TODO (Sprint 2):
#   - L3 граф: реализовать LadybugDB backend (core/l3_graph.py) — спайк pending.
#     (Kuzu заморожен окт.2025; LadybugDB — его Cypher-совместимый преемник.)
#   - Подключить HybridRetriever (BM25 + vector + HotGraph) поверх L3 vector index
#   - Подключить LLM для generate_answer()
#   - ESM: полная матрица переходов между состояниями

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
# Косинусная близость эмбеддингов вместо лексического пересечения токенов.
# Это убирает баг ранжирования по стоп-словам (запрос "...about the Sun" больше
# не цепляет факт по слову "the"). Эмбеддер сменный (core/embedding.py): дефолт —
# HashingEmbedder, реальная семантика — через VELANTRIM_EMBEDDER=sbert.
# TODO Sprint 2: гибрид (vector + HotGraph + HippoRAG PageRank).

# Порог отсечения шума от хэш-коллизий: ниже — не релевантно.
_RETRIEVAL_MIN_SIM = 0.05


def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Семантический поиск по DATABASE через косинус эмбеддингов.
    Возвращает топ-k фактов, отсортированных по score (близость × confidence).
    Все факты начинают с epistemic_state='Observed' (сырой вход).
    """
    embedder = get_embedder()
    q_vec = embedder.embed(query)
    scored: List[Dict[str, Any]] = []

    for item in DATABASE:
        sim = cosine(q_vec, embedder.embed(item["text"]))
        if sim < _RETRIEVAL_MIN_SIM:
            continue

        # близость взвешиваем базовой уверенностью источника
        final_score = sim * item.get("confidence", 1.0)

        scored.append({
            **item,
            "_score":          round(final_score, 4),
            "epistemic_state": "Observed",   # ESM: начальное состояние
            "origin":          "retrieval",
        })

    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:k]


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
    min_confidence: float = 0.05,
) -> tuple[bool, Optional[str]]:
    """
    Верифицирует факты перед записью в L3.
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


def _link_episode(
    graph,
    facts: List[Dict[str, Any]],
    query: str,
    episode: Optional[Dict[str, Any]],
) -> None:
    """Связать со-вспомненные факты эпизодическим ребром (who/where/when/event)."""
    ids = [f["fact_id"] for f in facts]
    if len(ids) < 2:
        return  # эпизодическая связь нужна минимум двум фактам

    episode = episode or {}
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
        return _blocked(f"Guardian: {guardian_reason}", query, facts_pack, trace)

    # 5. TruthGate (верификация)
    gate_ok, gate_reason = truth_gate(facts_pack)
    if not gate_ok:
        return _blocked(f"TruthGate: {gate_reason}", query, facts_pack, trace)

    # 6. ESM: перевести факты и trace в Validated через transition_esm (единственный путь).
    #    truth_status выставляется по claim_type: VERIFIED только для WORLD_FACT,
    #    субъективное валидируется как опыт (Validated), но истиной о мире не становится.
    graph = get_l3_graph()
    for fact in facts_pack["facts"]:
        transition_esm(fact["fact_id"], "Validated")
        updated = get_fact(fact["fact_id"])
        if updated:
            fact["epistemic_state"] = updated["epistemic_state"]
        fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"))
        # Единственный вход в L3: канонический MERGE строго после TruthGate.
        graph.merge_fact(fact)

    # 6b. Эпизодическая связка: факты, вспомненные в одном запросе, связаны.
    _link_episode(graph, facts_pack["facts"], query, episode)

    promote_trace(trace, "Validated")

    # 7. Generate
    return generate_answer(facts_pack, trace)


def _blocked(
    reason: str,
    query: str,
    facts_pack: Optional[Dict] = None,
    trace: Optional[List] = None,
) -> Dict[str, Any]:
    """Стандартный ответ при блокировке пайплайна."""
    return {
        "error":  reason,
        "answer": None,
        "query":  query,
        "facts":  facts_pack.get("facts", []) if facts_pack else [],
        "trace":  trace or [],
    }


# ─── TEST ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
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
