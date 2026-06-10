"""Tests for core/retrieval_config.py — bounded, audited retrieval knobs."""
import json

import pytest

from core import audit
from core.cli import main
from core.retrieval_config import (
    DEFAULTS, RetrievalConfig, get_retrieval_config, load_config,
    reset_retrieval_config, save_config,
)


# ─── Defaults / backwards compatibility ───────────────────────────────────────

def test_defaults_match_historical_constants():
    assert DEFAULTS.k == 3
    assert DEFAULTS.min_similarity == 0.05
    assert DEFAULTS.graph_walk_hops == 2
    assert DEFAULTS.graph_walk_decay == 0.5
    assert DEFAULTS.significance_weight == 0.5
    assert DEFAULTS.source == "default"


def test_singleton_without_env_returns_defaults():
    assert get_retrieval_config() is DEFAULTS
    assert get_retrieval_config() is get_retrieval_config()


# ─── Bounded validation (negative tests) ──────────────────────────────────────

@pytest.mark.parametrize("field,value", [
    ("k", 0), ("k", 51), ("k", 2.5),
    ("min_similarity", -0.1), ("min_similarity", 1.1),
    ("graph_walk_hops", -1), ("graph_walk_hops", 6),
    ("graph_walk_decay", -0.1), ("graph_walk_decay", 1.5),
    ("significance_weight", -0.5), ("significance_weight", 2.5),
    ("k", "3"), ("min_similarity", None), ("graph_walk_hops", True),
])
def test_out_of_range_or_wrong_type_raises(field, value):
    with pytest.raises(ValueError, match=field):
        RetrievalConfig(**{field: value})


def test_boundary_values_accepted():
    cfg = RetrievalConfig(k=1, min_similarity=0.0, graph_walk_hops=0,
                          graph_walk_decay=1.0, significance_weight=2.0)
    assert cfg.k == 1 and cfg.significance_weight == 2.0
    cfg = RetrievalConfig(k=50, min_similarity=1.0, graph_walk_hops=5)
    assert cfg.k == 50


def test_invalid_source_raises():
    with pytest.raises(ValueError, match="source"):
        RetrievalConfig(source="downloaded")


def test_unknown_keys_in_file_raise(tmp_path):
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps({"k": 5, "temperature": 0.9}))
    with pytest.raises(ValueError, match="temperature"):
        load_config(str(path))


def test_non_object_json_raises(tmp_path):
    path = tmp_path / "cfg.json"
    path.write_text("[1, 2, 3]")
    with pytest.raises(ValueError, match="object"):
        load_config(str(path))


# ─── Load / save round-trip + audit ───────────────────────────────────────────

def test_save_then_load_round_trip(tmp_path):
    path = str(tmp_path / "cfg.json")
    res = save_config(RetrievalConfig(k=7, min_similarity=0.2), path,
                      source="manual")
    cfg = load_config(path)
    assert cfg.k == 7
    assert cfg.min_similarity == 0.2
    assert cfg.source == "manual"
    assert cfg.saved_at is not None
    assert res["sha256"]


def test_save_audit_event_is_content_free(tmp_path):
    path = str(tmp_path / "cfg.json")
    save_config(RetrievalConfig(k=42), path)
    events = [e for e in audit.audit_log()
              if e["event"] == "retrieval_config_saved"]
    assert len(events) == 1
    detail = events[0]["detail"]
    # Only provenance enters the chain — never knob names or values.
    assert set(detail) == {"sha256", "source", "file"}
    assert len(detail["sha256"]) == 64
    assert detail["source"] == "manual"
    assert detail["file"] == "cfg.json"
    assert audit.verify_audit_log()["ok"] is True


def test_env_var_loads_config_into_singleton(tmp_path, monkeypatch):
    path = str(tmp_path / "cfg.json")
    save_config(RetrievalConfig(k=9), path)
    monkeypatch.setenv("VELANTRIM_RETRIEVAL_CONFIG", path)
    reset_retrieval_config()
    assert get_retrieval_config().k == 9


# ─── Pipeline integration ─────────────────────────────────────────────────────

def test_retrieve_uses_configured_k(tmp_path, monkeypatch):
    from core.ingest import ingest
    from core.pipeline import retrieve
    for name in ("Mercury", "Venus", "Saturn", "Neptune"):
        ingest(f"{name} is a planet orbiting in the sky")
    assert len(retrieve("planet sample sky", k=2)) <= 2
    path = str(tmp_path / "cfg.json")
    save_config(RetrievalConfig(k=1), path)
    monkeypatch.setenv("VELANTRIM_RETRIEVAL_CONFIG", path)
    reset_retrieval_config()
    assert len(retrieve("planet sample sky")) == 1      # config default
    assert len(retrieve("planet sample sky", k=3)) > 1  # explicit k wins


def test_significance_weight_changes_salience(monkeypatch, tmp_path):
    from core.l3_graph import _salience_score
    base = _salience_score(0.5, 1.0)
    assert base == 0.5 * 1.5
    path = str(tmp_path / "cfg.json")
    save_config(RetrievalConfig(significance_weight=2.0), path)
    monkeypatch.setenv("VELANTRIM_RETRIEVAL_CONFIG", path)
    reset_retrieval_config()
    assert _salience_score(0.5, 1.0) == 0.5 * 3.0


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_retrieval_config_show(capsys):
    assert main(["retrieval-config-show"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["k"] == 3
    assert out["_source"] == "default"


def test_cli_retrieval_config_set_round_trip(tmp_path, capsys):
    out_path = str(tmp_path / "cfg.json")
    rc = main(["retrieval-config-set", "k=5", "min_similarity=0.1",
               "--out", out_path])
    assert rc == 0
    captured = capsys.readouterr()
    res = json.loads(captured.out)
    assert res["config"]["k"] == 5
    assert "velantrim eval --gate" in captured.err
    assert load_config(out_path).k == 5


def test_cli_retrieval_config_set_rejects_bad_values(tmp_path, capsys):
    out_path = str(tmp_path / "cfg.json")
    assert main(["retrieval-config-set", "k=999", "--out", out_path]) == 1
    assert "invalid retrieval config" in capsys.readouterr().err
    assert main(["retrieval-config-set", "temperature=1", "--out", out_path]) == 1
    assert main(["retrieval-config-set", "k", "--out", out_path]) == 1
