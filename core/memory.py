# core/memory.py

from typing import Dict

# простая in-memory структура (вместо графа пока)
MEMORY: Dict[str, Dict] = {}


def store_fact(fact: Dict):
    MEMORY[fact["fact_id"]] = fact


def get_fact(fact_id: str):
    return MEMORY.get(fact_id)
