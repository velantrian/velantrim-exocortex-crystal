# Crystal — Substrate-Neutral Projection

**Status:** Documentation-only architectural projection. Not a new runtime, milestone, Canon policy, or authorization.

Crystal's durable architectural meaning is not SQLite, PostgreSQL, vectors, graphs, RAG, Python, or any particular model/provider.

For a declared scope, a replacement implementation should preserve these distinctions:

```text
retrieved/relevant candidate != evidence
observation != admitted claim
admitted claim != truth
provenance record != proof of correctness
integrity != truth
receipt != truth
read-side output != Canon write
capability to write != authority to write
```

The technology-neutral obligation is to make provenance, evidence state, admission boundaries, uncertainty, revision/lineage, and bounded trusted-write authority representable and inspectable without silently promoting retrieval or model output into truth.

A future substrate may implement these obligations differently. If it silently collapses candidate discovery, evidence admission, truth evaluation, and trusted mutation into one step, it is not semantically equivalent to Crystal for that scope even if final answers look similar.

Cross-project orientation and conformance checklist live in `velantrian/velantrim`; owning Crystal specifications remain authoritative for Crystal-specific semantics.
