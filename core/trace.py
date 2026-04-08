```python
# core/trace.py

from typing import List, Dict, Any


# =========================
# 🧭 TRACE BUILDER
# =========================
def build_trace(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    trace: List[Dict[str, Any]] = []

    for item in retrieved:
        trace.append({
            "fact_id": item.get("id"),
            "source": item.get("source"),
            "origin": "retrieval"
        })

    return trace
