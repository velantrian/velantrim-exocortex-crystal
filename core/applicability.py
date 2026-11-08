"""Query-local applicability, after canonical/evidence admission; never a verdict.

Writers own metadata["applicability"]. These declarations narrow already-admitted
facts; they are not independently verified evidence or an authority grant.
"""
from copy import deepcopy
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional

FIELDS = ("object", "primary_object", "linked_objects", "status_applies_to",
          "observed_at", "date", "recorded_at", "valid_from", "valid_until")


def declarations(record):
    """Read the durable namespace, with legacy top-level declarations supported."""
    metadata = record.get("metadata")
    nested = metadata.get("applicability") if isinstance(metadata, dict) else None
    result = {k: deepcopy(v) for k, v in nested.items() if k in FIELDS} if isinstance(nested, dict) else {}
    # Explicit primary_object, including malformed/empty values, remains decisive.
    for key in FIELDS:
        if key in record:
            result[key] = deepcopy(record[key])
    return result


def embed(fact):
    """Prepare a writer's dict before store_fact drops non-column fields."""
    values = declarations(fact)
    if values:
        metadata = deepcopy(fact.get("metadata", {}))
        metadata["applicability"] = values
        fact["metadata"] = metadata


def lift(target, source):
    """Copy declarations only; never carry verdicts from arbitrary labels."""
    target.update(declarations(source))


def _declared_primary_object(fact):
    value = fact.get("primary_object") if "primary_object" in fact else fact.get("object")
    return value.strip() if isinstance(value, str) and value.strip() else None


def _explicitly_transfers_status_to(fact, asked):
    raw = fact.get("status_applies_to")
    targets = [raw] if isinstance(raw, str) else raw if isinstance(raw, (list, tuple)) else []
    return any(isinstance(v, str) and v.strip() == asked for v in targets)


def object_exclusion(fact, asked):
    declared = _declared_primary_object(fact)
    # Missing or malformed primary identity cannot be repaired by a relation tag.
    if declared is None:
        return "object belonging not established"
    if declared != asked and not _explicitly_transfers_status_to(fact, asked):
        return "primary object differs; linked_objects does not transfer status"
    return None


def _facts_applicable_to_asked_object(facts, asked_object):
    if not isinstance(asked_object, str) or not asked_object.strip():
        return list(facts)
    return [f for f in facts if object_exclusion(f, asked_object.strip()) is None]


def _normalize_as_of(as_of: Any) -> Optional[str]:
    """Return a caller-supplied as_of as text, or None if none was given.

    Accepts a non-empty string, a datetime, or a date. Never reads the
    server clock and never invents a time from query text.
    """
    if isinstance(as_of, datetime):
        return as_of.isoformat()
    if isinstance(as_of, date):
        return as_of.isoformat()
    if isinstance(as_of, str) and as_of.strip():
        return as_of.strip()
    return None


def _parse_temporal_instant(value: Any) -> Optional[tuple]:
    """Parse an explicit date or datetime without clipping leftover characters.

    Returns ``("date", date)`` or ``("datetime", datetime)``. Strings such as
    ``2026-11-08oops`` are rejected instead of being read as ``2026-11-08``.
    """
    if isinstance(value, datetime):
        return ("datetime", value)
    if isinstance(value, date):
        return ("date", value)
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if len(text) == 10:
        try:
            return ("date", date.fromisoformat(text))
        except ValueError:
            return None
    iso = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        return ("datetime", datetime.fromisoformat(iso))
    except ValueError:
        return None


def _datetime_tzinfo(parsed: tuple):
    if parsed[0] == "datetime":
        return parsed[1].tzinfo
    return None


def _as_comparable_datetime(parsed: tuple, *, other_tz=None, end_of_day: bool = False) -> datetime:
    if parsed[0] == "datetime":
        return parsed[1]
    day = parsed[1]
    if end_of_day:
        dt = datetime(day.year, day.month, day.day, 23, 59, 59, 999999)
    else:
        dt = datetime(day.year, day.month, day.day, 0, 0, 0)
    if other_tz is not None:
        return dt.replace(tzinfo=other_tz)
    return dt


