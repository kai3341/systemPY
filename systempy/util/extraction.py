from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction

from .constants import lifecycle_disallowed_attrs
from .enums import DIRECTION
from .local_dataclasses import SeparatedLFMethods
from .local_typing import CTuple, P, R, TypeIterable
from .register import mark_as_target, register_direction


def extract_attrs(iterable: TypeIterable, name: str) -> list[Callable]:
    return [
        # ===
        getattr(item, name)
        for item in iterable
        if name in item.__dict__
    ]


@register_direction(DIRECTION.FORWARD)
@register_direction(DIRECTION.GATHER)
def callbacks_direct(iterable: TypeIterable, name: str) -> CTuple:
    callbacks = extract_attrs(iterable, name)
    return tuple(callbacks)


@register_direction(DIRECTION.BACKWARD)
def callbacks_reversed(iterable: TypeIterable, name: str) -> CTuple:
    callbacks = extract_attrs(iterable, name)
    callbacks.reverse()
    return tuple(callbacks)


def extract_bases(cls: type) -> tuple[type, ...]:
    bases = cls.mro()

    bases = [
        # ===
        Base
        for Base in bases
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
    return tuple(bases)


def separate_sync_async(iterable: CTuple[P, R]) -> SeparatedLFMethods[P, R]:
    callbacks_sync: list[Callable[P, R]] = []
    callbacks_async: list[Callable[P, Coroutine[R, None, None]]] = []

    for callback in iterable:
        assert callable(callback)
        if iscoroutinefunction(callback):
            callbacks_async.append(callback)
        else:
            callbacks_sync.append(callback)

    return SeparatedLFMethods(
        callbacks_sync=tuple(callbacks_sync),
        callbacks_async=tuple(callbacks_async),
    )
