# hybrid_biological_memory.py
# HybridBiologicalMemory v2.1 — биологически вдохновлённая память
# RFC0070–0073 | Velantrim ExoCortex Crystal
#
# Это фасад над четырьмя каноническими слоями. Реализации живут в отдельных
# модулях (single source of truth), а не дублируются здесь:
#   - FractalMemoryLayer          → fractal_memory_layer.py        (RFC0070)
#   - EpigeneticAdaptationModule  → epigenetic_adaptation_module.py (RFC0071)
#   - ImmuneCRISPRMemoryGuard     → immune_crispr_memory_guard.py   (RFC0072)
#   - NeurogenesisDynamicGrowth   → neurogenesis_dynamic_growth.py  (RFC0073)

import time
import uuid
from typing import Dict, List, Any, Optional

from fractal_memory_layer import FractalMemoryLayer
from epigenetic_adaptation_module import EpigeneticAdaptationModule
from immune_crispr_memory_guard import ImmuneCRISPRMemoryGuard
from neurogenesis_dynamic_growth import NeurogenesisDynamicGrowth

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

    def get_full_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "fractal": self.fractal_layer.get_stats(),
            "epigenetic": self.epigenetic_module.get_state_summary(),
            "immune": self.immune_guard.get_immunity_report(),
            "neurogenesis": self.neurogenesis_module.get_stats(),
            "total_memories": len(self.memory_log),
        }

    def get_full_stats(self) -> Dict[str, Any]:
        return self.get_full_status()
