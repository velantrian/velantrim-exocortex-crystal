# core/velum.py
# Velantrim ExoCortex — L1.5 Velum, the Synaptic Pre-Graph (RFC0016)
# v8.20.0-sprint3
#
# Velum sits between L1 (episodes) and L3 (the canon). It is the synaptic
# pre-graph: it *notices which entities keep appearing together* and strengthens a
# lightweight, in-memory edge between them — the analogue of LTP (long-term
# potentiation), synaptic strengthening that PRECEDES long-term consolidation.
#
# Crucial boundary (RFC0016 invariants):
#   I1: Velum stores ONLY edges (entity_a, entity_b, weight) — never episode
#       content. It observes a *connection*, not a fact.
#   I3: Velum is NOT a source of facts. Graph = Truth is untouched — Velum only
#       emits hints (VelumSignals) for schedulers/retrieval; nothing it produces
#       enters the canon except, later, through the TruthGate elsewhere.
#   I4: Velum is in-memory and not persistent across sessions by default.
#
# A co-occurrence bumps a pair's weight by PROMOTE_WEIGHT/CO_OCCUR_THRESHOLD, so a
# pair reaches the promotion weight exactly when it has co-occurred enough times;
# crossing the threshold emits a VelumSignal. On session end strong edges signal
# and weak edges decay. A _degree_cache gives O(1) "how connected is this entity".

import os
from collections import deque
from itertools import combinations
from typing import Dict, List, Tuple, Optional, Any

# ─── Configuration (RFC0016 defaults; env-overridable) ────────────────────────
_ENV_WINDOW = "VELANTRIM_VELUM_WINDOW"               # observation window (episodes)
_ENV_COOCCUR = "VELANTRIM_VELUM_COOCCUR"             # co-occurrences to record/signal
_ENV_PROMOTE = "VELANTRIM_VELUM_PROMOTE_WEIGHT"      # weight → L2/hint signal
_ENV_MAX_EDGES = "VELANTRIM_VELUM_MAX_EDGES"         # GC ceiling
_ENV_DECAY = "VELANTRIM_VELUM_DECAY"                 # fraction decayed per session


def _envi(name: str, default: int) -> int:
    try:
        return max(1, int(os.environ.get(name, default)))
    except ValueError:
        return default


