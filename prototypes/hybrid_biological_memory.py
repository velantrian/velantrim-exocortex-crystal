# prototypes/hybrid_biological_memory.py
# HybridBiologicalMemory v2.1 — biologically inspired memory
# RFC0070–0073 | Velantrim ExoCortex Crystal
#
# This is a facade over four layers. The implementations live in separate
# modules (single source of truth) rather than being duplicated here:
#   - FractalMemoryLayer          → prototypes/fractal_memory_layer.py       (RFC0070)
#   - EpigeneticAdaptationModule  → epigenetic_adaptation_module.py (wired into core, RFC0071)
#   - ImmuneCRISPRMemoryGuard     → prototypes/immune_crispr_memory_guard.py (RFC0072)
#   - NeurogenesisDynamicGrowth   → prototypes/neurogenesis_dynamic_growth.py (RFC0073)
#
# ⚠️ Prototype: NOT wired into the core pipeline (unlike epigenetic). See FUTURE.md §3.3.

import time
import uuid
from typing import Dict, List, Any, Optional

from prototypes.fractal_memory_layer import FractalMemoryLayer
from epigenetic_adaptation_module import EpigeneticAdaptationModule
from prototypes.immune_crispr_memory_guard import ImmuneCRISPRMemoryGuard
from prototypes.neurogenesis_dynamic_growth import NeurogenesisDynamicGrowth

# Known contradictions used to seed the immune guard — so that basic
# hallucinations are blocked out of the box (replaces the old hardcoded stubs).
# Mixed-language on purpose: the guard must also block contradictions in Russian.
_DEFAULT_CONTRADICTIONS = [
    "capital of france is berlin",
    "capital of germany is paris",
    "париж столица германии",
    "германия столица франции",
]

# Baseline generation parameters that the epigenetic layer adapts in place.
_DEFAULT_PARAMS = {
    "verification_strength": 0.5,
    "temperature": 1.0,
    "exploration_rate": 0.5,
}


class HybridBiologicalMemory:
    """Facade over the four biological layers (RFC0070–0073).

    Delegates the work to the canonical modules instead of redefining classes
    inside this file. The public API is kept for DEMO.md and integrations.
    """

    def __init__(self, name: str = "Velantrim-Hybrid"):
        self.name = name
        self.fractal_layer = FractalMemoryLayer()
        self.epigenetic_module = EpigeneticAdaptationModule()
        self.immune_guard = ImmuneCRISPRMemoryGuard()
        self.neurogenesis_module = NeurogenesisDynamicGrowth()
        self.memory_log: List[Dict[str, Any]] = []

        # Seed the known contradictions directly.
        for pattern in _DEFAULT_CONTRADICTIONS:
            self.immune_guard.blocked_patterns.add(pattern)

    def add_memory(self, text: str, importance: float = 0.5) -> str:
        """Store a memory in the fractal and neurogenesis layers. Returns the id."""
        mem_id = str(uuid.uuid4())
        item = {
            "id": mem_id,
            "text": text,
            "importance": importance,
            "timestamp": time.time(),
        }
        # The anchoring scale depends on importance (short / medium / long).
        scale = "long" if importance > 0.7 else "medium" if importance > 0.4 else "short"
        self.fractal_layer.recursive_anchor(item, scale=scale)
        self.neurogenesis_module.integrate_new_memory(item, importance)
        self.memory_log.append(item)
        return mem_id

    def adapt_behavior(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Adapt generation parameters via the epigenetic layer.

        We seed reasonable defaults that the caller may override with their own
        values; the epigenetic layer then adjusts them in place.
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
        """True == the input was blocked by the immune guard (known pattern)."""
        return self.immune_guard.check_and_block(text)

    def record_threat(self, threat_type: str, pattern: str, severity: float = 1.0) -> None:
        """Register a new threat/contradiction to be blocked."""
        self.immune_guard.record_threat(threat_type, pattern, severity)

    def inherit_to_child(self) -> "HybridBiologicalMemory":
        """Create a child memory with inherited epigenetic/neuro state."""
        child = HybridBiologicalMemory(f"{self.name}-child")
        child.epigenetic_module = self.epigenetic_module.inherit_to_child()
        child.neurogenesis_module = self.neurogenesis_module.inherit_to_child()
        child.immune_guard.blocked_patterns |= self.immune_guard.blocked_patterns
        return child

    def get_full_stats(self) -> Dict[str, Any]:
        """Combined status of all four layers (used by DEMO.md and the tests)."""
        return {
            "name": self.name,
            "fractal": self.fractal_layer.get_stats(),
            "epigenetic": self.epigenetic_module.get_state_summary(),
            "immune": self.immune_guard.get_immunity_report(),
            "neurogenesis": self.neurogenesis_module.get_stats(),
            "total_memories": len(self.memory_log),
        }


# Demo — mirrors the example in DEMO.md so that `python -m prototypes.hybrid_biological_memory`
# actually shows something. A prototype, not wired into the core pipeline (see FUTURE.md §3.3).
if __name__ == "__main__":  # pragma: no cover
    hbm = HybridBiologicalMemory()

    # 1. Memory (fractal + neurogenesis layers)
    hbm.add_memory(
        "Important event: first deep conversation about biological memory",
        importance=0.95,
    )

    # 2. Stress → epigenetic adaptation
    hbm.record_stress(0.82, "hallucination_detected")
    adapted = hbm.adapt_behavior()
    print("Adapted verification strength:", adapted["verification_strength"])

    # 3. Immune guard (CRISPR): block a known contradiction
    blocked = hbm.check_and_block_contradiction("The capital of France is Berlin")
    print("Contradiction blocked:", blocked)

    # 4. Neurogenesis: new plastic "neurons"
    print(hbm.add_new_neurons(15))

    # 5. Full per-layer summary
    print("Full stats:", hbm.get_full_stats())

    # 6. Child memory inheritance (like seeds in plants)
    child = hbm.inherit_to_child()
    print("Child system created:", child.name)
