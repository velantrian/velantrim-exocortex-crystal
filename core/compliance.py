# core/compliance.py
# Velantrim ExoCortex — GDPR Compliance Operations
# v8.9.0-sprint2
#
# Две операции подотчётности, не относящиеся к удалению (Art. 17 → erasure.py):
#
#   Art. 18 — ограничение обработки. restrict_processing() «замораживает» факт:
#     он хранится, но исключается из активной обработки (recall/ответы; см.
#     pipeline.retrieve, фильтр по node['restricted']). Обратимо через
#     unrestrict_processing(). Не удаление и не смена ESM-состояния.
#
#   Art. 30 — record of processing. record_of_processing() собирает агрегатный,
#     content-free отчёт об обработке: счётчики по категориям, ограничения,
#     удаления, бэкенды, расположение данных. Персональные данные (claim) НЕ
#     включаются — только метаданные и идентификаторы.

import os
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core.memory import set_restricted, get_fact, get_all_facts, get_tombstones
from core.l3_graph import get_l3_graph


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sync_restriction(fact_id: str) -> None:
    """Перенести флаг restricted в L3-узел, чтобы recall его видел."""
    fact = get_fact(fact_id)
    if fact is not None:
        get_l3_graph().merge_fact(fact)


def restrict_processing(
    fact_id: str, *, reason: str = "data_subject_request", actor: str = "operator"
) -> Dict[str, Any]:
    """
    Ограничить обработку факта (GDPR Art. 18): факт остаётся в памяти, но
    исключается из recall/ответов. Возвращает квитанцию; found=False, если
    факта нет.
    """
    found = set_restricted(fact_id, True)
    if found:
        _sync_restriction(fact_id)
    return {"fact_id": fact_id, "restricted": True, "found": found,
            "reason": reason, "actor": actor, "at": _now()}


def unrestrict_processing(
    fact_id: str, *, actor: str = "operator"
) -> Dict[str, Any]:
    """Снять ограничение обработки (Art. 18): факт снова участвует в recall."""
    found = set_restricted(fact_id, False)
    if found:
        _sync_restriction(fact_id)
    return {"fact_id": fact_id, "restricted": False, "found": found,
            "actor": actor, "at": _now()}


def is_restricted(fact_id: str) -> bool:
    """True, если обработка факта ограничена (Art. 18)."""
    fact = get_fact(fact_id)
    return bool(fact and fact.get("restricted"))


def restricted_facts() -> List[str]:
    """fact_id'ы всех фактов с ограничением обработки."""
    return [f["fact_id"] for f in get_all_facts() if f.get("restricted")]


def record_of_processing(controller: Optional[str] = None) -> Dict[str, Any]:
    """
    Сформировать record of processing (GDPR Art. 30): агрегатный content-free
    отчёт об обработке. Не содержит персональных данных (claim) — только
    счётчики, идентификаторы и конфигурацию.
    """
    facts = get_all_facts()
    by_claim_type = Counter(f.get("claim_type", "UNKNOWN") for f in facts)
    by_state = Counter(f.get("epistemic_state", "Observed") for f in facts)
    by_source_status = Counter(f.get("source_status", "UNKNOWN") for f in facts)
    restricted = [f["fact_id"] for f in facts if f.get("restricted")]
    erasures = get_tombstones()

    l3 = os.environ.get("VELANTRIM_L3_BACKEND", "auto")
    embedder = os.environ.get("VELANTRIM_EMBEDDER", "auto")
    generator = os.environ.get("VELANTRIM_GENERATOR", "extractive")
    transfers = (generator == "claude") or l3 == "neo4j"

    return {
        "generated_at": _now(),
        "regulation": "GDPR (EU) 2016/679, Art. 30",
        "controller": controller or os.environ.get(
            "VELANTRIM_CONTROLLER", "(operator-defined)"),
        "processing_purpose": (
            "Verifiable AI memory: storage and provenance-tracked retrieval "
            "of facts for trustworthy AI systems"),
        "data_location": (
            "local: L1 (SQLite) + L3 (embedded graph). No third-party transfer "
            "in the default configuration."),
        "backends": {"l3_graph": l3, "embedder": embedder, "generator": generator},
        "international_transfer": transfers,
        "fact_count": len(facts),
        "categories_of_data": dict(by_claim_type),
        "by_epistemic_state": dict(by_state),
        "by_source_status": dict(by_source_status),
        "restricted_count": len(restricted),
        "restricted_fact_ids": restricted,
        "erasure_count": len(erasures),
        "erasure_log": erasures,
        "data_subject_rights": {
            "access": "get_all_facts() / CLI report",
            "rectification": "update_fact / reconcile.supersede (Art. 16)",
            "erasure": "erasure.erase_fact (Art. 17)",
            "restriction": "compliance.restrict_processing (Art. 18)",
            "portability": "SQLite + JSON export (Art. 20)",
        },
        "security_measures": [
            "single-entry TruthGate (Graph = Truth, I1)",
            "Ring Zero immutability (I6)",
            "validated ESM transitions",
            "content-free erasure tombstones",
            "no telemetry; no outbound calls by default",
        ],
    }
