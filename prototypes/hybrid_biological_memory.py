# prototypes/hybrid_biological_memory.py
# HybridBiologicalMemory v2.1 — биологически вдохновлённая память
# RFC0070–0073 | Velantrim ExoCortex Crystal
#
# Это фасад над четырьмя слоями. Реализации живут в отдельных модулях
# (single source of truth), а не дублируются здесь:
#   - FractalMemoryLayer          → prototypes/fractal_memory_layer.py       (RFC0070)
#   - EpigeneticAdaptationModule  → epigenetic_adaptation_module.py (wired в core, RFC0071)
#   - ImmuneCRISPRMemoryGuard     → prototypes/immune_crispr_memory_guard.py (RFC0072)
#   - NeurogenesisDynamicGrowth   → prototypes/neurogenesis_dynamic_growth.py (RFC0073)
#
# ⚠️ Прототип: НЕ вшит в core-пайплайн (в отличие от epigenetic). См. FUTURE.md §3.3.

import time
import uuid
from typing import Dict, List, Any, Optional

from prototypes.fractal_memory_layer import FractalMemoryLayer
from epigenetic_adaptation_module import EpigeneticAdaptationModule
from prototypes.immune_crispr_memory_guard import ImmuneCRISPRMemoryGuard
from prototypes.neurogenesis_dynamic_growth import NeurogenesisDynamicGrowth

# Известные противоречия, которыми засевается иммунный страж — чтобы базовые
# галлюцинации блокировались "из коробки" (заменяет хардкод старых заглушек).
_DEFAULT_CONTRADICTIONS = [
    "capital of france is berlin",
    "capital of germany is paris",
    "париж столица германии",
    "германия столица франции",
]

# Базовые параметры генерации, которые эпигенетический слой адаптирует на месте.
_DEFAULT_PARAMS = {
    "verification_strength": 0.5,
    "temperature": 1.0,
    "exploration_rate": 0.5,
}


class HybridBiologicalMemory:
    """Фасад над четырьмя биологическими слоями (RFC0070–0073).

    Делегирует работу каноническим модулям вместо переопределения классов
    внутри файла. Публичный API сохранён ради DEMO.md и интеграций.
    """

    def __init__(self, name: str = "Velantrim-Hybrid"):
        self.name = name
        self.fractal_layer = FractalMemoryLayer()
        self.epigenetic_module = EpigeneticAdaptationModule()
        self.immune_guard = ImmuneCRISPRMemoryGuard()
        self.neurogenesis_module = NeurogenesisDynamicGrowth()
        self.memory_log: List[Dict[str, Any]] = []

        # Засев известных противоречий напрямую (без шумного record_threat-лога).
        for pattern in _DEFAULT_CONTRADICTIONS:
            self.immune_guard.blocked_patterns.add(pattern)

        print(f"🌿🧠 HybridBiologicalMemory '{self.name}' инициализирована "
              f"(4 биологических слоя)")

    def add_memory(self, text: str, importance: float = 0.5) -> str:
        """Записать память во фрактальный и нейрогенезный слои. Возвращает id."""
        mem_id = str(uuid.uuid4())
        item = {
            "id": mem_id,
            "text": text,
            "importance": importance,
            "timestamp": time.time(),
        }
        # Масштаб якорения зависит от важности (short / medium / long).
        scale = "long" if importance > 0.7 else "medium" if importance > 0.4 else "short"
        self.fractal_layer.recursive_anchor(item, scale=scale)
        self.neurogenesis_module.integrate_new_memory(item, importance)
        self.memory_log.append(item)
        return mem_id

    def adapt_behavior(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Адаптировать параметры генерации через эпигенетический слой.

        Засеваем разумные дефолты, поверх которых вызывающая сторона может
        передать свои значения; эпигенетический слой правит их на месте.
        """
        merged = dict(_DEFAULT_PARAMS)
        if params:
            merged.update(params)
        return self.epigenetic_module.adapt_behavior(merged)

    def add_new_neurons(self, count: int = 20) -> str:
        return self.neurogenesis_module.add_new_neurons(count)

    def record_stress(self, level: float, reason: str = "") -> None:
        self.epigenetic_module.record_stress(level, context=reason or "general")

    def check_and_block_contradiction(self, text: str) -> bool:
        """True == вход заблокирован иммунным стражем (известный паттерн)."""
        return self.immune_guard.check_and_block(text)

    def record_threat(self, threat_type: str, pattern: str, severity: float = 1.0) -> None:
        """Зарегистрировать новую угрозу/противоречие для блокировки."""
        self.immune_guard.record_threat(threat_type, pattern, severity)

    def inherit_to_child(self) -> "HybridBiologicalMemory":
        """Создать дочернюю память с унаследованным эпигенетическим/нейро-состоянием."""
        child = HybridBiologicalMemory(f"{self.name}-child")
        child.epigenetic_module = self.epigenetic_module.inherit_to_child()
        child.neurogenesis_module = self.neurogenesis_module.inherit_to_child()
        child.immune_guard.blocked_patterns |= self.immune_guard.blocked_patterns
        return child

    def get_full_stats(self) -> Dict[str, Any]:
        """Сводный статус всех четырёх слоёв (используется DEMO.md и тестами)."""
        return {
            "name": self.name,
            "fractal": self.fractal_layer.get_stats(),
            "epigenetic": self.epigenetic_module.get_state_summary(),
            "immune": self.immune_guard.get_immunity_report(),
            "neurogenesis": self.neurogenesis_module.get_stats(),
            "total_memories": len(self.memory_log),
        }


# Demo — повторяет пример из DEMO.md, чтобы `python -m prototypes.hybrid_biological_memory`
# действительно что-то показывал. Прототип, не вшит в core-пайплайн (см. FUTURE.md §3.3).
if __name__ == "__main__":  # pragma: no cover
    hbm = HybridBiologicalMemory()

    # 1. Память (фрактальный + нейрогенезный слои)
    hbm.add_memory(
        "Important event: first deep conversation about biological memory",
        importance=0.95,
    )

    # 2. Стресс → эпигенетическая адаптация
    hbm.record_stress(0.82, "hallucination_detected")
    adapted = hbm.adapt_behavior()
    print("Adapted verification strength:", adapted["verification_strength"])

    # 3. Иммунный страж (CRISPR): блок известного противоречия
    blocked = hbm.check_and_block_contradiction("The capital of France is Berlin")
    print("Contradiction blocked:", blocked)

    # 4. Нейрогенез: новые пластичные «нейроны»
    print(hbm.add_new_neurons(15))

    # 5. Полная сводка по слоям
    print("Full stats:", hbm.get_full_stats())

    # 6. Наследование дочерней памяти (как семена у растений)
    child = hbm.inherit_to_child()
    print("Child system created:", child.name)
