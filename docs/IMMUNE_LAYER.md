# Immune Layer

**What `core/immune.py` (the "CRISPR memory guard", RFC0072) checks, blocks,
and does not — described as implemented, not as design intent.**

## Implemented behaviour

### The model

The module borrows the CRISPR analogy: a persistent, curated store of known
*threat patterns* ("spacers") is screened against new claims before they
reach the canon. Screening returns one of three verdicts:

| Verdict | Meaning |
|---|---|
| `ADMIT` | Nothing matched — proceed to the normal Guardian/TruthGate path |
| `QUARANTINE` | Advisory: the claim contradicts the canon; not blocked |
| `BLOCK` | Matches the recorded threat memory, or (opt-in strict mode) contradicts the canon |

**Empty threat memory blocks nothing** — the guard is a no-op until a threat
is explicitly recorded; enabling the module does not by itself change
default ingest behaviour.

### What it checks

`screen(claim, fact_id=None, check_canon=True)` runs, in order:

1. **Threat-memory match** (`match_threat`) — whole-token containment against
   every recorded pattern at or above the block-severity floor (default
   `0.5`, `VELANTRIM_IMMUNE_BLOCK_SEVERITY`). Matching is on normalized,
   space-padded token strings, so a spacer `"the sky is green"` matches
   `"the sky is green because magic"` but `"car"` never matches `"scary"`
   (whole-token, not substring). On a match: `verdict=BLOCK`, a hit counter
   on the threat entry increments, and the highest-severity match wins if
   several patterns match.
2. **Canon contradiction** (`check_canon=True`, `screen()`'s own default
   when called standalone) — reuses `reconcile.find_conflicts()` and keeps
   only `CONTRADICTION`-kind results (see
   [`CONTRADICTION_POLICY.md`](./CONTRADICTION_POLICY.md) for what that
   classifier does and does not catch). If any exist:
   - **strict mode off (default):** `verdict=QUARANTINE` — advisory only.
   - **strict mode on** (`VELANTRIM_IMMUNE_STRICT=1`): `verdict=BLOCK`.

### Ingest-path usage differs from standalone `screen()`

The live `ingest()` path (`core/ingest.py`) does **not** call `screen()`
with `check_canon=True`. It calls `screen(utterance, fact_id=fid,
check_canon=False)` exactly once, *before* Guardian/TruthGate, purely as a
threat-memory pre-screen (step 1 above). Canon contradiction is checked
separately, *after* TruthGate passes, by calling `reconcile.find_conflicts()`
directly — not through `screen()` — with its own inline strict/non-strict
branch:

- **strict mode off (default):** the conflict is attached to the ingest
  result (`result["conflicts"]`) and the fact still promotes to `Validated`
  and merges into L3 in the same call. There is no separate `QUARANTINE`
  verdict object on this path — just the conflicts list on an otherwise
  successful `accepted=True` result.
