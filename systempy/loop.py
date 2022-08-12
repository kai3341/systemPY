import signal
import asyncio

from .target import Target
from .daemon import DaemonUnit


class LoopUnit(Target, DaemonUnit):
    loop: asyncio.AbstractEventLoop
    __main_async_task: asyncio.Task

    def pre_startup(self):
        self.loop = asyncio.get_event_loop()
        self.__init_loop__signals()

    __stop_signals = (
        signal.SIGINT,
        signal.SIGTERM,
        signal.SIGABRT,
    )

    def __init_loop__signals(self):
        loop: asyncio.AbstractEventLoop = self.loop
        for current_signal in self.__stop_signals:
            loop.add_signal_handler(current_signal, self.stop)

    def main_sync(self):
        run_coroutine = self.run_async()
        self.loop.run_until_complete(run_coroutine)

    async def run_async(self):
        async with self:
            coro = self.main_async()
            task = asyncio.create_task(coro)

            self.__main_async_task = task
            await task

    def stop(self):
        self.__main_async_task.cancel()
