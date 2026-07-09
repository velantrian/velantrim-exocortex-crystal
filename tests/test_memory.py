"""Tests for core/memory.py paths not covered by test_esm.py.

Focus: L0→L1 fallback, get_all_facts, and the input-validation / not-found
branches of store_fact / transition_esm.
"""
import sqlite3

import pytest

from core import memory
from core.memory import (
    store_fact,
    get_fact,
    transition_esm,
    get_all_facts,
    set_restricted,
    call_with_lock_retry,
    _L0,
    L0_CAP,
)


def test_store_fact_requires_fact_id():
    with pytest.raises(ValueError, match="fact_id"):
        store_fact({"claim": "no id", "source": "s"})


def test_get_fact_falls_back_to_l1_after_l0_eviction():
    """A fact pushed out of the L0 LRU must still be retrievable from L1."""
    store_fact({"fact_id": "deep", "claim": "persisted", "source": "disk",
                "confidence": 0.7})

    # Overflow L0 so "deep" is evicted from the in-memory cache.
    for i in range(L0_CAP + 2):
        store_fact({"fact_id": f"flood_{i}", "claim": "x", "source": "t",
                    "confidence": 0.5})
    assert "deep" not in _L0

    # get_fact must hit SQLite, rehydrate metadata, and re-promote into L0.
    f = get_fact("deep")
    assert f is not None
    assert f["claim"] == "persisted"
    assert f["metadata"] == {}          # JSON round-trips back to a dict
    assert "deep" in _L0                # promoted back into the cache


def test_get_fact_unknown_returns_none():
    assert get_fact("does-not-exist") is None


def test_store_fact_upsert_updates_existing_row():
    store_fact({"fact_id": "up1", "claim": "v1", "source": "s", "confidence": 0.5})
    store_fact({"fact_id": "up1", "claim": "v2", "source": "s", "confidence": 0.9})
    f = get_fact("up1")
    assert f["claim"] == "v2"
    assert f["confidence"] == pytest.approx(0.9)


def test_store_fact_upsert_preserves_restricted_and_created_at_in_l0():
    """A conflict-update must not poison the L0 cache with a reset `restricted`
    flag or a fresh `created_at` — both must reflect the persisted DB row, not
    the incoming/default values baked into a brand-new `record` dict.

    Regression for: after set_restricted(True), a later store_fact() upsert
    (e.g. a re-ingest of the same fact_id) used to overwrite the L0 entry with
    restricted missing entirely and created_at reset to "now", even though the
    DB row correctly kept restricted=1 and the original created_at.
    """
    store_fact({"fact_id": "res1", "claim": "v1", "source": "s", "confidence": 0.5})
    original_created_at = get_fact("res1")["created_at"]

    assert set_restricted("res1", True) is True
    assert get_fact("res1")["restricted"] == 1  # from L0

    # Upsert the same fact_id (e.g. a re-ingest) — must NOT poison L0.
    store_fact({"fact_id": "res1", "claim": "v2", "source": "s", "confidence": 0.9})
    cached = get_fact("res1")  # served from L0
    assert cached["restricted"] == 1
    assert cached["created_at"] == original_created_at
    assert cached["claim"] == "v2"  # other fields still update normally

    # And the L1/SQLite row must agree (no divergence between cache and disk).
    _L0.clear()
    persisted = get_fact("res1")
    assert persisted["restricted"] == 1
    assert persisted["created_at"] == original_created_at


def test_metadata_round_trips_through_l1():
    _L0.clear()  # force the L1 read path on get
    store_fact({"fact_id": "meta1", "claim": "c", "source": "s", "confidence": 0.5,
                "metadata": {"tags": ["a", "b"], "n": 3}})
    _L0.clear()
    f = get_fact("meta1")
    assert f["metadata"] == {"tags": ["a", "b"], "n": 3}


def test_transition_esm_rejects_unknown_state():
    store_fact({"fact_id": "tr1", "claim": "c", "source": "s", "confidence": 0.5})
    with pytest.raises(ValueError, match="invalid state"):
        transition_esm("tr1", "Imaginary")


def test_transition_esm_missing_fact_returns_false():
    assert transition_esm("ghost", "Validated") is False


