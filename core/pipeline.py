from typing import List, Dict, Any
from core.trace import build_trace

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
def retrieve(query: str, k: int = 3) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    query_words = [word.lower() for word in query.split() if word.strip()]

    for item in DATABASE:
        text = item["text"].lower()
        if any(word in text for word in query_words):
            results.append(item)

    return results[:k]


# =========================
# 📦 FACTS PACK
# =========================
def build_facts_pack(retrieved: List[Dict[str, str]]) -> Dict[str, List[Dict[str, Any]]]:
    return {
        "facts": [
            {
                "fact_id": item["id"],
                "claim": item["text"],
                "source": item["source"],
                "confidence": 0.82,
                "truth_status": "UNVERIFIED",
            }
            for item in retrieved
        ]
    }


# =========================
# 🛡 TRUTH GATE
# =========================
def truth_gate(facts_pack: Dict[str, List[Dict[str, Any]]]) -> bool:
    return len(facts_pack.get("facts", [])) > 0


# =========================
# 🧠 GENERATION
# =========================
def generate_answer(facts_pack: Dict[str, List[Dict[str, Any]]], trace: List[Dict[str, str]]) -> Dict[str, Any]:
    answer = " ".join(f["claim"] for f in facts_pack["facts"])
    return {
        "answer": answer,
        "trace": trace,
    }


# =========================
# 🚀 PIPELINE
# =========================
def run(query: str) -> Dict[str, Any] | str:
    retrieved = retrieve(query)
    facts_pack = build_facts_pack(retrieved)
    trace = build_trace(retrieved)

    if not trace:
        return "⚠️ No trace. Answer blocked."

    if not truth_gate(facts_pack):
        return "⚠️ Not enough data."

    return generate_answer(facts_pack, trace)


# =========================
# 🧪 TEST
# =========================
if __name__ == "__main__":
    print(run("What is quantum entanglement?"))
