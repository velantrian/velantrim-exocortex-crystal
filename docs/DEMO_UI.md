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
