# core/consolidate.py
# Velantrim ExoCortex — SleepCycle (фоновая консолидация)
# v8.7.0-sprint2
#
# Память-физиология: «use it or lose it». reinforce() поднимает confidence при
# использовании; consolidate() — временной спад при забвении. Значимое
# (significance) забывается медленнее. Это пара к reinforce и RFC0017 (FSRS)
# из ROADMAP.
#
# Спад не разрушает факт (не Deprecate) — лишь снижает confidence, а значит и
# ранг в retrieve() (score = близость × confidence). Забытое тускнеет, но не
# исчезает; повторное свидетельство (reinforce) возвращает его.
#
# Идемпотентность: спад считается от metadata['last_consolidated'] и сдвигает
# его на now. Повторный прогон в тот же момент → elapsed=0 → без изменений.

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from core.memory import get_fact, update_fact
from core.l3_graph import get_l3_graph

_HALF_LIFE_DAYS = 30.0   # период полу-распада confidence у незначимого факта
_FLOOR = 0.02            # ниже не опускаем — факт тускнеет, но не исчезает


def consolidate(
    *,
    now: Optional[datetime] = None,
    half_life_days: float = _HALF_LIFE_DAYS,
    floor: float = _FLOOR,
) -> Dict[str, Any]:
    """
    Прогнать спад confidence по каноническим (Validated) фактам L3.
    Эффективный полу-период = half_life_days × (1 + significance): значимое
    держится дольше. Возвращает {'decayed': n, 'at': iso}.
    """
    now = now or datetime.now(timezone.utc)
    graph = get_l3_graph()
    decayed = 0

    for node in graph.all_facts():
        if node.get("epistemic_state") != "Validated":
            continue
        meta = dict(node.get("metadata") or {})
        baseline = (meta.get("last_consolidated")
                    or node.get("created_at")
                    or node.get("updated_at"))
        if not baseline:
            # Узел без опорной метки времени — например, бэкенд канона не
            # персистит created_at как колонку (LadybugDB хранит только _COLS,
            # см. l3_graph.LadybugL3Graph._COLS). Раньше такой узел пропускался
            # НАВСЕГДА → спад по нему не запускался вообще. Вместо этого заводим
            # часы спада с текущего момента: метку кладём в metadata (её
            # персистят ВСЕ бэкенды — mock / ladybug / neo4j), и на следующем
            # прогоне baseline уже найдётся. Сам спад в этот раз не применяем —
            # возраст узла неизвестен, отсчёт честно стартует «сейчас».
            meta["last_consolidated"] = now.isoformat()
            if update_fact(node["fact_id"], metadata=meta):
                graph.merge_fact(get_fact(node["fact_id"]))
            continue
        try:
            last = datetime.fromisoformat(baseline)
        except (ValueError, TypeError):
            continue

        elapsed_days = (now - last).total_seconds() / 86400.0
        if elapsed_days <= 0.0:
            continue  # уже консолидировано на этот момент — идемпотентно

        sig = float(node.get("significance", 0.5))
        eff_hl = half_life_days * (1.0 + sig)
        factor = 0.5 ** (elapsed_days / eff_hl)
        conf = float(node.get("confidence", 0.5))
        new_conf = max(floor, round(conf * factor, 4))

        meta["last_consolidated"] = now.isoformat()
        update_fact(node["fact_id"], confidence=new_conf, metadata=meta)
        graph.merge_fact(get_fact(node["fact_id"]))
        if new_conf < conf:
            decayed += 1

    return {"decayed": decayed, "at": now.isoformat()}
