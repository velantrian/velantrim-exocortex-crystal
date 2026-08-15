<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- current-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
<!-- d5-locale: ja -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
# 🇯🇵 Crystal Extended Reference Guide

このページは日本語の extended reference surface です。historical RC-5 compatibility vocabulary を保持しながら、現在の post-RC-9 / post-NLI / RRTIC-v1 architecture truth を明示します。

## 📖 Reader progression

```text
RC-1 source-linked skeleton
→ RC-2 structural map
→ RC-3 multi-pass mechanics
→ RC-4 proposition extraction
→ RC-5 relation candidates
→ RC-6 bounded long-context working sets
→ RC-7 explicit cross-document candidates
→ RC-9 deterministic lexical PRE-ADMISSION discovery
```

RC-1…RC-7 と RC-9 は bounded implemented components/layers。`dedicated_reader_core=false`。

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
```

## 🧩 Historical RC-5 relation vocabulary

次の presentation/inspection categories は compatibility vocabulary として保持されます。

```text
POSSIBLE_CONTRADICTION
EXCEPTION
QUALIFICATION
TENSION
```

adjudicated truth を意味せず、Evidence Admission や Canon mutation を自動生成しません。

## 🔬 Current post-RC-9 evidence chain

```text
RC-9 lexical baseline
        ↓
Comparator v1
semantic recall recovered · discrimination FAIL
        ↓
NLI neutral-filter v1
discrimination improved · recall-safety FAIL
        ↓
architecture reassessment
        ↓
RRTIC-v1
architecture contract only
```

Comparator classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`。

RRTIC-v1 は typed suspicion/qualifier inspection contract。model、reranker、truth score、accept/reject policy、Evidence Admission、Contradiction Adjudication、Canon writer は提供しません。

## 🛡 Authority firewall

```text
retrieval match != evidence
similarity != identity
repetition != corroboration
ranking != epistemic authority
candidate discovery != candidate adjudication
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

## 🏛 Authority roles

```text
Guardian      = structural integrity / structural policy boundary
TruthGate     = L3 admission authority
TrustSnapshot = deny-dominant reconciliation surface
CanonicalView = strict trusted read-time projection
TRACE         = provenance / replay evidence, not proof of truth
```

Discovery/inspection components はこれらの authority roles を継承しません。

## 💾 Storage truth

```text
SQLite ordinary local-first = ACTIVE
PostgreSQL/pgvector = INACTIVE
active=false
successful import != backend activation
physical L3 != strict Canon
```

PostgreSQL/pgvector は inactive import/equivalence target であり、active Reader backend、automatic cutover、rollback、dual-write を意味しません。

## 💶 Grant truth

NLnet NGI0 Commons Fund: **submitted / under review / not awarded**。約 **€50,000** は planning context。**budget change: none**。

## 🌍 Localization state vocabulary

`CURRENT` = recorded source contract に対する technical parity/freshness。  
`REFRESH_NEEDED` = translation 自体は有用だが Reader-dependent semantics が現在の source に遅れている状態。  
どちらも native-speaker editorial certification ではありません。

Japanese はこの refresh 後 `CURRENT`。残る Reader-dependent root/detail refresh backlog は Arabic と Hindi です。

## 🚫 Non-claims

この extended reference は semantic/hybrid/vector Reader runtime、NLI runtime filter、RRTIC runtime provider、active PostgreSQL/pgvector Reader selection、automatic proposition identity、automatic corroboration、universal truth、zero hallucinations、legal/security/GDPR certification を主張しません。

English policy source: [`docs/EXTENDED_REFERENCE_POLICY.md`](../EXTENDED_REFERENCE_POLICY.md)。