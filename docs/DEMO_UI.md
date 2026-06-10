# Browser and PWA Companion Demo

This document defines how visual demos should relate to Velantrim Crystal.

## Purpose

A browser or PWA demo can help reviewers understand the memory-first interaction model visually.

It may show:

- local memory screens
- settings and provider controls
- notes and files
- fact extraction
- retrieval
- trace or receipt views
- offline-oriented behaviour

## Boundary

```text
Crystal = audited local-first verifiable memory core
Browser/PWA = optional visual companion
```

The UI is only a demonstration layer unless it is connected to the Crystal backend and uses the same TruthGate, provenance and receipt logic.

## Built-in review UI (Crystal, WP2)

Crystal itself ships one first-party UI: the curator review Kanban at
`GET /review/ui` on the optional FastAPI service (`pip install ".[api]"`,
then `velantrim-api`). It is a single static HTML shell
(`core/_webui/review.html`) with no build step, no external assets and no
embedded data.

Security boundary:

- the shell contains **no claims, fact ids or local memory content** (tested);
  everything it displays is fetched client-side from the `/review/*` JSON
  endpoints;
- with `VELANTRIM_API_TOKEN` set, those endpoints — GET and POST — require a
  Bearer token; the UI asks once and keeps it in `sessionStorage` (it dies
  with the tab), the curator name lives in `localStorage`;
- the service binds to `127.0.0.1` by default and should stay localhost-only
  (see [SECURITY.md](../SECURITY.md));
- there is no drag-and-drop: the only legal "moves" are the audited
  approve / reject / force-approve transitions, and force approval demands an
  explicit reason in a confirmation dialog (audited as
  `review_force_approve`).

## Recommended demo story

A good demo should show one small workflow:

```text
1. User enters a fact or imports a note.
2. The system extracts a claim.
3. The claim receives source metadata.
4. TruthGate decides whether it can enter canonical memory.
5. The user asks later.
6. The answer returns with trace or receipt.
```

## Screenshots to include

- dashboard or console home
- memory or facts screen
- settings or provider controls
- trace or receipt screen
- example answer using stored memory

## What not to claim

The UI should not claim that it is the full Crystal core unless backend integration is active and verified.

## Grant use

For grant reviewers, the demo should be framed as a visual explanation layer. The repository remains the auditable implementation of the core memory architecture.
