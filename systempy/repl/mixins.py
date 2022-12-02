import asyncio
import inspect
from typing import Dict, Any

from mypy_extensions import trait


@trait
class ReplLocalsMixin:
    # __slots__ = (
    #     "_repl_caller_frame",
    #     "repl_env_full",
    #     "repl_env",
    # )

    _repl_caller_frame: inspect.FrameInfo
    repl_env_full: Dict[str, Any]
    repl_variables: Dict[str, Any] = {}
    __repl_locals_keys_from_globals = (
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
