# Reader File Source Bridge v0.1

## Status

`PROPOSED ON BRANCH · GITHUB_AND_NOTION · NOT AUTHORITATIVE MAIN UNTIL MERGED`

Target baseline at branch creation:

`main@b28899989a0af67ed397264bb73cac8e970b101c`

## Problem

Reader Product Bridge v0.1 can orchestrate an existing `ReaderSession` and
`DocumentStructuralMap`, but an ordinary local text file still has to be converted into
those contracts by a caller. Crystal also has older WP4 knowledge-ingest adapters for PDF
and EPUB. Those adapters feed knowledge-ingest semantics and must not silently become
Reader authority.

## Decision

Add a separate read-side `core/reader_file_source.py` preparation layer for local UTF-8
`.txt` and `.md` files.

The v0.1 flow is:

```text
local UTF-8 TXT / Markdown file
  -> bounded local byte read
  -> exact SourceVersion hash + file URI
  -> deterministic blank-line paragraph spans
  -> DocumentStructuralMap
  -> ReaderSession
  -> existing ReaderProductBridge
  -> caller-supplied RegionExecutor
```

The prepared foreground object retains source text only so the caller-supplied executor
can replay exact node spans with `text_for(node)`. It does not persist, admit, index, embed,
or transmit the text.

## Boundedness

`DEFAULT_MAX_SOURCE_BYTES = 2_000_000` bounds only local file loading. The limit is checked
before and after the byte read so a file growth race cannot silently bypass it.

This does **not** claim a character, token, time, provider-cost, target-count, or executor
budget for Reader Product Bridge. Those remain separate decisions.

## Supported v0.1 surface

- `.txt` — UTF-8 only;
- `.md` — UTF-8 only;
- deterministic paragraph regions separated by blank lines;
- exact half-open character spans over the decoded source text;
- local `file://` source identity;
- caller-provided objective, optional document/session identity, restricted flag and
  sensitivity label;
- existing one-broad-pass / at-most-one-targeted-reread product bridge.

## Explicitly not included

- PDF Reader parsing;
- EPUB Reader parsing;
- DOCX Reader parsing;
- OCR, images, tables or layout reconstruction;
- Markdown AST/heading hierarchy;
- model/provider selection;
- semantic extraction or synthesis;
- vector/semantic retrieval;
- network access or remote egress;
- persistence, scheduler or background worker;
- `/learn`, knowledge ingest or WP4 adapter reuse;
- TruthGate, Guardian, memory or Canon writes;
- production/runtime authorization.

PDF and EPUB already have optional **knowledge-ingest** dependencies elsewhere in Crystal.
They are intentionally not imported here. A future Reader parser may reuse a low-level
library only under a separate reviewed Reader contract; it may not reuse ingest authority.

## Authority invariants

```text
file text != admitted evidence
paragraph region != claim
Reader processing != truth verification
Reader Product Result != Canon
WP4 ingest adapter != Reader parser authority
local file load != memory admission
merge != production authorization
```

## Failure behavior

The loader fails closed for:

- missing paths;
- non-file paths;
- unsupported extensions;
- files above the explicit byte ceiling;
- invalid UTF-8;
- whitespace-only sources;
- node replay against another source version;
- Reader file nodes without exact spans.

No fallback to knowledge ingest, lossy decoding, remote parsing, or another file type is
performed.

## Next separately reviewed stages

Possible follow-ups, none authorized by v0.1:

1. PDF/EPUB read-side parsers with exact/replayable locators;
2. DOCX support behind an explicit optional dependency decision;
3. a user-facing Reader CLI;
4. a bounded semantic executor/provider contract;
5. richer Markdown structural recovery;
6. explicit executor/resource budgeting.
