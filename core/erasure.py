# core/erasure.py
# Velantrim ExoCortex — Right to Erasure (GDPR Art. 17)
# v8.9.0-sprint2
#
# Физическое удаление факта по всем тканям памяти + подотчётность.
#
# Принцип: удаление обязано быть ПОЛНЫМ и ДОКАЗУЕМЫМ одновременно.
#   Полным  — узел исчезает из L0 (кэш), L1 (SQLite), L3 (канон: узел + рёбра +
#             mentions) и из L3-outbox (очередь до-мержа). Нигде не остаётся
#             персональных данных и висячих ссылок.
#   Доказуемым — в erasure_log пишется content-free tombstone: fact_id, время,
#             причина, актор и sha256-хэш стёртого claim (не сам claim). Это
#             record of processing (Art. 30): можно доказать, ЧТО и КОГДА было
#             удалено, не воссоздавая стёртое (Art. 17).
#
# Ring Zero / VALUES_CORE НЕ удаляются (инвариант I6): это системные ценности,
# а не персональные данные; их удаление сломало бы систему.

import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List

from core.memory import (
    get_fact,
    delete_fact_l1,
    clear_l3_write,
    write_tombstone,
    get_tombstone,
    get_tombstones,
    IMMUTABLE_FACT_IDS,
    ImmutableStateError,
)
from core.l3_graph import get_l3_graph


def _hash_claim(claim: str) -> str:
    """Хэш стёртого утверждения — доказательство без хранения содержимого."""
    return "sha256:" + hashlib.sha256(claim.encode("utf-8")).hexdigest()


def erase_fact(
    fact_id: str,
    *,
    reason: str = "data_subject_request",
    actor: str = "operator",
) -> Dict[str, Any]:
    """
    Физически и безвозвратно удалить факт (GDPR Art. 17, право на забвение).

    Снимает факт из L0, L1, канонического графа L3 (узел + все рёбра + mentions)
    и из L3-outbox, затем пишет content-free tombstone в erasure_log.

    Ring Zero / VALUES_CORE неудаляемы (I6) → ImmutableStateError.

    Идемпотентно: повторное удаление уже стёртого факта возвращает
    erased_now=False, tombstone не дублируется (фиксируется первое удаление).

    Возвращает квитанцию (receipt) с деталями операции.
    """
    if fact_id in IMMUTABLE_FACT_IDS:
        raise ImmutableStateError(
            f"erase_fact: '{fact_id}' защищён Ring Zero (I6) и не подлежит удалению"
        )

    fact = get_fact(fact_id)
    content_hash = _hash_claim(fact["claim"]) if fact and fact.get("claim") else None

    # Удаление по всем тканям. Каждый шаг идемпотентен и независим.
    l1_removed = delete_fact_l1(fact_id)
    l3_removed = get_l3_graph().erase_fact(fact_id)
    clear_l3_write(fact_id)  # снять возможную запись из очереди до-мержа

    erased_now = l1_removed or l3_removed

    # Tombstone иммутабелен: при повторном удалении сохраняется исходный хэш.
    write_tombstone(fact_id, reason=reason, actor=actor, content_hash=content_hash)
    tombstone = get_tombstone(fact_id)

    return {
        "fact_id": fact_id,
        "erased_now": erased_now,
        "l1_removed": l1_removed,
        "l3_removed": l3_removed,
        "reason": reason,
        "actor": actor,
        "content_hash": (tombstone or {}).get("content_hash"),
        "erased_at": (tombstone or {}).get(
            "erased_at", datetime.now(timezone.utc).isoformat()),
    }


def is_erased(fact_id: str) -> bool:
    """True, если для факта существует tombstone (он был стёрт)."""
    return get_tombstone(fact_id) is not None


def erasure_log() -> List[Dict[str, Any]]:
    """
    Журнал всех удалений (Art. 30, record of processing). Content-free:
    содержит fact_id / время / причину / актора / хэш, но не персональные данные.
    """
    return get_tombstones()
