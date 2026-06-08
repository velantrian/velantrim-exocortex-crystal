# core/_registry.py
# Velantrim ExoCortex — shared registry of pluggable backends.
#
# Removes the triple duplication of singleton factories (L3 graph, embedder,
# generator): each module supplies an env-variable name, a default and a creation
# function, while the singleton cache, env-based selection and reset-for-tests
# logic live here — in one place.

import os
from typing import Any, Callable, Optional


class BackendRegistry:
    """
    Singleton registry for a single family of backends.

    factory(name) -> instance; it must raise ValueError itself on an unknown name.
    get(backend=None): backend=None → name from env (or default) and a cached
    singleton; an explicit backend → a fresh instance without caching.
    """

    def __init__(
        self,
        env_var: str,
        default: str,
        factory: Callable[[str], Any],
    ) -> None:
        self._env_var = env_var
        self._default = default
        self._factory = factory
        self._instance: Optional[Any] = None

    def get(self, backend: Optional[str] = None) -> Any:
        if self._instance is not None and backend is None:
            return self._instance
        name = backend or os.environ.get(self._env_var, self._default)
        instance = self._factory(name)
        if backend is None:
            self._instance = instance
        return instance

    def reset(self) -> None:
        """Reset the singleton (for tests).

        If the cached instance holds a closable resource (e.g. SqliteL3Graph's
        connection), close it first so connections do not accumulate across the
        many resets a test suite performs.
        """
        close = getattr(self._instance, "close", None)
        if callable(close):
            try:
                close()
            except Exception:  # noqa: BLE001 — reset must never raise
                pass
        self._instance = None
