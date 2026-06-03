# core/ingest.py
# Velantrim ExoCortex — Ingestion Layer
# v8.4.0-sprint2
#
# Назначение: превратить реплику пользователя в факт с правильной модальностью
# (claim_type) и происхождением (source_status), провести через те же врата
# (Guardian → TruthGate) и записать в канон L3. Это «оживляет» субъективный путь:
# теперь EMOTION / OPINION / GOAL рождаются из живого ввода, а не только из корпуса.
#
# Классификатор — эвристический (без LLM-зависимости): ловит маркеры чувства,
# мнения, цели, предпочтения, предположения; иначе — утверждение о мире.
# Замена на LLM-классификатор — отдельный шаг (см. core/generation.py паттерн).

import hashlib
import re
from typing import Dict, Any, Optional

from core.memory import store_fact, get_fact, transition_esm
from core.l3_graph import get_l3_graph
from core.pipeline import guardian, truth_gate, _truth_status_for
from core.reconcile import reinforce, find_conflicts
from core import metrics

# Маркеры модальности (RU + EN). Порядок важен: проверяем от частного к общему.
_CLAIM_MARKERS = [
    ("EMOTION", [
        r"\bi\s+feel\b", r"\bi\s+felt\b", r"\bfeel(s|ing)?\b", r"\bafraid\b",
        r"\bя\s+чувству", r"\bя\s+почувствова", r"\bмне\s+(страшно|тревожно|больно|радостно)",
        r"\bчувству", r"\bтревог",
    ]),
    ("OPINION", [
        r"\bi\s+think\b", r"\bi\s+believe\b", r"\bin\s+my\s+opinion\b", r"\bimho\b",
        r"\bя\s+(думаю|считаю|полагаю)", r"\bпо-?моему\b", r"\bна\s+мой\s+взгляд\b",
    ]),
    ("GOAL", [
        r"\bi\s+want\b", r"\bi\s+need\b", r"\bmy\s+goal\b", r"\bi('?d| would)\s+like\b",
        r"\bя\s+хочу\b", r"\bмне\s+нужно\b", r"\bмоя\s+цель\b",
    ]),
    ("PREFERENCE", [
        r"\bi\s+prefer\b", r"\bi\s+like\b.*\bbetter\b", r"\bi\s+love\b",
        r"\bя\s+предпочита", r"\bмне\s+больше\s+нравится\b",
    ]),
    ("INTERPRETATION", [
        r"\bmaybe\b", r"\bprobably\b", r"\bperhaps\b", r"\bi\s+guess\b",
        r"\bseems?\s+(like|to)\b", r"\bit\s+looks\s+like\b",
        r"\bнаверное\b", r"\bвозможно\b", r"\bкажется\b", r"\bмне\s+кажется\b",
        r"\bпохоже\b",
    ]),
]


def classify_claim(utterance: str) -> tuple[str, str]:
    """
    (claim_type, source_status) для реплики пользователя.
    Реплика всегда USER_REPORTED; тип — по лингвистическим маркерам,
    иначе WORLD_FACT (утверждение о мире).
    """
    text = utterance.lower()
    for claim_type, patterns in _CLAIM_MARKERS:
        if any(re.search(p, text) for p in patterns):
            return claim_type, "USER_REPORTED"
    return "WORLD_FACT", "USER_REPORTED"


def _fact_id(utterance: str) -> str:
    return "ing:" + hashlib.md5(utterance.encode("utf-8")).hexdigest()[:12]


def ingest(
    utterance: str,
    *,
    fact_id: Optional[str] = None,
    source: str = "user",
    confidence: float = 0.6,
    significance: float = 0.5,
    claim_type: Optional[str] = None,
    episode: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Принять реплику, классифицировать, провести через врата, записать в L3.

    Возвращает результат: {accepted, fact, reason?}.
    - accepted=True  → факт прошёл TruthGate, переведён в Validated, MERGE в L3.
    - accepted=False → заблокирован (reason). В SQLite он остаётся как Observed.

    claim_type можно задать явно (минуя классификатор); source_status всегда
    USER_REPORTED — это сообщение пользователя.
    """
    if not utterance or not utterance.strip():
        raise ValueError("ingest: пустая реплика")

    ct, source_status = classify_claim(utterance)
    if claim_type is not None:
        ct = claim_type

    fid = fact_id or _fact_id(utterance)

    # Точный повтор уже принятого факта (тот же content-hash id, Validated) —
    # это независимое свидетельство: подкрепляем confidence, а не плодим дубль.
    metrics.incr("ingest.total")
    prior = get_fact(fid)
    if prior is not None and prior.get("epistemic_state") == "Validated":
        reinforce(fid)
        metrics.incr("ingest.reinforced")
        return {"accepted": True, "reinforced": True, "fact": get_fact(fid)}

    fact = {
        "fact_id": fid,
        "claim": utterance.strip(),
        "source": source,
        "confidence": confidence,
        "epistemic_state": "Observed",
        "claim_type": ct,
        "source_status": source_status,
        "significance": significance,
        "truth_status": "UNVERIFIED",
    }

    # L0/L1: сохраняем как сырой опыт (pending), даже если врата не пропустят.
    store_fact(fact)

    facts_pack = {"facts": [fact], "query": utterance, "total": 1}
    trace = [{
        "fact_id": fid, "source": source, "origin": "ingestion",
        "epistemic_state": "Observed", "confidence": confidence,
    }]

    ok, reason = guardian(facts_pack, trace)
    if ok:
        ok, reason = truth_gate(facts_pack)
    if not ok:
        metrics.incr("ingest.blocked")
        return {"accepted": False, "reason": reason, "fact": fact}

    # Прошёл врата → Validated, truth_status по модальности, MERGE в канон L3.
    transition_esm(fid, "Validated")
    updated = get_fact(fid)
    if updated:
        fact["epistemic_state"] = updated["epistemic_state"]
    fact["truth_status"] = _truth_status_for(ct)

    graph = get_l3_graph()
    graph.merge_fact(fact)

    metrics.incr("ingest.accepted")
    result = {"accepted": True, "fact": fact}
    # Immune-сигнал: для фактов о мире выявляем кандидатов на конфликт с каноном
    # (близкие, но другие). Не действуем автоматически — отдаём на решение.
    if ct == "WORLD_FACT":
        conflicts = find_conflicts(utterance, fact_id=fid)
        if conflicts:
            result["conflicts"] = conflicts
    return result
