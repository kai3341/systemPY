from typing import Coroutine, Any

from dataclasses import field
from asyncio import CancelledError, run

from mypy_extensions import trait

from .daemon import DaemonUnitBase


@trait
class LoopUnit(DaemonUnitBase):
    __main_async_coro: Coroutine[Any, Any, None] = field(init=False)

    def main_sync(self) -> None:
        run_coroutine = self.run_async()
        run(run_coroutine)

    async def run_async(self) -> None:
        async with self:
            self.__main_async_coro = self.main_async()
            await self.__main_async_coro

    def stop(self) -> None:
        self.__main_async_coro.throw(CancelledError)
