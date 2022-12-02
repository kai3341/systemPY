from asyncio import gather
from inspect import iscoroutinefunction
from typing import Type

from .extraction import separate_sync_async
from .register import register_handler_by_aio
from .callback_plan import build_callback_plan
from .local_typing import LFMethodTuple, T, CT, LFMethodSync, LFMethodAsync


@register_handler_by_aio("sync")
def handler_sync(
    cls: Type,
    reason: CT,
    callbacks: LFMethodTuple,
) -> LFMethodSync:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    def handler(self: T) -> None:
        for callback in callbacks_total:
            callback(self)

    return handler


@register_handler_by_aio("async")
def handler_async(
    cls: Type,
    reason: CT,
    callbacks: LFMethodTuple,
) -> LFMethodAsync:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    async def handler(self: T) -> None:
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                await callback(self)
            else:
                callback(self)

    return handler


@register_handler_by_aio("gather")
def handler_gather(
    cls: Type,
    reason: CT,
    callbacks: LFMethodTuple,
) -> LFMethodAsync:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    separated = separate_sync_async(callbacks_total)

    if separated.callbacks_sync and separated.callbacks_async:

        async def handler__having_both(self: T) -> None:
            for cb in separated.callbacks_sync:
                cb(self)
            await gather(cb(self) for cb in separated.callbacks_async)

        return handler__having_both

    elif separated.callbacks_async:

        async def handler__having_async(self: T) -> None:
            await gather(cb(self) for cb in separated.callbacks_async)

        return handler__having_async

    elif separated.callbacks_sync:

        async def handler__having_sync(self: T) -> None:
            for cb in separated.callbacks_sync:
                cb(self)

        return handler__having_sync

    else:

        async def handler__having_none(self: T) -> None:
            pass

        return handler__having_none
