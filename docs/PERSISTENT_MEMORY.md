# Persistent Memory Model

Velantrim separates **persistence**, **canonical truth**, and **immutability**. These are related but not identical.

> Persistent memory survives process restart.  
> Canonical memory has passed the TruthGate and entered the L3 graph.  
> Immutable memory is protected by Ring Zero / `ImmutableCore` rules.

---

## 1. Memory layers

| Layer | Backend | Default path | Persistent | Role |
|---|---|---:|---:|---|
| `L0` | in-process LRU cache | RAM only | No | Hot working cache for the current process |
| `L1` | SQLite | `./data/velantrim_memory.db` | Yes | Working memory, pending facts, ESM state, audit/compliance support |
| `L3` | Canonical graph backend | `./data/velantrim_l3.db` when SQLite backend is used | Yes, if using `sqlite`, `ladybug`, or `neo4j` | Canonical graph after Guardian + TruthGate |
| `MockL3Graph` | Python memory | RAM only | No | Tests / development only |

The important distinction:

```text
L1 = persistent working memory / pending layer
L3 = persistent canonical graph, if configured with a persistent backend
```

---

## 2. L1 SQLite: persistent working memory

`core/memory.py` stores L1 data in:

```text
./data/velantrim_memory.db
```

The L1 database contains:

| Table | Purpose |
|---|---|
| `facts` | fact records, ESM state, source, confidence, claim type, source status, significance |
| `l3_outbox` | retry queue for facts that passed validation but failed L3 promotion |
| `erasure_log` | GDPR Art. 17 deletion tombstones without restoring erased content |
| `audit_log` | tamper-evident hash-chained compliance events |

L1 is persistent, but L1 is **not automatically canonical truth**. It is the working/pending layer.

---

## 3. L3 SQLite graph: persistent canonical memory

The dependency-free persistent L3 backend is `SqliteL3Graph` in `core/l3_graph.py`.

Recommended local-first configuration:

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/velantrim_l3.db
```

The SQLite L3 graph stores:

| Table | Purpose |
|---|---|
| `nodes` | canonical fact nodes |
| `vectors` | stored vectors / hash embeddings for recall |
| `edges` | graph relations between facts |
| `entities` | first-class entity nodes such as people and places |
| `mentions` | fact → entity links |
| `meta` | backend metadata, including embedder fingerprint |

If `VELANTRIM_L3_PATH=:memory:` is used, the L3 graph is ephemeral and will not survive restart.

---

## 4. Canonical write path

A fact becomes canonical only through the validated pipeline:

```text
Query / Input
  ↓
Retrieval / Ingest
  ↓
FactsPack
  ↓
Trace
  ↓
Guardian
  ↓
TruthGate
  ↓
ESM transition to Validated
  ↓
L3 graph merge
```

A direct write to L3 without TruthGate is an architectural violation.

---

## 5. Persistent does not mean immutable

A persistent fact can still be:

- superseded;
- contradicted;
- deprecated;
- restricted from processing;
- erased under GDPR Art. 17;
- moved through the ESM lifecycle.

Immutability is a separate rule. Ring Zero / Values Core facts are protected through the `ImmutableCore` / immutable-fact guard.

---

## 6. Current guarantees

Current implementation provides:

- persistent L1 working memory through SQLite;
- persistent L3 canonical graph through `SqliteL3Graph` / optional persistent graph backends;
- WAL-enabled SQLite connections for safer concurrent read/write behavior;
- persistent outbox for self-healing L3 promotion failures;
- persistent deletion tombstones;
- persistent tamper-evident audit chain;
- embedder fingerprint persistence in SQLite L3 metadata.

---

## 7. Current limitations

The project has persistent memory, but it is not yet a complete autobiographical exocortex memory.

Still needed for a fuller long-term memory system:

1. **Source / chunk / span evidence store**  
   Facts should point to exact source spans, not only high-level source strings.

2. **Autobiographical timeline**  
   A first-class event timeline for personal episodes, life history, and temporal continuity.

3. **Semantic deduplication**  
   Near-duplicate facts should merge or link instead of accumulating as noise.

4. **Consolidation cycle**  
   A regular process that reviews pending facts, conflicts, decay, and significance.

5. **Backup and export policy**  
   Persistent memory should have explicit backup, restore, encryption, and migration procedures.

---

## 8. Recommended invariant wording

```text
L0 is volatile.
L1 is persistent working memory.
L3 is persistent canonical memory only when backed by sqlite/ladybug/neo4j.
Mock L3 is not persistent.
Persistence is not truth.
Truth requires Guardian + TruthGate + Trace.
Immutability requires Ring Zero / ImmutableCore.
```

---

## 9. Quick check commands

```bash
# Persistent local-first canonical graph
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/velantrim_l3.db \
velantrim ask "how does water behave"

# L1 working memory file
ls ./data/velantrim_memory.db

# L3 canonical graph file
ls ./data/velantrim_l3.db
```

---

## 10. Summary

Velantrim already has persistent memory.

The current model is:

```text
L1 SQLite = persistent working / pending memory
L3 Graph   = persistent canonical memory when configured with a persistent backend
L0 RAM     = temporary process cache
```

The next architectural step is to evolve persistent storage into a full **long-term exocortex memory** with exact evidence spans, autobiographical timelines, semantic deduplication, and scheduled consolidation.
