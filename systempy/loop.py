import signal

from asyncio import AbstractEventLoop, Task, get_event_loop, create_task

from mypy_extensions import trait

from .daemon import DaemonUnitBase
from .util import mark_as_target


@mark_as_target
@trait
class LoopUnit(DaemonUnitBase):
    loop: AbstractEventLoop
    __main_async_task: Task

    def pre_startup(self) -> None:
        self.loop = get_event_loop()
        self.__init_loop__signals()

    __stop_signals = (
        signal.SIGINT,
        signal.SIGTERM,
        signal.SIGABRT,
    )

    def __init_loop__signals(self) -> None:
        loop: AbstractEventLoop = self.loop
        for current_signal in self.__stop_signals:
            loop.add_signal_handler(current_signal, self.stop)

    def main_sync(self) -> None:
        run_coroutine = self.run_async()
        self.loop.run_until_complete(run_coroutine)

    async def run_async(self) -> None:
        async with self:
            coro = self.main_async()
            task = create_task(coro)

            self.__main_async_task = task
            await task

    def stop(self) -> None:
        self.__main_async_task.cancel()