def _compare_temporals(left: tuple, right: tuple) -> Optional[int]:
    """Return -1, 0 or 1; None when the pair cannot be compared safely."""
    if left[0] == "date" and right[0] == "date":
        if left[1] < right[1]:
            return -1
        if left[1] > right[1]:
            return 1
        return 0
    tz = _datetime_tzinfo(left) or _datetime_tzinfo(right)
    left_dt = _as_comparable_datetime(left, other_tz=tz)
    right_dt = _as_comparable_datetime(right, other_tz=tz)
    if (left_dt.tzinfo is None) != (right_dt.tzinfo is None):
        return None
    if left_dt.tzinfo is not None and right_dt.tzinfo is not None:
        left_dt = left_dt.astimezone(timezone.utc)
        right_dt = right_dt.astimezone(timezone.utc)
    if left_dt < right_dt:
        return -1
    if left_dt > right_dt:
        return 1
    return 0


def _optional_temporal_bound(fact: Dict[str, Any], key: str):
    """Return the parsed bound, None if missing, or False if present but invalid."""
    if key not in fact:
        return None
    value = fact.get(key)
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    parsed = _parse_temporal_instant(value)
    if parsed is None:
        return False
    return parsed


def _interval_exclusion(as_of_parsed: tuple, start, end) -> Optional[str]:
    # Dates in intervals denote inclusive calendar-day bounds. With a timestamp
    # counterpart the day uses that explicit offset, never the server timezone.
    tz = (_datetime_tzinfo(as_of_parsed)
          or _datetime_tzinfo(start or ("date", None))
          or _datetime_tzinfo(end or ("date", None)))
    for bound, end_of_day, label in ((start, False, "validity starts after as_of"),
                                     (end, True, "validity expired before as_of")):
        if bound is None:
            continue
        requested = ("datetime", _as_comparable_datetime(as_of_parsed, other_tz=tz, end_of_day=end_of_day))
        boundary = ("datetime", _as_comparable_datetime(bound, other_tz=tz, end_of_day=end_of_day))
        comparison = _compare_temporals(requested, boundary)
        if comparison is None:
            return "validity interval/as_of timezone awareness differs"
        if (not end_of_day and comparison < 0) or (end_of_day and comparison > 0):
            return label + (" (whole-day coverage required)" if as_of_parsed[0] == "date" else "")
    return None


def _interval_covers_as_of(as_of_parsed: tuple, start, end) -> bool:
    return _interval_exclusion(as_of_parsed, start, end) is None


def _observation_covers_as_of(observed: tuple, as_of_parsed: tuple) -> bool:
    if observed[0] == "date" and as_of_parsed[0] == "date":
        return observed[1] == as_of_parsed[1]
    if observed[0] == "datetime" and as_of_parsed[0] == "datetime":
        return _compare_temporals(observed, as_of_parsed) == 0
    return False


def _fact_observation(fact: Dict[str, Any]) -> Optional[tuple]:
    """Evidence time: observed_at, then probe date. Never recorded_at/created_at/updated_at."""
    for key in ("observed_at", "date"):
        if key not in fact:
            continue
        raw = fact.get(key)
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            continue
        return _parse_temporal_instant(raw)
    return None


def _fact_covers_as_of(fact: Dict[str, Any], as_of: Any) -> bool:
    """True when the fact's own evidence time covers as_of.

    An explicit validity interval, if present, decides coverage at full
    precision. Otherwise a date-only observation covers a date-only as_of
    on the same calendar day, and a timestamped observation covers only
    the same instant. recorded_at, created_at and updated_at are ignored.
    """
    as_of_parsed = _parse_temporal_instant(as_of)
    if as_of_parsed is None:
        return False
    start = _optional_temporal_bound(fact, "valid_from")
    end = _optional_temporal_bound(fact, "valid_until")
    if start is False or end is False:
        return False
    if start is not None or end is not None:
        return _interval_covers_as_of(as_of_parsed, start, end)
    observed = _fact_observation(fact)
    if observed is None:
        return False
    return _observation_covers_as_of(observed, as_of_parsed)


