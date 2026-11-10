"""Regression: issue #505, process-local L0 after erasure in another process.

The pytest process owns the long-lived L0; a separate Python interpreter
performs the deletion against the SAME SQLite database. This exercises actual
public memory/erasure functions rather than a mock of the L0 helpers.
"""

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from core import memory


_DELETE_IN_OTHER_PROCESS = """
import json
import sys

from core.erasure import erase_fact
from core.memory import delete_fact_l1, get_tombstone

mode, fact_id = sys.argv[1:]
if mode == "erase":
    first = erase_fact(fact_id, reason="first", actor="test")
    second = erase_fact(fact_id, reason="repeat", actor="test")
    tombstone = get_tombstone(fact_id)
    result = {
        "l1_removed": first["l1_removed"],
        "erased_now": first["erased_now"],
        "repeat_erased_now": second["erased_now"],
        "same_tombstone": (
            second["erased_at"] == first["erased_at"]
            and second["content_hash"] == first["content_hash"]
            and tombstone["reason"] == "first"
        ),
    }
else:
    result = {
        "l1_removed": delete_fact_l1(fact_id),
        "tombstone": get_tombstone(fact_id) is not None,
    }
print(json.dumps(result))
"""


def _delete_in_other_process(mode: str, fact_id: str) -> dict:
    env = dict(os.environ)
    env.update({
        "VELANTRIM_DB": str(memory.SQLITE_PATH),
        "VELANTRIM_L3_BACKEND": "mock",
        "VELANTRIM_EMBEDDER": "hashing",
        "VELANTRIM_QUEUE_BACKEND": "sqlite",
        "VELANTRIM_DEMO_SEED": "0",
    })
    completed = subprocess.run(
        [sys.executable, "-c", _DELETE_IN_OTHER_PROCESS, mode, fact_id],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    return json.loads(completed.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("mode", ["erase", "direct_delete"])
def test_second_process_deletion_invalidates_first_process_l0(mode):
    fact_id = "issue-505"
    memory.store_fact({
        "fact_id": fact_id,
        "claim": "ephemeral personal data for an isolated test",
        "source": "test",
    })
    assert memory.get_fact(fact_id) is not None
    assert fact_id in memory._L0

    # The deletion occurs in another interpreter and cannot call _l0_pop here.
    result = _delete_in_other_process(mode, fact_id)
    assert result["l1_removed"] is True
    if mode == "erase":
        assert result["erased_now"] is True
        assert result["repeat_erased_now"] is False
        assert result["same_tombstone"] is True
        assert memory.get_tombstone(fact_id) is not None
    else:
        assert result["tombstone"] is False

    # Two reads AFTER the second process exits may neither return nor re-cache it.
    assert memory.get_fact(fact_id) is None
    assert memory.get_fact(fact_id) is None
    assert fact_id not in memory._L0
    with sqlite3.connect(memory.SQLITE_PATH) as conn:
        assert conn.execute(
            "SELECT 1 FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone() is None


def test_tombstone_prevents_return_and_rehydration_even_if_l1_row_lingers():
    fact_id = "issue-505-partial"
    memory.store_fact({"fact_id": fact_id, "claim": "test", "source": "test"})
    memory.write_tombstone(fact_id, reason="partial_erasure", actor="test")

    # A tombstone suppresses a cached row from a partial/out-of-order erase.
    assert memory.get_fact(fact_id) is None
    assert fact_id not in memory._L0

    # An L0 miss also must not rehydrate a tombstoned row from L1.
    assert memory.get_fact(fact_id) is None
    assert fact_id not in memory._L0
