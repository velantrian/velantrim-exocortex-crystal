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
# 🔧 HELPERS
# =========================
def tokenize(text: str) -> List[str]:
    return [word.lower().strip(".,!?;:()[]{}\"'") for word in text.split() if word.strip()]


def normalize_score(score: float, max_score: float) -> float:
    if max_score <= 0:
        return 0.0
    value = score / max_score
    return max(0.0, min(1.0, value))


# =========================
# 🔍 RETRIEVAL
# =========================
def retrieve(query: str, k: int = 3) -> List[Dict[str, str]]:
    query_words = tokenize(query)
    scored: List[Dict[str, Any]] = []

    for item in DATABASE:
        text_words = tokenize(item["text"])
        overlap = len(set(query_words) & set(text_words))

        if overlap > 0:
            scored.append({
                **item,
                "_score": overlap
            })

    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:k]


# =========================
# 📦 FACTS PACK
# =========================
def build_facts_pack(retrieved: List[Dict[str, Any]], query: str) -> Dict[str, List[Dict[str, Any]]]:
    query_words = set(tokenize(query))
    facts: List[Dict[str, Any]] = []

    for item in retrieved:
        text_words = set(tokenize(item["text"]))
        overlap = len(query_words & text_words)
        confidence = normalize_score(overlap, max(1, len(query_words)))

        facts.append({
            "fact_id": item["id"],
            "claim": item["text"],
            "source": item["source"],
            "confidence": round(max(0.5, confidence), 2),
            "truth_status": "UNVERIFIED",
        })

    return {"facts": facts}


# =========================
# 🛡 GUARDIAN
# =========================
def guardian(facts_pack: Dict[str, List[Dict[str, Any]]], trace: List[Dict[str, Any]]) -> bool:
    facts = facts_pack.get("facts", [])

    if not facts:
        return False

    if not trace:
        return False

    if len(trace) != len(facts):
        return False

    for fact in facts:
        if not fact.get("fact_id"):
            return False
        if not fact.get("claim"):
            return False
        if not fact.get("source"):
            return False
        if fact.get("confidence", 0) <= 0:
            return False

    return True


# =========================
# 🛡 TRUTH GATE
# =========================
def truth_gate(facts_pack: Dict[str, List[Dict[str, Any]]]) -> bool:
    facts = facts_pack.get("facts", [])
    if not facts:
        return False

    for fact in facts:
        if not fact.get("source"):
            return False
        if fact.get("confidence", 0) <= 0:
            return False

    return True


# =========================
# 🧠 GENERATION
# =========================
def generate_answer(facts_pack: Dict[str, List[Dict[str, Any]]], trace: List[Dict[str, Any]]) -> Dict[str, Any]:
    answer = " ".join(f["claim"] for f in facts_pack["facts"])
    return {
        "answer": answer,
        "facts": facts_pack["facts"],
        "trace": trace,
    }


# =========================
# 🚀 PIPELINE
# =========================
def run(query: str) -> Dict[str, Any]:
    retrieved = retrieve(query)
    facts_pack = build_facts_pack(retrieved, query)
    trace = build_trace(retrieved)

    if not trace:
        return {
            "error": "No trace. Answer blocked.",
            "answer": None,
            "facts": facts_pack.get("facts", []),
            "trace": trace,
        }

    if not guardian(facts_pack, trace):
        return {
            "error": "Guardian blocked response.",
            "answer": None,
            "facts": facts_pack.get("facts", []),
            "trace": trace,
        }

    if not truth_gate(facts_pack):
        return {
            "error": "Not enough data.",
            "answer": None,
            "facts": facts_pack.get("facts", []),
            "trace": trace,
        }

    return generate_answer(facts_pack, trace)


# =========================
# 🧪 TEST
# =========================
if __name__ == "__main__":
    print(run("What is quantum entanglement?"))
