# NLnet Reviewer Q&A — Velantrim Crystal

Internal preparation for likely reviewer questions. These answers are written against current
public repository truth, not application-era snapshots. Where something is a proposed funded
delta rather than existing code, it is labelled as such.

The canonical existing-vs-future contract is
[baseline-funded-delta-matrix.md](./baseline-funded-delta-matrix.md).

---

### Q1. How is Crystal different from ordinary RAG, vector stores or chatbot memory?

Crystal separates **retrieval from epistemic authority**. Physical L3 is multi-status storage,
while strict read membership is a separately reconciled projection under Guardian/TruthGate
boundaries. Retrieval rank, similarity, repetition and model confidence do not become evidence
or truth by themselves.

```text
retrieval match != evidence
similarity      != identity
ranking         != epistemic authority
```

The project also preserves source/provenance and replayable proof artifacts. Existing admitted-
memory vector/query retrieval is allowed to retrieve; it is not allowed to silently promote
retrieved material into verified knowledge.

### Q2. What is the concrete funding objective?

A reproducible, deployable, local-first open-source MVP whose **new funded delta** can be checked
against public acceptance evidence. Potential work envelopes include deployment/setup hardening,
service-layer hardening, stronger source-span/receipt replay, larger evaluation gates,
knowledge/adapters, multilingual access and reviewer onboarding.

The precise paid delta must be frozen against live `main` at agreement time. Existing code is
not counted again as future delivery.

### Q3. What already works today, before any funding agreement?

Crystal already has a tested local-first memory/evidence core, explicit Guardian/TruthGate and
strict-read boundaries, provenance/receipt infrastructure, query surfaces, SQLite storage and
an inactive PostgreSQL/pgvector import/equivalence target with `active=false`.

The Reader foundation has also advanced through **RC-9**:

- RC-1..RC-3: source/session/structure + explicit multi-pass mechanics;
- RC-4: source-linked proposition candidates;
- RC-5: bounded relation candidates;
- RC-6: bounded long-context working sets and caller-supplied summaries;
- RC-7: explicit cross-document candidate links;
- RC-8: retrieval architecture decision + frozen adversarial corpus;
- RC-9: offline stdlib-only deterministic BM25 PRE-ADMISSION candidate discovery + benchmark.

`dedicated_reader_core=false` remains correct. PR #378 subsequently merged an RC-10
reuse/comparison preregistration contract only; no semantic/hybrid comparator or Reader retrieval
runtime was executed.

### Q4. What evidence supports the Reader retrieval claim?

The committed RC-9 result is `eval/reader_rc9_lexical_baseline.json`, generated from the frozen
20-case synthetic/adversarial RC-8 paired corpus at K=5:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Paired hard-negative hits | 4 / 4 |

The cross-lingual pair `rc8-004` is missed; all four paired hard negatives surface in top-5.
Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

This is intentionally not presented as “94% accuracy”. Recall@5, Precision@5 and MRR are
retrieval metrics under the documented paired benchmark construction. They do not measure
semantic equivalence, truth, evidence admission or contradiction correctness.

### Q5. Why request funding if a substantial baseline already exists?

Because the proposed value is the **new measurable engineering delta**, not payment for prior
work. The accounting invariant is:

```text
verified baseline at agreement time
+
new independently testable funded delta
=
public deliverable
```

Approx. €50,000 is planning context only. The proposal is submitted / under review / not
awarded; no approved budget or payment commitment is claimed.

### Q6. Does RC-9 mean semantic/vector retrieval is now required?

No. RC-9 deliberately implemented the deterministic lexical baseline first. Its result shows
both strengths and measurable gaps: the cross-lingual pair is missed and lexical hard negatives
surface aggressively.

That evidence supports future research decisions, not a predetermined backend choice. Embeddings,
semantic/hybrid retrieval, ANN/vector DB and Reader FTS remain separate future possibilities
requiring their own authorization, dependency/privacy/resource review and stronger evaluation.

### Q7. But Crystal already has embedding/vector code — is that Reader vector retrieval?

No. Crystal has older/general **admitted-memory** retrieval machinery in modules such as
`core/embedding.py`, `core/query_pipeline.py`, `core/legacy_retrieval.py` and `core/rrf.py`.
Reader RC-9 operates on PRE-ADMISSION proposition snapshots upstream of evidence/admission.

These domains may share helpers only after explicit compatibility review. Existing admitted-
memory vector capability must not be presented as Reader semantic/identity authority.

### Q8. How do you validate claims instead of just asserting them?

Through named code paths, frozen machine-readable artifacts, tests, exact-head CI, post-merge CI
and explicit limitations. For RC-9, the benchmark runner is reproducible:

```bash
python scripts/bench_reader_rc9_lexical.py \
  --corpus eval/reader_rc8_retrieval_adversarial.jsonl \
  --k 5 \
  --json-out /tmp/reader-rc9-lexical.json
```

The repository-wide CI also maintains Python 3.11/3.12 coverage, Ring Zero, code-quality,
security, eval, JSONL-integrity, Docker and docs-status gates.

### Q9. What are the main architecture safety boundaries?

```text
physical L3             != strict Canon
Reader candidate        != admitted evidence
cross-document candidate != Canon relation
retrieval match         != evidence
similarity              != identity
repetition              != corroboration
ranking                 != epistemic authority
candidate discovery     != candidate adjudication
comparison pass         != runtime authorization
```

No Reader retrieval result is allowed to become a truth/evidence/Canon verdict merely because
it ranks highly.

### Q10. What is the privacy/security position?

Crystal is local-first by design and the ordinary active path uses SQLite. PostgreSQL/pgvector
remains inactive `active=false`. Local-first can reduce unnecessary external data transfer, but
it does **not** itself prove GDPR compliance or complete security.

The project does not claim legal certification, zero privacy risk or production multi-tenant
security. Known PII/supply-chain hygiene remains separate under #214.

### Q11. What are the main residual risks?

- Reader is bounded rather than autonomous (`dedicated_reader_core=false`).
- RC-9 benchmark is small, frozen and synthetic/paired rather than production-scale.
- cross-lingual / low-overlap lexical recall remains incomplete;
- high-overlap hard negatives remain a retrieval risk;
- Reader semantic/hybrid/vector retrieval and automatic identity/adjudication are not implemented;
- PostgreSQL/pgvector is not active runtime;
- security/supply-chain debt remains under #214;
- #155 and #165 remain separate architecture/data-lifecycle backlogs;
- localized Reader-dependent documentation has explicit refresh debt.

### Q12. What is explicitly not promised?

Crystal does not claim semantic understanding, automatic truth verification, automatic claim
identity, automatic corroboration, contradiction resolution, autonomous evidence admission,
zero hallucinations, universal truth, full security/GDPR certification, production-grade
semantic search or a completed autonomous Reader.

---

## One-line positioning

> **Velantrim Crystal is open-source, local-first memory and Reader infrastructure that makes
> source/provenance and authority boundaries explicit, measures retrieval before promoting new
> machinery, and keeps candidate discovery separate from evidence and Canon authority.**
