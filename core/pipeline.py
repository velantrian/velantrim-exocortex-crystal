# core/pipeline.py
# Velantrim ExoCortex — Core Pipeline
#
# Principle: Graph = Truth · LLM = Language · Memory = layered storage tiers
# Pipeline: Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer
#
# Retrieval — vector-based (cosine of embeddings) over the seed corpus + recall from L3.
# The answer — a pluggable Generator (extractive by default, optional LLM). L3 — a pluggable
# backend (auto→LadybugDB / mock / neo4j). Full L0–L6 architecture:
# docs/archive/Velantrim_V8_Crystal_Sprint1_toc.md
#
# TODO (next):
#   - ESM: full transition matrix + automatic Supported/Hypothesized
#   - First-class episodic nodes (Person/Place/Time) instead of edge props
# (Done: HybridRetriever graph-walk over vector-recall — see _graph_walk below.)

import logging
import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from core.trace import build_trace, promote_trace, format_trace
from core.memory import (
    store_fact, get_fact, _repair_fact_from_canon,
    transition_esm, ESM_TRANSITIONS, l3_secondary_sync_admissible,
    DEFAULT_SOURCE_STATUS, CLAIM_TYPES, SOURCE_STATUSES,
)
from core.queue import get_outbox_queue
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder, cosine, assert_compatible_embedder
from core.retrieval_config import get_retrieval_config
from core.generation import get_generator
from core.canonical_view import project_canonical, _in, _normalize_restricted_bit
from core.rrf import rrf_fuse
from core import metrics, adaptation

logger = logging.getLogger(__name__)


