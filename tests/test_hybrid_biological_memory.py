# tests/test_hybrid_biological_memory.py
# Unit tests for HybridBiologicalMemory (RFC0070–0073)

import pytest
from hybrid_biological_memory import HybridBiologicalMemory


def test_initialization():
    hbm = HybridBiologicalMemory()
    assert hbm is not None
    assert hbm.fractal_layer is not None
    assert hbm.epigenetic_module is not None
    assert hbm.immune_guard is not None
    assert hbm.neurogenesis_module is not None


def test_add_memory_returns_id_and_logs():
    hbm = HybridBiologicalMemory()
    mem_id = hbm.add_memory("Test event: first meeting with Grok", importance=0.9)
    # add_memory returns the fractal-layer memory id (a uuid string), not a bool
    assert isinstance(mem_id, str) and mem_id
    assert len(hbm.memory_log) == 1
    assert hbm.memory_log[0]["text"] == "Test event: first meeting with Grok"


def test_adapt_behavior_with_no_params_returns_defaults():
    # Regression: adapt_behavior() with the default params=None must not crash.
    hbm = HybridBiologicalMemory()
    adapted = hbm.adapt_behavior()
    assert adapted["verification_strength"] == pytest.approx(0.6)
    assert set(adapted) >= {"temperature", "verification_strength", "creativity", "exploration"}


def test_stress_adaptation_increases_verification():
    hbm = HybridBiologicalMemory()
    hbm.record_stress(0.85, "hallucination")
    adapted = hbm.adapt_behavior()
    assert adapted["verification_strength"] > 0.7  # verification mode kicks in


def test_adapt_behavior_caller_params_override_defaults():
    hbm = HybridBiologicalMemory()
    adapted = hbm.adapt_behavior({"temperature": 0.1, "custom": 42})
    assert adapted["temperature"] == 0.1
    assert adapted["custom"] == 42


def test_neurogenesis_grows_neuron_count():
    hbm = HybridBiologicalMemory()
    initial = hbm.neurogenesis_module.active_neurons
    returned = hbm.add_new_neurons(10)
    assert hbm.neurogenesis_module.active_neurons == initial + 10
    assert returned == initial + 10


def test_immune_guard_blocks_known_contradiction():
    hbm = HybridBiologicalMemory()
    # A normal fact passes the guard (True == allowed).
    assert hbm.check_and_block_contradiction("Париж столица Франции") is True
    # A known contradiction is blocked (False == rejected).
    assert hbm.check_and_block_contradiction("Париж столица Германии") is False
    assert hbm.immune_guard.blocked_count == 1


def test_inheritance_passes_stress_to_child():
    hbm = HybridBiologicalMemory()
    hbm.record_stress(0.85, "high_load")
    child = hbm.inherit_to_child()
    assert child is not None
    assert child is not hbm
    assert child.epigenetic_module.stress_level == hbm.epigenetic_module.stress_level


def test_full_status_has_all_layers():
    hbm = HybridBiologicalMemory()
    hbm.add_memory("Important meeting", importance=0.95)
    hbm.record_stress(0.7, "high_load")
    hbm.adapt_behavior()
    hbm.add_new_neurons(5)
    stats = hbm.get_full_stats()
    assert "fractal" in stats
    assert "epigenetic" in stats
    assert "immune" in stats
    assert "neurogenesis" in stats
    assert stats["total_memories"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
