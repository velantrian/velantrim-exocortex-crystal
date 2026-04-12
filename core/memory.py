# core/memory.py
# Velantrim ExoCortex — Memory Layer
# v8.0.2-sprint1
#
# Уровни памяти:
#   L0: in-memory dict (рабочая память сессии)
#   L1: SQLite (краткосрочная, персистентная между запусками)
#
# Полная архитектура L0–L6: см. docs/Velantrim_V8_Crystal_Sprint1_toc.md
# ESM (Epistemic State Machine): 8 состояний жизненного цикла факта.

import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, Optional

# ─── ESM: допустимые состояния факта ──────────────────────────────────────────
# Observed → Hypothesized → Supported → Validated → ImmutableCore
#                                    ↘ Contradicted → Deprecated → Collapsed
ESM_STATES = {
    "Observed",       # сырой вход, до классификации
    "Hypothesized",   # принят, ещё не подтверждён
    "Supported",      # есть доказательства
    "Validated",      # проверен TruthGate
    "Contradicted",   # конфликт с другим фактом
    "Deprecated",     # устарел
    "Collapsed",      # удалён логически
    "ImmutableCore",  # неизменяем (Ring Zero)
}

# ─── L0: рабочая память (in-memory, живёт только в сессии) ────────────────────
_L0: Dict[str, Dict] = {}

# ─── L1: SQLite путь ──────────────────────────────────────────────────────────
SQLITE_PATH = "./data/velantrim_memory.db"


def _get_conn() -> sqlite3.Connection:
    import os
    os.makedirs("./data", exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            fact_id        TEXT PRIMARY KEY,
            claim          TEXT NOT NULL,
            source         TEXT NOT NULL,
            confidence     REAL DEFAULT 0.5,
            epistemic_state TEXT DEFAULT 'Observed',
            created_at     TEXT NOT NULL,
            updated_at     TEXT NOT NULL,
            metadata       TEXT DEFAULT '{}'
        )
    """)
    conn.commit()
    return conn


# ─── API ───────────────────────────────────────────────────────────────────────

def store_fact(fact: Dict) -> None:
    """
    Сохранить факт в L0 (RAM) и L1 (SQLite).
    Начальное состояние ESM: Observed.
    Прямая запись в L3 граф — только через TruthGate (не здесь).
    """
    fact_id = fact.get("fact_id")
    if not fact_id:
        raise ValueError("store_fact: fact_id обязателен")

    now = datetime.now(timezone.utc).isoformat()
    epistemic_state = fact.get("epistemic_state", "Observed")

    if epistemic_state not in ESM_STATES:
        raise ValueError(f"store_fact: недопустимое ESM-состояние '{epistemic_state}'")

    record = {
        "fact_id":         fact_id,
        "claim":           fact.get("claim", ""),
        "source":          fact.get("source", "unknown"),
        "confidence":      round(float(fact.get("confidence", 0.5)), 4),
        "epistemic_state": epistemic_state,
        "created_at":      now,
        "updated_at":      now,
        "metadata":        json.dumps(fact.get("metadata", {})),
    }

    # L0
    _L0[fact_id] = record

    # L1
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO facts
                (fact_id, claim, source, confidence, epistemic_state,
                 created_at, updated_at, metadata)
            VALUES
                (:fact_id, :claim, :source, :confidence, :epistemic_state,
                 :created_at, :updated_at, :metadata)
            ON CONFLICT(fact_id) DO UPDATE SET
                claim           = excluded.claim,
                source          = excluded.source,
                confidence      = excluded.confidence,
                epistemic_state = excluded.epistemic_state,
                updated_at      = excluded.updated_at,
                metadata        = excluded.metadata
        """, record)


def get_fact(fact_id: str) -> Optional[Dict]:
    """Получить факт: сначала L0, потом L1."""
    if fact_id in _L0:
        return _L0[fact_id]
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        if row:
            result = dict(row)
            result["metadata"] = json.loads(result["metadata"])
            _L0[fact_id] = result  # прогреть L0
            return result
    return None


def transition_esm(fact_id: str, new_state: str) -> bool:
    """
    Перевести факт в новое ESM-состояние.
    Прямой SET epistemic_state минуя эту функцию — архитектурный баг.
    В полной реализации: переходы проверяются матрицей допустимых переходов.
    """
    if new_state not in ESM_STATES:
        raise ValueError(f"transition_esm: недопустимое состояние '{new_state}'")

    fact = get_fact(fact_id)
    if not fact:
        return False

    now = datetime.now(timezone.utc).isoformat()
    fact["epistemic_state"] = new_state
    fact["updated_at"] = now

    _L0[fact_id] = fact
    with _get_conn() as conn:
        conn.execute(
            "UPDATE facts SET epistemic_state = ?, updated_at = ? WHERE fact_id = ?",
            (new_state, now, fact_id)
        )
    return True


def get_all_facts(epistemic_state: Optional[str] = None) -> list:
    """Получить все факты из L1. Опционально — фильтр по ESM-состоянию."""
    with _get_conn() as conn:
        if epistemic_state:
            rows = conn.execute(
                "SELECT * FROM facts WHERE epistemic_state = ?",
                (epistemic_state,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM facts").fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["metadata"] = json.loads(r["metadata"])
            result.append(r)
        return result
