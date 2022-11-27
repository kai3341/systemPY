import ctypes
import signal as _signal
from threading import Thread
from typing import Type, Union


PyThreadState_SetAsyncExc = ctypes.pythonapi.PyThreadState_SetAsyncExc


def thread_send_exception(
    thread: Thread,
    exception: Type[BaseException],
) -> None:

    target_tid = thread.ident
    assert target_tid
    PyThreadState_SetAsyncExc(
        ctypes.c_long(target_tid),
        ctypes.py_object(exception),
    )


def thread_send_signal(
    thread: Thread,
    signal: Union[_signal.Signals, int],
) -> None:

    target_tid = thread.ident
    assert target_tid
    _signal.pthread_kill(
        target_tid,
        signal,
    )
