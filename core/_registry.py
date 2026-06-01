# core/_registry.py
# Velantrim ExoCortex — общий реестр сменных backend'ов.
#
# Убирает тройное дублирование singleton-фабрик (L3-граф, эмбеддер, генератор):
# каждый модуль задаёт имя env-переменной, дефолт и функцию создания, а кэш
# singleton'а, выбор по env и сброс для тестов живут здесь — в одном месте.

import os
from typing import Any, Callable, Optional


class BackendRegistry:
    """
    Singleton-реестр одного семейства backend'ов.

    factory(name) -> экземпляр; должна сама бросать ValueError на неизвестное имя.
    get(backend=None): backend=None → имя из env (или дефолт) и кэшируемый
    singleton; явный backend → свежий экземпляр без кэширования.
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
        """Сбросить singleton (для тестов)."""
        self._instance = None
