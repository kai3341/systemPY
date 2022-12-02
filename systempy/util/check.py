from inspect import iscoroutinefunction
from typing import Tuple

from . import constants
from .local_typing import CT, LFMethod, function_types
from .register import register_check_method_type


check_callback_error_message__template = (
    "{name} must be %sronous function, but {func} is %sronous"
)

reversed_sync_or_async = tuple(reversed(constants.sync_or_async))

check_callback_signature__error_message: Tuple[str, ...] = (
    check_callback_error_message__template % constants.sync_or_async,
    check_callback_error_message__template % reversed_sync_or_async,
)


def check_callback_signature(reason: LFMethod, func: LFMethod) -> None:
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


@register_check_method_type("gather")
def gather(target: CT) -> None:
    if not iscoroutinefunction(target):
        error_message = "Can not `asyncio.gather` syncronous method"
        raise ValueError(error_message, target)
