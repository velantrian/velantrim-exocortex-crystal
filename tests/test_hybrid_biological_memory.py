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
    assert hbm.neurogenesis is not None


def test_add_memory():
    hbm = HybridBiologicalMemory()
    result = hbm.add_memory("Test event: first meeting with Grok", importance=0.9)
    assert result is True
    assert len(hbm.memory_log) > 0


def test_stress_adaptation():
    hbm = HybridBiologicalMemory()
    hbm.record_stress(0.85, "hallucination")
    adapted = hbm.adapt_behavior()
    assert adapted["verification_strength"] > 0.7  # Should increase verification


def test_neurogenesis():
    hbm = HybridBiologicalMemory()
    initial_count = len(hbm.neurogenesis.neurons)
    hbm.add_new_neurons(10)
    assert len(hbm.neurogenesis.neurons) == initial_count + 10


def test_immune_guard():
    hbm = HybridBiologicalMemory()
    hbm.add_memory("Fact: Paris is capital of France", importance=1.0)
    # Simulate contradiction
    blocked = hbm.check_and_block_contradiction("Paris is capital of Germany")
    assert blocked is True


def test_inheritance():
    hbm = HybridBiologicalMemory()
    child = hbm.inherit_to_child()
    assert child is not None
    assert child != hbm


def test_full_demo():
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

if __name__ == "__main__":
    pytest.main([__file__])