# core/reconcile.py
# Velantrim ExoCortex — Truth Maintenance (reconcile)
# v8.6.0-sprint2
#
# Что происходит, когда новый факт встречает уже существующий канон:
#   reinforce()  — повторное независимое свидетельство → confidence растёт
#                  (Laplace-затухание), противоречащее → падает. Память отражает
#                  накопленную надёжность, а не последнюю запись.
#   supersede()  — переформулировка: старый факт → Deprecated + ребро
#                  SUPERSEDED_BY на новый (новый → Validated). Память обновляется
#                  версионно, а не перезаписывается вслепую.
#   contradict() — старый факт → Contradicted + ребро CONTRADICTS на источник.
#                  (Immune-слой из README.) Не затирает молча.
#
# Всё детерминировано и явно. Авто-детекция семантических противоречий (NLI/LLM)
# намеренно НЕ делается здесь — она дала бы ложные срабатывания; оставлена как
# будущий хук. Единственная авто-операция — reinforce при точном повторе claim
# (см. ingest.ingest), это безопасно.

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from core.memory import get_fact, store_fact, transition_esm, update_fact
from core.l3_graph import get_l3_graph

REL_SUPERSEDED_BY = "SUPERSEDED_BY"
REL_CONTRADICTS = "CONTRADICTS"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sync_l3(fact_id: str) -> Optional[Dict[str, Any]]:
    """Пере-смержить факт из SQLite в L3, чтобы канон отражал свежее состояние."""
    fact = get_fact(fact_id)
    if fact is not None:
        get_l3_graph().merge_fact(fact)
    return fact


def reinforce(fact_id: str, agreement: bool = True) -> Optional[float]:
    """
    Подкрепить факт независимым свидетельством. Возвращает новый confidence
    (или None, если факта нет).

    agreement=True  → confidence += (1 - confidence) / (obs + 1)  — затухающий рост.
    agreement=False → confidence *= obs / (obs + 1)               — затухающее падение.
    Счётчик наблюдений хранится в metadata['observations'].
    """
    fact = get_fact(fact_id)
    if fact is None:
        return None

    meta = dict(fact.get("metadata") or {})
    obs = int(meta.get("observations", 1))
    conf = float(fact.get("confidence", 0.5))

    if agreement:
        new_conf = round(conf + (1.0 - conf) / (obs + 1), 4)
    else:
        new_conf = round(conf * obs / (obs + 1), 4)

    meta["observations"] = obs + 1
    update_fact(fact_id, confidence=new_conf, metadata=meta)
    _sync_l3(fact_id)
    return new_conf


def supersede(old_id: str, new_fact: Dict[str, Any]) -> str:
    """
    Новый факт замещает старый. Старый: Validated → Contradicted → Deprecated
    (+ ребро old -SUPERSEDED_BY-> new). Новый: сохраняется и Validated.
    Возвращает fact_id нового факта.
    """
    new_id = new_fact.get("fact_id")
    if not new_id:
        raise ValueError("supersede: new_fact.fact_id обязателен")

    store_fact({**new_fact, "epistemic_state": "Observed"})
    transition_esm(new_id, "Validated")
    _sync_l3(new_id)

    old = get_fact(old_id)
    if old is not None and old.get("epistemic_state") == "Validated":
        # Прямого Validated→Deprecated в матрице нет: идём через Contradicted.
        transition_esm(old_id, "Contradicted")
        transition_esm(old_id, "Deprecated")
        _sync_l3(old_id)

    get_l3_graph().add_edge(old_id, REL_SUPERSEDED_BY, new_id, {"at": _now()})
    return new_id


def contradict(fact_id: str, by_id: str) -> bool:
    """
    Пометить факт как опровергнутый источником by_id: Validated → Contradicted
    (+ ребро fact -CONTRADICTS-> by). Возвращает True, если состояние изменилось.
    """
    fact = get_fact(fact_id)
    changed = False
    if fact is not None and fact.get("epistemic_state") == "Validated":
        transition_esm(fact_id, "Contradicted")
        _sync_l3(fact_id)
        changed = True
    get_l3_graph().add_edge(fact_id, REL_CONTRADICTS, by_id, {"at": _now()})
    return changed