def test_update_fact_changes_columns_without_touching_esm():
    store_fact({"fact_id": "u1", "claim": "c", "source": "s", "confidence": 0.5})
    transition_esm("u1", "Validated")
    from core.memory import update_fact
    assert update_fact("u1", confidence=0.9, metadata={"observations": 3}) is True
    f = get_fact("u1")
    assert f["confidence"] == 0.9
    assert f["metadata"] == {"observations": 3}
    assert f["epistemic_state"] == "Validated"   # ESM untouched


def test_update_fact_missing_or_no_fields_returns_false():
    from core.memory import update_fact
    assert update_fact("nope", confidence=0.9) is False          # missing fact
    store_fact({"fact_id": "u2", "claim": "c", "source": "s"})
    assert update_fact("u2", epistemic_state="Validated") is False  # not updatable


def test_update_fact_cas_rejects_stale_snapshot_without_poisoning_cache():
    """Regression: update_fact() blindly overwrote based on whatever the
    caller last saw (indirectly, via get_fact), with no version check —
    concurrent update_fact() calls on the same fact_id (e.g. two reconcile.
    reinforce() calls) could silently drop one writer's update.

    Simulate a stale L0 snapshot racing a write that landed underneath it:
    a direct SQL write bypasses the L0-invalidating helpers, so L0 keeps
    serving the pre-write snapshot — the same shape a second worker thread
    that read *before* the first worker's write completed would see."""
    from core import crypto
    from core.memory import update_fact
    from datetime import datetime, timezone

    store_fact({"fact_id": "cas1", "claim": "v0", "source": "s", "confidence": 0.5})
    stale = get_fact("cas1")  # this snapshot is what L0 now serves

    # A competing writer's update landed via a fresh connection, bypassing the
    # cache-invalidating helpers — L0 does not know about it.
    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET claim = ?, updated_at = ? WHERE fact_id = ?",
            (crypto.encrypt("v1-from-another-writer"),
             datetime.now(timezone.utc).isoformat(), "cas1"),
        )

    # update_fact()'s internal get_fact() still returns the stale L0 snapshot,
    # so its CAS check must find the persisted updated_at has moved and abort —
    # not silently overwrite the other writer's claim.
    assert update_fact("cas1", confidence=0.9) is False

    # L0 must be evicted on the CAS miss: the next read reflects the real
    # persisted state, not a re-served stale copy.
    fresh = get_fact("cas1")
    assert fresh["claim"] == "v1-from-another-writer"
    assert fresh["confidence"] == stale["confidence"]  # our update never landed

    # A fresh retry (re-read, then update) against the current state succeeds.
    assert update_fact("cas1", confidence=0.9) is True
    assert get_fact("cas1")["confidence"] == 0.9


def test_update_fact_normal_sequential_calls_still_succeed():
    """The CAS guard must not get in the way of the common (non-racing) case:
    each update_fact() call re-reads the just-written state, so successive
    calls on the same fact_id keep succeeding."""
    from core.memory import update_fact
    store_fact({"fact_id": "cas2", "claim": "c", "source": "s", "confidence": 0.1})
    assert update_fact("cas2", confidence=0.2) is True
    assert update_fact("cas2", confidence=0.3) is True
    assert update_fact("cas2", confidence=0.4) is True
    assert get_fact("cas2")["confidence"] == 0.4


def test_db_uses_wal_journal_mode():
    """Evidence/audit store runs in WAL so writers don't block readers."""
    from core import memory
    with memory._db() as conn:
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert mode.lower() == "wal"


def test_db_rolls_back_on_exception():
    """_db() must roll back (and re-raise) when the with-block raises."""
    from core import memory
    with pytest.raises(ValueError, match="boom"):
        with memory._db() as conn:
            conn.execute(
                "INSERT INTO facts (fact_id, claim, source, created_at, updated_at) "
                "VALUES ('rb', 'c', 's', 't', 't')"
            )
            raise ValueError("boom")
    # The insert must not have been committed.
    assert get_fact("rb") is None


def test_get_all_facts_unfiltered_and_filtered():
    store_fact({"fact_id": "a1", "claim": "c", "source": "s", "confidence": 0.5})
    store_fact({"fact_id": "a2", "claim": "c", "source": "s", "confidence": 0.5})
    transition_esm("a2", "Validated")

    all_facts = get_all_facts()
    ids = {f["fact_id"] for f in all_facts}
    assert {"a1", "a2"} <= ids
    # metadata is deserialized for every row
    assert all(isinstance(f["metadata"], dict) for f in all_facts)

    validated = get_all_facts(epistemic_state="Validated")
    assert {f["fact_id"] for f in validated} == {"a2"}


