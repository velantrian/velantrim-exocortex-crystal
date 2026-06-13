# TRACE Visualization

## Status

Reviewer tooling — read-only formatter. Not a runtime component.

## Purpose

Make TRACE / Receipt paths inspectable for reviewers and operators.

## What it does

- Reads a receipt / trace JSON file
- Exports a Markdown evidence tree
- Exports a DOT graph for static rendering
- Helps inspect provenance and boundary decisions

## What it does not do

- Does not verify truth
- Does not modify memory
- Does not write to L3
- Does not bypass TruthGate
- Does not replace receipt verification

Trace visualization observes. It does not verify. It does not promote. It does not write. It does not change truth.

## Usage

```bash
python scripts/trace_visualize.py receipt.json --format markdown
python scripts/trace_visualize.py receipt.json --format dot
python scripts/trace_visualize.py receipt.json --format markdown --out trace.md
python scripts/trace_visualize.py receipt.json --format dot --out trace.dot
```

## Reviewer value

This helps reviewers see why Velantrim differs from ordinary RAG: retrieval candidates are not trusted until boundary checks and receipts are present. The evidence path — query → claim → source → boundary decision → receipt — is made visible without modifying the underlying system.

## Security / privacy note

The formatter only uses data already present in the public receipt fields (query, answer, citation IDs, truth statuses, source names). It does not access raw memory, private payloads, or claim text beyond what the receipt already exposes.