def _envf(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


def _window() -> int: return _envi(_ENV_WINDOW, 5)
def _cooccur() -> int: return _envi(_ENV_COOCCUR, 3)
def _promote() -> float: return _envf(_ENV_PROMOTE, 0.6)
def _max_edges() -> int: return _envi(_ENV_MAX_EDGES, 1000)
def _decay() -> float: return _envf(_ENV_DECAY, 0.3)


def _increment() -> float:
    """Weight gained per co-occurrence — calibrated so `cooccur` co-occurrences
    reach exactly the promotion weight."""
    return _promote() / _cooccur()


def _key(a: str, b: str) -> Tuple[str, str]:
    return (a, b) if a <= b else (b, a)


class Velum:
    """In-memory synaptic pre-graph over entities (RFC0016)."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._edges: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self._degree: Dict[str, int] = {}          # entity → number of edges (cache)
        self._signaled: set = set()                # pairs already promoted this session
        self._window: deque = deque(maxlen=_window())
        self.signals_emitted = 0

    # ─── Observation ──────────────────────────────────────────────────────────
    def observe_episode(self, episode_id: str, entities: List[str]) -> List[Dict[str, Any]]:
        """
        Called when entities co-occur (e.g. facts recalled together). Strengthens
        the edge for every entity pair; returns a VelumSignal for each pair that
        crosses the promotion threshold for the first time this session.
        """
        ents = sorted({e for e in entities if e})
        self._window.append((episode_id, ents))
        cooccur, promote, inc = _cooccur(), _promote(), _increment()
        signals: List[Dict[str, Any]] = []
        for a, b in combinations(ents, 2):
            key = _key(a, b)
            edge = self._edges.get(key)
            if edge is None:
                edge = {"count": 0, "weight": 0.0}
                self._edges[key] = edge
                self._degree[a] = self._degree.get(a, 0) + 1
                self._degree[b] = self._degree.get(b, 0) + 1
            edge["count"] += 1
            edge["weight"] = min(1.0, round(edge["count"] * inc, 4))
            if (edge["count"] >= cooccur and edge["weight"] >= promote
                    and key not in self._signaled):
                self._signaled.add(key)
                self.signals_emitted += 1
                signals.append({"pair": key, "weight": edge["weight"],
                                "count": edge["count"], "kind": "THRESHOLD"})
        self._gc()
        return signals

    # ─── Session boundary ───────────────────────────────────────────────────────
    def on_session_end(self) -> List[Dict[str, Any]]:
        """
        On a session change: strong edges (weight ≥ promote) emit a SESSION_END
        signal (hint for accelerated promotion); weak edges decay by DECAY. Edges
        that fade to ~0 are pruned. Clears the window and the per-session signal set.
        """
        promote, decay = _promote(), _decay()
        signals: List[Dict[str, Any]] = []
        for key, edge in list(self._edges.items()):
            if edge["weight"] >= promote:
                signals.append({"pair": key, "weight": edge["weight"],
                                "count": edge["count"], "kind": "SESSION_END"})
            else:
                edge["weight"] = round(edge["weight"] * (1.0 - decay), 4)
                if edge["weight"] < 1e-6:
                    self._remove(key)
        self._window.clear()
        self._signaled.clear()
        return signals

    # ─── Queries ────────────────────────────────────────────────────────────────
    def get_neighbors(self, entity: str, min_weight: float = 0.3) -> List[Tuple[str, float]]:
        """Entities synaptically connected to `entity` at weight ≥ min_weight,
        strongest first. The Fast-Path context hint (fire-and-forget)."""
        out: List[Tuple[str, float]] = []
        for (a, b), edge in self._edges.items():
            if edge["weight"] < min_weight:
                continue
            if a == entity:
                out.append((b, edge["weight"]))
            elif b == entity:
                out.append((a, edge["weight"]))
        out.sort(key=lambda nb: (-nb[1], nb[0]))
        return out

    def degree(self, entity: str) -> int:
        """O(1) synaptic degree of an entity (number of edges) — _degree_cache."""
        return self._degree.get(entity, 0)

    def report(self) -> Dict[str, Any]:
        promote = _promote()
        strong = sum(1 for e in self._edges.values() if e["weight"] >= promote)
        top = sorted(
            ({"pair": list(k), "weight": e["weight"], "count": e["count"]}
             for k, e in self._edges.items()),
            key=lambda d: (-d["weight"], d["pair"]))[:5]
        return {
            "edges": len(self._edges),
            "entities": len(self._degree),
            "strong_edges": strong,
            "signals_emitted": self.signals_emitted,
            "max_edges": _max_edges(),
            "top_edges": top,
        }

    # ─── Internals ────────────────────────────────────────────────────────────
    def _remove(self, key: Tuple[str, str]) -> None:
        if key not in self._edges:
            return
        del self._edges[key]
        self._signaled.discard(key)
        for ent in key:
            d = self._degree.get(ent, 0) - 1
            if d <= 0:
                self._degree.pop(ent, None)
            else:
                self._degree[ent] = d

    def _gc(self) -> None:
        """When edges exceed the ceiling, drop the weakest 25% (RFC0016 GC)."""
        cap = _max_edges()
        if len(self._edges) <= cap:
            return
        ordered = sorted(self._edges.items(), key=lambda kv: (kv[1]["weight"], kv[0]))
        for key, _edge in ordered[: max(1, len(self._edges) // 4)]:
            self._remove(key)


# ─── Process-wide singleton (in-memory, resettable for tests) ─────────────────
_INSTANCE: Optional[Velum] = None


def get_velum() -> Velum:
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = Velum()
    return _INSTANCE


def reset_velum() -> None:
    """Reset the singleton (new session / tests)."""
    global _INSTANCE
    _INSTANCE = None
