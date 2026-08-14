# Crystal RFC contracts

This directory contains bounded architecture contracts that are **not runtime claims by default**.

Current entry:

- [`RFC_EPIS_001_EPISTEMIC_ROUTER.md`](./RFC_EPIS_001_EPISTEMIC_ROUTER.md) — Epistemic Router / Evidence State Layer; architecture contract only, runtime not implemented.
- [`EPIS_001_STATUS.json`](./EPIS_001_STATUS.json) — machine-readable architecture/runtime-authority status for EPIS-001.

## Authority rule

An RFC may define a future contract without implementing it. Check live GitHub, runtime code/tests, exact CI, and machine implementation truth before treating any RFC capability as available.

```text
architecture contract != runtime implementation
architecture contract != runtime authorization
```