# ─── claim_type / source_status / significance (modality axis) ──────────────

def test_new_fields_default_when_omitted():
    """store_fact must apply sane defaults for the orthogonal modality axis."""
    _L0.clear()
    store_fact({"fact_id": "d1", "claim": "c", "source": "s", "confidence": 0.5})
    _L0.clear()  # force the L1 read path
    f = get_fact("d1")
    assert f["claim_type"] == "WORLD_FACT"
    assert f["source_status"] == "UNKNOWN"
    assert f["significance"] == pytest.approx(0.5)


def test_new_fields_round_trip_through_l1():
    _L0.clear()
    store_fact({"fact_id": "e1", "claim": "felt anxious", "source": "user",
                "confidence": 0.9, "claim_type": "EMOTION",
                "source_status": "USER_REPORTED", "significance": 0.7})
    _L0.clear()
    f = get_fact("e1")
    assert f["claim_type"] == "EMOTION"
    assert f["source_status"] == "USER_REPORTED"
    assert f["significance"] == pytest.approx(0.7)


def test_store_fact_rejects_unknown_claim_type():
    with pytest.raises(ValueError, match="claim_type"):
        store_fact({"fact_id": "bad", "claim": "c", "source": "s",
                    "claim_type": "TELEPATHY"})


def test_store_fact_rejects_unknown_source_status():
    with pytest.raises(ValueError, match="source_status"):
        store_fact({"fact_id": "bad2", "claim": "c", "source": "s",
                    "source_status": "OUIJA_BOARD"})


def test_migration_adds_columns_to_legacy_table(monkeypatch, tmp_path):
    """A pre-existing DB built on the old schema must gain the new columns."""
    import sqlite3
    from core import memory

    legacy = str(tmp_path / "legacy.db")
    conn = sqlite3.connect(legacy)
    conn.execute("""
        CREATE TABLE facts (
            fact_id TEXT PRIMARY KEY, claim TEXT NOT NULL, source TEXT NOT NULL,
            confidence REAL DEFAULT 0.5, epistemic_state TEXT DEFAULT 'Observed',
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            metadata TEXT DEFAULT '{}'
        )
    """)
    conn.commit()
    conn.close()

    memory._L0.clear()
    monkeypatch.setattr(memory, "SQLITE_PATH", legacy)
    # store_fact opens _db(), which must ALTER the legacy table before INSERT.
    store_fact({"fact_id": "leg1", "claim": "c", "source": "s",
                "claim_type": "OPINION", "significance": 0.3})
    memory._L0.clear()
    f = get_fact("leg1")
    assert f["claim_type"] == "OPINION"
    assert f["significance"] == pytest.approx(0.3)


# ─── call_with_lock_retry (audit/provenance_chain write-lock contention) ─────

def test_call_with_lock_retry_retries_transient_lock_then_succeeds(monkeypatch):
    monkeypatch.setattr(memory.time, "sleep", lambda seconds: None)
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise sqlite3.OperationalError("database is locked")
        return "ok"

    assert call_with_lock_retry(flaky, retries=5, base_delay=0.01) == "ok"
    assert calls["n"] == 3


def test_call_with_lock_retry_reraises_once_retries_are_exhausted(monkeypatch):
    monkeypatch.setattr(memory.time, "sleep", lambda seconds: None)

    def always_locked():
        raise sqlite3.OperationalError("database is locked")

    with pytest.raises(sqlite3.OperationalError, match="locked"):
        call_with_lock_retry(always_locked, retries=3, base_delay=0.01)


def test_call_with_lock_retry_does_not_retry_unrelated_operational_errors():
    calls = {"n": 0}

    def other_error():
        calls["n"] += 1
        raise sqlite3.OperationalError("disk I/O error")

    with pytest.raises(sqlite3.OperationalError, match="disk I/O error"):
        call_with_lock_retry(other_error, retries=5, base_delay=0.01)
    assert calls["n"] == 1  # no retry for a non-lock OperationalError


