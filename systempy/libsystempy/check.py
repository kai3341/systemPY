from collections.abc import Callable
from inspect import iscoroutinefunction

from .constants import sync_or_async
from .enums import DIRECTION
from .local_typing import function_types
from .register import register_check_method_type

sync_or_async_names = tuple(i.value for i in sync_or_async)
sync_or_async_names_rev = tuple(reversed(sync_or_async_names))

CHECK_CALLBACK_ERROR_MESSAGE__TEMPLATE = (
    "{name} must be %sronous function, but {func} is %sronous"
)

check_callback_signature__error_message: tuple[str, ...] = (
    CHECK_CALLBACK_ERROR_MESSAGE__TEMPLATE % sync_or_async_names,
    CHECK_CALLBACK_ERROR_MESSAGE__TEMPLATE % sync_or_async_names_rev,
)


def check_callback_signature(reason: Callable, func: Callable) -> None:
    """
    When `reason` is syncronous, `func` have to be syncronous too
    Asyncronous `reason` executors may to execute both `func` types
    """

    assert isinstance(reason, function_types)
    assert isinstance(func, function_types)

    reason_async = iscoroutinefunction(reason)
    if reason_async:
        return

    if not iscoroutinefunction(func):
        return

    template = check_callback_signature__error_message[reason_async]

    error_message = template.format(
        name=reason.__name__,
        func=func,
    )

    raise ValueError(error_message)


@register_check_method_type(DIRECTION.GATHER)
def gather(target: Callable) -> None:
    if not iscoroutinefunction(target):
        error_message = "Can not `asyncio.gather` syncronous method"
        raise ValueError(error_message, target)
