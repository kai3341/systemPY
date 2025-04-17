from asyncio import gather
from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction

from .callback_plan import build_callback_plan
from .enums import CONST, TYPE
from .extraction import separate_sync_async
from .local_typing import CTuple, MaybeCoro, P
from .register import register_handler_by_aio


def _create_repr(group: str, callbacks: tuple[Callable]) -> str:
    names = ";".join(c.__name__ for c in callbacks)
    return f"<{group} {names}>"


@register_handler_by_aio(TYPE.SYNC)
def handler_sync(
    cls: type,
    reason: Callable[P, None],
    callbacks: CTuple[P, None],
) -> Callable[P, None]:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            callback(*args, **kwargs)

    handler.__name__ = _create_repr("Sync", callbacks_total)
    return handler


@register_handler_by_aio(TYPE.ASYNC)
def handler_async(
    cls: type,
    reason: Callable[P, MaybeCoro[None]],
    callbacks: CTuple[P, MaybeCoro[None]],
) -> Callable[P, Coroutine[None, None, None]]:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)

    handler.__name__ = _create_repr("Async", callbacks_total)
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

        async def handler__having_both(*args: P.args, **kwargs: P.kwargs) -> None:
            for cb in separated.callbacks_sync:
                cb(*args, **kwargs)

            await gather(*[cb(*args, **kwargs) for cb in separated.callbacks_async])

        handler__having_both.__name__ = _create_repr("GatherBoth", callbacks_total)
        return handler__having_both

    if separated.callbacks_async:

        async def handler__having_async(*args: P.args, **kwargs: P.kwargs) -> None:
            await gather(*[cb(*args, **kwargs) for cb in separated.callbacks_async])

        handler__having_async.__name__ = _create_repr("GatherAsync", callbacks_total)
        return handler__having_async

    if separated.callbacks_sync:

        async def handler__having_sync(*args: P.args, **kwargs: P.kwargs) -> None:
            for cb in separated.callbacks_sync:
                cb(*args, **kwargs)

        handler__having_sync.__name__ = _create_repr("GatherBoth", callbacks_total)
        return handler__having_sync

    async def handler__having_none(*args: P.args, **kwargs: P.kwargs) -> None:
        pass

    handler__having_none.__name__ = _create_repr("GatherNone", callbacks_total)
    return handler__having_none
