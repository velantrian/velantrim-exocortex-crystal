# core/memory.py
# Velantrim ExoCortex — Memory Layer
# v8.7.0-sprint2
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

# ─── CLAIM TYPE: модальность утверждения (ось, ортогональная ESM) ─────────────
# ESM отвечает на «насколько проверено», claim_type — на «что это за утверждение».
# WORLD_FACT отделён от FACT намеренно: «факт о внешнем мире», а не «проверено».
# Чувство реально как чувство — EMOTION может стать Validated, но НЕ WORLD_FACT.
CLAIM_TYPES = {
    "WORLD_FACT",       # утверждение о внешнем мире (требует доказательств)
    "USER_EXPERIENCE",  # событие, как его пережил пользователь
    "EMOTION",          # внутреннее состояние / чувство
    "INTERPRETATION",   # вывод / объяснение (гипотеза)
    "OPINION",          # мнение пользователя
    "GOAL",             # цель
    "PREFERENCE",       # предпочтение
}
DEFAULT_CLAIM_TYPE = "WORLD_FACT"

# ─── SOURCE STATUS: происхождение утверждения (source monitoring) ─────────────
# Защита от source-confusion: путаницы «видел / вообразил / услышал / додумал».
SOURCE_STATUSES = {
    "USER_REPORTED",  # сообщил пользователь
    "OBSERVED",       # наблюдалось системой
    "DERIVED",        # выведено из других фактов
    "EXTERNAL",       # внешний источник / retrieval
    "LLM_OUTPUT",     # ответ модели — сам по себе НЕ факт о мире
    "UNKNOWN",
}
DEFAULT_SOURCE_STATUS = "UNKNOWN"

# claim_type, для которых TruthGate НЕ требует доказательной планки:
# они валидны как субъективный опыт, но не как факт о мире.
SUBJECTIVE_CLAIM_TYPES = {
    "USER_EXPERIENCE", "EMOTION", "OPINION", "PREFERENCE", "GOAL",
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
        claim_type     TEXT DEFAULT 'WORLD_FACT',
        source_status  TEXT DEFAULT 'UNKNOWN',
        significance   REAL DEFAULT 0.5,
        created_at     TEXT NOT NULL,
        updated_at     TEXT NOT NULL,
        metadata       TEXT DEFAULT '{}'
    )
"""

# ─── L3 OUTBOX: персистентная очередь до-мержа в канон ────────────────────────
# L3 (канон) и SQLite (pending) не делят транзакцию. Если merge в L3 упал (бэкенд
# недоступен), факт остаётся Validated в SQLite без узла в графе. Outbox делает
# это самовосстанавливающимся: упавший факт ставится в очередь и идемпотентно
# до-мержится при следующем обращении (drain), а не ждёт повтора того же запроса.
_OUTBOX_DDL = """
    CREATE TABLE IF NOT EXISTS l3_outbox (
        fact_id     TEXT PRIMARY KEY,
        enqueued_at TEXT NOT NULL
    )
