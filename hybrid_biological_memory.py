# hybrid_biological_memory.py — финальная исправленная версия v1.3
import time
from fractal_memory_layer import FractalMemoryLayer
from epigenetic_adaptation_module import EpigeneticAdaptationModule
from immune_crispr_memory_guard import ImmuneCRISPRMemoryGuard
from neurogenesis_dynamic_growth import NeurogenesisDynamicGrowth

class HybridBiologicalMemory:
    def __init__(self, name="Velantrim-Hybrid"):
        self.name = name
        self.fractal_layer = FractalMemoryLayer()
        self.epigenetic_module = EpigeneticAdaptationModule()
        self.immune_guard = ImmuneCRISPRMemoryGuard()
        self.neurogenesis_module = NeurogenesisDynamicGrowth()
        self.neurogenesis = self.neurogenesis_module   # алиас для тестов
        self.memory_log = []
        print(f"🌿🧠 HybridBiologicalMemory '{self.name}' initialized with 4 biological layers.")

    def add_memory(self, text: str, importance: float = 0.5):
        self.fractal_layer.add_memory(text, importance)
        self.neurogenesis_module.integrate_new_memory({"text": text}, importance)
        self.immune_guard.check_fact(text)
        self.memory_log.append({"text": text, "importance": importance})
        return True

    def adapt_behavior(self, params: dict = None):
        if params is None:
            params = {}
        return self.epigenetic_module.adapt_behavior(params)

    def add_new_neurons(self, count: int):
        return self.neurogenesis_module.add_new_neurons(count)

    def record_stress(self, level: float, reason: str = ""):
        self.epigenetic_module.record_stress(level, reason)

    def check_and_block_contradiction(self, text: str):
        return self.immune_guard.check_fact(text)

    def inherit_to_child(self):
        return HybridBiologicalMemory(name=f"{self.name}-child")

    def get_full_status(self):
        return {
            "fractal": self.fractal_layer.get_stats(),
            "epigenetic": self.epigenetic_module.get_state(),
            "immune": self.immune_guard.get_immunity_report(),
            "neurogenesis": self.neurogenesis_module.get_stats()
        }

    def get_full_stats(self):
        return self.get_full_status()