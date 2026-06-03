# core/metrics.py
# Velantrim ExoCortex — lightweight in-process metrics
# v8.8.0-sprint2
#
# Счётчики операций памяти (запросы, ingest, врата) — наблюдаемость без внешних
# зависимостей. Структура простая (name → count), легко экспортируется в
# Prometheus позже. Потокобезопасность для MVP не требуется (sync-пайплайн).

from typing import Dict

_COUNTERS: Dict[str, int] = {}


def incr(name: str, n: int = 1) -> None:
    """Увеличить счётчик `name` на n."""
    _COUNTERS[name] = _COUNTERS.get(name, 0) + n


def value(name: str) -> int:
    """Текущее значение счётчика (0, если не было)."""
    return _COUNTERS.get(name, 0)


def snapshot() -> Dict[str, int]:
    """Копия всех счётчиков."""
    return dict(_COUNTERS)


def reset() -> None:
    """Обнулить все счётчики (для тестов / нового окна наблюдения)."""
    _COUNTERS.clear()
