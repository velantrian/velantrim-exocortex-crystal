# Explicit conflict-resolution surfaces

Crystal does not treat a contradiction as a normal approval. A curator must
select one explicit disposition and provide an accountable actor and reason.

## CLI

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "the claims describe different contexts" \
  --expected-report-id REPORT_ID
```

For `SUPERSEDE`, repeat `--target` for every canonical fact selected for
deprecation:

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition SUPERSEDE \
  --actor alice \
  --reason "newer independently verified evidence" \
  --target OLD_FACT_ID \
  --expected-report-id REPORT_ID
```

Exit codes:

- `0`: decision applied;
- `1`: core rejected or could not apply the decision;
- `2`: malformed public input.

## HTTP

The host FastAPI application registers the route with its existing bearer-token
dependency:

```python
from core.conflict_surfaces import register_conflict_routes

register_conflict_routes(app, dependencies=[Depends(require_api_token)])
```

This exposes:

```text
POST /review/resolve-conflict
```

Example body:

```json
{
  "fact_id": "ing:...",
  "disposition": "CONTEXTUALIZE",
  "actor": "alice",
  "reason": "the claims apply to different jurisdictions",
  "target_fact_ids": [],
  "expected_report_id": "sha256:..."
}
```

The helper fails closed when no authentication dependency is supplied. An
unguarded route is available only through the explicit
`allow_unguarded_local=True` development option.

Both surfaces delegate directly to `core.review.resolve_conflict`; they do not
create an alternate admission or Canon write path.
