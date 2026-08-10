<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Crystal Glossary and Claim-Discipline Guide

**Status date:** 2026-08-10  
**Purpose:** authoritative English terminology source for D4 translations.  
**Authority:** merged implementation, executable tests, exact CI and detailed English contracts remain stronger than this summary.

## Contract names

Programmatic identifiers remain unchanged in code, schemas, CLI, APIs and translated documents.

| Term | Meaning and boundary |
|---|---|
| **claim** | A typed assertion. A claim is not automatically a verified fact. |
| **admission** | A decision allowing a claim to enter a more trusted state or projection. |
| **Guardian** | Structural, safety and policy checks before epistemic admission; not a replacement for TruthGate. |
| **TruthGate** | The controlled epistemic admission boundary; not a universal truth detector. |
| **physical L3** | Multi-status graph-oriented storage and retrieval state. Storage membership is not strict Canon membership. |
| **strict Canon** | The deny-dominant trusted read projection allowed by current evidence and policy. |
| **CanonicalView** | A fail-closed read projection for grounded responses. |
| **TrustSnapshot** | A read-time trusted state view; it does not rewrite physical storage. |
| **TRACE** | Machine-readable grounding path connecting an answer to admitted claims and evidence. |
| **Receipt** | Replayable, tamper-sensitive operation or answer evidence. A migration receipt is not claim evidence. |
| **provenance** | The source, creation path and lifecycle of a claim or artifact. |
| **evidence span** | A source-linked passage supporting a candidate or admitted claim. |
| **source status** | The origin class of a claim, such as external source, user statement or model output. |
| **epistemic state** | The typed status describing how a claim may be treated; not merely a confidence score. |
| **grounding** | Linking an answer to admitted claims, evidence and traceable sources. |
| **FactsPack** | A bounded, traceable context assembled for answering; not an authority owner. |
| **read-only query** | A query contract that cannot mutate facts, ESM, L3, outbox, episode links, embedder identity or candidate state. |
| **fail-closed** | Refusal or bounded failure instead of hidden admission when evidence, policy or state is uncertain. |
| **storage profile** | Durable deployment identity for a backend and non-secret locator; not epistemic authority. |
| **migration bundle** | Deterministic portable operation artifact for approved datasets; not a whole-system truth export. |
| **exact equivalence** | Equality of approved dataset counts, canonical bytes and hashes; not activation or retrieval acceptance. |
| **active=false** | The PostgreSQL target is inactive and cannot serve ordinary runtime reads or writes. |
| **baseline** | Work already merged and independently evidenced before a funded agreement. |
| **funded delta** | New, measurable work beyond the frozen baseline, accepted through public evidence. |
| **deliverable** | A bounded public artifact with explicit acceptance evidence. |
| **local-first** | Data and ordinary operation remain local by default; remote services are optional. |
| **provider independence** | Models and providers are replaceable interfaces and do not own truth authority. |
| **restriction** | A technical limit on use or disclosure of stored material. |
| **erasure** | Removal through implemented active-store lifecycle; independent copies need separate handling. |
| **review queue** | Pending or blocked claims awaiting explicit curator action. |
| **curator override** | An attributed, audited human decision; not a silent TruthGate bypass. |
| **Reader Core RC-1** | Implemented/tested bounded evidence-linked source/session skeleton with source-version identity, locators, fidelity, coverage, bookmarks/open loops and stale/failure/privacy semantics; no truth/admission authority. |
| **Reader Core RC-2** | Implemented/tested caller-supplied Structural Document Map with version-bound hierarchy/order and explicit ambiguity; not an automatic parser and not truth/confidence authority. |
| **dedicated Reader Core** | Future multi-pass Semantic Reading runtime beyond RC-1/RC-2; not implemented. |

## Terms requiring caution

### “Truth” and “canonical graph”

Do not write that every graph node is truth. Preferred wording:

```text
physical L3 stores typed multi-status records
strict Canon is the evidence- and policy-allowed read projection
```

### “Implemented”, “tested”, “current” and “planned”

Use these labels distinctly:

- **implemented** — merged code exists;
- **tested** — named executable evidence exists;
- **current** — reconciled against an exact source checkpoint;
- **planned / research** — no runtime claim.

An open PR, RFC, issue, prototype or Notion page is not current runtime evidence.

### “Reader Core implemented”

Do not collapse the current bounded milestones into a full capability claim. Preferred wording:

```text
RC-1 minimal evidence-linked skeleton = implemented/tested
RC-2 Structural Document Map          = implemented/tested
dedicated multi-pass Reader runtime   = not implemented
coverage                              != comprehension proof
structure/order/prominence            != epistemic authority
```

### “GDPR compliant”, “secure” and “hardened”

Preferred wording:

```text
GDPR-oriented technical controls
security-relevant checks
hardened against documented threats
```

Do not claim legal, GDPR or security certification without external authoritative evidence.

### “Replay”

```text
Receipt replay    = re-check existing evidence
trajectory replay = repeat an execution path for evaluation
```

### “Grant funded” or “awarded”

The current public status is:

```text
submitted / under review / not awarded
```

Merged baseline work cannot be relabelled as future funded delivery. Budget or award state may change only from verified external grant communication.

### “Default backend”

SQLite is the ordinary active local-first profile. First durable `auto` may choose optional LadybugDB when available, otherwise SQLite, and then locks the deployment identity. Explicit Mock is development/CI state. PostgreSQL/pgvector is an inactive `active=false` import/equivalence target, not ordinary runtime.

## Translation rules

- Keep code identifiers and contract names unchanged.
- Translate explanations, not machine identifiers.
- Preserve `physical L3 != strict Canon`.
- Preserve public-query read-only and explicit-ingest write separation.
- Preserve SQLite ordinary runtime and PostgreSQL `active=false`.
- Preserve `import/equivalence != activation`.
- Preserve RC-1/RC-2-bounded-implemented versus dedicated-Reader-not-implemented distinction.
- Preserve `coverage != comprehension proof` and structure/order/prominence != epistemic authority.
- Preserve no-certification and no-award boundaries.
- Do not imply native-speaker editorial certification unless it occurred.

## Authoritative related documents

- [Project, grant and governance summary](./PROJECT_GRANT_AND_GOVERNANCE.md)
- [Full architecture](./ARCHITECTURE.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [Reader implementation status](./IMPLEMENTATION_STATUS.md)
- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Contributing](../CONTRIBUTING.md)