"""

# ─── Миграция: колонки, добавленные после первого релиза схемы ────────────────
# CREATE TABLE IF NOT EXISTS не трогает уже существующую БД, поэтому старые файлы
# velantrim_memory.db нужно догнать через ALTER TABLE ADD COLUMN (idempotent).
_MIGRATIONS = [
    ("claim_type",    "TEXT DEFAULT 'WORLD_FACT'"),
    ("source_status", "TEXT DEFAULT 'UNKNOWN'"),
    ("significance",  "REAL DEFAULT 0.5"),
]


def _migrate(conn) -> None:
    """Добавить недостающие колонки в существующую таблицу facts (idempotent)."""
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(facts)")}
    for column, ddl in _MIGRATIONS:
        if column not in existing:
            conn.execute(f"ALTER TABLE facts ADD COLUMN {column} {ddl}")


@contextmanager
def _db():
    """Connection per operation — no global state, no database-is-locked."""
    db_dir = os.path.dirname(SQLITE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    # WAL: writer не блокирует readers (лучше параллелизм для evidence/audit).
    # Свойство файла БД — ставится один раз и сохраняется; повтор безвреден.
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(_DDL)
    conn.execute(_OUTBOX_DDL)
    _migrate(conn)
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

    claim_type = fact.get("claim_type", DEFAULT_CLAIM_TYPE)
    if claim_type not in CLAIM_TYPES:
        raise ValueError(f"store_fact: недопустимый claim_type '{claim_type}'")

    source_status = fact.get("source_status", DEFAULT_SOURCE_STATUS)
    if source_status not in SOURCE_STATUSES:
        raise ValueError(f"store_fact: недопустимый source_status '{source_status}'")

    metadata_dict = fact.get("metadata", {})

    record = {
        "fact_id":         fact_id,
        "claim":           fact.get("claim", ""),
        "source":          fact.get("source", "unknown"),
        "confidence":      round(float(fact.get("confidence", 0.5)), 4),
        "epistemic_state": epistemic_state,
        "claim_type":      claim_type,
        "source_status":   source_status,
        "significance":    round(float(fact.get("significance", 0.5)), 4),
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
                 claim_type, source_status, significance,
                 created_at, updated_at, metadata)
            VALUES
                (:fact_id, :claim, :source, :confidence, :epistemic_state,
                 :claim_type, :source_status, :significance,
                 :created_at, :updated_at, :metadata)
            ON CONFLICT(fact_id) DO UPDATE SET
                claim           = excluded.claim,
                source          = excluded.source,
                confidence      = excluded.confidence,
                epistemic_state = excluded.epistemic_state,
                claim_type      = excluded.claim_type,
                source_status   = excluded.source_status,
                significance    = excluded.significance,
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


# ─── Колонки, которые можно точечно обновлять без смены ESM-состояния ─────────
_UPDATABLE = {"claim", "source", "confidence", "significance",
              "claim_type", "source_status", "metadata"}


def update_fact(fact_id: str, **fields) -> bool:
    """
    Точечно обновить поля факта, НЕ трогая epistemic_state.
    Смена ESM-состояния — только через transition_esm. Возвращает True, если
    факт найден и обновлён.
    """
    fields = {k: v for k, v in fields.items() if k in _UPDATABLE}
    existing = get_fact(fact_id)
    if existing is None or not fields:
        return False

    now = datetime.now(timezone.utc).isoformat()
    sets, params = [], {"fact_id": fact_id, "updated_at": now}
    for key, value in fields.items():
        sets.append(f"{key} = :{key}")
        params[key] = json.dumps(value) if key == "metadata" else value

    with _db() as conn:
        conn.execute(
            f"UPDATE facts SET {', '.join(sets)}, updated_at = :updated_at "
            f"WHERE fact_id = :fact_id",
            params,
        )

    merged = {**existing, **fields, "updated_at": now}
    _l0_put(fact_id, merged)
    return True


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


# ─── L3 OUTBOX API ────────────────────────────────────────────────────────────

def enqueue_l3_write(fact_id: str) -> None:
    """Поставить факт в очередь до-мержа в L3 (idempotent: upsert по fact_id)."""
    now = datetime.now(timezone.utc).isoformat()
    with _db() as conn:
        conn.execute(
            "INSERT INTO l3_outbox (fact_id, enqueued_at) VALUES (?, ?) "
            "ON CONFLICT(fact_id) DO UPDATE SET enqueued_at = excluded.enqueued_at",
            (fact_id, now),
        )


def pending_l3_writes() -> list:
    """fact_id'ы, ожидающие до-мержа в L3 (в порядке постановки)."""
    with _db() as conn:
        return [row["fact_id"] for row in conn.execute(
            "SELECT fact_id FROM l3_outbox ORDER BY enqueued_at, fact_id")]


def clear_l3_write(fact_id: str) -> None:
    """Убрать факт из очереди (после успешного мержа или если он больше не нужен)."""
    with _db() as conn:
        conn.execute("DELETE FROM l3_outbox WHERE fact_id = ?", (fact_id,))
