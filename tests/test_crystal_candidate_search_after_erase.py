"""Synthetic Crystal F-02 B regression: tombstoned facts must not resurface.

Scenario: a fact is stored in L1 and merged into L3, a backup is taken, the
fact is then erased (L1 row deleted, tombstone written to the current L1
``erasure_log``), and the older backup is restored into a separate candidate
L3. The restored L3 still physically contains the erased fact. Canonical query
search must not resolve it while the current L1 holds a tombstone for it.

Four independent pytest functions cover the scenarios for the current-tombstone
guard in ``core.query_pipeline._resolve_canonical_fact``:

1. direct ``search_result()`` negative: a current-L1 tombstoned old fact must
   not be returned against the restored old L3;
2. MCP ``tools/call`` ``search`` negative: the same exclusion via ``_tool_search``;
3. positive control (F-02 A): a full pre-erasure L1/L3 pair remains searchable
   via both direct and MCP;
4. negative control: a non-erased sibling synthetic fact that lives in the same
   restored L3 remains searchable after the guard (the guard is targeted, not a
   blanket filter of the restored database).

Each test writes a JSON diagnostic artifact under its tmp/scratch directory
(returncode, stdout/stderr, returned fact_ids, target_present, fact ids used,
and whether a tombstone for the target exists in the current L1 erasure_log)
before any returncode or presence assertion, so both surfaces stay visible if
one fails. SQLite ``-shm`` is a WAL-index service file: the active-state
snapshots compare its presence and size only, never its bytes.

All data is synthetic. The four scenarios above run in child processes with an
isolated HOME/TMP and storage paths; the pytest parent does not import project
modules for them. One additional in-process unit test
(``test_resolver_returns_none_for_tombstoned_id_without_touching_l3``) executes
the guard's early return directly in the parent so that it is visible to
parent-process coverage, and asserts that no L3 / L1 / trust-snapshot path is
reached when a tombstone is present.
Run from the repository root (or set ``CRYSTAL_REPO_ROOT``); the test does not
clone or fetch anything.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any
from unittest import mock

import pytest


F02_OLD_FACT_ID = "synthetic.crystal.f02.erased.v1"
F02_OLD_CLAIM = "Synthetic-only: the cobalt ceramic sample is marked viperquartz."
F02_OLD_QUERY = "cobalt ceramic viperquartz"
F02_CONTROL_FACT_ID = "synthetic.crystal.f02.control.v1"
F02_CONTROL_CLAIM = "Synthetic-only: the amber glass sample is marked amberquartz."
F02_CONTROL_QUERY = "amber glass amberquartz"


_PREPARE_SCENARIO = textwrap.dedent(
    r"""
    import hashlib
    import json
    import os
    import sqlite3
    from pathlib import Path

    from core import l3_graph, memory, storage_backup
    from core.erasure import erase_fact, is_erased

    root = Path(os.environ["CRYSTAL_TEST_ROOT"]).resolve()
    active_l1 = Path(os.environ["VELANTRIM_DB"]).resolve()
    active_l3 = Path(os.environ["VELANTRIM_L3_PATH"]).resolve()
    active_profile = Path(os.environ["VELANTRIM_STORAGE_PROFILE_PATH"]).resolve()
    candidate_l1 = root / "candidate-l1.sqlite3"
    bundle = root / "synthetic-pre-erasure-backup"
    case = os.environ["CRYSTAL_F02_CASE"]
    old_id = os.environ["F02_OLD_FACT_ID"]
    old_claim = os.environ["F02_OLD_CLAIM"]
    control_id = os.environ["F02_CONTROL_FACT_ID"]
    control_claim = os.environ["F02_CONTROL_CLAIM"]

    def write_profile(path: Path, locator: Path) -> None:
        configuration = {"path": str(locator.resolve())}
        canonical = json.dumps(
            {"backend": "sqlite", "configuration": configuration},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        payload = {
            "schema_version": 1,
            "profile": "l3",
            "backend": "sqlite",
            "durable": True,
            "configuration": configuration,
            "locator_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

    write_profile(active_profile, active_l3)
    graph = l3_graph.get_l3_graph()

    def store_synthetic_fact(fact_id: str, claim: str) -> None:
        memory.store_fact({
            "fact_id": fact_id,
            "claim": claim,
            "source": "synthetic://crystal/f02-candidate-search",
            "confidence": 0.9,
            "epistemic_state": "Validated",
        })
        fact = memory.get_fact(fact_id)
        assert fact is not None
        graph.merge_fact(fact)
        assert graph.get_fact(fact_id) is not None

    store_synthetic_fact(old_id, old_claim)
    if case in {"B", "B-sibling"}:
        # Sibling is written to the same L3 before the pre-erasure backup, so
        # the restored candidate L3 contains both old_id and control_id.
        store_synthetic_fact(control_id, control_claim)
    elif case != "A":
        raise AssertionError(f"unknown F-02 case: {case!r}")

    backup = storage_backup.create_backup(bundle, profile_path=active_profile)
    assert backup["status"] == "PASS"
    assert storage_backup.verify_backup(bundle)["status"] == "PASS"

    if case == "A":
        # Candidate L1 will pair with restored candidate L3 to form the full
        # pre-erasure snapshot; active files remain a separate synthetic store.
        candidate_l1.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(active_l1)) as source:
            with sqlite3.connect(str(candidate_l1)) as target:
                source.backup(target)
    else:
        erased = erase_fact(old_id, reason="synthetic_test", actor="pytest")
        assert erased["erased_now"] is True
        assert is_erased(old_id) is True
        assert memory.get_fact(old_id) is None
        assert graph.get_fact(old_id) is None
        assert memory.get_fact(control_id) is not None
        assert is_erased(control_id) is False

    # Setup and all intentional active-store writes/erasure are complete before
    # the parent takes its pre-restore snapshot and starts the restore child.
    """
)


_RESTORE_SCENARIO = textwrap.dedent(
    r"""
    import json
    import os
    from pathlib import Path

    from core import storage_restore

    root = Path(os.environ["CRYSTAL_TEST_ROOT"]).resolve()
    active_profile = Path(os.environ["VELANTRIM_STORAGE_PROFILE_PATH"]).resolve()
    candidate_l3 = root / "candidate-l3.sqlite3"
    candidate_profile = root / "candidate-profile.json"
    bundle = root / "synthetic-pre-erasure-backup"
    receipt = root / "candidate-restore-receipt.json"

    restored = storage_restore.restore_backup(
        bundle,
        target_database=candidate_l3,
        target_profile=candidate_profile,
        receipt_path=receipt,
    )
    assert restored["status"] == "PASS"
    candidate_profile_payload = json.loads(candidate_profile.read_text(encoding="utf-8"))
    assert candidate_profile_payload["profile"] == "l3"
    assert candidate_profile_payload["configuration"]["path"] == str(candidate_l3.resolve())
    assert os.environ["VELANTRIM_STORAGE_PROFILE_PATH"] == str(active_profile)
    assert candidate_profile.resolve() != active_profile.resolve()
    """
)


_DIRECT_SEARCH_SCENARIO = textwrap.dedent(
    r"""
    import json
    import os
    from pathlib import Path

    profile_path = Path(os.environ["VELANTRIM_STORAGE_PROFILE_PATH"]).resolve()
    candidate_l3 = Path(os.environ["VELANTRIM_L3_PATH"]).resolve()
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    assert profile["configuration"]["path"] == str(candidate_l3)
    assert Path(profile["configuration"]["path"]).resolve() == candidate_l3
    assert os.environ["VELANTRIM_L3_BACKEND"] == "sqlite"

    artifact_path = Path(os.environ["CRYSTAL_F02_ARTIFACT"])
    target_id = os.environ["F02_TARGET_FACT_ID"]
    query = os.environ["F02_SEARCH_QUERY"]
    expect = os.environ["F02_EXPECT"]
    old_id = os.environ["F02_OLD_FACT_ID"]
    sibling_id = os.environ["F02_CONTROL_FACT_ID"]
    payload = {
        "surface": "direct",
        "case": os.environ["CRYSTAL_F02_CASE"],
        "target_id": target_id,
        "old_fact_id": old_id,
        "sibling_fact_id": sibling_id,
        "query": query,
        "expect": expect,
        "returned_fact_ids": None,
        "target_present": None,
        "old_id_present": None,
        "sibling_id_present": None,
        "result_count": None,
        "error": None,
        "k": 10,
    }
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from core.query_pipeline import search_result

        def search(query: str) -> dict:
            return search_result(query, k=10)

        results = search(query)["results"]
        fact_ids = [row.get("fact_id") for row in results]
        payload["returned_fact_ids"] = fact_ids
        payload["target_present"] = target_id in fact_ids
        payload["old_id_present"] = old_id in fact_ids
        payload["sibling_id_present"] = sibling_id in fact_ids
        payload["result_count"] = len(fact_ids)
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        artifact_path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    if expect == "present":
        assert payload["target_present"] is True, "expected target fact to be searchable via search_result()"
    elif expect == "absent":
        assert payload["target_present"] is False, "current L1 tombstone must exclude the target fact"
    else:
        raise AssertionError(f"unknown F02_EXPECT: {expect!r}")
    """
)


_MCP_SEARCH_SCENARIO = textwrap.dedent(
    r"""
    import json
    import os
    from pathlib import Path

    profile_path = Path(os.environ["VELANTRIM_STORAGE_PROFILE_PATH"]).resolve()
    candidate_l3 = Path(os.environ["VELANTRIM_L3_PATH"]).resolve()
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    assert profile["configuration"]["path"] == str(candidate_l3)
    assert Path(profile["configuration"]["path"]).resolve() == candidate_l3
    assert os.environ["VELANTRIM_L3_BACKEND"] == "sqlite"

    artifact_path = Path(os.environ["CRYSTAL_F02_ARTIFACT"])
    target_id = os.environ["F02_TARGET_FACT_ID"]
    query = os.environ["F02_SEARCH_QUERY"]
    expect = os.environ["F02_EXPECT"]
    old_id = os.environ["F02_OLD_FACT_ID"]
    sibling_id = os.environ["F02_CONTROL_FACT_ID"]
    payload = {
        "surface": "mcp",
        "case": os.environ["CRYSTAL_F02_CASE"],
        "target_id": target_id,
        "old_fact_id": old_id,
        "sibling_fact_id": sibling_id,
        "query": query,
        "expect": expect,
        "returned_fact_ids": None,
        "target_present": None,
        "old_id_present": None,
        "sibling_id_present": None,
        "result_count": None,
        "mcp_is_error": None,
        "error": None,
        "k": 10,
    }
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from core import mcp_server

        def search(query: str) -> dict:
            response = mcp_server.handle_message({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "search", "arguments": {"query": query, "k": 10}},
            })
            assert response is not None
            result = response["result"]
            payload["mcp_is_error"] = result.get("isError")
            if result["isError"] is not False:
                raise AssertionError(f"MCP search returned isError: {result}")
            return json.loads(result["content"][0]["text"])

        results = search(query)["results"]
        fact_ids = [row.get("fact_id") for row in results]
        payload["returned_fact_ids"] = fact_ids
        payload["target_present"] = target_id in fact_ids
        payload["old_id_present"] = old_id in fact_ids
        payload["sibling_id_present"] = sibling_id in fact_ids
        payload["result_count"] = len(fact_ids)
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        artifact_path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    if expect == "present":
        assert payload["target_present"] is True, "expected target fact to be searchable via MCP search"
    elif expect == "absent":
        assert payload["target_present"] is False, "current L1 tombstone must exclude the target fact via MCP search"
    else:
        raise AssertionError(f"unknown F02_EXPECT: {expect!r}")
    """
)



_TOMBSTONE_PROBE_SCENARIO = textwrap.dedent(
    r"""
    import json
    import os
    from pathlib import Path

    from core.erasure import is_erased
    from core.memory import get_tombstone

    artifact_path = Path(os.environ["CRYSTAL_F02_TOMBSTONE_ARTIFACT"])
    old_id = os.environ["F02_OLD_FACT_ID"]
    sibling_id = os.environ["F02_CONTROL_FACT_ID"]
    target_id = os.environ["F02_TARGET_FACT_ID"]
    l1_path = Path(os.environ["VELANTRIM_DB"]).resolve()
    label = os.environ["CRYSTAL_F02_L1_LABEL"]

    def record(fact_id: str) -> dict:
        tombstone = get_tombstone(fact_id)
        present = tombstone is not None
        erased = is_erased(fact_id)
        body = None
        if tombstone is not None:
            body = {
                "fact_id": tombstone.get("fact_id"),
                "erased_at": tombstone.get("erased_at"),
                "reason": tombstone.get("reason"),
                "actor": tombstone.get("actor"),
                "content_hash": tombstone.get("content_hash"),
            }
        return {
            "fact_id": fact_id,
            "is_erased": erased,
            "tombstone_present": present,
            "tombstone": body,
        }

    payload = {
        "source": "core.erasure.is_erased + core.memory.get_tombstone",
        "l1_label": label,
        "l1_path": str(l1_path),
        "old_fact_id": old_id,
        "sibling_fact_id": sibling_id,
        "target_fact_id": target_id,
        "old": record(old_id),
        "sibling": record(sibling_id),
        "target": record(target_id),
        "target_tombstone_present": record(target_id)["tombstone_present"],
    }
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
    """
)


def _child_environment(
    repo_root: Path,
    root: Path,
    label: str,
    *,
    case: str,
    l1_path: Path,
    l3_path: Path,
    profile_path: Path,
    extra_env: dict[str, str] | None = None,
) -> tuple[dict[str, str], Path]:
    process_root = root / label
    home = process_root / "home"
    work = process_root / "work"
    temp = process_root / "tmp"
    for directory in (home, work, temp):
        directory.mkdir(parents=True, exist_ok=True)

    env = {
        name: os.environ[name]
        for name in ("PATH", "SYSTEMROOT", "WINDIR")
        if name in os.environ
    }
    env.update({
        "HOME": str(home),
        "USERPROFILE": str(home),
        "TMPDIR": str(temp),
        "TEMP": str(temp),
        "TMP": str(temp),
        "PYTHONPATH": str(repo_root),
        "PYTHONDONTWRITEBYTECODE": "1",
        "CRYSTAL_TEST_ROOT": str(root),
        "CRYSTAL_F02_CASE": case,
        "CRYSTAL_REPO_ROOT": str(repo_root),
        "VELANTRIM_DB": str(l1_path),
        "VELANTRIM_L3_BACKEND": "sqlite",
        "VELANTRIM_L3_PATH": str(l3_path),
        "VELANTRIM_STORAGE_PROFILE_PATH": str(profile_path),
        "VELANTRIM_EMBEDDER": "hashing",
        "VELANTRIM_GENERATOR": "extractive",
        "VELANTRIM_QUEUE_BACKEND": "sqlite",
        "VELANTRIM_DEMO_SEED": "0",
        "F02_OLD_FACT_ID": F02_OLD_FACT_ID,
        "F02_OLD_CLAIM": F02_OLD_CLAIM,
        "F02_OLD_QUERY": F02_OLD_QUERY,
        "F02_CONTROL_FACT_ID": F02_CONTROL_FACT_ID,
        "F02_CONTROL_CLAIM": F02_CONTROL_CLAIM,
        "F02_CONTROL_QUERY": F02_CONTROL_QUERY,
    })
    if extra_env:
        env.update(extra_env)
    return env, work


def _run_child(
    repo_root: Path,
    root: Path,
    label: str,
    scenario: str,
    *,
    case: str,
    l1_path: Path,
    l3_path: Path,
    profile_path: Path,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env, work = _child_environment(
        repo_root,
        root,
        label,
        case=case,
        l1_path=l1_path,
        l3_path=l3_path,
        profile_path=profile_path,
        extra_env=extra_env,
    )
    return subprocess.run(
        [sys.executable, "-c", scenario],
        cwd=work,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


def _sqlite_files_snapshot(database: Path) -> dict[str, object]:
    # Durable comparison: main and -wal bytes; -journal presence/bytes.
    # -shm is a WAL-index service file: presence and size only, never bytes.
    snapshot: dict[str, object] = {}
    main = Path(str(database))
    snapshot["main"] = main.read_bytes() if main.exists() else None
    wal = Path(str(database) + "-wal")
    snapshot["-wal"] = wal.read_bytes() if wal.exists() else None
    journal = Path(str(database) + "-journal")
    snapshot["-journal_present"] = journal.exists()
    snapshot["-journal"] = journal.read_bytes() if journal.exists() else None
    shm = Path(str(database) + "-shm")
    snapshot["-shm_present"] = shm.exists()
    snapshot["-shm_size"] = shm.stat().st_size if shm.exists() else None
    return snapshot


def _active_state_snapshot(root: Path) -> dict[str, object]:
    active_profile = root / "active-profile.json"
    active_l1 = root / "active-l1.sqlite3"
    active_l3 = root / "active-l3.sqlite3"
    return {
        "profile": active_profile.read_bytes(),
        "l1_and_sidecars": _sqlite_files_snapshot(active_l1),
        "l3_and_sidecars": _sqlite_files_snapshot(active_l3),
    }


def _candidate_l3_has_fact(candidate_l3: Path, fact_id: str) -> bool:
    if not candidate_l3.is_file():
        return False
    uri = candidate_l3.resolve().as_uri() + "?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        row = connection.execute(
            "SELECT data FROM nodes WHERE fact_id = ?", (fact_id,)
        ).fetchone()
    return row is not None


def _prepare_and_restore(tmp_path: Path, *, case: str) -> dict[str, Any]:
    repo_root = Path(os.environ.get("CRYSTAL_REPO_ROOT", Path.cwd())).resolve()
    assert (repo_root / "core" / "query_pipeline.py").is_file(), (
        "Run from the Crystal repository root, or set CRYSTAL_REPO_ROOT; "
        "this test does not clone or fetch."
    )

    root = (tmp_path / f"synthetic-crystal-f02-{case.lower()}").resolve()
    root.mkdir(parents=True)
    active_l1 = root / "active-l1.sqlite3"
    active_l3 = root / "active-l3.sqlite3"
    active_profile = root / "active-profile.json"
    candidate_l1 = root / "candidate-l1.sqlite3"
    candidate_l3 = root / "candidate-l3.sqlite3"
    candidate_profile = root / "candidate-profile.json"

    setup = _run_child(
        repo_root,
        root,
        "setup-process",
        _PREPARE_SCENARIO,
        case=case,
        l1_path=active_l1,
        l3_path=active_l3,
        profile_path=active_profile,
    )
    assert setup.returncode == 0, (
        "Synthetic F-02 setup child failed.\n"
        f"stdout:\n{setup.stdout}\nstderr:\n{setup.stderr}"
    )

    active_profile_payload = json.loads(active_profile.read_text(encoding="utf-8"))
    assert active_profile_payload["configuration"]["path"] == str(active_l3.resolve())

    # All intended synthetic writes/erasure are complete. This parent-side
    # snapshot is the exact active-state boundary immediately before restore.
    before_restore = _active_state_snapshot(root)
    restore = _run_child(
        repo_root,
        root,
        "restore-process",
        _RESTORE_SCENARIO,
        case=case,
        l1_path=active_l1,
        l3_path=active_l3,
        profile_path=active_profile,
    )
    after_restore = _active_state_snapshot(root)
    assert before_restore == after_restore, (
        "candidate restore changed active profile or active L1/L3 files/sidecars"
    )
    assert restore.returncode == 0, (
        "Synthetic candidate restore child failed.\n"
        f"stdout:\n{restore.stdout}\nstderr:\n{restore.stderr}"
    )

    search_l1 = candidate_l1 if case == "A" else active_l1
    return {
        "repo_root": repo_root,
        "root": root,
        "case": case,
        "search_l1": search_l1,
        "candidate_l3": candidate_l3,
        "candidate_profile": candidate_profile,
        "active_l1": active_l1,
        "active_l3": active_l3,
        "active_profile": active_profile,
    }


def _run_bound_search(
    ctx: dict[str, Any],
    *,
    surface: str,
    label: str,
    target_id: str,
    query: str,
    expect: str,
    artifact_path: Path,
) -> dict[str, Any]:
    # Do not assert here: the caller persists diagnostics in a finally block
    # first, then checks returncode, target_present, and active-state equality.
    scenario = _DIRECT_SEARCH_SCENARIO if surface == "direct" else _MCP_SEARCH_SCENARIO
    before_search = _active_state_snapshot(ctx["root"])
    result = _run_child(
        ctx["repo_root"],
        ctx["root"],
        label,
        scenario,
        case=ctx["case"],
        l1_path=ctx["search_l1"],
        l3_path=ctx["candidate_l3"],
        profile_path=ctx["candidate_profile"],
        extra_env={
            "CRYSTAL_F02_ARTIFACT": str(artifact_path),
            "F02_TARGET_FACT_ID": target_id,
            "F02_SEARCH_QUERY": query,
            "F02_EXPECT": expect,
        },
    )
    after_search = _active_state_snapshot(ctx["root"])
    return {
        "proc": result,
        "artifact_path": artifact_path,
        "surface": surface,
        "active_state_unchanged": before_search == after_search,
    }


def _erasure_log_from_copied_l1(l1: Path, scratch: Path, fact_ids: list[str]) -> dict[str, Any]:
    # Parent-side corroboration: stdlib only, never imports project modules.
    # Copies L1 + sidecars and opens the copy read-only.
    report: dict[str, Any] = {
        "source": "stdlib sqlite3 read-only copy of L1 erasure_log",
        "l1_path": str(l1),
        "opened": False,
        "error": None,
        "rows": {},
    }
    if not l1.is_file():
        report["error"] = "missing_l1"
        return report
    dest_dir = scratch / f"l1-copy-{l1.name}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("", "-wal", "-shm", "-journal"):
        src_path = Path(str(l1) + suffix)
        if src_path.exists() and src_path.is_file():
            shutil.copy2(src_path, dest_dir / src_path.name)
    copy = dest_dir / l1.name
    try:
        uri = copy.resolve().as_uri() + "?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            connection.row_factory = sqlite3.Row
            present = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            report["tables"] = sorted(present)
            if "erasure_log" not in present:
                report["error"] = "no_erasure_log_table"
                report["opened"] = True
                return report
            for fact_id in fact_ids:
                row = connection.execute(
                    "SELECT fact_id, erased_at, reason, actor, content_hash "
                    "FROM erasure_log WHERE fact_id = ?",
                    (fact_id,),
                ).fetchone()
                report["rows"][fact_id] = (
                    None if row is None else {k: row[k] for k in row.keys()}
                )
            report["opened"] = True
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    return report


def _probe_l1_tombstones(
    ctx: dict[str, Any],
    scratch: Path,
    *,
    l1_path: Path,
    label: str,
    target_id: str,
) -> dict[str, Any]:
    artifact = scratch / f"tombstone-probe-{label}.json"
    proc = _run_child(
        ctx["repo_root"],
        ctx["root"],
        f"tombstone-probe-{label}",
        _TOMBSTONE_PROBE_SCENARIO,
        case=ctx["case"],
        l1_path=l1_path,
        l3_path=ctx["candidate_l3"],
        profile_path=ctx["candidate_profile"],
        extra_env={
            "CRYSTAL_F02_TOMBSTONE_ARTIFACT": str(artifact),
            "F02_TARGET_FACT_ID": target_id,
            "CRYSTAL_F02_L1_LABEL": label,
        },
    )
    body: dict[str, Any] = {}
    if artifact.is_file():
        body = json.loads(artifact.read_text(encoding="utf-8"))
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "artifact_written": artifact.is_file(),
        "probe": body,
    }


def _surface_record(
    surface: str,
    proc: subprocess.CompletedProcess[str],
    child_artifact: Path,
) -> dict[str, Any]:
    child: dict[str, Any] = {}
    if child_artifact.is_file():
        child = json.loads(child_artifact.read_text(encoding="utf-8"))
    return {
        "surface": surface,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "returned_fact_ids": child.get("returned_fact_ids"),
        "target_present": child.get("target_present"),
        "target_id": child.get("target_id"),
        "old_fact_id": child.get("old_fact_id"),
        "sibling_fact_id": child.get("sibling_fact_id"),
        "old_id_present": child.get("old_id_present"),
        "sibling_id_present": child.get("sibling_id_present"),
        "query": child.get("query"),
        "expect": child.get("expect"),
        "result_count": child.get("result_count"),
        "error": child.get("error"),
        "k": child.get("k"),
        "child_artifact_written": child_artifact.is_file(),
    }


def _write_diagnostics(
    path: Path,
    *,
    surfaces: dict[str, dict[str, Any]],
    extra: dict[str, Any],
) -> dict[str, Any]:
    document: dict[str, Any] = dict(extra)
    document["surfaces"] = {}
    for name, packed in surfaces.items():
        document["surfaces"][name] = _surface_record(
            name, packed["proc"], packed["artifact_path"]
        )
        document["surfaces"][name]["active_state_unchanged"] = packed.get(
            "active_state_unchanged"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return document


def _assert_search_diagnostics(
    path: Path,
    document: dict[str, Any],
    surfaces: dict[str, dict[str, Any]],
) -> None:
    for name, packed in surfaces.items():
        proc = packed["proc"]
        record = document["surfaces"][name]
        assert packed.get("active_state_unchanged") is True, (
            f"{name} search changed active profile or active L1/L3 files/sidecars; see {path}"
        )
        assert proc.returncode == 0, (
            f"{name} search child failed.\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}\n"
            f"diagnostics: {path}"
        )
        expect = record.get("expect")
        present = record.get("target_present")
        if expect == "present":
            assert present is True, f"{name}: expected target_present true; see {path}"
        elif expect == "absent":
            assert present is False, f"{name}: expected target_present false; see {path}"


def _scenario_extra(ctx: dict[str, Any], scratch: Path, target_id: str) -> dict[str, Any]:
    current_l1 = ctx["active_l1"]
    search_l1 = ctx["search_l1"]
    probe_current = _probe_l1_tombstones(
        ctx, scratch, l1_path=current_l1, label="current_active_l1", target_id=target_id
    )
    probes = {"current_active_l1": probe_current}
    if search_l1.resolve() != current_l1.resolve():
        probes["search_l1"] = _probe_l1_tombstones(
            ctx, scratch, l1_path=search_l1, label="search_l1", target_id=target_id
        )
    fact_ids = [F02_OLD_FACT_ID, F02_CONTROL_FACT_ID, target_id]
    sqlite_current = _erasure_log_from_copied_l1(current_l1, scratch, fact_ids)
    sqlite_search = None
    if search_l1.resolve() != current_l1.resolve():
        sqlite_search = _erasure_log_from_copied_l1(search_l1, scratch, fact_ids)
    current_probe = probe_current.get("probe") or {}
    target_tombstone = current_probe.get("target_tombstone_present")
    if target_tombstone is None and sqlite_current.get("opened"):
        row = (sqlite_current.get("rows") or {}).get(target_id)
        target_tombstone = row is not None
    return {
        "fact_ids_used": {
            "old_erased_id": F02_OLD_FACT_ID,
            "sibling_id": F02_CONTROL_FACT_ID,
            "target_id": target_id,
        },
        "paths": {
            "current_l1": str(current_l1),
            "search_l1": str(search_l1),
            "candidate_l3": str(ctx["candidate_l3"]),
            "case": ctx["case"],
        },
        "tombstone_probes": probes,
        "erasure_log_sqlite_current_l1": sqlite_current,
        "erasure_log_sqlite_search_l1": sqlite_search,
        "target_tombstone_present_in_current_l1": target_tombstone,
    }


def test_direct_search_result_excludes_tombstoned_old_fact(tmp_path: Path) -> None:
    """(1) Direct search_result() must not return a current-L1 tombstoned fact."""
    ctx = _prepare_and_restore(tmp_path, case="B")
    scratch = tmp_path / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    child_artifact = scratch / "direct-search-result.json"
    diag = scratch / "f02-p1-1-direct-search-diagnostics.json"
    surfaces: dict[str, dict[str, Any]] = {}
    extra = _scenario_extra(ctx, scratch, F02_OLD_FACT_ID)
    try:
        surfaces["direct"] = _run_bound_search(
            ctx,
            surface="direct",
            label="direct-search-process",
            target_id=F02_OLD_FACT_ID,
            query=F02_OLD_QUERY,
            expect="absent",
            artifact_path=child_artifact,
        )
    finally:
        document = _write_diagnostics(diag, surfaces=surfaces, extra=extra)
    _assert_search_diagnostics(diag, document, surfaces)


def test_mcp_search_excludes_tombstoned_old_fact(tmp_path: Path) -> None:
    """(2) MCP tools/call search must not return a current-L1 tombstoned fact."""
    ctx = _prepare_and_restore(tmp_path, case="B")
    scratch = tmp_path / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    child_artifact = scratch / "mcp-search-result.json"
    diag = scratch / "f02-p1-2-mcp-search-diagnostics.json"
    surfaces: dict[str, dict[str, Any]] = {}
    extra = _scenario_extra(ctx, scratch, F02_OLD_FACT_ID)
    try:
        surfaces["mcp"] = _run_bound_search(
            ctx,
            surface="mcp",
            label="mcp-search-process",
            target_id=F02_OLD_FACT_ID,
            query=F02_OLD_QUERY,
            expect="absent",
            artifact_path=child_artifact,
        )
    finally:
        document = _write_diagnostics(diag, surfaces=surfaces, extra=extra)
    _assert_search_diagnostics(diag, document, surfaces)


def test_full_pre_erasure_l1_l3_pair_is_searchable_via_direct_and_mcp(
    tmp_path: Path,
) -> None:
    """(3) Positive control: full pre-erasure pair stays searchable on both surfaces."""
    ctx = _prepare_and_restore(tmp_path, case="A")
    scratch = tmp_path / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    direct_artifact = scratch / "direct-search-result.json"
    mcp_artifact = scratch / "mcp-search-result.json"
    diag = scratch / "f02-p1-3-positive-control-diagnostics.json"
    surfaces: dict[str, dict[str, Any]] = {}
    extra = _scenario_extra(ctx, scratch, F02_OLD_FACT_ID)
    try:
        surfaces["direct"] = _run_bound_search(
            ctx,
            surface="direct",
            label="direct-search-process",
            target_id=F02_OLD_FACT_ID,
            query=F02_OLD_QUERY,
            expect="present",
            artifact_path=direct_artifact,
        )
        surfaces["mcp"] = _run_bound_search(
            ctx,
            surface="mcp",
            label="mcp-search-process",
            target_id=F02_OLD_FACT_ID,
            query=F02_OLD_QUERY,
            expect="present",
            artifact_path=mcp_artifact,
        )
    finally:
        document = _write_diagnostics(diag, surfaces=surfaces, extra=extra)
    _assert_search_diagnostics(diag, document, surfaces)


def test_non_erased_sibling_in_restored_l3_remains_searchable(
    tmp_path: Path,
) -> None:
    """(4) Negative control: a non-erased sibling in the same restored L3 stays visible."""
    ctx = _prepare_and_restore(tmp_path, case="B-sibling")
    scratch = tmp_path / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    # Stdlib-only inspection of the restored candidate: the sibling was merged
    # into L3 before the pre-erasure backup and must be physically present
    # there. This proves the search target is in the restored L3, not only in
    # the current active store.
    assert _candidate_l3_has_fact(ctx["candidate_l3"], F02_CONTROL_FACT_ID), (
        "sibling fact must be physically present in the restored candidate L3"
    )
    assert _candidate_l3_has_fact(ctx["candidate_l3"], F02_OLD_FACT_ID), (
        "tombstoned old fact is expected to remain physically present in restored L3"
    )
    direct_artifact = scratch / "direct-search-result.json"
    mcp_artifact = scratch / "mcp-search-result.json"
    diag = scratch / "f02-p1-4-sibling-control-diagnostics.json"
    surfaces: dict[str, dict[str, Any]] = {}
    extra = _scenario_extra(ctx, scratch, F02_CONTROL_FACT_ID)
    extra["candidate_l3_physical"] = {
        "sibling_present": True,
        "old_fact_present": True,
    }
    try:
        surfaces["direct"] = _run_bound_search(
            ctx,
            surface="direct",
            label="direct-search-process",
            target_id=F02_CONTROL_FACT_ID,
            query=F02_CONTROL_QUERY,
            expect="present",
            artifact_path=direct_artifact,
        )
        surfaces["mcp"] = _run_bound_search(
            ctx,
            surface="mcp",
            label="mcp-search-process",
            target_id=F02_CONTROL_FACT_ID,
            query=F02_CONTROL_QUERY,
            expect="present",
            artifact_path=mcp_artifact,
        )
    finally:
        document = _write_diagnostics(diag, surfaces=surfaces, extra=extra)
    _assert_search_diagnostics(diag, document, surfaces)
    # Independent parent-side checks on each surface's persisted result: the
    # erased id must be absent and the non-erased sibling present, for the
    # direct and the MCP search separately.
    for surface in ("direct", "mcp"):
        returned = document["surfaces"][surface]["returned_fact_ids"]
        assert F02_OLD_FACT_ID not in returned, (
            f"{surface}: erased fact {F02_OLD_FACT_ID} must be absent; see {diag}"
        )
        assert F02_CONTROL_FACT_ID in returned, (
            f"{surface}: non-erased sibling {F02_CONTROL_FACT_ID} must be present; see {diag}"
        )


def test_resolver_returns_none_for_tombstoned_id_without_touching_l3() -> None:
    """(5) In-process unit test of the guard's early return.

    With the current-L1 tombstone check returning True for a synthetic id,
    ``_resolve_canonical_fact`` must return None before it touches the L3 graph,
    reads L1, or builds a trust snapshot. Each of those is stubbed so that any
    call raises and is also recorded.
    """
    from core import query_pipeline

    def forbidden(name: str) -> mock.Mock:
        return mock.Mock(side_effect=AssertionError(f"{name} must not be reached"))

    tombstone_check = mock.Mock(return_value=True)
    l3_graph = forbidden("get_l3_graph")
    l1_read = forbidden("get_fact")
    snapshot = forbidden("TrustSnapshot")
    with mock.patch.object(query_pipeline, "is_erased", tombstone_check), \
            mock.patch.object(query_pipeline, "get_l3_graph", l3_graph), \
            mock.patch.object(query_pipeline, "get_fact", l1_read), \
            mock.patch.object(query_pipeline, "TrustSnapshot", snapshot):
        resolved = query_pipeline._resolve_canonical_fact({"fact_id": F02_OLD_FACT_ID})

    assert resolved is None
    tombstone_check.assert_called_once_with(F02_OLD_FACT_ID)
    l3_graph.assert_not_called()
    l1_read.assert_not_called()
    snapshot.assert_not_called()
