# Crystal Reader PDF Source Bridge v0.1

**Status:** MERGED / IN MAIN · NOT RUNTIME-AUTHORIZED  
**Merged:** PR #458 · exact reviewed head `5f3aeed2830966b55605e7a79ef2acc48d94b490` · signed merge `ca1d0e2b9b1948c3cb1502a8cd029d82922d0961`  
**Validation:** exact-head CI #1803 / run `32725224598` — 9/9 SUCCESS; bounded review `5007665602` — PASS, P0=0/P1=0  
**Scope:** local read-side PDF preparation for the existing Reader Product Bridge

## Path

```text
local .pdf
   ↓ bounded binary read
exact captured PDF-byte snapshot
   ↓ SHA-256 + file URI
same captured bytes → optional low-level pypdf extraction
   ↓
page text + pdf:page:N locators
   ↓
DocumentStructuralMap
   ↓
ReaderSession
   ↓
existing ReaderProductBridge
   ↓
caller-supplied RegionExecutor
```

## Boundedness

v0.1 has three independent local preparation ceilings:

- `DEFAULT_MAX_PDF_BYTES = 20_000_000`;
- `DEFAULT_MAX_PDF_PAGES = 512`;
- `DEFAULT_MAX_EXTRACTED_CHARS = 2_000_000`.

The byte ceiling is enforced before and during the read. Page count is checked before the page collection is materialized or page text extraction begins. Extracted characters are accumulated page-by-page and fail closed when the ceiling is crossed.

These limits do **not** claim a token, time, provider-cost, semantic-executor, parser-internal decompression/transient-memory, or total Reader-work budget.

## Source identity and replay

PDF source identity is SHA-256 of the exact captured PDF bytes, not of extracted text. The same captured byte snapshot is passed to `pypdf`; the parser does not reopen the source path after identity is established. This prevents a file-change race from pairing one PDF hash with text extracted from different bytes.

Because character offsets in extracted text are not offsets into PDF bytes, v0.1 does not invent exact spans. Pages use explicit structural locators:

```text
pdf:document
pdf:page:1
pdf:page:2
...
```

Extracted page text is retained only in the foreground prepared object so the caller-supplied Reader executor can replay the page text associated with each locator.

## Fail-closed cases

Preparation rejects:

- missing/non-file/non-PDF paths;
- files beyond the byte ceiling;
- invalid PDF signature;
- parser-open failures;
- encrypted PDFs;
- zero-page PDFs;
- page counts beyond the ceiling;
- page extraction failures;
- extracted text beyond the character ceiling;
- PDFs with no extractable text.

Scanned/image-only PDFs therefore fail closed in v0.1. OCR is a separate future stage.

## Dependency and authority boundary

Crystal already declares optional `pypdf` support for WP4 knowledge adapters. Reader PDF v0.1 may use the same low-level third-party library but **does not import or reuse `core.adapters`**.

```text
same parser library != same ingest authority
PDF extracted text != admitted evidence
page locator != claim
Reader result != verified fact
Reader result != Canon
merge != production authorization
```

No TruthGate, Guardian, memory, ingest, pipeline, embedding, model/provider, remote-egress, persistence, vector retrieval or background-worker integration is added.

## Merge evidence

PR #458 was guarded-merged from exact reviewed head `5f3aeed2830966b55605e7a79ef2acc48d94b490` onto unchanged tested base `fea1971ebf2420df8c677a1d0a4c74c18700d095`. Final pre-merge exact-head CI #1803 / run `32725224598` completed 9/9 SUCCESS. Fresh bounded review `5007665602` found no remaining P0/P1 blocker. The resulting merge commit `ca1d0e2b9b1948c3cb1502a8cd029d82922d0961` is signed and verified.

No separate post-merge CI is claimed here unless independently observed. Merge records repository lifecycle state only; it does not authorize production/runtime activation, evidence admission, Canon writes, OCR, DOCX/EPUB, or semantic/model execution.

## Explicit non-goals

- OCR / image understanding;
- layout reconstruction, tables or figures;
- DOCX / EPUB;
- semantic/model execution;
- CLI/API;
- memory/evidence admission;
- Canon writes;
- production authorization.
