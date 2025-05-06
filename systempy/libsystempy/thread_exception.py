from ctypes import c_int, c_ulong, py_object, pythonapi

PyThreadState_SetAsyncExc = pythonapi.PyThreadState_SetAsyncExc
PyThreadState_SetAsyncExc.argtypes = (c_ulong, py_object)
PyThreadState_SetAsyncExc.restype = c_int

ZERO_THREADS_AFFECTED = "Thread not found"
TOO_MANY_AFFECTED = "Too many threads affected"


def thread_send_exception(
    thread_id: int,
    exception: type[BaseException],
) -> None:
    ret: int = PyThreadState_SetAsyncExc(
        c_ulong(thread_id),
        py_object(exception),
    )

    if ret == 1:
        return

    if ret == 0:
        raise ValueError(ZERO_THREADS_AFFECTED)

    PyThreadState_SetAsyncExc(thread_id, None)
    raise SystemError(TOO_MANY_AFFECTED, ret)
