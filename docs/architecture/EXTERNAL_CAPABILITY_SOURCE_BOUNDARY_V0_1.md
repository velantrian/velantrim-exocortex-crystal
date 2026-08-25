# External Capability / Source Boundary v0.1

Status: BOUNDED ARCHITECTURAL DECISION
Date: 2026-08-24

Crystal may borrow manifest-first discovery ideas from external operational systems such as OpenClaw only for bounded source/adaptor inspection.

## Authority

Crystal remains the owner of trusted evidence, provenance, admission, audit, and bounded Canon writes. External manifests, plugins, channels, sessions, schedulers, tools, or gateways do not gain epistemic authority by being discoverable or executable elsewhere.

`discovered != admitted`

`retrieved != evidence`

`evidence != truth`

`adapter metadata != Canon authority`

## Allowed donor patterns

- inspect adapter/source metadata before loading runtime code;
- typed, versioned source manifests;
- explicit enable/disable state;
- declared input type, limits, provenance expectations, and side effects;
- immutable metadata snapshot for one read/admission attempt;
- fail-closed behavior for unknown/invalid manifest fields.

## Explicitly out of scope

- chat/channel routing;
- cron or autonomous scheduling;
- multi-agent delegation;
- native in-process third-party plugin trust;
- provider/model routing;
- identity/persona semantics;
- bypass of Guardian, TruthGate, admission, provenance, or Canon boundaries.

## Reuse-first rule

Any future external-source manifest must extend the existing bounded Reader/source path rather than create a second ingestion or Reader pipeline.

The existing local-file and PDF source bridges remain pre-admission/read-side mechanisms. Manifest support may describe them; it must not silently widen them to network ingestion or trusted writes.

## Minimum manifest semantics if implemented

A future source manifest should declare at least:

- `source_kind`;
- `semantic_version`;
- `input_media_types`;
- `network_required`;
- `max_bytes` / other bounded resource limits;
- `side_effects`;
- `provenance_contract`;
- `authority` explicitly fixed to `NONE` for discovery/read-side adapters;
- `runtime_loader` identity/version, if any.

## Safety properties

- manifest inspection must not execute untrusted source code;
- unknown source kind fails closed;
- declared `authority` cannot elevate Crystal admission policy;
- network-disabled source cannot become network-enabled through configuration drift;
- bytes/digest/locator provenance remains tied to the exact captured source used by Reader;
- successful parsing does not imply evidence admission or Canon write.

This document records an architectural boundary only. It does not authorize new runtime, provider, OCR, DOCX/EPUB, network ingestion, or production behavior.
