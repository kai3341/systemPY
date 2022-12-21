import asyncio
import inspect
from dataclasses import field
from typing import ClassVar, Dict, Tuple, Any

from mypy_extensions import trait


@trait
class ReplLocalsMixin:
    _repl_caller_frame: inspect.FrameInfo = field(init=False)
    repl_env_full: Dict[str, Any] = field(init=False)
    repl_variables: ClassVar[Dict[str, Any]] = {}
    __repl_locals_keys_from_globals: ClassVar[Tuple[str, ...]] = (
        "__name__",
        "__package__",
        "__loader__",
        "__spec__",
        "__builtins__",
        "__file__",
    )

    def _repl_env_defaults(self) -> Dict[str, Any]:
        return {"asyncio": asyncio, "unit": self}

    def _setup_repl_env(self) -> None:
        repl_env = self._repl_env_defaults()
        repl_env.update(self.repl_variables)
        self.repl_env = repl_env
        self.repl_env_full = repl_env.copy()

        env = self._repl_caller_frame[0].f_globals

        for key in self.__repl_locals_keys_from_globals:
            self.repl_env_full[key] = env[key]

    def _setup_repl_caller_frame(self) -> None:
        "Firstly"
        frames = inspect.stack()
        self._repl_caller_frame = frames[-1]
