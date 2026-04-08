# core/pipeline.py

from typing import List, Dict


# =========================
# 📦 MOCK DATABASE
# =========================
DATABASE = [
    {"id": "f1", "text": "Water boils at 100°C", "source": "physics"},
    {"id": "f2", "text": "Quantum entanglement links particles instantly", "source": "physics"},
    {"id": "f3", "text": "Earth revolves around the Sun", "source": "astronomy"},
]


# =========================
# 🔍 RETRIEVAL
# =========================
def retrieve(query: str, k: int = 3) -> List[Dict]:
    results = []
    for item in DATABASE:
        if any(word.lower() in item["text"].lower() for word in query.split()):
            results.append(item)
    return results[:k]


# =========================
# 📦 FACTS PACK
# =========================
def build_facts_pack(retrieved: List[Dict]) -> Dict:
    return {
        "facts": [
            {
                "fact_id": item["id"],
                "claim": item["text"],
                "source": item["source"]
            }
            for item in retrieved
        ]
    }


# =========================
# 🛡 TRUTH GATE
# =========================
def truth_gate(facts_pack: Dict) -> bool:
    return len(facts_pack["facts"]) > 0


# =========================
# 🧠 GENERATION
# =========================
def generate_answer(facts_pack: Dict) -> str:
    return " ".join(f["claim"] for f in facts_pack["facts"])


# =========================
# 🚀 PIPELINE
# =========================
def run(query: str) -> str:
    retrieved = retrieve(query)
    facts_pack = build_facts_pack(retrieved)

    if not truth_gate(facts_pack):
        return "⚠️ Not enough data."

    return generate_answer(facts_pack)


# =========================
# 🧪 TEST
# =========================
if __name__ == "__main__":
    print(run("What is quantum entanglement?"))
