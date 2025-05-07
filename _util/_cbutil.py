__all__ = (
    "_method_async",
    "_method_sync",
)

from collections.abc import Callable, Coroutine
from functools import wraps
from typing import TypeVar

T = TypeVar("T")


def _method_sync(
    cb: Callable[[str], None],
    postfix: str,
) -> Callable[[Callable[[T], None]], Callable[[T], None]]:
    def outer(target: Callable[[T], None]) -> Callable[[T], None]:
        result = f"{target.__name__}:{postfix}"

        @wraps(target)
        def inner(self: T) -> None:  # noqa: ARG001
            cb(result)

        return inner

    return outer


def _method_async(
    cb: Callable[[str], None],
    postfix: str,
) -> Callable[
    [Callable[[T], Coroutine[None, None, None]]],
    Callable[[T], Coroutine[None, None, None]],
]:
    def outer(
        target: Callable[[T], Coroutine[None, None, None]],
    ) -> Callable[[T], Coroutine[None, None, None]]:
        result = f"{target.__name__}:{postfix}"

        @wraps(target)
        async def inner(self: T) -> None:  # noqa: ARG001
            cb(result)

        return inner

    return outer
