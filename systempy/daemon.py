import signal
from dataclasses import field

from mypy_extensions import trait
from typing import Optional, ClassVar, Tuple
from types import FrameType

from .target import ProcessTargetABC, DaemonTargetABC, Target
from .util import mark_as_target


@trait
class DaemonUnitBase(Target, DaemonTargetABC, ProcessTargetABC):
    reload_signals: ClassVar[Tuple[signal.Signals, ...]] = (
        # signal.Signals
        signal.SIGHUP,
    )

    __reloading: bool = field(init=False)

    def on_init(self) -> None:
        for reload_signal in self.reload_signals:
            signal.signal(reload_signal, self.__signal_handler)
        self.__reloading = False

    def __signal_handler(self, sig: int, frame: Optional[FrameType]) -> None:
        self.reload()

    def reload(self) -> None:
        self.__reloading = True
        self.stop()

    async def run_async(self) -> None:
        async with self:
            await self.main_async()

    def run_sync(self) -> None:
        while True:
            with self:
                self.main_sync()
            if self.__reloading:
                self.__reloading = False
                continue
            break


@mark_as_target
@trait
class DaemonUnit(DaemonUnitBase):
    async def run_async(self) -> None:
        async with self:
            await self.main_async()