- **strict mode on:** ingest blocks outright, and — **only on this branch**
  — `VELANTRIM_IMMUNE_LEARN=1` additionally calls `record_threat()` to learn
  the utterance as a new threat. This auto-learning is implemented in
  `core/ingest.py`, not inside `screen()`/`immune.py` itself, so a
  standalone `screen()` call (e.g. via the `immune-check` CLI command, or
  `review.py`'s own pre-screen at `check_canon=False`) never triggers it.

So the ADMIT/QUARANTINE/BLOCK table above describes `screen()` itself and
what a direct/standalone caller gets. The live ingest path's actual
contradiction handling is the bespoke logic in `core/ingest.py` described
here — it reuses `find_conflicts()`, not `screen()`'s `QUARANTINE` branch.

### What it blocks (strict vs advisory)

| Condition | Default | With `VELANTRIM_IMMUNE_STRICT=1` |
|---|---|---|
| Matches recorded threat memory | `BLOCK` | `BLOCK` |
| Contradicts a `Validated` canon `WORLD_FACT` | `QUARANTINE` (advisory) | `BLOCK` |
| Neither | `ADMIT` | `ADMIT` |

Blocking power comes from **explicit, curated** threat memory by default —
canon contradiction alone is advisory unless an operator opts into strict
mode. This mirrors the project's truth-first, non-destructive-by-default
principle: a heuristic must never silently reject on its own judgment of
"this looks wrong."

### Threat memory lifecycle

- `record_threat(pattern, threat_type="manual", severity=1.0, actor="system")`
  — idempotent by normalized pattern (re-recording refreshes type/severity,
  keeps the accumulated hit count); appends a content-free event to the
  tamper-evident audit log (`core/audit.py`).
- `forget_threat(pattern_id, actor="system")` — curator revocation; also
  audited.
- `list_threats()` / `immunity_report()` — observability: every recorded
  threat, total hits, and a breakdown by `threat_type`.
- **Persistent and adaptive**: threats live in the `immune_memory` SQLite
  table and survive restarts.
- **`VELANTRIM_IMMUNE_LEARN`** (off by default): on the live `ingest()`
  path's strict-contradiction branch only (see "Ingest-path usage differs
  from standalone `screen()`" above — this is *not* implemented inside
  `screen()`/`immune.py`), a strict-blocked contradiction is additionally
  recorded as a new threat automatically. It is off by default
  *deliberately* — the module docstring is explicit that the system cannot
  know which side of a contradiction is the hallucination, so auto-learning
  from a clash risks immunising against a true correction. Enable only for a
  source expected to be wrong-by-default (e.g. an untrusted feed behind
  manual review).

### Accountability

Every `record_threat` / `forget_threat` call appends a content-free entry to
`core/audit.py`'s hash-chained log (pattern hash / type / severity / actor —
never the claim text itself).

## Non-goals

- **Not an NLI/LLM classifier.** Pattern matching is normalized whole-token
  containment; contradiction detection is the same lexical, high-precision
  classifier described in `CONTRADICTION_POLICY.md` — the same coverage
  limits apply (see that document's Current limitations).
- **Not a silent auto-reject on suspicion.** Canon contradiction alone is
  advisory (`QUARANTINE`) unless an operator explicitly opts into
  `VELANTRIM_IMMUNE_STRICT`.
- **Not self-learning by default.** `VELANTRIM_IMMUNE_LEARN` is off; the
  threat memory only grows from explicit `record_threat()` calls unless an
  operator opts in.
- **Not a replacement for TruthGate/Guardian.** `screen()` runs as a
  pre-check; it does not itself admit facts to canon or replace the gate
  sequence in `core/pipeline.py`.

## Examples (from current behaviour)

**Allowed (`ADMIT`):** an empty threat memory, `check_canon=False`, and a
claim with no recorded pattern match — always admits, regardless of content.

**Blocked (`BLOCK`) by threat memory:** `record_threat("the sky is green")`
then `screen("the sky is green today")` — whole-token containment matches,
verdict `BLOCK`, `reason` names the matched `threat_type` and `severity`.

**Advisory (`QUARANTINE`):** with no recorded threat and strict mode off,
`screen("water does not boil at 100°C")` against a canon `Validated` fact
"water boils at 100°C" — the contradiction classifier fires (negation
signal), but default mode surfaces it as `QUARANTINE` with the conflicting
`fact_id`s, not a block.

**Strict block:** the same case with `VELANTRIM_IMMUNE_STRICT=1` set —
`verdict=BLOCK`, `reason="contradicts N canonical fact(s) (strict mode)"`.

## Relationship to the contradiction policy

`immune.screen()`'s canon-contradiction check is a direct consumer of
`reconcile.find_conflicts()` and `core/contradiction.py`. See
[`CONTRADICTION_POLICY.md`](./CONTRADICTION_POLICY.md) for the full
implemented-behaviour / current-limitations / safe-policy breakdown of
conflict detection and resolution — it applies unchanged here: `screen()`
surfacing `QUARANTINE` does not, by itself, mark anything as `Contradicted`
in the canon; that still requires an explicit `reconcile.contradict()` call,
which (as of this document) has no CLI/API entry point.
