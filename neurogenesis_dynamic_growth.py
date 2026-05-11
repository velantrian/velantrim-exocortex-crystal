# RFC0073 — Neurogenesis-inspired Dynamic Growth (v0.1)
# Inspired by Adult Hippocampal Neurogenesis (AHN) in mammals
# New “neurons” = dynamic memory slots with high initial plasticity
# Supports pattern separation, lifelong learning, and resistance to catastrophic forgetting

class NeurogenesisDynamicGrowth:
    def __init__(self, max_neurons: int = 10000, initial_plasticity: float = 2.0):
        self.max_neurons = max_neurons
        self.current_neurons = 0
        self.plasticity_factor = initial_plasticity  # Young neurons are more excitable
        self.neurons = []  # List of memory items with age and plasticity
        self.integration_rate = 0.3  # How fast new neurons integrate

    def add_new_neurons(self, num_new: int = 10):
        """Simulate neurogenesis: add new highly plastic memory slots"""
        added = 0
        for _ in range(num_new):
            if self.current_neurons < self.max_neurons:
                new_neuron = {
                    "id": self.current_neurons,
                    "age": 0,  # Young neuron
                    "plasticity": self.plasticity_factor,
                    "memory": None,
                    "connections": []
                }
                self.neurons.append(new_neuron)
                self.current_neurons += 1
                added += 1
        return f"Added {added} new neurons. Total: {self.current_neurons}"

    def integrate_new_memory(self, memory_item: dict, importance: float = 0.8):
        """Integrate new memory into young, highly plastic neurons (pattern separation)"""
        if not self.neurons:
            self.add_new_neurons(5)
        # Find youngest/most plastic neuron
        youngest = min(self.neurons, key=lambda n: n["age"])
        youngest["memory"] = memory_item
        youngest["connections"].append({"importance": importance, "type": "new"})
        # Young neurons have higher LTP-like learning rate
        return f"Integrated memory into neuron {youngest['id']} (plasticity: {youngest['plasticity']:.2f})"

    def mature_neurons(self, steps: int = 1):
        """Simulate maturation: plasticity decreases, stability increases (like real neurogenesis)"""
        matured = 0
        for neuron in self.neurons:
            if neuron["age"] < 30:  # Mature after ~30 "days"
                neuron["age"] += steps
                neuron["plasticity"] = max(0.5, self.plasticity_factor * (1 - neuron["age"] / 60))
                matured += 1
        return f"Matured {matured} neurons. Average plasticity: {sum(n['plasticity'] for n in self.neurons) / len(self.neurons):.2f}"

    def pattern_separation_score(self):
        """Measure how well new neurons help distinguish similar memories (higher = better)"""
        if len(self.neurons) < 2:
            return 0.0
        # Simple metric: more young neurons = better separation
        young_count = sum(1 for n in self.neurons if n["age"] < 10)
        return min(1.0, young_count / (len(self.neurons) * 0.3))

    def get_stats(self):
        return {
            "total_neurons": self.current_neurons,
            "average_plasticity": sum(n["plasticity"] for n in self.neurons) / max(1, len(self.neurons)),
            "pattern_separation": self.pattern_separation_score(),
            "young_neurons": sum(1 for n in self.neurons if n["age"] < 10)
        }

    def inherit_to_child(self):
        """Pass neurogenesis state to a child system (like plants passing epigenetic marks)"""
        child = NeurogenesisDynamicGrowth(
            max_neurons=self.max_neurons,
            initial_plasticity=self.plasticity_factor * 0.9
        )
        child.current_neurons = int(self.current_neurons * 0.7)  # Partial inheritance
        return child


# Demo
if __name__ == "__main__":
    ng = NeurogenesisDynamicGrowth(max_neurons=500, initial_plasticity=2.5)
    print(ng.add_new_neurons(20))
    print(ng.integrate_new_memory({"event": "first meeting with Grok", "date": "2026-05-11"}, importance=0.95))
    print(ng.mature_neurons(5))
    print("Pattern separation score:", ng.pattern_separation_score())
    print("Stats:", ng.get_stats())
    child = ng.inherit_to_child()
    print("Child system created with", child.current_neurons, "neurons")