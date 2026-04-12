# core/trace.py
# Velantrim ExoCortex — Trace / Provenance Layer
# v8.0.2-sprint1
#
# Назначение: строит цепочку провенанса для каждого факта.
# Принцип: Trace → Validation → Answer (не наоборот).
# Каждый trace-элемент содержит epistemic_state из ESM.
#
# Полная архитектура: docs/Velantrim_V8_Crystal_Sprint1_toc.md

from typing import List, Dict, Any
from datetime import datetime, timezone


# ─── TRACE BUILDER ────────────────────────────────────────────────────────────

def build_trace(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Построить trace-цепочку из списка извлечённых фактов.

    Каждый элемент содержит:
      - fact_id:         идентификатор факта
      - source:          источник (откуда пришёл факт)
      - origin:          способ получения (retrieval / ingestion / volition)
      - epistemic_state: текущее ESM-состояние факта
      - retrieved_at:    временная метка извлечения

    epistemic_state:
      Observed → факт только что получен из retrieval, ещё не верифицирован.
      Validated → прошёл TruthGate (выставляется в pipeline после truth_gate()).
      Полный список ESM-состояний: core/memory.py → ESM_STATES.
    """
    trace: List[Dict[str, Any]] = []
    now = datetime.now(timezone.utc).isoformat()

    for item in retrieved:
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue  # пропустить некорректные записи

        trace.append({
            "fact_id":         fact_id,
            "source":          item.get("source", "unknown"),
            "origin":          item.get("origin", "retrieval"),
            "epistemic_state": item.get("epistemic_state", "Observed"),
            "confidence":      round(float(item.get("_score", 0.5)), 4),
            "retrieved_at":    now,
        })

    return trace


def promote_trace(
    trace: List[Dict[str, Any]],
    new_state: str
) -> List[Dict[str, Any]]:
    """
    Обновить epistemic_state всех элементов trace после прохождения TruthGate.
    Вызывается из pipeline после truth_gate() → True.

    Пример: promote_trace(trace, "Validated")
    """
    now = datetime.now(timezone.utc).isoformat()
    for element in trace:
        element["epistemic_state"] = new_state
        element["promoted_at"] = now
    return trace


def format_trace(trace: List[Dict[str, Any]]) -> str:
    """
    Человекочитаемый вывод trace-цепочки для логов и ответа.
    """
    if not trace:
        return "TRACE: empty"
    lines = ["TRACE:"]
    for i, el in enumerate(trace, 1):
        lines.append(
            f"  [{i}] {el['fact_id']} | "
            f"source={el['source']} | "
            f"state={el['epistemic_state']} | "
            f"confidence={el.get('confidence', '?')}"
        )
    return "\n".join(lines)
