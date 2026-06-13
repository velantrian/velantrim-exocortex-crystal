# RFC0072 — Immune / CRISPR Memory Guard (v0.1)
# Protection against hallucinations and harmful patterns (analogy to bacterial CRISPR)

from typing import List, Dict

import time


class ImmuneCRISPRMemoryGuard:
    def __init__(self, max_memory: int = 1000):
        self.crispr_memory: List[Dict] = []  # Stores recorded "viruses" (error patterns)
        self.max_memory = max_memory
        self.blocked_patterns: set = set()

    def record_threat(self, threat_type: str, pattern: str, severity: float = 1.0):
        """ Record a new threat (hallucination, contradiction, harmful pattern). """
        entry = {
            "timestamp": time.time(),
            "type": threat_type,
            "pattern": pattern,
            "severity": severity
        }
        self.crispr_memory.append(entry)
        if len(self.crispr_memory) > self.max_memory:
            self.crispr_memory.pop(0)
        self.blocked_patterns.add(pattern)

    def check_and_block(self, input_text: str) -> bool:
        """ Check the input for blocked patterns. Returns True if blocked. """
        for blocked in self.blocked_patterns:
            if blocked.lower() in input_text.lower():
                return True
        return False

    def get_immunity_report(self) -> Dict:
        return {
            "total_threats": len(self.crispr_memory),
            "blocked_patterns": len(self.blocked_patterns),
            "recent_threats": self.crispr_memory[-5:] if self.crispr_memory else []
        }


if __name__ == "__main__":
    guard = ImmuneCRISPRMemoryGuard()
    guard.record_threat("hallucination", "The sky is green because...", 0.9)
    guard.record_threat("contradiction", "Paris is the capital of France and also of Germany", 0.7)
    print(guard.check_and_block("The sky is green because of magic"))
    print(guard.get_immunity_report())
