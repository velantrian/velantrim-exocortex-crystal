---
name: Bug report
description: Report a reproducible problem in Velantrim Crystal
title: "bug: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug. Please do not include secrets, private datasets or personal data.
  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: What happened?
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to reproduce
      description: Minimal commands or code needed to reproduce the issue.
      render: bash
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behaviour
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual behaviour
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version / commit
      placeholder: v0.1.0 or commit SHA
  - type: dropdown
    id: area
    attributes:
      label: Area
      options:
        - Memory L0/L1
        - L3 graph
        - TruthGate / Guardian
        - Retrieval / answer
        - Provenance / receipts
        - External ingestion
        - GDPR / privacy
        - MCP / integration
        - Packaging / CI
        - Documentation
        - Other
  - type: textarea
    id: logs
    attributes:
      label: Logs / output
      render: text
  - type: checkboxes
    id: privacy
    attributes:
      label: Privacy check
      options:
        - label: I removed secrets, API keys, personal data and private datasets from this report.
          required: true
---
