# core/path_safety.py
# Velantrim ExoCortex — ingest path sandboxing.
#
# Local-trust mode (default): relative paths must stay under cwd; absolute paths
# are accepted as-is (typical CLI usage).
#
# Strict mode: set VELANTRIM_INGEST_BASE so every path must resolve inside that
# directory (recommended for HTTP or shared-volume deployments).

import os
from pathlib import Path
from typing import Union


def ingest_base_dir() -> Path:
    """Return the resolved ingest base directory when strict mode is enabled."""
    raw = os.environ.get("VELANTRIM_INGEST_BASE")
    if not raw:
        return Path.cwd().resolve()
    return Path(raw).resolve()


def _strict_base() -> Path | None:
    raw = os.environ.get("VELANTRIM_INGEST_BASE")
    return Path(raw).resolve() if raw else None


def resolve_safe_path(path: Union[str, Path], *, base_dir: Union[str, Path, None] = None) -> Path:
    """Resolve ``path`` for file ingest / CLI reads.

    Raises ``ValueError`` when a relative path escapes the allowed base.
    Raises ``FileNotFoundError`` when the target does not exist.
    """
    if not path or (isinstance(path, str) and not str(path).strip()):
        raise ValueError("path must be non-empty")

    candidate = Path(path)
    strict = Path(base_dir).resolve() if base_dir is not None else _strict_base()

    if strict is not None:
        resolved = (strict / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
        try:
            resolved.relative_to(strict)
        except ValueError as exc:
            raise ValueError(
                f"path escapes ingest base directory ({strict}): {path!r}"
            ) from exc
    else:
        cwd = Path.cwd().resolve()
        resolved = (cwd / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
        if not candidate.is_absolute():
            try:
                resolved.relative_to(cwd)
            except ValueError as exc:
                raise ValueError(
                    f"path escapes working directory ({cwd}): {path!r}"
                ) from exc

    if not resolved.is_file():
        raise FileNotFoundError(f"file not found: {resolved}")
    return resolved
