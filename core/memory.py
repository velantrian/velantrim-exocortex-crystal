# core/memory.py
# Velantrim ExoCortex — Memory Layer
# v8.1.0-sprint1
#
# Уровни памяти:
#   L0: LRU in-memory cache (CAP=5, OrderedDict)
#   L1: SQLite (краткосрочная, персистентная между запусками)
#
# Полная архитектура L0–L6: docs/Velantrim_V8_Crystal_Sprint1_toc.md
# ESM (Epistemic State Machine): 8 состояний жизненного цикла факта.

import os
import sqlite3
import json
from collections import OrderedDict
from contextlib import contextmanager
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

# ─── ESM: матрица допустимых переходов ────────────────────────────────────────
# MVP fast-path: Observed → Validated разрешён напрямую для демо-пайплайна.
# I6: VALUES_CORE / RING_ZERO защищены в transition_esm, не через матрицу.
ESM_TRANSITIONS: Dict[str, set] = {
    "Observed":      {"Hypothesized", "Supported", "Validated", "Collapsed"},
    "Hypothesized":  {"Supported", "Validated", "Collapsed"},
    "Supported":     {"Validated", "Collapsed"},
    "Validated":     {"Contradicted", "ImmutableCore", "Collapsed"},
    "Contradicted":  {"Deprecated", "Collapsed"},
    "Deprecated":    {"Collapsed"},
    "Collapsed":     set(),
    "ImmutableCore": set(),
}

# ─── RING ZERO / VALUES CORE: неизменяемые факты (I6) ─────────────────────────
IMMUTABLE_FACT_IDS = {"VALUES_CORE", "RING_ZERO"}


class ImmutableStateError(Exception):
    """Raised when attempting to transition a Ring Zero / VALUES_CORE fact."""
    pass


# ─── L0: LRU cache (in-memory, живёт только в сессии) ─────────────────────────
L0_CAP = 5
_L0: OrderedDict = OrderedDict()

# ─── L1: SQLite путь ──────────────────────────────────────────────────────────
SQLITE_PATH = "./data/velantrim_memory.db"

_DDL = """
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
"""


@contextmanager
def _db():
    """Connection per operation — no global state, no database-is-locked."""
    db_dir = os.path.dirname(SQLITE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(_DDL)
    conn.commit()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─── L0 helpers ───────────────────────────────────────────────────────────────

def _l0_put(fact_id: str, record: Dict) -> None:
    """Insert into L0 LRU cache, evict oldest entry when over capacity."""
    if fact_id in _L0:
        del _L0[fact_id]
    _L0[fact_id] = record
    if len(_L0) > L0_CAP:
        _L0.popitem(last=False)  # evict least-recently-used


def _l0_get(fact_id: str) -> Optional[Dict]:
    """Return from L0, refreshing recency. Returns None on miss."""
    if fact_id not in _L0:
        return None
    _L0.move_to_end(fact_id)
    return _L0[fact_id]


# ─── API ───────────────────────────────────────────────────────────────────────

def store_fact(fact: Dict) -> None:
    """
    Сохранить факт в L0 (LRU RAM) и L1 (SQLite).
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

    metadata_dict = fact.get("metadata", {})

    record = {
        "fact_id":         fact_id,
        "claim":           fact.get("claim", ""),
        "source":          fact.get("source", "unknown"),
        "confidence":      round(float(fact.get("confidence", 0.5)), 4),
        "epistemic_state": epistemic_state,
        "created_at":      now,
        "updated_at":      now,
        "metadata":        metadata_dict,
    }

    _l0_put(fact_id, record)

    l1_record = {**record, "metadata": json.dumps(metadata_dict)}
    with _db() as conn:
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
        """, l1_record)


def get_fact(fact_id: str) -> Optional[Dict]:
    """Получить факт: сначала L0 (LRU), потом L1."""
    cached = _l0_get(fact_id)
    if cached is not None:
        return cached
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        if row:
            result = dict(row)
            result["metadata"] = json.loads(result["metadata"])
            _l0_put(fact_id, result)
            return result
    return None


def transition_esm(fact_id: str, new_state: str) -> bool:
    """
    Перевести факт в новое ESM-состояние.
    Прямой SET epistemic_state минуя эту функцию — архитектурный баг.
    """
    if new_state not in ESM_STATES:
        raise ValueError(f"transition_esm: недопустимое состояние '{new_state}'")

    if fact_id in IMMUTABLE_FACT_IDS:
        raise ImmutableStateError(
            f"transition_esm: факт '{fact_id}' защищён Ring Zero (I6), "
            f"переход в '{new_state}' запрещён"
        )

    fact = get_fact(fact_id)
    if not fact:
        return False

    current_state = fact.get("epistemic_state", "Observed")
    allowed = ESM_TRANSITIONS.get(current_state)
    if allowed is not None and new_state not in allowed:
        raise ValueError(
            f"transition_esm: переход '{current_state}' → '{new_state}' недопустим"
        )

    now = datetime.now(timezone.utc).isoformat()
    fact["epistemic_state"] = new_state
    fact["updated_at"] = now

    _l0_put(fact_id, fact)
    with _db() as conn:
        conn.execute(
            "UPDATE facts SET epistemic_state = ?, updated_at = ? WHERE fact_id = ?",
            (new_state, now, fact_id)
        )
    return True


def get_all_facts(epistemic_state: Optional[str] = None) -> list:
    """Получить все факты из L1. Опционально — фильтр по ESM-состоянию."""
    with _db() as conn:
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
