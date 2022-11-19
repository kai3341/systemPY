from asyncio import gather
from inspect import iscoroutinefunction
from typing import Type, Awaitable, Generator

from .register import register_handler_by_iscoroutinefunction
from .callback_plan import build_callback_plan
from .typing import LFMethodTuple, T, CT, LFMethodSync, LFMethodAsync


@register_handler_by_iscoroutinefunction("sync")
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


@register_handler_by_iscoroutinefunction("async")
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


@register_handler_by_iscoroutinefunction("gather")
def handler_gather(
    cls: Type,
    reason: CT,
    callbacks: LFMethodTuple,
) -> LFMethodAsync:
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    def handler_gather_iter(self: T) -> Generator[Awaitable, None, None]:
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                yield callback(self)
            else:
                callback(self)

    async def handler(self: T) -> None:
        coroutines = handler_gather_iter(self)
        await gather(*coroutines)

    return handler
