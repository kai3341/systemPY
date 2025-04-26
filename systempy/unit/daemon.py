import signal
from dataclasses import field
from types import FrameType
from typing import ClassVar

from ..target import DaemonMixinABC, ProcessMixinABC


class DaemonBaseUnit(DaemonMixinABC, ProcessMixinABC):
    reload_signals: ClassVar[tuple[signal.Signals, ...]] = (signal.SIGHUP,)

    _daemon_reloading: bool = field(init=False, default=False)

    def on_init(self) -> None:
        for reload_signal in self.reload_signals:
            signal.signal(reload_signal, self.__signal_handler)

    def __signal_handler(self, _sig: int, _frame: FrameType | None) -> None:
        self.reload()

    def reload(self) -> None:
        self._daemon_reloading = True
        self.stop()

    def run_sync(self) -> None:
        while True:
            with self:
                try:
                    self.main_sync()

                    if not self._daemon_reloading:
                        return
                except SystemExit:
                    if not self._daemon_reloading:
                        raise

            self._daemon_reloading = False


class DaemonUnit(DaemonBaseUnit):
    async def run_async(self) -> None:
        async with self:
            await self.main_async()
