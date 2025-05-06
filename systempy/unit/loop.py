from asyncio import AbstractEventLoop, get_running_loop, run
from collections.abc import Coroutine
from dataclasses import field
from typing import ParamSpec

from ..libsystempy import ROLE
from ..target import AsyncMixinABC
from .daemon import _BaseDaemonUnitABC

A = ParamSpec("A")


def handle_error(exc: RuntimeError) -> None:
    if len(exc.args) == 0:
        raise exc

    if exc.args[0] == "cannot reuse already awaited coroutine":
        return

    raise exc


class LoopUnit(AsyncMixinABC, _BaseDaemonUnitABC[A], role=ROLE.MIXIN):
    _main_async_coro: Coroutine[None, None, None] = field(init=False, repr=False)
    __loop: AbstractEventLoop = field(init=False, repr=False)

    def main_sync(self) -> None:
        run_coroutine = self.run_async()
        run(run_coroutine)

    async def run_async(self) -> None:
        self.__loop = get_running_loop()
        async with self:
            self._main_async_coro = self.main_async()
            try:
                await self._main_async_coro
            except RuntimeError as e:
                handle_error(e)

    def _stop_samethread(self) -> None:
        try:
            return self._main_async_coro.throw(SystemExit)
        except RuntimeError as e:
            handle_error(e)

    def _stop_threadsafe(self, thread_id: int) -> None:  # noqa: ARG002
        self.__loop.call_soon_threadsafe(self._stop_samethread)