def _safe_confidence(value: Any, default: float = 0.0) -> float:
    """Coerce a retrieved/persisted confidence value to a float, failing
    closed (0.0) on:
      - a non-numeric-TYPE value (e.g. a string/list/dict from a corrupted
        or legacy node) — only a real `int`/`float` (never `bool`, an int
        subclass) is accepted; a numeric-looking string such as "0.9" must
        not be normalized into trusted metadata just because float() happens
        to accept it (#257 review round 5) — would otherwise raise
        TypeError/ValueError for the genuinely non-numeric cases anyway;
      - a non-finite value (NaN, +/-Infinity) — float("nan") and
        float("inf") both convert without raising, but NaN compares False
        against every relational operator (>, <=, <), so a downstream
        `confidence > 0` / `confidence <= 0` check silently passes it
        through instead of rejecting it, and +Infinity legitimately
        satisfies every "confidence >= threshold" check there is (#257
        review round 4);
      - a value outside the canonical [0.0, 1.0] confidence domain
        (schemas/fact.schema.json: minimum 0.0, maximum 1.0; core/api.py's
        IngestRequest.confidence: Field(ge=0.0, le=1.0));
      - a real int too large to convert to a float (e.g. 10**1000) —
        float(value) itself raises OverflowError for this rather than
        producing inf, which the non-finite check above would otherwise
        catch (#257 independent-review round 5).
    Used everywhere a raw L3 node's `confidence` field is read arithmetically
    (retrieve()'s scoring) or compared (Guardian), which must not raise on,
    or be fooled by, any of the above."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    try:
        confidence = float(value)
    except OverflowError:
        return default
    if not math.isfinite(confidence):
        return default
    if not 0.0 <= confidence <= 1.0:
        return default
    return confidence


def _safe_source(value: Any) -> Optional[str]:
    """A non-empty string, or None. A malformed non-string source (e.g. a
    list/dict from a corrupted node) is treated as missing, not stored
    as-is — the `source` column is TEXT NOT NULL, so a raw non-string value
    would raise out of store_fact() instead of failing closed at Guardian
    (#257 review round 3)."""
    return value if isinstance(value, str) and value.strip() else None


# ─── RECALL RECONCILIATION (#257 review round 5) ─────────────────────────────
# run()'s ordinary-recall branch (an in-flight fact that already has a
# physical L3 node) used to copy only epistemic_state/truth_status from the
# L3 node onto the in-flight fact. That let a stale/partial read silently
# win over a fresher, stricter representation: a fresher terminal ESM state
# (Collapsed/Contradicted/Deprecated) already reflected elsewhere could be
# overwritten by an older Validated L3 read, and a real L3 restriction could
# be left un-synced onto a transient item that never carried it. This is a
# narrow reconciliation for exactly this one call site — not a general
# distributed-consistency redesign. It also re-syncs L1's claim/source via
# update_fact() when build_facts_pack()'s earlier store_fact() call is
# detected to have polluted them with a disagreeing transient value (#257
# independent-review round 2) — through a narrow private Canon-repair path;
# public update_fact()/store_fact() claim-identity locking remains unchanged.

_TERMINAL_ESM_STATES = frozenset({"Collapsed", "Contradicted", "Deprecated"})

# Sentinel epistemic_state for an unresolvable disagreement between the
# in-flight fact and the physical L3 node (neither terminal, but not equal
# either) — guaranteed to never be a member of
# core.canonical_view.STRICT_CANONICAL_ESM_STATES, so it fails closed via the
# existing allowlist check without inventing a second parallel state machine.
STORE_STATE_CONFLICT = "STORE_STATE_CONFLICT"


# _normalize_restricted_bit is defined in core/canonical_view.py (imported
# above) — CanonicalView is an independent trust boundary and must not rely
# on pipeline.py's normalization, so pipeline.py imports the single shared
# implementation instead of maintaining a second copy that could drift out
# of sync (#257 independent-review round).


def _effective_restricted(fact_restricted: Any, l3_restricted: Any) -> bool:
    """Reconcile `restricted` for an ORDINARY RECALL: True if either side
    confirms a restriction, but a merely-UNKNOWN/missing L3 field does NOT
    override an L1-confirmed False.

    `fact_restricted` is not an arbitrary second representation: by the time
    _reconcile_recalled_fact() calls this, build_facts_pack() has already
    synced it from L1's own persisted `restricted` column, which always has
    a real 0/1 value (`restricted INTEGER DEFAULT 0` — even a brand-new row
    with no explicit `restricted` key gets the SQL DEFAULT, not NULL), so it
    is already a confirmed, authoritative bool in practice, not UNKNOWN.
    `l3_restricted` is the physical L3 node's own field, which some backends
    (e.g. LadybugL3Graph) never persist at all — treating that structural
    absence (or any other non-True L3 value: malformed, wrong type) as
    equivalent to a confirmed restriction would make every such recalled
    fact permanently non-groundable even though L1 already confirms it is
    not restricted (#257 independent-review round 5; mirrors the identical
    correction already applied to the retrieval layer's
    _may_seed_vector_hit()/_may_propagate_activation() in round 4).

    Still defensively fails closed (True) if fact_restricted itself is ever
    not a confirmed False (True, or — should the L1-sync assumption above
    ever be violated — UNKNOWN); a confirmed True from L3 also always wins,
    even over an L1 False, since a real L3-side restriction must never be
    silently dropped."""
    if _normalize_restricted_bit(fact_restricted) is not False:
        return True
    return _normalize_restricted_bit(l3_restricted) is True


def _effective_epistemic_state(fact_state: Any, l3_state: Any) -> Any:
    """Reconcile the in-flight fact's epistemic_state with the physical L3
    node's own epistemic_state for an ORDINARY RECALL. A stale L3 read must
    never resurrect a fact that another representation already shows in a
    terminal state — and an unresolvable disagreement between the two fails
    closed (STORE_STATE_CONFLICT) rather than silently preferring either
    side. Uses _in() (not raw `in`) so an unhashable fact_state/l3_state
    (e.g. a corrupted node's list/dict epistemic_state) fails closed instead
    of raising TypeError (#257 independent-review round)."""
    if _in(fact_state, _TERMINAL_ESM_STATES):
        return fact_state
    if _in(l3_state, _TERMINAL_ESM_STATES):
        return l3_state
    if fact_state != l3_state:
        return STORE_STATE_CONFLICT
    return l3_state


def _fact_metadata_conflicts(fact: Dict[str, Any], existing_node: Dict[str, Any]) -> bool:
    """True if the in-flight fact's confidence/claim_type/source_status
    disagrees with the physical L3 node's own values (#257 corrective
    hardening, follow-up).

    _reconcile_recalled_fact() already takes truth_status from the L3 node.
    Silently also taking confidence/claim_type/source_status from a
    DIFFERENT representation (the transient item) — instead of noticing they
    disagree — is exactly the hybrid-record anti-pattern this reconciliation
    exists to refuse: a truth_status from one source stitched together with
    other trust-relevant fields from another, never explicitly checked for
    equality. A real disagreement here means either a race (the L3 node
    changed between retrieve() and this admission loop) or a transient item
    from an unrelated origin that merely shares this fact_id — neither
    should be resolved by silently preferring one side.
    """
    if not math.isclose(
        _safe_confidence(fact.get("confidence")),
        _safe_confidence(existing_node.get("confidence")),
        abs_tol=1e-9,
    ):
        return True
    if fact.get("claim_type") != existing_node.get("claim_type"):
        return True
    if fact.get("source_status") != existing_node.get("source_status"):
        return True
    return False


def _reconcile_recalled_fact(fact: Dict[str, Any], existing_node: Dict[str, Any]) -> None:
    """Ordinary recall of a fact with a physical L3 node: refresh the
    strict-grounding fields from the authoritative L3 record, but never let
    it resurrect a fresher terminal state, never let a stale/missing
    restriction bit under-count a real restriction from either side, and
    never let a disagreeing confidence/claim_type/source_status pass through
    unnoticed. Mutates the transient `fact` dict, and — only when this
    reconciliation detects that L1 was just polluted (see below) — L1's own
    claim/source columns via update_fact(); never touches L3."""
    effective_state = _effective_epistemic_state(
        fact.get("epistemic_state"), existing_node.get("epistemic_state"))
    if _fact_metadata_conflicts(fact, existing_node):
        # Content-free fail-closed: block via the same sentinel used for an
        # unresolvable ESM disagreement, rather than exposing which field
        # disagreed or what either value was.
        effective_state = STORE_STATE_CONFLICT
    fact["epistemic_state"] = effective_state
    fact["truth_status"] = existing_node.get("truth_status")
    fact["restricted"] = _effective_restricted(
        fact.get("restricted"), existing_node.get("restricted"))
    # claim/source/confidence/claim_type/source_status: the physical L3 node
    # is the single authoritative record for this fact_id — a transient
    # item's own values (e.g. from a different retrieval origin that happens
    # to share this fact_id) must not be trusted over it, even if the L3
    # node's own value turns out to be missing/malformed (which then
    # correctly fails Guardian/CanonicalView's own checks instead of
    # grounding on unverified provenance).
    #
    # L1 re-sync (#257 independent-review rounds 2 and 4): build_facts_pack()
    # has already called store_fact(fact) for this fact_id BEFORE this
    # reconciliation runs, and store_fact() always overwrites an existing
    # row's claim/source/confidence/claim_type/source_status with whatever
    # the transient item said — regardless of whether that agrees with L3.
    # If the transient item disagreed with the L3 record on any of these
    # fields, L1 now holds the WRONG value: this answer/trace correctly
    # grounds on the L3 record below, but a later memory.get_fact() read
    # (and provenance.verify_receipt(), which diffs a receipt against a
    # fresh L1 read, or a secondary sync that reads L1's polluted trust
    # metadata back into L3) would see the polluted L1 value. Re-sync L1
    # back to the authoritative L3 value here for every field this function
    # already trusts L3 for, undoing that pollution — but only for a value
    # that is itself genuinely well-typed, never writing a missing/malformed
    # L3 value into L1.
    l3_claim = existing_node.get("claim")
    l3_source = existing_node.get("source")
    l3_confidence = existing_node.get("confidence")
    l3_claim_type = existing_node.get("claim_type")
    l3_source_status = existing_node.get("source_status")
    resync_fields: Dict[str, Any] = {}
    if (isinstance(l3_claim, str) and l3_claim.strip()
            and fact.get("claim") != l3_claim):
        resync_fields["claim"] = l3_claim
    if (isinstance(l3_source, str) and l3_source.strip()
            and fact.get("source") != l3_source):
        resync_fields["source"] = l3_source
    try:
        # math.isfinite() requires a C double conversion internally and
        # raises OverflowError (rather than returning False) for a real int
        # too large to convert to a float (e.g. 10**1000) — malformed, not
        # finite, and must fail this validity check rather than crash the
        # whole reconciliation (#257 independent-review round 5).
        l3_confidence_is_valid = (
            isinstance(l3_confidence, (int, float)) and not isinstance(l3_confidence, bool)
            and math.isfinite(l3_confidence) and 0.0 <= l3_confidence <= 1.0
        )
    except OverflowError:
        l3_confidence_is_valid = False
    if (l3_confidence_is_valid
            and not math.isclose(_safe_confidence(fact.get("confidence")),
                                  _safe_confidence(l3_confidence), abs_tol=1e-9)):
        resync_fields["confidence"] = l3_confidence
    # _in(), not raw `in`: an unhashable l3_claim_type/l3_source_status
    # (e.g. a corrupted L3 node's list/dict value) must fail this
    # membership check closed, not raise TypeError inside run()'s broad
    # L3-promotion exception handler — which would enqueue the
    # already-polluted L1 row for drain_l3_outbox() to later merge back
    # over the authoritative L3 record instead of just failing this recall
    # closed (#257 independent-review round 5).
    if _in(l3_claim_type, CLAIM_TYPES) and fact.get("claim_type") != l3_claim_type:
        resync_fields["claim_type"] = l3_claim_type
    if _in(l3_source_status, SOURCE_STATUSES) and fact.get("source_status") != l3_source_status:
        resync_fields["source_status"] = l3_source_status
    if resync_fields:
        # Public update_fact() correctly rejects promoted claim rewrites. This
        # narrow private path is different: L3 is already the physical
        # canonical record for this fact_id, and the write only repairs the L1
        # copy created/refreshed from an untrusted transient retrieval item.
        _repair_fact_from_canon(fact["fact_id"], **resync_fields)
    fact["claim"] = l3_claim
    fact["source"] = l3_source
    fact["confidence"] = l3_confidence
    fact["claim_type"] = l3_claim_type
    fact["source_status"] = l3_source_status


# ─── RETRIEVAL CORPUS (source for retrieve, not L3) ──────────────────────────
# Issue #65: demo seed facts are opt-in only (VELANTRIM_DEMO_SEED=1).
# The production pipeline starts with an empty corpus; all facts must enter
# through ingest() / velantrim learn and pass the normal TruthGate path.
# A direct MERGE into L3 bypassing the TruthGate is an architectural bug.

def _load_demo_seed():
    """Return demo seed facts when VELANTRIM_DEMO_SEED=1, else empty list.

    Called inside retrieve() so the env flag is evaluated at query time, not at
    module import time. This keeps the production default (no seed) working even
    when tests monkeypatch the env var after the module has been imported.
    """
    import os
    if os.environ.get("VELANTRIM_DEMO_SEED", "0") == "1":
        from core.demo_seed import DEMO_FACTS
        return DEMO_FACTS
    return []


# ─── RETRIEVAL (vector / semantic) ────────────────────────────────────────────
# Cosine similarity of embeddings over TWO sources:
#   1) demo seed corpus (opt-in via VELANTRIM_DEMO_SEED=1) — curated reference facts;
#   2) the L3 canon — what the system has already learned and run through the gates.
# Recall from L3 closes the loop "learned → remembered → recalled": facts accepted
# via ingest()/pipeline become available for the answer. Dedup by id.
# The embedder is pluggable (core/embedding.py): default HashingEmbedder, sbert optional.
# Hybrid: vector-recall + multi-hop graph-walk (spreading activation / HippoRAG-lite).

# The numeric knobs (top-k, similarity cutoff, walk depth/damping) live in
# core/retrieval_config.py: bounded, validated, optionally loaded from
# VELANTRIM_RETRIEVAL_CONFIG. Defaults are bit-identical to the historical
# constants (k=3, min_similarity=0.05, hops=2, decay=0.5).
# Activation propagation is default-deny. Graph edges are navigation signals,
# not evidence or truth, and an edge writer must not gain ranking influence
# merely by inventing a new relation type. Start conservatively with the one
# explicitly associative relation already used by episodic recall.
_WALK_EDGE_WEIGHTS = {
    "CO_OCCURRED": 1.0,
}
_WALK_DEFAULT_EDGE_WEIGHT = 0.0

# graph.vector_search(k=...) returns at most k rows straight from the
# backend, ranked by similarity, BEFORE _may_seed_vector_hit()'s deny
# filtering runs. Fetching exactly k means a denied row (restricted,
# L1-terminal, or UNKNOWN-restricted) consumes a top-k slot and can hide a
# valid lower-ranked candidate that the backend never even returned — a
# false zero-hit/refusal even though usable canon exists (#257
# independent-review round 4). Fetching with a margin and trimming to k
# only at the very end (see retrieve()'s final `fused[:k]`) mirrors the
# same margin-then-rerank pattern LadybugL3Graph.vector_search() already
# uses internally (its own "k*3" fetch, re-ranked by significance).
_VECTOR_SEARCH_FETCH_MARGIN = 3


def _l1_terminal_state_blocks(fact_id: Any) -> bool:
    """True if L1 holds a terminal epistemic_state (Collapsed/Contradicted/
    Deprecated) for fact_id that must win over a stale L3 copy still reading
    e.g. Validated. Fails closed to False (does not additionally block) when
    fact_id is malformed or L1 has no record for it at all — a graph-walk-
    encountered node commonly has no L1 record (L1 only ever holds facts
    this process itself learned via store_fact), and that absence is not
    itself a disagreement to fail closed on (#257 independent-review
    round 2)."""
    if not isinstance(fact_id, str):
        return False
    l1_record = get_fact(fact_id)
    return l1_record is not None and _in(l1_record.get("epistemic_state"), _TERMINAL_ESM_STATES)


def _l1_restricted_blocks(fact_id: Any) -> bool:
    """True if L1 confirms fact_id as restricted (or UNKNOWN, deny-dominant),
    which must win over a stale L3 copy that has not yet caught up to a
    set_restricted() call made directly against L1. Fails closed to False
    (does not additionally block) when fact_id is malformed or L1 has no
    record for it — the caller is expected to separately check the L3 node's
    own restricted bit (#257 independent-review round 2)."""
    if not isinstance(fact_id, str):
        return False
    l1_record = get_fact(fact_id)
    return l1_record is not None and _normalize_restricted_bit(l1_record.get("restricted")) is not False


def _may_propagate_activation(node: Dict[str, Any]) -> bool:
    """True only if `node` (a physical L3 node reached by the graph-walk) may
    receive spreading-activation credit as a TARGET in retrieve()'s Source 3.

    The graph-walk used to gate this using only the L3 node's OWN (possibly
    stale) epistemic_state/restricted fields with naive truthy checks — and
    it runs BEFORE run()'s later _reconcile_recalled_fact() (which only
    reconciles facts that already made it into facts_pack) ever executes. A
    fact that has already gone terminal in L1 (Collapsed/Contradicted/
    Deprecated), or whose L1 record is itself confirmed-restricted while the
    L3 copy is stale, must not inflate an unrelated neighbor's relevance
    score just because the L3 copy hasn't caught up yet (#257
    independent-review round).

    Deliberately narrower than _effective_epistemic_state(): that fully
    reconciles two representations of the SAME in-flight fact and fails
    closed on any epistemic_state disagreement, including a missing L1
    record. Here, a graph-walk-encountered node commonly has no L1 record
    at all — that is not itself a disagreement to fail closed on, so this
    only checks whether L1, when present, disagrees in the specific
    terminal-resurrection / restriction direction.

    The L3 node's OWN restricted field only blocks on a CONFIRMED True, not
    merely UNKNOWN/missing — see _may_seed_vector_hit()'s docstring for why
    (some L3 backends, e.g. LadybugL3Graph, never persist this field at
    all; L1, checked above, is the actual always-typed source of truth for
    a fact_id this process has learned)."""
    if node.get("epistemic_state") != "Validated":
        return False
    fact_id = node.get("fact_id")
    if _l1_terminal_state_blocks(fact_id) or _l1_restricted_blocks(fact_id):
        return False
    return _normalize_restricted_bit(node.get("restricted")) is not True


def _may_seed_vector_hit(node: Dict[str, Any]) -> bool:
    """True if a direct vector-search hit `node` (retrieve()'s Source 2) may
    surface as output and seed graph-walk activation as a SOURCE.

    Unlike _may_propagate_activation, does not require epistemic_state ==
    "Validated" — a vector hit's own epistemic state has never been
    restricted to Validated-only (Observed/Hypothesized material can be a
    legitimate direct hit).

    Also excludes a node already terminal in L1 (Collapsed/Contradicted/
    Deprecated) even though its L3 copy still looks unrestricted/Validated:
    admitting it as a vector hit consumes a top-k slot that
    run()'s later reconciliation will fail closed anyway, potentially
    hiding a valid lower-ranked candidate (#257 independent-review round 4;
    see retrieve()'s vector_search margin fix for the companion top-k-
    starvation issue).

    Restricted is checked against BOTH L1's (deny-dominant: True or UNKNOWN
    both block — set_restricted() already applied to L1 must not be
    defeated by a stale L3 copy) and the L3 node's own field — but the L3
    field only blocks on a CONFIRMED True, not merely UNKNOWN/missing. Some
    L3 backends (e.g. LadybugL3Graph) never persist a `restricted` column
    at all — a known, structural backend limitation, not per-record
    corruption — so treating that structural absence as equivalent to a
    confirmed restriction would make every vector hit on that backend
    permanently unretrievable. L1's SQLite `restricted INTEGER DEFAULT 0`
    column is always populated for any fact_id this process has learned, so
    it is the authoritative check; a missing L3 field defers to L1 rather
    than deny-by-default (#257 independent-review round 4)."""
    fact_id = node.get("fact_id")
    if _l1_terminal_state_blocks(fact_id) or _l1_restricted_blocks(fact_id):
        return False
    return _normalize_restricted_bit(node.get("restricted")) is not True


def retrieve(query: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Hybrid search: cosine of embeddings over the demo seed corpus (opt-in) and
    the L3 canon, then a multi-hop graph-walk (spreading activation).
    Returns the top-k by score, deduped by id.
    Seed facts arrive as Observed; recall from L3 uses its stored ESM state.
    An explicit k wins over the configured default (retrieval_config.k).
    """
    cfg = get_retrieval_config()
    if k is None:
        k = cfg.k
    min_sim = cfg.min_similarity
    embedder = get_embedder()
    graph = get_l3_graph()
    # Guard against mixing embedders: we catch an embedder swap on a persistent
    # store (incomparable vectors → broken ranking). The first call stamps it.
    assert_compatible_embedder(graph)
    q_vec = embedder.embed(query)
    seed_items: List[Dict[str, Any]] = []
    vector_items: List[Dict[str, Any]] = []
    graph_items: List[Dict[str, Any]] = []

    # Source 1: seed corpus (opt-in demo facts when VELANTRIM_DEMO_SEED=1).
    for item in _load_demo_seed():
        sim = cosine(q_vec, embedder.embed(item["text"]))
        if sim < min_sim:
            continue
        seed_items.append({
            **item,
            "_score":          round(sim * item.get("confidence", 1.0), 4),
            "epistemic_state": "Observed",
            "origin":          "retrieval",
        })

    def _from_node(node: Dict[str, Any], score: float, origin: str) -> Dict[str, Any]:
        # source_status/epistemic_state: default to the safe, non-privileged
        # pending values (UNKNOWN / Observed) rather than a value that implies
        # verification (DERIVED is a "privileged" source_status per
        # core.pipeline._truth_status_for; "Validated" is already-canonical) —
        # a malformed/legacy L3 node missing these fields must not silently
        # gain trust it never earned (#257 review). truth_status is propagated
        # AS-IS (no default at all): this is the node's own persisted verdict,
        # read-through by run()'s recall path (never recomputed on ordinary
        # recall — see run()'s ESM-promotion loop) and judged by
        # core.canonical_view, which fails closed on a missing/unknown value.
        # source/confidence: no fail-open synthesis either — a node missing
        # real provenance (source=None, not "memory") or confidence
        # (confidence=0.0, not 1.0) must fail Guardian's structural checks
        # (all_have_source / all_have_positive_confidence), not pass through
        # looking like an authoritative, fully-confident fact (#257 review
        # round 3). build_facts_pack() is responsible for not crashing L1
        # storage on a None/malformed source — see its own docstring.
        return {
            "id":              node["fact_id"],
            "text":            node.get("claim", ""),
            "source":          node.get("source"),
            "confidence":      _safe_confidence(node.get("confidence", 0.0)),
            "claim_type":      node.get("claim_type", "WORLD_FACT"),
            "source_status":   node.get("source_status", DEFAULT_SOURCE_STATUS),
            "significance":    node.get("significance", 0.5),
            "_score":          round(score, 4),
            "epistemic_state": node.get("epistemic_state", "Observed"),
            "truth_status":    node.get("truth_status"),
            "origin":          origin,
        }

    # Source 2: L3 canonical memory (recall of what was learned).
    # Fetch with a margin (see _VECTOR_SEARCH_FETCH_MARGIN) so a denied row
    # cannot starve a valid lower-ranked candidate out of the top-k window;
    # the final `fused[:k]` below still trims the actual output to k.
    vector_hits = []
    for node in graph.vector_search(q_vec, k=k * _VECTOR_SEARCH_FETCH_MARGIN):
        sim = node.get("_relevance", 0.0)
        if sim < min_sim:
            continue
        if not _may_seed_vector_hit(node):
            continue  # GDPR Art. 18 / L1-terminal: denied facts do not take part or seed a walk
        # confidence: 0.0 (not 1.0) for a node missing it, and coerced safely
        # for a malformed non-numeric value — a malformed node must not rank
        # as if maximally confident, or crash the multiplication (#257 review
        # round 3).
        vector_items.append(_from_node(node, sim * _safe_confidence(node.get("confidence", 0.0)), "memory"))
        vector_hits.append(node)

    # Source 3: multi-hop graph-walk from vector hits (associative recall).
    # Personalized PageRank (without iterating to convergence): activation flows from
    # vector hits along edges, on each hop multiplied by damping and split among
    # outgoing neighbors proportionally to the edge type's weight (_WALK_EDGE_WEIGHTS:
    # truth-maintenance edges weight 0 — do not propagate). What is reachable via SEVERAL
    # paths is summed — well-connected "hubs" rise. Only Validated nodes
    # propagate and are returned; activation is not poured into seed hits (they have
    # an authoritative vector score). Depth — cfg.graph_walk_hops, damping <1 +
    # the hop limit guarantee convergence without blowing up on cycles.
    seeds = {hit["fact_id"] for hit in vector_hits}
    graph_score: Dict[str, float] = {}
    node_cache: Dict[str, Dict[str, Any]] = {}
    current = {
        # confidence: 0.0 default + safe coercion — see the note above.
        hit["fact_id"]: hit.get("_relevance", 0.0) * _safe_confidence(hit.get("confidence", 0.0))
        for hit in vector_hits
    }
    # Bound even the initial vector-seed frontier. Stable score/fact-id order
    # prevents backend insertion order from changing graph work.
    current = dict(sorted(
        current.items(), key=lambda item: (-item[1], item[0])
    )[:cfg.graph_walk_frontier_limit])
    best_path: Dict[str, Dict[str, Any]] = {
        fid: {
            "seed_fact_id": fid,
            "fact_ids": [fid],
            "edge_types": [],
            "hop_count": 0,
            "activation_contribution": act,
        }
        for fid, act in current.items()
    }
    graph_best_path: Dict[str, Dict[str, Any]] = {}
    graph_exclusion_codes: set[str] = set()

    for _hop in range(cfg.graph_walk_hops):
        nxt: Dict[str, float] = {}
        nxt_best_path: Dict[str, Dict[str, Any]] = {}
        for fid, act in sorted(current.items(), key=lambda item: item[0]):
            # Only explicitly approved relation types are requested from the
            # backend. Each backend receives a hard LIMIT so a dense node cannot
            # materialize an unbounded outgoing-edge set for this query.
            targets = []
            remaining_edges = cfg.graph_walk_edges_per_node
            for rel_type, weight in sorted(_WALK_EDGE_WEIGHTS.items()):
                if remaining_edges <= 0:
                    break
                edges = graph.get_edges(
                    fid, rel_type=rel_type, limit=remaining_edges
                )
                for edge in edges:
                    remaining_edges -= 1
                    node = graph.get_fact(edge["target"])
                    if node is None or not _may_propagate_activation(node):
                        continue
                    targets.append((node, weight, rel_type))
            total_weight = sum(weight for _, weight, _ in targets)
            if total_weight <= 0.0:
                continue
            for node, weight, rel_type in targets:
                nid = node["fact_id"]
                if nid in seeds:
                    continue
                share = act * cfg.graph_walk_decay * (weight / total_weight)
                nxt[nid] = nxt.get(nid, 0.0) + share
                node_cache[nid] = node
                parent_path = best_path.get(fid)
                if parent_path is not None:
                    candidate_path = {
                        "seed_fact_id": parent_path["seed_fact_id"],
                        "fact_ids": [*parent_path["fact_ids"], nid],
                        "edge_types": [*parent_path["edge_types"], rel_type],
                        "hop_count": parent_path["hop_count"] + 1,
                        "activation_contribution": share,
                    }
                    previous = nxt_best_path.get(nid)
                    if (previous is None
                            or share > previous["activation_contribution"]
                            or (share == previous["activation_contribution"]
                                and tuple(candidate_path["fact_ids"]) < tuple(previous["fact_ids"]))):
                        nxt_best_path[nid] = candidate_path
        if not nxt:
            break

        # Highest activation wins; fact_id is the deterministic tie-breaker.
        # Candidate and frontier ceilings are independent: one limits distinct
        # graph-origin results over the whole walk, the other limits work in
        # the next hop. Existing candidates may still accumulate activation.
        ranked_nxt = sorted(nxt.items(), key=lambda item: (-item[1], item[0]))
        bounded_next: Dict[str, float] = {}
        for nid, val in ranked_nxt:
            is_new_candidate = nid not in graph_score
            if (is_new_candidate
                    and len(graph_score) >= cfg.graph_walk_candidate_limit):
                graph_exclusion_codes.add("GRAPH_CANDIDATE_LIMIT_REACHED")
                continue
            graph_score[nid] = graph_score.get(nid, 0.0) + val
            bounded_next[nid] = val
            path = nxt_best_path.get(nid)
            if path is not None:
                previous = graph_best_path.get(nid)
                if (previous is None
                        or path["activation_contribution"] > previous["activation_contribution"]):
                    graph_best_path[nid] = path
            if len(bounded_next) >= cfg.graph_walk_frontier_limit:
                if len(ranked_nxt) > len(bounded_next):
                    graph_exclusion_codes.add("FRONTIER_LIMIT_REACHED")
                break
        if not bounded_next:
            break
        current = bounded_next
        best_path = {nid: nxt_best_path[nid] for nid in bounded_next if nid in nxt_best_path}

    for nid, score in graph_score.items():
        item = _from_node(node_cache[nid], score, "graph")
        path = graph_best_path.get(nid)
        if path is not None:
            item["_graph_explanation"] = {
                "seed_fact_id": path["seed_fact_id"],
                "contributor_paths": [{
                    "fact_ids": path["fact_ids"],
                    "edge_types": path["edge_types"],
                    "hop_count": path["hop_count"],
                    "activation_contribution": round(path["activation_contribution"], 6),
                }],
                "final_activation": round(score, 6),
                "exclusion_reason_codes": sorted(graph_exclusion_codes),
            }
        graph_items.append(item)

    # Fuse ranked candidate lists with RRF (ordering only — no truth/confidence change).
    rankings: List[List[Dict[str, Any]]] = []
    if vector_items:
        rankings.append(sorted(vector_items, key=lambda x: x["_score"], reverse=True))
    if graph_items:
        rankings.append(sorted(graph_items, key=lambda x: x["_score"], reverse=True))
    if seed_items:
        rankings.append(sorted(seed_items, key=lambda x: x["_score"], reverse=True))
    if not rankings:
        return []
    fused = (rankings[0] if len(rankings) == 1
             else rrf_fuse(rankings, key=lambda x: x["id"]))

    signals: Dict[str, set[str]] = {}
    graph_explanations: Dict[str, Dict[str, Any]] = {}
    for signal, items in (
        ("vector", vector_items),
        ("graph", graph_items),
        ("seed", seed_items),
    ):
        for item in items:
            signals.setdefault(item["id"], set()).add(signal)
            if signal == "graph" and isinstance(item.get("_graph_explanation"), dict):
                graph_explanations[item["id"]] = item["_graph_explanation"]

    result: List[Dict[str, Any]] = []
    for rank, item in enumerate(fused[:k], 1):
        annotated = dict(item)
        annotated["_retrieval_rank"] = rank
        annotated["_retrieval_signals"] = sorted(signals.get(item["id"], {item.get("origin", "retrieval")}))
        if item["id"] in graph_explanations:
            annotated["_graph_explanation"] = graph_explanations[item["id"]]
        result.append(annotated)
    return result


# ─── FACTS PACK ───────────────────────────────────────────────────────────────

def build_facts_pack(
    retrieved: List[Dict[str, Any]],
    query: str,
) -> Dict[str, Any]:
    """
    Assemble a FactsPack from the retrieved facts.
    Each fact is stored in L0/L1 memory via store_fact().
    truth_status: an item recalled from L3 (core.pipeline._from_node) carries
    its own persisted verdict through unchanged — a brand-new item (no prior
    verdict) defaults to UNVERIFIED. Never invented here; run()'s ESM-
    promotion loop is the only place a fresh truth_status is computed (for a
    genuinely new admission), and it never recomputes/overwrites an existing
    persisted verdict on ordinary recall (#257 review).
    epistemic_state is taken from retrieve() — the owner of the initial ESM state.
    """
    facts: List[Dict[str, Any]] = []

    for item in retrieved:
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue  # consistent with build_trace: skip entries without an id

        fact = {
            "fact_id":         fact_id,
            "claim":           item["text"],
            # confidence — EPISTEMIC confidence (from the source or the L3 canon),
            # not a relevance rank. Previously item["_score"]
            # (similarity × confidence) was written here, and that value traveled via merge_fact
            # into the canon, silently eroding the node's confidence on EVERY recall (sim ≤ 1 →
            # confidence only fell). The relevance rank lives separately, in
            # _score, and does not reach the canon (see _l3_payload).
            "confidence":      round(_safe_confidence(item.get("confidence", item.get("_score", 0.5))), 4),
            "epistemic_state": item["epistemic_state"],  # from retrieve(), not duplicated
            # retrieval facts — claims about the world from an external source.
            "claim_type":      item.get("claim_type", "WORLD_FACT"),
            "source_status":   item.get("source_status", DEFAULT_SOURCE_STATUS),
            "significance":    item.get("significance", 0.5),
            "truth_status":    item.get("truth_status", "UNVERIFIED"),
        }
        # source: only set the key when it's a genuine non-empty string. A
        # missing/malformed source (core.pipeline._from_node no longer
        # invents "memory" for it) is left OUT of `fact` entirely — Guardian
        # (fact.get("source")) then correctly sees it as missing and blocks,
        # while store_fact()'s own "unknown" fallback (fact.get("source",
        # "unknown")) keeps the L1 write itself from raising on the
        # source TEXT NOT NULL column (#257 review round 3).
        safe_source = _safe_source(item.get("source"))
        if safe_source is not None:
            fact["source"] = safe_source
        # L0/L1 store (store_fact does not persist the transient _score).
        store_fact(fact)
        # Sync epistemic_state and restricted from the persisted store:
        # store_fact preserves the existing state on conflict, so the fact
        # dict may carry a stale retrieve() value (e.g. demo-seed items
        # always arrive as "Observed") while the DB already holds a more
        # advanced state such as "Validated" — or a processing restriction
        # applied after this fact_id was last retrieved. `restricted` is
        # required by core.canonical_view.is_strict_canonical(); retrieve()
        # already excludes restricted L3 nodes from candidacy, but syncing it
        # here too is defense-in-depth against this exact field going stale
        # or missing by the time generate_answer() runs.
        persisted = get_fact(fact_id)
        if persisted:
            fact["epistemic_state"] = persisted["epistemic_state"]
            fact["restricted"] = bool(persisted.get("restricted"))
        # _score — the relevance rank, only for ordering the pack; not written
        # to the canon (_l3_payload takes the clean persistent record without _score).
        fact["_score"] = round(float(item.get("_score", fact["confidence"])), 4)
        facts.append(fact)

    # retrieve() already returns facts by descending _score; we rank by relevance
    # (_score), not by confidence — these are different axes.
    facts.sort(key=lambda x: x["_score"], reverse=True)

    return {
        "facts": facts,
        "query": query,
        "total": len(facts),
    }


# ─── GUARDIAN ─────────────────────────────────────────────────────────────────
# Structural check — the last line of defense before the answer.
# 0 tokens · synchronous · Fast Path.
#
# Contract (baseline): detect structural defects → flag/block before TruthGate.
# Verdicts: pass | block. Does not assign truth, confidence, or epistemic state.

GUARDIAN_VERDICT_PASS = "pass"
GUARDIAN_VERDICT_BLOCK = "block"

GUARDIAN_CONTRACT = (
    "Structural integrity gate on FactsPack + Trace before TruthGate. "
    "Blocks on: empty FactsPack, empty Trace, trace/fact count mismatch, "
    "missing fact_id, missing claim, missing source, or zero confidence. "
    "Does not promote facts or bypass TruthGate."
)


def guardian_diagnose(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Run the Guardian contract and return a structured verdict."""
    facts = facts_pack.get("facts", [])
    checks: Dict[str, bool] = {
        "facts_non_empty": bool(facts),
        "trace_non_empty": bool(trace),
        "trace_covers_facts": len(trace) >= len(facts),
        "all_have_fact_id": all(bool(f.get("fact_id")) for f in facts),
        "all_have_claim": all(bool(f.get("claim")) for f in facts),
        "all_have_source": all(bool(f.get("source")) for f in facts),
        # _safe_confidence(), not a raw float(...) > 0: Guardian must reject
        # non-finite (NaN/+-Infinity) and malformed confidence itself, not
        # merely trust that a caller already sanitized it (#257 review round
        # 4) — NaN compares False against every relational operator, so a raw
        # `float(x) > 0` silently treats it as "not positive" here but a raw
        # `<= 0` below would ALSO be False, letting it slip through the
        # per-fact block undetected; a raw `float(x)` on a non-numeric value
        # would also crash this comprehension outright.
        "all_have_positive_confidence": all(
            _safe_confidence(f.get("confidence", 0)) > 0 for f in facts),
    }

    if not checks["facts_non_empty"]:
        return {"verdict": GUARDIAN_VERDICT_BLOCK, "reason": "FactsPack is empty",
                "checks": checks}
    if not checks["trace_non_empty"]:
        return {"verdict": GUARDIAN_VERDICT_BLOCK,
                "reason": "Trace is empty — provenance is missing", "checks": checks}
    if not checks["trace_covers_facts"]:
        return {"verdict": GUARDIAN_VERDICT_BLOCK,
                "reason": (f"Mismatch: {len(facts)} facts, "
                           f"{len(trace)} trace elements"),
                "checks": checks}

    for fact in facts:
        if not fact.get("fact_id"):
            return {"verdict": GUARDIAN_VERDICT_BLOCK,
                    "reason": f"Fact without fact_id: {fact}", "checks": checks}
        if not fact.get("claim"):
            return {"verdict": GUARDIAN_VERDICT_BLOCK,
                    "reason": f"Fact without claim: {fact['fact_id']}", "checks": checks}
        if not fact.get("source"):
            return {"verdict": GUARDIAN_VERDICT_BLOCK,
                    "reason": f"Fact without source: {fact['fact_id']}", "checks": checks}
        if _safe_confidence(fact.get("confidence", 0)) <= 0:
            return {"verdict": GUARDIAN_VERDICT_BLOCK,
                    "reason": f"Zero confidence: {fact['fact_id']}", "checks": checks}

    return {"verdict": GUARDIAN_VERDICT_PASS, "reason": None, "checks": checks}


def guardian(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> tuple[bool, Optional[str]]:
    """
    Checks the structural integrity of the FactsPack and Trace.
    Returns (passed: bool, reason: str | None).
    """
    diag = guardian_diagnose(facts_pack, trace)
    return diag["verdict"] == GUARDIAN_VERDICT_PASS, diag.get("reason")


# ─── TRUTH GATE ───────────────────────────────────────────────────────────────
# The only entry into the L3 graph. Bypassing it = an architectural bug.
# The gate now lives in core/truth_gate.py as a first-class module; this
# re-export keeps `from core.pipeline import truth_gate` (ingest/review/
# reconcile/imports) and `monkeypatch.setattr(pipeline, "truth_gate", …)`
# working unchanged — run() resolves the name through this module's globals.

from core.truth_gate import truth_gate  # noqa: E402  (re-export, see above)


def _truth_status_for(claim_type: str, source_status: Optional[str] = None) -> str:
    """
    Source-aware truth status by claim modality (issue #63).

    WORLD_FACT truth status depends on origin:
      EXTERNAL / DERIVED / OBSERVED  → VERIFIED  (independently sourced knowledge)
      USER_REPORTED                  → USER_CLAIMED (stored as recalled, not yet verified)
      LLM_OUTPUT                     → UNVERIFIED (blocked by truth_gate, but defensive)
      UNKNOWN / None                 → UNVERIFIED

    A user saying "Earth orbits the Sun" is a USER_CLAIMED world claim, not a
    VERIFIED fact — even if it is true. VERIFIED requires an independent external
    source or evidence span.
    """
    if claim_type == "WORLD_FACT":
        if source_status in {"EXTERNAL", "DERIVED", "OBSERVED"}:
            return "VERIFIED"
        if source_status == "USER_REPORTED":
            return "USER_CLAIMED"
        return "UNVERIFIED"
    if claim_type == "INTERPRETATION":
        return "HYPOTHESIS"
    return "SUBJECTIVE"


# ─── GENERATION ───────────────────────────────────────────────────────────────
# The answer is formed by a pluggable Generator (core/generation.py): default — extractive,
# optionally — an LLM (Claude) with the FactsPack in system. The graph remains the source of truth.

def _public_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Strip facts of internal service fields (keys prefixed with '_', e.g.
    the transient _score) before returning to the caller. The relevance rank is
    a retrieval detail, not part of the answer; it also does not reach the canon (see _l3_payload).
    """
    return [{k: v for k, v in f.items() if not k.startswith("_")} for f in facts]


def generate_answer(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate an answer from strict-canonical facts via get_generator().
    Default backend extractive (concatenation); LLM — via VELANTRIM_GENERATOR=anthropic.

    Grounding uses core.canonical_view's default STRICT read projection, not a
    raw ESM-state filter: physical L3 membership or epistemic_state ==
    "Validated"/"Supported" does not by itself make a fact suitable grounding
    for a confident factual answer — e.g. a USER_CLAIMED WORLD_FACT can reach
    epistemic_state "Validated" without ever being externally verified. See
    docs/CANONICAL_VIEW_RFC.md and core/canonical_view.py for the full
    rationale; this is the smallest production-safe runtime slice of that RFC.
    """
    canonical_facts = project_canonical(facts_pack["facts"])
    if not canonical_facts:
        # Issue #64 + CanonicalView: a verifiable memory system must not answer
        # from material that is not strict-canonical (VERIFIED, non-contradicted/
        # -deprecated, unrestricted, identity-complete). No such facts →
        # insufficient grounding → block, even if unvalidated/non-canonical
        # material (e.g. USER_CLAIMED) is present.
        logger.warning(
            "generate_answer: no strict-canonical facts — blocking answer "
            "(%d non-canonical fact(s) present but not usable as grounding)",
            len(facts_pack["facts"]),
        )
        # A refusal must not report a false "Validated" trace (#257 review
        # round 5): run()'s blanket promote_trace(trace, "Validated") call
        # (for the CanonicalView-success path) stamps every trace element
        # "Validated" before generate_answer() is even called, regardless of
        # whether CanonicalView actually admits anything. Sync each element's
        # epistemic_state to its fact's REAL current state instead of
        # returning the blanket-promoted trace verbatim — a blocked response
        # must never look like validation.
        # isinstance(..., str), not just truthy: a direct generate_answer()
        # caller can hand this a fact whose fact_id is an unhashable list/
        # dict — CanonicalView correctly rejects it as non-canonical
        # upstream, but a raw dict-comprehension/`.get()` would still crash
        # on that value as a dict key instead of reaching this intended
        # fail-closed refusal (#257 independent-review round 2).
        facts_by_id = {
            f["fact_id"]: f for f in facts_pack["facts"]
            if isinstance(f.get("fact_id"), str) and f["fact_id"]
        }
        refusal_trace = []
        for t in trace:
            entry = dict(t)
            fid = t.get("fact_id")
            fact = facts_by_id.get(fid) if isinstance(fid, str) else None
            # An unmatched/malformed trace entry (no corresponding fact in
            # facts_pack) has no REAL current state to report — leaving
            # whatever epistemic_state it already carried would let a stale
            # blanket-promoted "Validated" survive for exactly the entries
            # this sync cannot verify (#257 corrective hardening, follow-up).
            entry["epistemic_state"] = fact.get("epistemic_state") if fact is not None else None
            refusal_trace.append(entry)
        return {
            "answer":      None,
            "error":       "insufficient grounding: no strict-canonical (VERIFIED) facts available",
            "query":       facts_pack.get("query", ""),
            "facts":       [],
            "trace":       refusal_trace,
            "trace_fmt":   format_trace(refusal_trace),
            "total_facts": 0,
        }

    answer = get_generator().generate(facts_pack.get("query", ""), canonical_facts)

    # Prune the trace to exactly the fact_ids that grounded this answer: the
    # public trace must not claim provenance for retrieved-but-excluded
    # material (e.g. a USER_CLAIMED candidate that never grounded anything).
    # set(result["facts"] fact_ids) == set(result["trace"] fact_ids) for every
    # successful strict answer (#257 review). Each surviving trace element's
    # epistemic_state is also synced to the corresponding fact's REAL final
    # state — run()'s blanket promote_trace(trace, "Validated") call stamps
    # every trace element "Validated" regardless of what the fact actually
    # is, so an ImmutableCore (or any non-"Validated" but still strict-
    # canonical) grounding fact must not be misreported as "Validated" in its
    # own trace entry (#257 review round 3).
    canonical_by_id = {f["fact_id"]: f for f in canonical_facts}
    grounded_trace = []
    for t in trace:
        fid = t.get("fact_id")
        # isinstance guard before the dict lookup: an unhashable fid (list/
        # dict) from a malformed trace entry must not crash this membership
        # check (#257 independent-review round 2) — canonical_by_id's own
        # keys are always valid strings (project_canonical() already
        # requires it), but a mismatched/malformed trace entry's fid is not
        # guaranteed to be.
        if not isinstance(fid, str) or fid not in canonical_by_id:
            continue
        entry = dict(t)
        canonical_fact = canonical_by_id[fid]
        entry["epistemic_state"] = canonical_fact.get("epistemic_state")
        # source: _reconcile_recalled_fact() may have replaced the in-flight
        # fact's source with the L3-authoritative value AFTER this trace was
        # built by build_trace(retrieved) — syncing only epistemic_state
        # left a stale/disagreeing source in the public trace, so the trace
        # no longer proved the actually-grounded fact's real source (#257
        # independent-review round 2).
        entry["source"] = canonical_fact.get("source")
        grounded_trace.append(entry)

    return {
        "answer":       answer,
        "query":        facts_pack.get("query", ""),
        "facts":        _public_facts(canonical_facts),
        "trace":        grounded_trace,
        "trace_fmt":    format_trace(grounded_trace),
        "total_facts":  len(canonical_facts),
    }


# ─── EPISODIC BINDING ─────────────────────────────────────────────────────────
# Episodic memory: "what-where-when-with-whom". Facts recalled together are
# linked in L3 by an undirected pair of CO_OCCURRED edges with the episode context.
# The edges connect already validated nodes — this is not a TruthGate bypass (it guards
# only a fact node's entry into the canon).

_EPISODE_REL = "CO_OCCURRED"


def _entity_refs(episode: Dict[str, Any]) -> List[tuple]:
    """Episode entities → [(entity_id, kind, label)] for who/where."""
    refs = []
    for name in (episode.get("who") or []):
        refs.append((f"who:{name}", "person", name))
    where = episode.get("where")
    if where is not None:
        refs.append((f"where:{where}", "place", where))
    return refs


def _link_episode(
    graph,
    facts: List[Dict[str, Any]],
    query: str,
    episode: Optional[Dict[str, Any]],
) -> None:
    """Link co-recalled facts by an episode: who/where → entity nodes (for any
    number of facts) + a CO_OCCURRED edge between pairs (at least two facts)."""
    ids = [f["fact_id"] for f in facts]
    episode = episode or {}

    # First-class who/where entity nodes: each fact mentions the entity.
    for entity_id, kind, label in _entity_refs(episode):
        graph.merge_entity(entity_id, kind, label)
        for fid in ids:
            graph.link_fact_to_entity(fid, entity_id)

    if len(ids) < 2:
        return  # an episodic edge needs at least two facts

    props: Dict[str, Any] = {
        "query": query,
        "when": episode.get("when") or datetime.now(timezone.utc).isoformat(),
    }
    for key in ("who", "where", "event"):
        if episode.get(key) is not None:
            props[key] = episode[key]

    # A chain of adjacent pairs (not all pairs) — O(n) links, enough for an episode.
    for a, b in zip(ids, ids[1:]):
        graph.add_edge(a, _EPISODE_REL, b, props)
        graph.add_edge(b, _EPISODE_REL, a, props)

    # L1.5 Velum (RFC0016): feed the co-recalled set to the synaptic pre-graph as a
    # fire-and-forget hint. Velum is NOT a source of facts (I3) and must never
    # break the pipeline, so failures are swallowed.
    try:
        from core.velum import get_velum
        get_velum().observe_episode(query, ids)
    except Exception:  # noqa: BLE001 — a hint layer must not affect the canon
        pass


def recall_episode(fact_id: str) -> List[Dict[str, Any]]:
    """
    Episodic recall: with which facts and in what context (who/where/when/
    query) this fact was recalled together. Reads CO_OCCURRED edges — makes
    the episodic data that _link_episode wrote queryable.
    """
    out: List[Dict[str, Any]] = []
    for edge in get_l3_graph().get_edges(fact_id, _EPISODE_REL):
        props = edge.get("props", {})
        out.append({
            "with":  edge["target"],
            "who":   props.get("who"),
            "where": props.get("where"),
            "when":  props.get("when"),
            "query": props.get("query"),
        })
    return out


def recall_by_entity(
    *, who: Optional[str] = None, where: Optional[str] = None,
) -> List[str]:
    """
    Recall by entity: ids of facts mentioning a person/place. A direct reverse
    traversal of first-class entity nodes (facts_for_entity), not an edge scan.
    who/where are combined by union.
    """
    if who is None and where is None:
        return []
    graph = get_l3_graph()
    matched = set()
    if who is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"who:{who}"))
    if where is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"where:{where}"))
    return sorted(matched)


