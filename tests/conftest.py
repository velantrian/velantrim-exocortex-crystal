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
    from core import memory, l3_graph, embedding, generation

    memory._L0.clear()
    monkeypatch.setattr(memory, "SQLITE_PATH", str(tmp_path / "test.db"))
    # Pin the deterministic, dependency-free backends so tests never load a
    # neural model, touch disk, or hit the network (production defaults differ:
    # L3=auto→LadybugDB, embedder=auto→sbert, generator=extractive).
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "mock")
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    monkeypatch.setenv("VELANTRIM_GENERATOR", "extractive")
    # Fresh module-level singletons per test.
    l3_graph.reset_l3_graph()
    embedding.reset_embedder()
    generation.reset_generator()
    yield
    memory._L0.clear()
    l3_graph.reset_l3_graph()
    embedding.reset_embedder()
    generation.reset_generator()
