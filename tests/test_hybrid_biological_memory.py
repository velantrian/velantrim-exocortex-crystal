# tests/test_hybrid_biological_memory.py
# Unit tests for HybridBiologicalMemory (RFC0070–0073)
#
# HybridBiologicalMemory is now a thin facade that delegates to the canonical
# standalone layer modules (tested in detail in test_bio_modules.py); these
# tests pin the facade's wiring and its public API surface (used by DEMO.md).

import pytest
from prototypes.hybrid_biological_memory import HybridBiologicalMemory
from epigenetic_adaptation_module import EpigeneticAdaptationModule
from prototypes.neurogenesis_dynamic_growth import NeurogenesisDynamicGrowth


def test_initialization_wires_canonical_modules():
    hbm = HybridBiologicalMemory()
    assert hbm.fractal_layer is not None
    assert isinstance(hbm.epigenetic_module, EpigeneticAdaptationModule)
    assert isinstance(hbm.neurogenesis_module, NeurogenesisDynamicGrowth)
    assert hbm.immune_guard is not None


def test_add_memory_returns_id_and_logs():
    hbm = HybridBiologicalMemory()
    mem_id = hbm.add_memory("Test event: first meeting with Grok", importance=0.9)
    assert isinstance(mem_id, str) and mem_id
    assert len(hbm.memory_log) == 1
    assert hbm.memory_log[0]["text"] == "Test event: first meeting with Grok"
    # High-importance memory propagates into the fractal layer's anchors.
    assert hbm.fractal_layer.get_stats()["total_anchors"] == 1


def test_adapt_behavior_with_no_params_returns_seeded_defaults():
    # Regression: adapt_behavior() with default params=None must not crash and
    # must surface the seeded generation parameters.
    hbm = HybridBiologicalMemory()
    adapted = hbm.adapt_behavior()
    assert adapted["verification_strength"] == pytest.approx(0.5)
    assert {"verification_strength", "temperature", "exploration_rate"} <= set(adapted)


def test_stress_raises_verification_strength():
    baseline = HybridBiologicalMemory().adapt_behavior()["verification_strength"]
    hbm = HybridBiologicalMemory()
    hbm.record_stress(0.85, "hallucination")
    stressed = hbm.adapt_behavior()["verification_strength"]
    assert stressed > baseline


def test_adapt_behavior_caller_params_flow_through():
    hbm = HybridBiologicalMemory()
    adapted = hbm.adapt_behavior({"verification_strength": 0.95, "custom": 42})
    assert adapted["verification_strength"] == pytest.approx(0.95)  # max(0.95, tag)
    assert adapted["custom"] == 42                                  # untouched key


def test_add_new_neurons_grows_count():
    hbm = HybridBiologicalMemory()
    before = hbm.neurogenesis_module.current_neurons
    returned = hbm.add_new_neurons(10)
    assert isinstance(returned, str)
    assert hbm.neurogenesis_module.current_neurons == before + 10


def test_immune_guard_blocks_seeded_and_recorded_threats():
    hbm = HybridBiologicalMemory()
    # Seeded default contradiction is blocked (True == blocked).
    assert hbm.check_and_block_contradiction("The capital of France is Berlin") is True
    # A benign statement passes.
    assert hbm.check_and_block_contradiction("The sky is blue today") is False
    # Newly recorded threats are then blocked too.
    hbm.record_threat("hallucination", "unicorns built the pyramids")
    assert hbm.check_and_block_contradiction("clearly UNICORNS BUILT THE PYRAMIDS") is True


def test_inheritance_passes_epigenetic_state_to_child():
    hbm = HybridBiologicalMemory()
    hbm.record_stress(0.85, "high_load")
    child = hbm.inherit_to_child()
    assert child is not hbm
    assert child.epigenetic_module.epigenetic_tags == hbm.epigenetic_module.epigenetic_tags
    # Child inherits the parent's blocked-contradiction immunity.
    assert child.check_and_block_contradiction("The capital of France is Berlin") is True


def test_full_status_has_all_layers():
    hbm = HybridBiologicalMemory()
    hbm.add_memory("Important meeting", importance=0.95)
    hbm.record_stress(0.7, "high_load")
    hbm.adapt_behavior()
    hbm.add_new_neurons(5)
    stats = hbm.get_full_stats()
    assert {"fractal", "epigenetic", "immune", "neurogenesis"} <= set(stats)
    assert "tags" in stats["epigenetic"]
    assert stats["total_memories"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