# ─── MAIN PIPELINE ────────────────────────────────────────────────────────────

def _l3_payload(fact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonical payload for merge_fact: take the PERSISTENT record from L0/L1
    (get_fact) — with created_at / updated_at / metadata — and overlay truth_status
    (it is not among the SQLite columns, it lives only in the canon).

    Why: previously a "bare" in-memory fact without created_at/metadata went to L3, and
    SleepCycle (consolidate) did not find a reference timestamp → decay was NEVER
    applied to freshly ingested nodes until reconcile touched them. The clean
    persistent record fixes this and guarantees that the real confidence reaches the canon,
    not the transient _score (which is not in the record).
    """
    record = get_fact(fact["fact_id"]) or fact
    return {**record, "truth_status": fact.get("truth_status")}


def drain_l3_outbox(graph=None) -> int:
    """
    Re-merge into L3 the facts whose write to the canon previously failed (self-heal).

    L3 and SQLite do not share a transaction: on a merge failure a fact stays Validated in
    SQLite but without a node in the graph (see enqueue in run()). Here we idempotently
    retry the MERGE for the queue and remove the successful ones. If the backend is still
    unavailable — we leave it in the queue and stop trying until next time.
    Returns the number of successfully re-merged facts.
    """
    graph = graph or get_l3_graph()
    queue = get_outbox_queue()
    healed = 0
    for fid in queue.pending():
        fact = get_fact(fid)
        if fact is None:
            queue.clear(fid)  # the fact vanished from SQLite — drop the stale entry
            continue
        if not l3_secondary_sync_admissible(fact, graph=graph):
            queue.clear(fid)  # outbox is for post-gate canon merges only
            continue
        fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))
        try:
            graph.merge_fact(_l3_payload(fact))
        except Exception as e:  # noqa: BLE001 — backend still unavailable, do not lose the queue
            logger.warning(
                "drain_l3_outbox: %s is still waiting (%s)", fid, type(e).__name__)
            break
        queue.clear(fid)
        healed += 1
    return healed


def run(query: str, episode: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    The full Velantrim pipeline:
    Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer

    Principle: Trace → Validation → Answer.
    Not the other way around.

    episode — optional episode context (who / where / when / event):
    facts recalled together are linked in L3 by an episodic edge.
    """
    metrics.incr("query.total")
    # 0. Self-heal: re-merge facts whose write to L3 previously failed (outbox).
    drain_l3_outbox()
    # 1. Retrieval
    retrieved = retrieve(query)

    # NeuroCore Phase 0 (RFC0068): record the surprise of this retrieval as a
    # passive plasticity tick. Surprise ≈ 1 − top relevance (a weak best match is
    # novel/surprising). Placed BEFORE the zero-hit early return so the most
    # surprising case — a query with no retrieval hits (surprise = 1.0), e.g. on a
    # cold-start empty corpus — is also recorded. Gated by VELANTRIM_NEUROCORE
    # (off by default); observe() writes only to its own delta log — never L3
    # (invariant I68) — and only above θ. A passive tracker must never break the
    # pipeline, so failures are swallowed.
    try:
        from core import neurocore
        if neurocore.enabled():
            top = max((float(f.get("_score", 0.0)) for f in retrieved), default=0.0)
            surprise = round(max(0.0, 1.0 - top), 4)
            neurocore.observe(surprise, delta_norm=surprise, domain="pipeline")
    except Exception:  # noqa: BLE001 — Phase 0 tracker must not affect the canon
        pass

    if not retrieved:
        return _blocked("Retrieval returned 0 results.", query)

    # 2. FactsPack
    facts_pack = build_facts_pack(retrieved, query)

    # 3. Trace
    trace = build_trace(retrieved)

    # 4. Guardian (structural check)
    guardian_ok, guardian_reason = guardian(facts_pack, trace)
    if not guardian_ok:
        adaptation.record_block()   # stress → verification rises (RFC0071)
        return _blocked(f"Guardian: {guardian_reason}", query, facts_pack, trace)

    # 5. TruthGate (verification)
    gate_ok, gate_reason = truth_gate(facts_pack)
    if not gate_ok:
        adaptation.record_block()
        return _blocked(f"TruthGate: {gate_reason}", query, facts_pack, trace)

    # 6. ESM: transition facts and trace to Validated via transition_esm (the only path).
    #    truth_status is set by claim_type: VERIFIED only for WORLD_FACT,
    #    the subjective is validated as experience (Validated), but does not become truth about the world.
    #
    #    Cross-store nuance: SQLite (pending) and L3 (canon) — two stores without a shared
    #    transaction. We catch a write failure to L3 and return _blocked, rather than crash
    #    the pipeline with a traceback. Partial state self-heals: failed
    #    facts are put into the outbox (enqueue_l3_write) and idempotently re-merged on the
    #    next access (drain_l3_outbox, step 0). The source of truth is the graph,
    #    SQLite is just a pending cache.
    graph = get_l3_graph()
    try:
        for fact in facts_pack["facts"]:
            # Admission-vs-recall must key off PHYSICAL L3 presence, not ESM
            # state (#257 review round 3): an L3 node that already exists —
            # legitimately Observed/Hypothesized/Supported, or with a
            # missing/malformed epistemic_state on a corrupted/legacy record —
            # is an ORDINARY RECALL, not a new admission, regardless of what
            # epistemic_state the retrieved item/L1 row currently shows
            # (build_facts_pack()'s store_fact() upsert can create/refresh an
            # L1 row for a fact_id that is already a physical L3 node, e.g.
            # when L1 lost its copy — that must not be mistaken for "this
            # fact has never been admitted"). Using ESM state alone here was
            # the actual bug: it let a malformed L3 node (missing
            # epistemic_state -> _from_node() defaults it to "Observed") be
            # treated as brand new, auto-transitioned to Validated, and have
            # its real persisted truth_status silently recomputed/overwritten.
            existing_node = graph.get_fact(fact["fact_id"])
            if existing_node is not None:
                # Ordinary recall: do not auto-transition it merely because a
                # query touched it, and do not recompute/overwrite its
                # persisted verdict — promotion of pending or non-canonical
                # physical-L3 material requires an explicit admission/review
                # path (core.review.approve / core.reconcile), not ordinary
                # answer retrieval. No write to L3 happens for this fact.
                # _reconcile_recalled_fact (#257 review round 5) refreshes
                # the strict-grounding fields from the L3 record without
                # letting a stale L3 read resurrect a fresher terminal state
                # or under-count a real restriction from either side.
                _reconcile_recalled_fact(fact, existing_node)
                continue

            # Genuinely new to the L3 canon (this also correctly covers the
            # L1-Validated/L3-missing outbox-recovery case: epistemic_state is
            # already "Validated" here, so the transition attempt below is
            # skipped — Validated->Validated is illegal in the ESM matrix —
            # but there is still no PRIOR L3 verdict to preserve, since this
            # fact_id was never actually merged, so truth_status is computed
            # fresh below, exactly reproducing what the original admission
            # would have set).
            if fact.get("epistemic_state") != "Validated":
                # Promotion guard: only attempt the transition if "Validated" is a
                # reachable next state from the fact's current ESM state. Terminal
                # states (Collapsed, ImmutableCore) and non-promotable states
                # (Contradicted, Deprecated) would raise ValueError inside
                # transition_esm, which the broad L3 exception handler would catch
                # and misroute into the L3 outbox — letting drain_l3_outbox() later
                # merge a non-Validated fact into Canon without re-checking the gate.
                if "Validated" not in ESM_TRANSITIONS.get(
                    fact.get("epistemic_state", "Observed"), set()
                ):
                    continue
                # CAS guard: if the persisted state changed under us (a competing
                # writer), transition_esm returns False and evicts the stale L0
                # entry. Do NOT merge a stale payload into the canon — skip this
                # fact. Defense-in-depth, not a full atomicity guarantee.
                if not transition_esm(fact["fact_id"], "Validated"):
                    continue
                updated = get_fact(fact["fact_id"])
                if updated:
                    fact["epistemic_state"] = updated["epistemic_state"]

            fact["truth_status"] = _truth_status_for(
                fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))
            # The only entry into L3: the canonical MERGE strictly after the TruthGate.
            # We merge the persistent record (created_at/metadata → for SleepCycle),
            # not the transient fact with _score (see _l3_payload).
            graph.merge_fact(_l3_payload(fact))
    except Exception as e:  # noqa: BLE001 — an L3 failure must not crash the pipeline
        logger.error("L3 promotion failed: %s", e)
        adaptation.record_block()
        # We put the failed facts into the outbox — they will be re-merged on the next access.
        queue = get_outbox_queue()
        for f in facts_pack["facts"]:
            queue.enqueue(f["fact_id"])
        return _blocked(f"L3 promotion failed: {e}", query, facts_pack, trace)

    promote_trace(trace, "Validated")

    # 7. Generate — metrics/adaptation must reflect the ACTUAL CanonicalView
    # outcome, not merely that L3 promotion succeeded. A CanonicalView refusal
    # here (no strict-canonical facts) is a block, not a success — reaching
    # this line does not itself guarantee generate_answer() will answer.
    result = generate_answer(facts_pack, trace)
    if result.get("answer") is not None:
        metrics.incr("query.answered")
        adaptation.record_success()     # a healthy outcome → the threshold relaxes
        # 8. Episodic binding (#257 corrective hardening, independent finding):
        # only an EXPLICIT episode may create episodic graph mutations, and
        # only AFTER a successful strict-grounded answer, linking only the
        # facts that actually grounded it. Implicit co-recall linking (any
        # 2+ facts retrieved together, episode or not) is removed — a
        # blocked answer, or a query with no explicit episode, must never
        # write CO_OCCURRED/MENTIONS edges. A failure here must not turn an
        # epistemically correct answer into a false failure: it is logged as
        # a safe, content-free, observable event and swallowed.
        if episode is not None:
            try:
                _link_episode(graph, result["facts"], query, episode)
            except Exception:  # noqa: BLE001 — a grounded answer must survive this
                logger.warning(
                    "episode_link failed after a successful grounded answer "
                    "(fact_count=%d) — answer unaffected", len(result["facts"]),
                )
                metrics.incr("episode_link.failed")
    else:
        metrics.incr("query.blocked")
        adaptation.record_block()       # stress → verification rises (RFC0071)
    return result


def _blocked(
    reason: str,
    query: str,
    facts_pack: Optional[Dict] = None,
    trace: Optional[List] = None,
) -> Dict[str, Any]:
    """Standard response when the pipeline is blocked."""
    metrics.incr("query.blocked")
    return {
        "error":  reason,
        "answer": None,
        "query":  query,
        "facts":  _public_facts(facts_pack.get("facts", [])) if facts_pack else [],
        "trace":  trace or [],
    }


# ─── TEST ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    queries = [
        "What is quantum entanglement?",
        "How does DNA work?",
        "Tell me about the Sun",
    ]
    for q in queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {q}")
        result = run(q)
        print(f"ANSWER: {result.get('answer', 'BLOCKED')}")
        if result.get("error"):
            print(f"ERROR:  {result['error']}")
        if result.get("trace_fmt"):
            print(result["trace_fmt"])