def test_l0_cache_survives_concurrent_access():
    """Regression: the L0 LRU cache is module-level mutable state driven from
    worker threads (core/aio.py runs the pipeline via asyncio.to_thread; the
    FastAPI service layer is multi-threaded). Before _L0_LOCK guarded them, the
    check-then-act sequences raced: _l0_get does `if k in _L0` then
    `_L0.move_to_end(k)`, so a competing _l0_pop/eviction between the two lines
    raised KeyError; concurrent _l0_put could also drive len(_L0) past L0_CAP.

    Hammer the L0 helpers directly (the unit the lock fixes) from many threads
    over a key space larger than the cache — no SQLite, so this isolates the
    cache race without touching L1 write concurrency. A worker exception
    re-raises here via future.result(); the LRU size invariant must still hold."""
    import sys
    import threading
    from concurrent.futures import ThreadPoolExecutor

    keys = [f"cc_{i}" for i in range(L0_CAP * 4)]  # 20 keys, cap 5 → eviction churn
    n_workers = 8
    barrier = threading.Barrier(n_workers)

    def worker(seed):
        barrier.wait()  # release all workers together to maximise contention
        for n in range(4000):
            memory._l0_put(keys[(seed + n) % len(keys)], {"fact_id": "x", "claim": "c"})
            memory._l0_get(keys[(seed * 7 + n) % len(keys)])
            if n % 4 == 0:
                memory._l0_pop(keys[(seed * 3 + n) % len(keys)])

    # Force aggressive thread pre-emption so the check-then-act window is
    # actually hit: with the default switch interval the GIL lets a helper run
    # to completion too often for the unsynchronised race to surface. Verified
    # to fail (KeyError) on every run when _L0_LOCK is removed.
    prev_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-7)
    try:
        with ThreadPoolExecutor(max_workers=n_workers) as ex:
            futures = [ex.submit(worker, s) for s in range(n_workers)]
            for f in futures:
                f.result()  # re-raise any KeyError/RuntimeError from a race
    finally:
        sys.setswitchinterval(prev_interval)

    assert len(memory._L0) <= L0_CAP


# ─── _l0_put_if_fresher (L0 cache-freshness guard) ────────────────────────────
#
# store_fact() writes to L1 first, then populates L0 — with no lock spanning
# both steps. Two concurrent store_fact() calls for the same fact_id can
# commit to L1 in one order (SQLite serializes writes) but reach the L0
# write in the OTHER order (whichever thread's scheduled first), leaving a
# stale record cached even though L1 already holds the newer one.
# _l0_put_if_fresher() compares `updated_at` (ISO-8601 UTC, safe to compare
# lexically) and refuses to overwrite a cached record with an older one.
# This is a cache-coherence guard, not a CAS/revision scheme (see #244,
# which is a separate, still-on-hold change to update_fact() specifically) —
# it never rejects a write to L1, never raises, and never changes what
# store_fact()/get_fact() return; it only decides what ends up cached.

def test_l0_put_if_fresher_accepts_when_nothing_cached():
    memory._l0_pop("if_fresher_new")
    rec = {"fact_id": "if_fresher_new", "claim": "v1",
           "updated_at": "2024-01-01T00:00:00+00:00"}
    memory._l0_put_if_fresher("if_fresher_new", rec)
    assert memory._l0_get("if_fresher_new") == rec


def test_l0_put_if_fresher_rejects_older_record():
    """Helper-level guard: an older incoming record must not evict a newer
    one that is already cached."""
    newer = {"fact_id": "if_fresher1", "claim": "v2",
             "updated_at": "2024-01-02T00:00:00+00:00"}
    older = {"fact_id": "if_fresher1", "claim": "v1",
              "updated_at": "2024-01-01T00:00:00+00:00"}
    memory._l0_put_if_fresher("if_fresher1", newer)
    memory._l0_put_if_fresher("if_fresher1", older)
    assert memory._l0_get("if_fresher1") == newer


def test_l0_put_if_fresher_accepts_newer_record():
    """A genuinely newer incoming record still overwrites the cache normally
    — the guard only blocks the STALE-overwriting-fresh direction."""
    older = {"fact_id": "if_fresher2", "claim": "v1",
              "updated_at": "2024-01-01T00:00:00+00:00"}
    newer = {"fact_id": "if_fresher2", "claim": "v2",
             "updated_at": "2024-01-02T00:00:00+00:00"}
    memory._l0_put_if_fresher("if_fresher2", older)
    memory._l0_put_if_fresher("if_fresher2", newer)
    assert memory._l0_get("if_fresher2") == newer


