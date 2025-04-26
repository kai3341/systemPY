from asyncio import AbstractEventLoop, get_running_loop, run
from collections.abc import Coroutine
from dataclasses import field

from .daemon import DaemonBaseUnit


class LoopUnit(DaemonBaseUnit):
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
                if len(e.args) == 0:
                    raise

                if e.args[0] == "cannot reuse already awaited coroutine":
                    return

                raise

    def stop(self) -> None:
        self._main_async_coro.throw(SystemExit)

    def stop_threadsafe(self) -> None:
        """
        Used only when event loop is running in other thread
        """
        self.__loop.call_soon_threadsafe(self.stop)

    def reload_threadsafe(self) -> None:
        """
        Used only when event loop is running in other thread
        """
        self.__loop.call_soon_threadsafe(self.reload)
