# Hybrid Biological Memory System (RFC0070 + RFC0071 + RFC0072)
# Интеграция фрактальной, эпигенетической и иммунной памяти

from fractal_memory_layer import FractalMemoryLayer

from epigenetic_adaptation_module import EpigeneticAdaptationModule

from immune_crispr_memory_guard import ImmuneCRISPRMemoryGuard


class HybridBiologicalMemory:
    def __init__(self):
        self.fractal = FractalMemoryLayer()
        self.epigenetic = EpigeneticAdaptationModule()
        self.immune = ImmuneCRISPRMemoryGuard()
        print("🧬 Hybrid Biological Memory initialized (Human + Animals + Plants + Bacteria + Fractals)")

    def process_input(self, text: str, stress_level: float = 0.0):
        # 1. Иммунная проверка (CRISPR)
        if self.immune.check_and_block(text):
            return {"status": "blocked", "reason": "CRISPR guard activated"}

        # 2. Эпигенетическая адаптация
        self.epigenetic.record_stress(stress_level, "input_processing")
        adapted = self.epigenetic.adapt_behavior({"temperature": 0.7})

        # 3. Фрактальное хранение
        memory_id = self.fractal.store_memory(text, importance=0.8 if stress_level > 0.5 else 0.5)

        return {
            "status": "processed",
            "memory_id": memory_id,
            "adapted_params": adapted,
            "fractal_stats": self.fractal.get_stats()
        }

    def get_full_report(self):
        return {
            "fractal": self.fractal.get_stats(),
            "epigenetic": self.epigenetic.get_status(),
            "immune": self.immune.get_immunity_report()
        }


if __name__ == "__main__":
    hybrid = HybridBiologicalMemory()
    result = hybrid.process_input("The capital of France is Paris.", stress_level=0.2)
    print(result)
    print(hybrid.get_full_report())