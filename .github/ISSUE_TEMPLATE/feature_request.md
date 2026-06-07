---
name: Feature request
description: Propose a feature or improvement for Velantrim Crystal
title: "feat: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Please keep proposals aligned with the core invariants: Graph = Truth, local-first defaults, provenance-first memory and no silent L3 writes.
  - type: textarea
    id: problem
    attributes:
      label: Problem / use case
      description: What problem does this solve?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposed solution
      description: What should change?
    validations:
      required: true
  - type: dropdown
    id: area
    attributes:
      label: Area
      options:
        - Evidence / provenance
        - External ingestion
        - Evaluation
        - Local-first storage
        - GDPR / privacy
        - MCP / integration
        - Documentation
        - Optional backend
        - Browser/PWA companion demo
        - Other
  - type: textarea
    id: invariants
    attributes:
      label: Invariant impact
      description: Does this affect TruthGate, L3 writes, source tracking, privacy, receipts or optional external services?
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
---
