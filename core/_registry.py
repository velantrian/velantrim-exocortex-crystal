# core/_registry.py
# Velantrim ExoCortex — shared registry of pluggable backends.
#
# Removes the triple duplication of singleton factories (L3 graph, embedder,
# generator): each module supplies an env-variable name, a default and a creation
# function, while the singleton cache, env-based selection and reset-for-tests
# logic live here — in one place.

import os
import threading
from typing import Any, Callable, Optional


class BackendRegistry:
    """
    Singleton registry for a single family of backends.

    factory(name) -> instance; it must raise ValueError itself on an unknown name.
    get(backend=None): backend=None → name from env (or default) and a cached
    singleton; an explicit backend → a fresh instance without caching.

    Singleton creation and reset are serialized by an RLock so concurrent
    first access (e.g. two request threads under FastAPI's thread pool) cannot
    construct two live backend instances that silently diverge — see the L0
    cache race fixed in 4df0c2c for the same bug class on a different cache.
    The explicit-backend path never touches shared state, so it runs outside
    the lock.
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
        self._lock = threading.RLock()

    def get(self, backend: Optional[str] = None) -> Any:
        if backend is not None:
            return self._factory(backend)  # explicit backend: always fresh, never cached
        with self._lock:
            if self._instance is not None:
                return self._instance
            name = os.environ.get(self._env_var, self._default)
            self._instance = self._factory(name)
            return self._instance

    def reset(self) -> None:
        """Reset the singleton (for tests).

        If the cached instance holds a closable resource (e.g. SqliteL3Graph's
        connection), close it first so connections do not accumulate across the
        many resets a test suite performs.
        """
        with self._lock:
            close = getattr(self._instance, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:  # noqa: BLE001 — reset must never raise
                    pass
            self._instance = None
