# 🌀 Hybrid Biological Memory — Quick Demo

**Inspired by:** Human + Dolphins + Birds + Octopus + Insects + Plants + Trees + Bacteria + Fractals

## Quick Start

```bash
python -m prototypes.hybrid_biological_memory
```

## Example Usage

```python
from prototypes.hybrid_biological_memory import HybridBiologicalMemory

# Initialize the full hybrid system
hbm = HybridBiologicalMemory()

# 1. Add a new memory (Fractal + Neurogenesis layers)
hbm.add_memory(
    "Important event: First deep conversation about biological memory with Grok",
    importance=0.95
)

# 2. Record stress and adapt (Epigenetic layer)
hbm.record_stress(0.82, "hallucination_detected")
adapted_params = hbm.adapt_behavior()
print("Adapted verification strength:", adapted_params["verification_strength"])

# 3. Check for contradictions (Immune / CRISPR layer)
blocked = hbm.check_and_block_contradiction(
    "The capital of France is Berlin"  # Contradiction
)
print("Contradiction blocked:", blocked)

# 4. Create new neurons (Neurogenesis)
hbm.add_new_neurons(15)

# 5. Get full system stats
stats = hbm.get_full_stats()
print(stats)

# 6. Inherit to child instance (like plants passing memory to seeds)
child = hbm.inherit_to_child()
print("Child system created successfully")
```

## What Happens Under the Hood

- **Fractal Layer**: Memory is stored at multiple time scales (short / medium / long)
- **Epigenetic Layer**: System automatically increases verification and reduces creativity under stress
- **Immune Guard**: Immediately blocks contradictory or hallucinatory facts
- **Neurogenesis**: New high-plasticity neurons are added for better pattern separation

## Expected Output (example)

```
🌿🧠 HybridBiologicalMemory 'Velantrim-Hybrid' инициализирована (4 биологических слоя)
Adapted verification strength: 0.65
🔒 Blocked by CRISPR guard: capital of france is berlin
Contradiction blocked: True
Added 15 new neurons. Total: 20
Full stats: {'name': ..., 'fractal': {...}, 'epigenetic': {...}, 'immune': {...}, 'neurogenesis': {...}}
Child system created: Velantrim-Hybrid-child
```

## Integration with Velantrim / Eiti

This module is designed to be plugged directly into:
- `velantrim-exocortex-crystal`
- `Eiti-Wizard`
- `velantrim-core`

**Status**: Production-ready prototype ✅

---

*Created as part of the Hybrid Biological Memory Vision (May 2026)*