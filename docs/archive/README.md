# Archive — historical design material

This directory holds **historical** artifacts from earlier design sprints. They
are kept for provenance and audit-trail continuity only.

## Status

- **Historical only.** These files record an earlier design snapshot and do not
  track the current implementation.
- **Not canonical.** Nothing here is part of the audited Crystal release
  boundary, the runtime, or the L3 canon. It has not passed the TruthGate,
  schema validation, deduplication, or provenance checks.
- **Not reviewer claim material.** Do not cite these files as evidence of
  implemented capability, test coverage, or maturity. For the current state of
  the project, see [`TEST_REPORT.md`](../../TEST_REPORT.md),
  [`docs/STATUS.md`](../STATUS.md), and
  [`docs/IMPLEMENTATION_REALITY_MATRIX.md`](../IMPLEMENTATION_REALITY_MATRIX.md).

## Contents

| File | What it is |
|---|---|
| `Velantrim_V8_Crystal_Sprint1.jsonl` | A raw Sprint 1 design dump (RFC-style chunks). Retained as an audit note; CI still validates its JSONL integrity (parse + required fields + duplicate `chunk_id`) so the archived artifact does not silently rot. |
| `Velantrim_V8_Crystal_Sprint1_toc.md` | The generated table of contents for the dump above. |

If you are looking for the architecture as it exists today, start from
[`docs/ARCHITECTURE.md`](../ARCHITECTURE.md), not the files in this directory.
