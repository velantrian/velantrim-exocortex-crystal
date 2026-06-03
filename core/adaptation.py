# core/adaptation.py
# Velantrim ExoCortex — Epigenetic Adaptation wiring (RFC0071)
# v8.9.0-sprint2
#
# Оживляет прототип epigenetic_adaptation_module в ядре: блокировки на вратах —
# это «стресс»; накапливаясь, он поднимает тег verification, а тот ужесточает
# порог TruthGate. Защита от галлюцинаций адаптируется без переобучения; при
# здоровом потоке (успехи) порог постепенно расслабляется.

from typing import Dict, Any, Optional

from epigenetic_adaptation_module import EpigeneticAdaptationModule

# Базовый порог confidence для WORLD_FACT на вратах (verification == 0.5).
_BASE_CONFIDENCE = 0.05
# На сколько максимум поднимается порог при verification == 1.0.
_MAX_BOOST = 0.3
_STRESS_HIGH = 0.85   # блок на вратах
_STRESS_LOW = 0.2     # успешный ответ

_MODULE: Optional[EpigeneticAdaptationModule] = None


def get_adaptation() -> EpigeneticAdaptationModule:
    global _MODULE
    if _MODULE is None:
        _MODULE = EpigeneticAdaptationModule()
    return _MODULE


def reset_adaptation() -> None:
    """Сбросить состояние (для тестов / нового окна)."""
    global _MODULE
    _MODULE = None


def record_block() -> None:
    """Зафиксировать стресс — блок на Guardian/TruthGate/L3."""
    get_adaptation().record_stress(_STRESS_HIGH, context="gate_block")


def record_success() -> None:
    """Зафиксировать здоровый исход — успешный ответ."""
    get_adaptation().record_stress(_STRESS_LOW, context="answered")


def verification_threshold() -> float:
    """
    Адаптивный порог confidence для WORLD_FACT: растёт с тегом verification.
    verification 0.5 → базовый 0.05; 1.0 → 0.05 + _MAX_BOOST.
    """
    v = get_adaptation().epigenetic_tags["verification"]
    return round(_BASE_CONFIDENCE + max(0.0, v - 0.5) * (_MAX_BOOST / 0.5), 4)


def state() -> Dict[str, Any]:
    """Сводка эпигенетического состояния (теги, средний стресс)."""
    return get_adaptation().get_state_summary()
