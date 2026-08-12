<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-translation-source: docs/GLOSSARY.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
# Глоссарий Crystal — RC-6

**physical L3** — multi-status storage; не strict Canon.  
**strict Canon** — trusted deny-dominant read projection.  
**source owner** — чья позиция представлена proposition.  
**proposition presentation category** — source presentation (`FACTUAL_ASSERTION`, opinion, hypothesis, conditional и др.), не verification.

RC-1, RC-2, RC-3, RC-4, RC-5, RC-6 — bounded Reader layers; dedicated/full Reader not implemented.

`POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` — RC-5 relation candidates, не resolved truth.

**Reader working set** — RC-6 bounded context snapshot direct RC-4 leaves.  
**candidate atomicity** — candidate и direct locators не разделяются.  
**SUMMARY** — caller-supplied synthesis с direct leaf provenance, не evidence/truth.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != evidence
summary != verified fact
```

SQLite ordinary active local-first; PostgreSQL `active=false`. NLnet `submitted / under review / not awarded`; €50,000 planning only; budget change: none; award: not awarded.
