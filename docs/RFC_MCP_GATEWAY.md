# RFC: MCP Gateway and Capability-Based Agent Access

**Status:** Proposed  
**Scope:** Architecture / access-control layer  
**Runtime impact:** None until implemented  
**Grant relevance:** Verifiable AI memory, controlled agent access, auditability, GDPR-aligned separation of duties

---

## 1. Purpose

Velantrim ExoCortex is designed as verifiable memory infrastructure where the canonical graph remains the source of truth and language models act only as language or proposal layers.

This RFC proposes an optional **MCP Gateway** layer that exposes Velantrim memory capabilities to external AI clients and agents through explicit role-based and capability-based access.

The goal is to make memory access visible, limited, auditable, and aligned with the existing Velantrim architecture.

---

## 2. Core Principle

```text
Graph = Truth
MCP = Controlled Access Layer
Guardian = Permission and Safety Gate
TruthGate = Canonical Write Gate
Trace = Accountability Path
LLM = Language / Proposal Layer
```

MCP must not become the source of truth.

The canonical memory remains the L3 graph. Any operation that may affect canonical truth must pass through Guardian, TruthGate, provenance checks, and trace construction.

---

## 3. Capability-Based Tool Registration

Velantrim should expose tools according to role and capability, not merely rely on runtime warnings.

A client should receive only the capabilities it is structurally allowed to use.

### Proposed roles

| Role | Intended access | Canonical write access |
|---|---|---:|
| `reader` | Read L3 facts, traces, evidence, receipts | No |
| `researcher` | Propose hypotheses and relations | No |
| `ingester` | Add observations to L1/L2 Pending | No |
| `guardian` | Review and promote validated knowledge | Controlled |
| `admin` | Maintenance and audit workflows | Controlled / audited |

### Access rule

```text
role -> registered capabilities -> allowed operations
```

This keeps the public interface aligned with the internal Velantrim rule: no canonical mutation without review, trace, and gatekeeping.

---

## 4. Typed Edge Registry

Graph mutation should not be arbitrary.

Velantrim should maintain an explicit edge registry that defines the semantics of each relation type.

Example edge types:

```text
SUPPORTS
CONTRADICTS
REQUIRES
DERIVED_FROM
CAUSES
ENABLES
BLOCKS
MENTIONS
CO_OCCURRED
ANALOGOUS_TO
SUPERSEDED_BY
```

Each edge type should define:

```text
edge_type
direction_rule
weight
truth_effect
allowed_claim_types
source_required
review_required
reversible
```

This prevents the graph from becoming a noisy collection of unlabeled associations.

---

## 5. Graph Observability and Integrity

A verifiable memory system must expose its structural health.

The MCP layer and CLI should eventually expose read-only diagnostic capabilities such as:

```text
graph statistics
path lookup
neighbor lookup
contradiction report
duplicate edge report
duplicate claim report
dangling edge report
L1/L3 consistency report
missing evidence report
restriction consistency report
```

A CLI equivalent should also exist:

```bash
velantrim integrity
```

Expected report shape:

```json
{
  "dangling_edges": [],
  "orphan_nodes": [],
  "duplicate_claims": [],
  "duplicate_edges": [],
  "wrong_direction_edges": [],
  "contradictions": [],
  "l1_l3_mismatches": [],
  "restricted_mismatches": [],
  "missing_evidence_ref": []
}
```

This supports grant-facing claims around transparency, auditability, and verifiable AI memory.

---

## 6. LLM-Generated Relations Are Hypotheses

If an LLM proposes an edge, classifies a relation, or infers a causal link, that output must not become canonical truth directly.

Correct path:

```text
LLM-proposed relation
  -> HYPOTHESIS / UNVERIFIED
  -> Pending Layer
  -> Guardian Review
  -> TruthGate
  -> L3 only if validated
```

Forbidden path:

```text
LLM output -> direct FACT edge in L3
```

This preserves the Velantrim invariant that language models may propose, but they do not define truth.

---

## 7. Local-First Constraint

This RFC does not require a cloud database, hosted embeddings provider, or managed AI service.

The preferred Velantrim MVP stack remains:

| Component | Role |
|---|---|
| SQLite | Evidence, audit, trace, L1/Pending, metadata |
| Kuzu / SQLite L3 | Local graph truth store |
| DuckDB | Analytics and evaluation reports |
| MCP Gateway | Optional controlled access interface |
| LLM | Optional language/proposal layer, not truth source |

Cloud services may be used only as explicit opt-in integrations, not as default dependencies.

---

## 8. GDPR and Public-Benefit Relevance

Capability-based access helps Velantrim support GDPR-aligned design principles:

- **data minimisation:** clients receive only the capabilities and data they need;
- **purpose limitation:** roles constrain what an agent may do;
- **auditability:** meaningful operations leave trace and audit records;
- **access control:** canonical writes are restricted and reviewed;
- **local-first operation:** personal memory can remain under user control.

This makes Velantrim suitable as open European infrastructure for verifiable AI memory rather than a generic cloud-first agent framework.

---

## 9. Implementation Roadmap

### Phase 1: Documentation and contracts

- Define roles and capabilities.
- Define MCP naming conventions.
- Define typed edge registry schema.
- Define integrity report schema.

### Phase 2: Read-only MCP gateway

- Expose fact lookup, graph path, graph neighbors, trace lookup, and receipt verification.
- No canonical write tools.

### Phase 3: Pending-only proposal layer

- Allow external agents to propose facts and edges.
- Store outputs as HYPOTHESIS / UNVERIFIED.
- Require source, source_status, claim_type, and trace.

### Phase 4: Guardian-mediated promotion

- Add review and promotion workflows.
- Require Guardian + TruthGate + audit trail.

### Phase 5: Integrity and observability

- Add graph statistics, contradiction reports, duplicate detection, L1/L3 consistency reports, and missing evidence reports.

---

## 10. Summary

The MCP Gateway should be an access-control layer, not a truth layer.

Its value for Velantrim is:

```text
controlled agent access
role-separated memory operations
typed graph mutation contracts
read-only graph observability
auditable promotion from hypothesis to canon
```

This strengthens Velantrim's position as verifiable, local-first AI memory infrastructure.
