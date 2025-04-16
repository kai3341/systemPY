from asyncio import CancelledError, run
from collections.abc import Coroutine
from dataclasses import field

from .daemon import DaemonUnitBase


class LoopUnit(DaemonUnitBase, final=False):
    _main_async_coro: Coroutine[None, None, None] = field(init=False, repr=False)

    def main_sync(self) -> None:
        run_coroutine = self.run_async()
        run(run_coroutine)

    async def run_async(self) -> None:
        async with self:
            self._main_async_coro = self.main_async()
            await self._main_async_coro

    def stop(self) -> None:
        self._main_async_coro.throw(CancelledError)
