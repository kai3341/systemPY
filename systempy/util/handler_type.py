from asyncio import gather
from inspect import iscoroutinefunction

from .register import register_handler_by_iscoroutinefunction
from .callback_plan import build_callback_plan, build_callback_plan_iter


@register_handler_by_iscoroutinefunction("sync")
def handler_sync(cls, reason, callbacks):
    callbacks_total = build_callback_plan(cls, reason, callbacks)

    def handler(self, *args, **kwargs):
        for callback in callbacks_total:
            callback(self)

    return handler


@register_handler_by_iscoroutinefunction("async")
def handler_async(cls, reason, callbacks):
    callbacks_total = build_callback_plan_iter(cls, reason, callbacks)
    callbacks_total = tuple(callbacks_total)

    async def handler(self, *args, **kwargs):
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                await callback(self)
            else:
                callback(self)

    return handler


@register_handler_by_iscoroutinefunction("gather")
def handler_gather(cls, reason, callbacks):
    callbacks_total = build_callback_plan_iter(cls, reason, callbacks)
    callbacks_total = tuple(callbacks_total)

    async def handler_gather_iter(self, *args, **kwargs):
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                yield callback(self)
            else:
                callback(self)

    async def handler(self, *args, **kwargs):
        coroutines = handler_gather_iter(self, *args, **kwargs)
        await gather(*coroutines)

    return handler
