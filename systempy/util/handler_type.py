from asyncio import gather
from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction

from .callback_plan import build_callback_plan
from .enums import CONST, TYPE
from .extraction import separate_sync_async
from .local_typing import CTuple, MaybeCoro, P, R
from .register import register_handler_by_aio


def with_repr(
    group: str,
    callbacks: CTuple,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def inner(handler: Callable[P, R]) -> Callable[P, R]:
        names = ";".join(c.__qualname__.split(".")[0] for c in callbacks)
        handler.__qualname__ = f"{group}({names})"
        return handler

    return inner


@register_handler_by_aio(TYPE.SYNC)
def handler_sync(
    cls: type,
    reason: Callable[P, None],
    callbacks: CTuple[P, None],
) -> Callable[P, None]:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    @with_repr("Sync", callbacks_total)
    def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            callback(*args, **kwargs)

    return handler


@register_handler_by_aio(TYPE.ASYNC)
def handler_async(
    cls: type,
    reason: Callable[P, MaybeCoro[None]],
    callbacks: CTuple[P, MaybeCoro[None]],
) -> Callable[P, Coroutine[None, None, None]]:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    @with_repr("Async", callbacks_total)
    async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)

    return handler


@register_handler_by_aio(CONST.GATHER)
def handler_gather(
    cls: type,
    reason: Callable[P, MaybeCoro[None]],
    callbacks: CTuple[P, MaybeCoro[None]],
) -> Callable[P, Coroutine[None, None, None]]:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    separated = separate_sync_async(callbacks_total)

    if separated.callbacks_sync and separated.callbacks_async:

        @with_repr("GatherBoth", callbacks_total)
        async def handler__having_both(*args: P.args, **kwargs: P.kwargs) -> None:
            for cb in separated.callbacks_sync:
                cb(*args, **kwargs)

            await gather(*[cb(*args, **kwargs) for cb in separated.callbacks_async])

        return handler__having_both

    if separated.callbacks_async:

        @with_repr("GatherAsync", callbacks_total)
        async def handler__having_async(*args: P.args, **kwargs: P.kwargs) -> None:
            await gather(*[cb(*args, **kwargs) for cb in separated.callbacks_async])

        return handler__having_async

    if separated.callbacks_sync:

        @with_repr("GatherBoth", callbacks_total)
        async def handler__having_sync(*args: P.args, **kwargs: P.kwargs) -> None:
            for cb in separated.callbacks_sync:
                cb(*args, **kwargs)

        return handler__having_sync

    @with_repr("GatherNone", callbacks_total)
    async def handler__having_none(*args: P.args, **kwargs: P.kwargs) -> None:
        pass

    return handler__having_none
