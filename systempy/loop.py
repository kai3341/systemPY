from typing import Coroutine, Any
from traceback import print_exc
from sys import stderr

from dataclasses import field
from asyncio import CancelledError, run

from mypy_extensions import trait

from .daemon import DaemonUnitBase


@trait
class LoopUnit(DaemonUnitBase):
    _main_async_coro: Coroutine[Any, Any, None] = field(init=False, repr=False)

    def main_sync(self) -> None:
        run_coroutine = self.run_async()
        run(run_coroutine)

    async def run_async(self) -> None:
        async with self:
            try:
                self._main_async_coro = self.main_async()
                await self._main_async_coro
            except Exception:
                print_exc(file=stderr)
                raise

    def stop(self) -> None:
        self._main_async_coro.throw(CancelledError)
