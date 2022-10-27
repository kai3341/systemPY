import asyncio
import signal
from . import target


class DaemonUnit(target.DaemonTargetABC):
    reload_signals = (signal.SIGHUP,)

    __reloading: bool

    def on_init(self):
        for reload_signal in self.reload_signals:
            signal.signal(reload_signal, self.reload)
        self.__reloading = False

    def reload(self, *args):
        self.__reloading = True
        self.stop()

    async def run_async(self):
        async with self:
            await self.main_async()

    def run_sync(self):
        while True:
            try:
                with self:
                    self.main_sync()
            except asyncio.CancelledError:
                if self.__reloading:
                    self.__reloading = False
                    continue

                break