def _facts_covering_as_of(
    facts: List[Dict[str, Any]],
    as_of: Any,
    temporal_scope: Any,
) -> List[Dict[str, Any]]:
    """Keep facts that may ground a current-state answer at as_of.

    Only omitted scope is a no-op. Unknown scope and missing/invalid as_of
    fail closed; callers use request_error() for the explanatory message.
    """
    if temporal_scope is None:
        return list(facts)
    if not isinstance(temporal_scope, str) or temporal_scope.strip().casefold() != "current":
        return []
    as_of_text = _normalize_as_of(as_of)
    if as_of_text is None:
        return []
    if _parse_temporal_instant(as_of_text) is None:
        return []
    return [fact for fact in facts if _fact_covers_as_of(fact, as_of_text)]



def temporal_exclusion(fact, as_of):
    """Explain a failed coverage check, without revising historical truth."""
    instant = _parse_temporal_instant(as_of)
    for key in ("valid_from", "valid_until"):
        if _optional_temporal_bound(fact, key) is False:
            return "invalid " + key
    start = _optional_temporal_bound(fact, "valid_from")
    end = _optional_temporal_bound(fact, "valid_until")
    if start is not None or end is not None:
        return _interval_exclusion(instant, start, end)
    observed = _fact_observation(fact)
    if observed is None:
        if any(fact.get(k) not in (None, "") for k in ("observed_at", "date")):
            return "invalid observation time"
        return "observation time not established; write timestamps are not observation time"
    if observed[0] != instant[0]:
        return ("date-only observation cannot establish state at a timestamp" if observed[0] == "date"
                else "instant observation cannot establish a whole queried date")
    comparison = _compare_temporals(observed, instant)
    if comparison is None:
        return "observation/as_of timezone awareness differs"
    if comparison > 0:
        return "observation later than as_of"
    return "historical observation does not cover as_of"


def _historical_observation(observed, instant):
    if not observed or not instant:
        return False
    if observed[0] != instant[0]:
        # A date-only observation on the same day might be later than the
        # requested instant. Do not silently assign it midnight even in context.
        left = observed[1].date() if observed[0] == "datetime" else observed[1]
        right = instant[1].date() if instant[0] == "datetime" else instant[1]
        return left < right
    comparison = _compare_temporals(observed, instant)
    return comparison is not None and comparison < 0


def request_error(asked_object=None, as_of=None, temporal_scope=None):
    if asked_object is not None and (not isinstance(asked_object, str) or not asked_object.strip()):
        return "asked_object must be a non-empty object identifier"
    if temporal_scope is not None and (
        not isinstance(temporal_scope, str) or temporal_scope.strip().casefold() != "current"
    ):
        return "invalid temporal_scope: expected 'current' or omitted (None); unknown values cannot disable time filtering"
    if temporal_scope is not None:
        if _parse_temporal_instant(as_of) is None:
            return "current status is not established: temporal_scope=current requires a valid explicit as_of (ISO date or datetime)"
    return None


def select(facts, *, asked_object=None, as_of=None, temporal_scope=None):
    """Return copies plus content-free exclusions and dated historical context."""
    kept, excluded, historical, context = [], [], [], []
    current = isinstance(temporal_scope, str) and temporal_scope.strip().casefold() == "current"
    error = request_error(asked_object, as_of, temporal_scope)
    for original in facts:
        fact = deepcopy(original)
        lift(fact, original)
        reason = error
        if not reason and asked_object is not None:
            reason = object_exclusion(fact, asked_object.strip())
        if reason and not error:
            if fact.get("linked_objects"):
                context.append({"fact_id": fact["fact_id"], "primary_object": _declared_primary_object(fact),
                                "linked_objects": deepcopy(fact["linked_objects"]), "status_transferred": False})
        if not reason and current and not _fact_covers_as_of(fact, as_of):
            reason = temporal_exclusion(fact, as_of)
            observed = _fact_observation(fact)
            instant = _parse_temporal_instant(as_of)
            # Only genuinely earlier observations are labelled historical.
            if _historical_observation(observed, instant):
                historical.append({"fact_id": fact["fact_id"], "claim": fact["claim"],
                                   **declarations(fact), "use": "historical only, not current grounding"})
        if reason:
            excluded.append({"fact_id": fact["fact_id"], "reason": reason})
        else:
            kept.append(fact)
    return kept, {"exclusions": excluded, "historical_facts": historical,
                  "context_relations": context, "request_error": error}