def test_l0_put_if_fresher_accepts_incoming_record_on_tied_timestamp():
    """Defined tie-breaking rule: an EQUAL `updated_at` accepts the incoming
    record, preserving the pre-existing unconditional-overwrite behavior for
    the common non-racing case (e.g. two calls close enough in time to round
    to the same timestamp) rather than inventing a new first-write-wins rule
    nothing in the codebase depends on."""
    ts = "2024-01-01T00:00:00+00:00"
    first = {"fact_id": "if_fresher3", "claim": "v1", "updated_at": ts}
    second = {"fact_id": "if_fresher3", "claim": "v2", "updated_at": ts}
    memory._l0_put_if_fresher("if_fresher3", first)
    memory._l0_put_if_fresher("if_fresher3", second)
    assert memory._l0_get("if_fresher3") == second


def test_l0_freshness_guard_prevents_the_reordering_that_would_otherwise_poison_cache():
    """Deterministic simulation of the actual race (no sleep/threads needed):
    two concurrent store_fact() calls for the same fact_id can commit to L1
    in one order but reach the L0 write in the other order. Simulate the
    'loser' (older DB commit) reaching its L0 write AFTER the 'winner'
    (newer DB commit) already populated L0.

    First prove the failure mode is real with the raw, unguarded _l0_put()
    (what store_fact() called before this fix): it happily overwrites the
    fresher cached record with stale data. Then prove _l0_put_if_fresher()
    — what store_fact() calls now — is immune to the identical reordering."""
    store_fact({"fact_id": "race1", "claim": "winner (newer)", "source": "s",
                "confidence": 0.9})
    winner_cached = dict(memory._l0_get("race1"))
    assert winner_cached["claim"] == "winner (newer)"

    # The "loser" writer's own store_fact() call committed to L1 BEFORE the
    # winner's (an earlier updated_at), but its thread only reaches the L0
    # write line now, after the winner's record has already landed.
    stale_record = {**winner_cached, "claim": "loser (older, stale)",
                     "updated_at": "2000-01-01T00:00:00+00:00"}

    # Failure mode: the raw primitive poisons the cache with stale data.
    memory._l0_put("race1", stale_record)
    assert memory._l0_get("race1")["claim"] == "loser (older, stale)"

    # Restore the winner and prove the freshness guard is immune to the same
    # reordering.
    memory._l0_put("race1", winner_cached)
    memory._l0_put_if_fresher("race1", stale_record)
    assert memory._l0_get("race1")["claim"] == "winner (newer)"


def test_store_fact_does_not_let_a_delayed_stale_l0_write_win():
    """Exercises _l0_put_if_fresher() with real store_fact()-produced records
    (not synthetic ones): even if a delayed read's L0-populate step arrives
    after a fresher store_fact() call already landed, the helper keeps the
    fresher record. (store_fact() itself no longer calls this helper for its
    OWN populate step — see test_store_fact_l0_reflects_actual_l1_winner_not_
    capture_time_order below for why, and _l0_put_if_fresher()'s docstring —
    but get_fact()'s L1-rehydration path does, and this is the shape of
    protection it gets.)"""
    store_fact({"fact_id": "race2", "claim": "first", "source": "s", "confidence": 0.5})
    first_cached = dict(memory._l0_get("race2"))

    store_fact({"fact_id": "race2", "claim": "second", "source": "s", "confidence": 0.6})
    assert memory._l0_get("race2")["claim"] == "second"

    # Simulate the FIRST call's L0-populate step arriving late — e.g. its
    # thread was preempted right after its DB commit, before reaching
    # _l0_put_if_fresher, and only resumes well after the SECOND call
    # already committed and cached.
    memory._l0_put_if_fresher("race2", first_cached)
    assert memory._l0_get("race2")["claim"] == "second"   # still the fresher one
    assert get_fact("race2")["claim"] == "second"


def test_get_fact_rehydration_does_not_clobber_a_fresher_l0_entry():
    """get_fact()'s L1-rehydration path (core/memory.py) calls
    _l0_put_if_fresher() — a stale L1 read reaching it after a fresher
    record is already cached must not overwrite it. This is a valid use of
    timestamp comparison here specifically because get_fact()'s `record` is
    always a value actually read from a committed row (a true historical
    snapshot), unlike store_fact()'s pre-write `now` (see
    _l0_put_if_fresher()'s docstring and the Codex P1 test below). The value
    get_fact() RETURNS to its caller is unaffected either way (it always
    returns what it just read) — this only protects what ends up cached for
    the NEXT reader."""
    store_fact({"fact_id": "race3", "claim": "fresh", "source": "s", "confidence": 0.5})
    fresh_cached = dict(memory._l0_get("race3"))

    stale_l1_read = {**fresh_cached, "claim": "stale",
                      "updated_at": "2000-01-01T00:00:00+00:00"}
    memory._l0_put_if_fresher("race3", stale_l1_read)
    assert memory._l0_get("race3")["claim"] == "fresh"


