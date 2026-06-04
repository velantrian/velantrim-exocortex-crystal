# core/consolidate.py
# Velantrim ExoCortex — SleepCycle (background consolidation)
# v8.7.0-sprint2
#
# Memory physiology: "use it or lose it". reinforce() raises confidence on
# use; consolidate() — a time-based decay on forgetting. The significant
# (significance) is forgotten more slowly. This is the counterpart to reinforce and RFC0017 (FSRS)
# from the ROADMAP.
#
# Decay does not destroy a fact (no Deprecate) — it only lowers confidence, and thus the
# rank in retrieve() (score = similarity × confidence). What is forgotten fades but does not
# disappear; repeated evidence (reinforce) brings it back.
#
# Idempotency: decay is computed from metadata['last_consolidated'] and shifts
# it to now. A repeated run at the same moment → elapsed=0 → no changes.

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from core.memory import get_fact, update_fact
from core.l3_graph import get_l3_graph

_HALF_LIFE_DAYS = 30.0   # confidence half-life period for an insignificant fact
_FLOOR = 0.02            # we do not go below this — a fact fades but does not disappear


def consolidate(
    *,
    now: Optional[datetime] = None,
    half_life_days: float = _HALF_LIFE_DAYS,
    floor: float = _FLOOR,
) -> Dict[str, Any]:
    """
    Run confidence decay over canonical (Validated) L3 facts.
    Effective half-life = half_life_days × (1 + significance): the significant
    holds out longer. Returns {'decayed': n, 'at': iso}.
    """
    now = now or datetime.now(timezone.utc)
    graph = get_l3_graph()
    decayed = 0

    for node in graph.all_facts():
        if node.get("epistemic_state") != "Validated":
            continue
        meta = dict(node.get("metadata") or {})
        baseline = (meta.get("last_consolidated")
                    or node.get("created_at")
                    or node.get("updated_at"))
        if not baseline:
            # A node without a reference timestamp — for example, the canon backend does not
            # persist created_at as a column (LadybugDB stores only _COLS,
            # see l3_graph.LadybugL3Graph._COLS). Previously such a node was skipped
            # FOREVER → decay never ran on it at all. Instead we start
            # the decay clock from the current moment: the mark goes into metadata (which
            # ALL backends persist — mock / ladybug / neo4j), and on the next
            # run baseline will already be found. We do not apply decay this time —
            # the node's age is unknown, the count honestly starts "now".
            meta["last_consolidated"] = now.isoformat()
            if update_fact(node["fact_id"], metadata=meta):
                graph.merge_fact(get_fact(node["fact_id"]))
            continue
        try:
            last = datetime.fromisoformat(baseline)
        except (ValueError, TypeError):
            continue

        elapsed_days = (now - last).total_seconds() / 86400.0
        if elapsed_days <= 0.0:
            continue  # already consolidated at this moment — idempotent

        sig = float(node.get("significance", 0.5))
        eff_hl = half_life_days * (1.0 + sig)
        factor = 0.5 ** (elapsed_days / eff_hl)
        conf = float(node.get("confidence", 0.5))
        new_conf = max(floor, round(conf * factor, 4))

        meta["last_consolidated"] = now.isoformat()
        update_fact(node["fact_id"], confidence=new_conf, metadata=meta)
        graph.merge_fact(get_fact(node["fact_id"]))
        if new_conf < conf:
            decayed += 1

    return {"decayed": decayed, "at": now.isoformat()}
