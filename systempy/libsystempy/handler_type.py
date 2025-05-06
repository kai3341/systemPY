from asyncio import gather
from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction

from .callback_plan import build_callback_plan
from .constants import handler_metadata
from .enums import DIRECTION, TYPE
from .extraction import separate_sync_async
from .local_dataclasses import CallbackMetadata, SeparatedLFMethods
from .local_typing import CTuple, MaybeCoro, P, R, WeakTypeIterable
from .register import register_handler_by_aio


def with_repr(
    group: str,
    reason: Callable,
    callbacks: CTuple,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def inner(handler: Callable[P, R]) -> Callable[P, R]:
        call_order = tuple(".".join(c.__qualname__.split(".")[-2:]) for c in callbacks)
        handler.__qualname__ = f"{group}[{reason.__name__}]({';'.join(call_order)})"
        handler_metadata[handler] = CallbackMetadata(call_order)
        return handler

    return inner


# Make closure as minimal as possible to avoid memory leak
def __handler_sync(
    callbacks_total: tuple[Callable[P, None], ...],
    with_current_repr: Callable[[Callable[P, None]], Callable[P, None]],
) -> Callable[P, None]:
    @with_current_repr
    def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            callback(*args, **kwargs)

    return handler


@register_handler_by_aio(TYPE.SYNC)
def handler_sync(
    cls: type,
    bases: WeakTypeIterable,
    reason: Callable[P, None],
    callbacks: CTuple[P, None],
) -> Callable[P, None]:
    callbacks_total = build_callback_plan(cls, bases, reason, callbacks)
    with_current_repr = with_repr("Sync", reason, callbacks_total)
    return __handler_sync(callbacks_total, with_current_repr)


# Make closure as minimal as possible to avoid memory leak
def __handler_async(
    callbacks_total: tuple[Callable[P, MaybeCoro[None]], ...],
    with_current_repr: Callable[
        [Callable[P, Coroutine[None, None, None]]],
        Callable[P, Coroutine[None, None, None]],
    ],
) -> Callable[P, Coroutine[None, None, None]]:
    @with_current_repr
    async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            if iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)

    return handler


@register_handler_by_aio(TYPE.ASYNC)
def handler_async(
    cls: type,
    bases: WeakTypeIterable,
    reason: Callable[P, MaybeCoro[None]],
    callbacks: CTuple[P, MaybeCoro[None]],
) -> Callable[P, Coroutine[None, None, None]]:
    callbacks_total = build_callback_plan(cls, bases, reason, callbacks)
    with_current_repr = with_repr("Async", reason, callbacks_total)
    return __handler_async(callbacks_total, with_current_repr)


# Make closure as minimal as possible to avoid memory leak
def __handler_gather_both(
    separated: SeparatedLFMethods[P, None],
    with_current_repr: Callable[
        [Callable[P, Coroutine[None, None, None]]],
        Callable[P, Coroutine[None, None, None]],
    ],
) -> Callable[P, Coroutine[None, None, None]]:
    @with_current_repr
    async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for cb in separated.callbacks_sync:
            cb(*args, **kwargs)

        await gather(*[cb(*args, **kwargs) for cb in separated.callbacks_async])

    return handler


# Make closure as minimal as possible to avoid memory leak
def __handler_gather_async(
    callbacks_total: tuple[Callable[P, Coroutine[None, None, None]], ...],
    with_current_repr: Callable[
        [Callable[P, Coroutine[None, None, None]]],
        Callable[P, Coroutine[None, None, None]],
    ],
) -> Callable[P, Coroutine[None, None, None]]:
    @with_current_repr
    async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        await gather(*[cb(*args, **kwargs) for cb in callbacks_total])

    return handler


# Make closure as minimal as possible to avoid memory leak
def __handler_gather_sync(
    callbacks_total: tuple[Callable[P, None], ...],
    with_current_repr: Callable[
        [Callable[P, Coroutine[None, None, None]]],
        Callable[P, Coroutine[None, None, None]],
    ],
) -> Callable[P, Coroutine[None, None, None]]:
    @with_current_repr
    async def handler(*args: P.args, **kwargs: P.kwargs) -> None:
        for callback in callbacks_total:
            callback(*args, **kwargs)

    return handler


# Make closure as minimal as possible to avoid memory leak
def __handler_gather_void(
    with_current_repr: Callable[
        [Callable[P, Coroutine[None, None, None]]],
        Callable[P, Coroutine[None, None, None]],
    ],
) -> Callable[P, Coroutine[None, None, None]]:
    @with_current_repr
    async def handler(*args: P.args, **kwargs: P.kwargs) -> None: ...

    return handler


@register_handler_by_aio(DIRECTION.GATHER)
def handler_gather(
    cls: type,
    bases: WeakTypeIterable,
    reason: Callable[P, MaybeCoro[None]],
    callbacks: CTuple[P, MaybeCoro[None]],
) -> Callable[P, Coroutine[None, None, None]]:
    callbacks_total = build_callback_plan(cls, bases, reason, callbacks)

    separated = separate_sync_async(callbacks_total)

    if separated.callbacks_sync and separated.callbacks_async:
        with_current_repr = with_repr("GatherBoth", reason, callbacks_total)
        return __handler_gather_both(separated, with_current_repr)

    if separated.callbacks_async:
        with_current_repr = with_repr("GatherAsync", reason, callbacks_total)
        return __handler_gather_async(separated.callbacks_async, with_current_repr)

    if separated.callbacks_sync:
        with_current_repr = with_repr("GatherBoth", reason, callbacks_total)
        return __handler_gather_sync(separated.callbacks_sync, with_current_repr)

    with_current_repr = with_repr("GatherNone", reason, callbacks_total)
    return __handler_gather_void(with_current_repr)
