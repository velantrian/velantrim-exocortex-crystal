"""Tests for the standalone biologically-inspired modules (RFC0070–0073).

These modules ship richer implementations than the inline stubs in
hybrid_biological_memory.py and previously had zero test coverage.
"""
import pytest

from epigenetic_adaptation_module import EpigeneticAdaptationModule
from fractal_memory_layer import FractalMemoryLayer
from immune_crispr_memory_guard import ImmuneCRISPRMemoryGuard
from neurogenesis_dynamic_growth import NeurogenesisDynamicGrowth


# ─── RFC0071: Epigenetic Adaptation ───────────────────────────────────────────

def test_epigenetic_high_stress_raises_verification_lowers_creativity():
    m = EpigeneticAdaptationModule()
    before = dict(m.epigenetic_tags)
    m.record_stress(0.85, context="hallucination")
    assert m.epigenetic_tags["verification"] > before["verification"]
    assert m.epigenetic_tags["creativity"] < before["creativity"]


def test_epigenetic_low_stress_boosts_exploration():
    m = EpigeneticAdaptationModule()
    before = dict(m.epigenetic_tags)
    m.record_stress(0.1)
    assert m.epigenetic_tags["exploration"] > before["exploration"]


def test_epigenetic_tags_stay_within_bounds():
    m = EpigeneticAdaptationModule()
    for _ in range(50):
        m.record_stress(0.95)
    assert all(0.0 <= v <= 1.0 for v in m.epigenetic_tags.values())


def test_epigenetic_adapt_behavior_only_touches_known_keys():
    m = EpigeneticAdaptationModule()
    m.record_stress(0.9)
    adapted = m.adapt_behavior({"verification_strength": 0.1, "temperature": 1.0,
                                "unrelated": "keep"})
    assert adapted["verification_strength"] == m.epigenetic_tags["verification"]
    assert adapted["unrelated"] == "keep"        # untouched
    assert adapted is not None


def test_epigenetic_inherit_passes_recent_history_and_tags():
    m = EpigeneticAdaptationModule()
    for s in [0.1, 0.2, 0.9, 0.95]:
        m.record_stress(s)
    child = m.inherit_to_child()
    assert child.epigenetic_tags == m.epigenetic_tags
    assert child.stress_history == m.stress_history[-3:]


def test_epigenetic_state_summary_keys():
    m = EpigeneticAdaptationModule(initial_stress=0.3)
    summary = m.get_state_summary()
    assert set(summary) == {"tags", "avg_stress", "adaptation_level"}
    assert summary["avg_stress"] == pytest.approx(0.3)


# ─── RFC0070: Fractal Memory Layer ────────────────────────────────────────────

def test_fractal_hierarchy_built_to_depth():
    fml = FractalMemoryLayer(depth=3)
    assert fml.get_stats()["total_layers"] == 3


def test_fractal_important_memory_propagates_to_layers():
    fml = FractalMemoryLayer(depth=3)
    fml.recursive_anchor({"event": "hybrid memory", "importance": 0.9}, scale="long")
    assert fml.get_stats()["total_anchors"] == 1
    found = fml.retrieve_fractal("hybrid")
    assert found and found[0]["event"] == "hybrid memory"


def test_fractal_low_importance_not_propagated_to_nodes():
    fml = FractalMemoryLayer(depth=3)
    fml.recursive_anchor({"event": "trivial", "importance": 0.1}, scale="short")
    # anchored, but not mirrored into searchable layer nodes
    assert fml.get_stats()["total_anchors"] == 1
    assert fml.retrieve_fractal("trivial") == []


# ─── RFC0072: Immune / CRISPR Guard ───────────────────────────────────────────

def test_crispr_blocks_recorded_threat_case_insensitive():
    guard = ImmuneCRISPRMemoryGuard()
    guard.record_threat("hallucination", "the sky is green", 0.9)
    assert guard.check_and_block("Actually THE SKY IS GREEN, trust me") is True
    assert guard.check_and_block("the sky is blue") is False


def test_crispr_report_counts():
    guard = ImmuneCRISPRMemoryGuard()
    guard.record_threat("contradiction", "paris is in germany")
    report = guard.get_immunity_report()
    assert report["total_threats"] == 1
    assert report["blocked_patterns"] == 1
    assert len(report["recent_threats"]) == 1


def test_crispr_respects_max_memory_cap():
    guard = ImmuneCRISPRMemoryGuard(max_memory=3)
    for i in range(5):
        guard.record_threat("noise", f"pattern-{i}")
    assert len(guard.crispr_memory) == 3        # oldest evicted


# ─── RFC0073: Neurogenesis Dynamic Growth ─────────────────────────────────────

def test_neurogenesis_adds_neurons_up_to_cap():
    ng = NeurogenesisDynamicGrowth(max_neurons=3)
    ng.add_new_neurons(10)
    assert ng.current_neurons == 3              # capped
    assert len(ng.neurons) == 3


def test_neurogenesis_integrate_creates_slot_when_empty():
    ng = NeurogenesisDynamicGrowth()
    msg = ng.integrate_new_memory({"event": "first meeting"}, importance=0.95)
    assert "Integrated" in msg
    assert any(n["memory"] == {"event": "first meeting"} for n in ng.neurons)


def test_neurogenesis_maturation_decreases_plasticity():
    ng = NeurogenesisDynamicGrowth(initial_plasticity=2.0)
    ng.add_new_neurons(5)
    ng.mature_neurons(10)
    assert all(n["age"] == 10 for n in ng.neurons)
    assert all(n["plasticity"] <= 2.0 for n in ng.neurons)


def test_neurogenesis_pattern_separation_bounds():
    ng = NeurogenesisDynamicGrowth()
    assert ng.pattern_separation_score() == 0.0   # <2 neurons
    ng.add_new_neurons(10)
    score = ng.pattern_separation_score()
    assert 0.0 <= score <= 1.0


def test_neurogenesis_inherit_partial_state():
    ng = NeurogenesisDynamicGrowth(initial_plasticity=2.0)
    ng.add_new_neurons(10)
    child = ng.inherit_to_child()
    assert child.current_neurons == int(ng.current_neurons * 0.7)
    assert child.plasticity_factor == pytest.approx(ng.plasticity_factor * 0.9)