def test_store_fact_l0_reflects_actual_l1_winner_not_capture_time_order(monkeypatch):
    """Regression for the Codex P1 finding on #248.

    store_fact() captures `updated_at` BEFORE performing its SQLite write.
    In a real race, a call that captures an EARLIER `now` can still be the
    one whose write actually lands LAST in L1 (e.g. it was scheduled out
    right after capturing `now`, before reaching the write, while a
    second call captured a later `now` but reached the write first). The
    old timestamp-only L0 guard would reject that genuinely-latest call's
    cache update because its `updated_at` looked older than what was
    already cached — exactly backwards. L0 must reflect whichever write
    actually persisted last, never whichever call merely captured the
    latest clock reading.

    Reproduced deterministically (no threads/sleeps needed): mock the clock
    store_fact() reads so call "B" gets a LATER `now` but call "A" — called
    SECOND, so its write is genuinely the last one to commit to L1 — gets an
    EARLIER `now`."""
    from datetime import datetime as real_datetime, timezone
    real_datetime_cls = memory.datetime

    class _FixedClock:
        def __init__(self, fixed):
            self._fixed = fixed
        def now(self, tz=None):
            return self._fixed

    later_clock = real_datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    earlier_clock = real_datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)

    # "B" captures a LATER clock reading and reaches its write + L0-populate
    # first.
    monkeypatch.setattr(memory, "datetime", _FixedClock(later_clock))
    store_fact({"fact_id": "cas_order1", "claim": "B", "source": "s", "confidence": 0.5})
    assert memory._l0_get("cas_order1")["claim"] == "B"

    # "A" captures an EARLIER clock reading, but its write happens SECOND —
    # i.e. it is the actual, true L1 winner (plain last-write-wins upsert),
    # simulating a call that started before B but was delayed reaching the
    # write until after B's had already committed and cached.
    monkeypatch.setattr(memory, "datetime", _FixedClock(earlier_clock))
    store_fact({"fact_id": "cas_order1", "claim": "A", "source": "s", "confidence": 0.5})

    # L0 must reflect A immediately — the call that just genuinely won L1 —
    # even though A's timestamp (11:00) is numerically EARLIER than B's
    # already-cached timestamp (12:00). Under the old timestamp-only guard
    # this assertion fails: A's populate would have been rejected as "stale"
    # and L0 would still show "B".
    assert memory._l0_get("cas_order1")["claim"] == "A"

    # Confirm A really is the persisted L1 winner too (not just an L0
    # artifact): restore the real clock and force a clean L1 read.
    monkeypatch.setattr(memory, "datetime", real_datetime_cls)
    _L0.clear()
    assert get_fact("cas_order1")["claim"] == "A"


def test_store_fact_sequential_behavior_unchanged_by_freshness_guard():
    """The store_fact()-specific lock must not change store_fact()'s normal
    (non-racing) contract: the second call's claim/source/confidence win, and
    epistemic_state/restricted are preserved from the persisted row rather
    than reset — exactly as before this PR."""
    store_fact({"fact_id": "seq1", "claim": "v1", "source": "s1", "confidence": 0.5})
    transition_esm("seq1", "Validated")
    set_restricted("seq1", True)

    store_fact({"fact_id": "seq1", "claim": "v2", "source": "s2", "confidence": 0.8})

    cached = get_fact("seq1")
    assert cached["claim"] == "v2"
    assert cached["source"] == "s2"
    assert cached["confidence"] == 0.8
    assert cached["epistemic_state"] == "Validated"    # preserved, not reset
    assert cached["restricted"] == 1                    # preserved, not reset

    _L0.clear()  # force the L1 read path too
    persisted = get_fact("seq1")
    assert persisted["claim"] == "v2"
    assert persisted["epistemic_state"] == "Validated"
    assert persisted["restricted"] == 1
