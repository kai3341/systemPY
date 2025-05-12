from __future__ import annotations

from inspect import iscoroutinefunction
from typing import TYPE_CHECKING, cast
from weakref import ref

from .constants import lifecycle_registered_methods
from .enums import DIRECTION, ROLE
from .local_dataclasses import SeparatedLFMethods
from .register import class_role_registry, register_direction

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    from .local_typing import CTuple, P, R, WeakTypeIterable


def extract_attrs(iterable: WeakTypeIterable, reason: Callable) -> list[Callable]:
    result: list[Callable] = []
    cfg = lifecycle_registered_methods[reason]
    interface = cfg.interface()

    assert interface

    for cls_ref in iterable:
        cls = cls_ref()
        assert cls

        if not issubclass(cls, interface):
            continue

        cls_dict = cls.__dict__

        if (maybe_val := cls_dict.get(reason.__name__)) is not None:
            result.append(maybe_val)

    return result


@register_direction(DIRECTION.FORWARD)
@register_direction(DIRECTION.GATHER)
def callbacks_direct(iterable: WeakTypeIterable, reason: Callable) -> CTuple:
    callbacks = extract_attrs(iterable, reason)
    return tuple(callbacks)


@register_direction(DIRECTION.BACKWARD)
def callbacks_reversed(iterable: WeakTypeIterable, reason: Callable) -> CTuple:
    callbacks = extract_attrs(iterable, reason)
    callbacks.reverse()
    return tuple(callbacks)


extract_bases__whitelist = {ROLE.UNIT, ROLE.APP}


def extract_bases(cls: type) -> WeakTypeIterable:
    bases = [
        # ===
        Base
        for Base in cls.mro()
        if class_role_registry[Base] in extract_bases__whitelist
    ]

    app_class = bases.pop(0)
    bases.append(app_class)

    return tuple(map(ref, bases))


def separate_sync_async(
    iterable: CTuple[P, R | Coroutine[R, None, None]],
) -> SeparatedLFMethods[P, R]:
    callbacks_sync: list[Callable[P, R]] = []
    callbacks_async: list[Callable[P, Coroutine[R, None, None]]] = []

    for callback in iterable:
        if iscoroutinefunction(callback):
            callbacks_async.append(callback)
        else:
            callbacks_sync.append(cast("Callable[P, R]", callback))

    return SeparatedLFMethods(
        callbacks_sync=tuple(callbacks_sync),
        callbacks_async=tuple(callbacks_async),
    )
