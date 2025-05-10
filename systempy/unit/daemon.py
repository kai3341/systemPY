from abc import abstractmethod
from collections.abc import Callable
from ctypes import pythonapi
from dataclasses import field
from signal import Signals, getsignal, signal
from threading import current_thread
from types import FrameType
from typing import ClassVar, ParamSpec

from ..libsystempy import ROLE
from ..libsystempy.thread_exception import thread_send_exception
from ..target import SyncMixinABC
from ._compat_signal import default_reload_signals

PyThreadState_Get = pythonapi.PyThreadState_Get
PyEval_RestoreThread = pythonapi.PyEval_RestoreThread
PyThreadState_GetID = pythonapi.PyThreadState_GetID

A = ParamSpec("A")


class _BaseDaemonUnitABC(SyncMixinABC[A]):
    reload_signals: ClassVar[tuple[Signals, ...]] = default_reload_signals

    __thread_id: int | None = field(init=False, default=None, repr=False)
    __daemon_reloading: bool = field(init=False, default=False, repr=False)
    __original_signals: dict[
        Signals,
        Callable[[int, FrameType | None], None] | int | None,
    ] = field(
        init=False,
        default_factory=dict,
        repr=False,
    )

    def on_init(self) -> None:
        for sig in self.reload_signals:
            self.__original_signals[sig] = getsignal(sig)
            signal(sig, self.__signal_handler)

    def __signal_handler(self, _sig: int, _frame: FrameType | None) -> None:
        self.reload()

    def remove_signal_handlers(self, *signals: Signals) -> None:
        if not signals:
            signals = self.reload_signals

        for sig in signals:
            signal(sig, self.__original_signals[sig])

    @abstractmethod
    def _stop_threadsafe(self, thread_id: int) -> None: ...
    @abstractmethod
    def _stop_samethread(self) -> None: ...

    def stop(self) -> None:
        if current_thread().ident == self.__thread_id:
            return self._stop_samethread()
        thread_id = self.__thread_id
        assert thread_id
        return self._stop_threadsafe(thread_id)

    def reload(self) -> None:
        self.__daemon_reloading = True
        self.stop()

    def run_sync(self) -> None:
        while True:
            self.__thread_id = current_thread().ident
            with self:
                try:
                    self.main_sync()

                    if not self.__daemon_reloading:
                        return
                except SystemExit:
                    if not self.__daemon_reloading:
                        raise

                except KeyboardInterrupt:
                    return

            self.__daemon_reloading = False


class DaemonUnit(_BaseDaemonUnitABC[A], role=ROLE.MIXIN):
    def _stop_samethread(self) -> None:
        raise SystemExit

    def _stop_threadsafe(self, thread_id: int) -> None:
        thread_send_exception(thread_id, SystemExit)
