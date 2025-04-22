from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction
from typing import cast
from weakref import ref

from .constants import lifecycle_disallowed_attrs
from .enums import DIRECTION
from .local_dataclasses import SeparatedLFMethods
from .local_typing import CTuple, P, R, WeakTypeIterable
from .register import mark_as_target, register_direction


def extract_attrs(iterable: WeakTypeIterable, name: str) -> list[Callable]:
    result: list[Callable] = []

    for item_ref in iterable:
        item = item_ref()
        assert item
        item_dict = item.__dict__

        if (maybe_val := item_dict.get(name)) is not None:
            result.append(maybe_val)

    return result


@register_direction(DIRECTION.FORWARD)
@register_direction(DIRECTION.GATHER)
def callbacks_direct(iterable: WeakTypeIterable, name: str) -> CTuple:
    callbacks = extract_attrs(iterable, name)
    return tuple(callbacks)


@register_direction(DIRECTION.BACKWARD)
def callbacks_reversed(iterable: WeakTypeIterable, name: str) -> CTuple:
    callbacks = extract_attrs(iterable, name)
    callbacks.reverse()
    return tuple(callbacks)


def extract_bases(cls: type) -> WeakTypeIterable:
    bases = [
        # ===
        Base
        for Base in cls.mro()
        if Base not in mark_as_target
    ]

    for base in bases:
        clsdict = vars(base)
        for check_attribute, description in lifecycle_disallowed_attrs:
            if check_attribute in clsdict:
                message = f"Attribute {check_attribute} is not allowed"

                if description:
                    message = f"{message}. {description}"

                raise ValueError(message, base)

    first = bases.pop(0)
    bases.append(first)
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
