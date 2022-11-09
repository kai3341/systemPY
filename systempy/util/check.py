from inspect import iscoroutinefunction
from typing import Tuple

from . import constants
from . import register
from .typing import Named, FT


check_callback_error_message__template = (
    "{name} must be %sronous function, but {func} is %sronous"
)

reversed_sync_or_async = tuple(reversed(constants.sync_or_async))

check_callback_signature__error_message: Tuple[str, ...] = (
    check_callback_error_message__template % constants.sync_or_async,
    check_callback_error_message__template % reversed_sync_or_async,
)


def check_callback_signature(reason: Named, func: Named) -> None:
    reason_async = iscoroutinefunction(reason)
    if reason_async == iscoroutinefunction(func):
        return None

    template = check_callback_signature__error_message[reason_async]

    error_message = template.format(
        name=reason.__name__,
        func=func,
    )

    raise ValueError(error_message)


@register.register_check_method_type("gather")
def check_direction(target: FT) -> None:
    if not iscoroutinefunction(target):
        error_message = "Can not `asyncio.gather` syncronous method"
        raise ValueError(error_message, target)
