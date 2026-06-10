"""Shared pytest fixtures for the Velantrim test suite."""
import os
import sys

import pytest

# Ensure project root (core/, utils/, top-level modules) is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    """Give every test its own SQLite file and a fresh L0 LRU cache.

    core.memory opens a new connection per operation (see _db()), so there is
    no long-lived connection to tear down — we only need to redirect the DB
    path and clear the module-level in-memory cache.
    """
    from core import (memory, l3_graph, embedding, generation, metrics,
                      adaptation, queue, velum, retrieval_config)

    memory._L0.clear()
    velum.reset_velum()
    # Retrieval knobs: every test starts from the historical defaults, never
    # from a config file left in the caller's environment.
    monkeypatch.delenv("VELANTRIM_RETRIEVAL_CONFIG", raising=False)
    retrieval_config.reset_retrieval_config()
    monkeypatch.setattr(memory, "SQLITE_PATH", str(tmp_path / "test.db"))
    # Pin the deterministic, dependency-free backends so tests never load a
    # neural model, touch disk, or hit the network (production defaults differ:
    # L3=auto→LadybugDB, embedder=auto→sbert, generator=extractive,
    # queue=auto→Redis-if-present). The SQLite queue shares the per-test DB.
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "mock")
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    monkeypatch.setenv("VELANTRIM_GENERATOR", "extractive")
    monkeypatch.setenv("VELANTRIM_QUEUE_BACKEND", "sqlite")
    # Issue #65: tests opt-in to the demo seed corpus. The production default
    # is VELANTRIM_DEMO_SEED=0 (empty corpus — all facts must enter via ingest).
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "1")
    # Fresh module-level singletons per test.
    l3_graph.reset_l3_graph()
    embedding.reset_embedder()
    generation.reset_generator()
    queue.reset_outbox_queue()
    velum.reset_velum()
    metrics.reset()
    adaptation.reset_adaptation()
    yield
    memory._L0.clear()
    l3_graph.reset_l3_graph()
    embedding.reset_embedder()
    generation.reset_generator()
    queue.reset_outbox_queue()
    velum.reset_velum()
    retrieval_config.reset_retrieval_config()
