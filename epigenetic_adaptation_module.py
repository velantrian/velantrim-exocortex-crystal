# Epigenetic Adaptation Module (RFC0071 v0.1)
# Engineering metaphor for adaptive threshold behaviour — not a biological
# cognition or plant-memory claim. See docs/METAPHOR_VS_MECHANISM.md.

class EpigeneticAdaptationModule:
    """
    Core module for RFC0071: Epigenetic Adaptation.
    
    Mimics how plants pass stress memory to offspring via epigenetic tags
    and bacteria adapt immune response.
    
    Key features:
    - Dynamic "epigenetic tags" that activate/deactivate pathways
    - Stress recording and adaptation
    - Inheritance to child processes/sessions
    - No full retraining required
    """

    def __init__(self, initial_stress: float = 0.0):
        self.epigenetic_tags = {
            "verification": 0.5,      # Higher = more fact-checking
            "creativity": 0.5,        # Higher = more exploratory generation
            "conservatism": 0.5,      # Higher = prefer known patterns
            "exploration": 0.5        # Higher = try new connections
        }
        self.stress_history = [initial_stress]
        self.adaptation_threshold = 0.6

    def record_stress(self, stress_level: float, context: str = "general"):
        """
        Record a stress event (e.g. hallucination, error, high load).
        Updates epigenetic tags accordingly.
        """
        self.stress_history.append(stress_level)
        
        if stress_level > self.adaptation_threshold:
            # High stress → increase verification, decrease creativity
            self.epigenetic_tags["verification"] = min(1.0, self.epigenetic_tags["verification"] + 0.15)
            self.epigenetic_tags["creativity"] = max(0.1, self.epigenetic_tags["creativity"] - 0.12)
            self.epigenetic_tags["conservatism"] = min(1.0, self.epigenetic_tags["conservatism"] + 0.1)
        else:
            # Low stress → slight increase in exploration
            self.epigenetic_tags["exploration"] = min(1.0, self.epigenetic_tags["exploration"] + 0.08)
            self.epigenetic_tags["creativity"] = min(1.0, self.epigenetic_tags["creativity"] + 0.05)

    def adapt_behavior(self, current_params: dict) -> dict:
        """
        Apply epigenetic modifications to current system parameters.
        Returns adapted parameters (no retraining needed).
        """
        adapted = current_params.copy()
        
        # Verification boost
        if "verification_strength" in adapted:
            adapted["verification_strength"] = max(
                adapted["verification_strength"],
                self.epigenetic_tags["verification"]
            )
        
        # Creativity adjustment
        if "temperature" in adapted:
            adapted["temperature"] = adapted["temperature"] * (0.7 + 0.3 * self.epigenetic_tags["creativity"])
        
        # Exploration rate
        if "exploration_rate" in adapted:
            adapted["exploration_rate"] = self.epigenetic_tags["exploration"]
        
        return adapted

    def inherit_to_child(self):
        """
        Create a child module with inherited epigenetic state.
        Like plants passing memory through seeds.
        """
        child = EpigeneticAdaptationModule()
        child.epigenetic_tags = self.epigenetic_tags.copy()
        child.stress_history = self.stress_history[-3:]  # Pass recent history
        return child

    def get_state_summary(self) -> dict:
        """Return current epigenetic state for logging/debugging."""
        return {
            "tags": self.epigenetic_tags,
            "avg_stress": sum(self.stress_history) / len(self.stress_history) if self.stress_history else 0.0,
            "adaptation_level": sum(self.epigenetic_tags.values()) / len(self.epigenetic_tags)
        }


# Example usage
if __name__ == "__main__":
    print("=== RFC0071 Epigenetic Adaptation Module Demo ===")
    
    module = EpigeneticAdaptationModule(initial_stress=0.3)
    
    # Simulate high stress (hallucination detected)
    module.record_stress(0.85, context="hallucination")
    print("After high stress:", module.get_state_summary())
    
    # Adapt parameters
    params = {"verification_strength": 0.6, "temperature": 0.8, "exploration_rate": 0.4}
    adapted = module.adapt_behavior(params)
    print("Adapted params:", adapted)
    
    # Inherit to child
    child = module.inherit_to_child()
    print("Child inherited tags:", child.epigenetic_tags)
    
    print("\nModule ready for integration with Fractal Layer and core graph.")