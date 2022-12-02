from inspect import iscoroutinefunction
from typing import Tuple, List, Callable
from .register import register_direction
from . import constants

from .local_typing import (
    LFMethodTuple,
    TypeIterable,
    LFMethodSync,
    LFMethodAsync,
    function_types,
)
from .local_dataclasses import SeparatedLFMethods


def extract_attrs(iterable: TypeIterable, name: str) -> List[Callable]:
    return [
        # ===
        getattr(item, name)
        for item in iterable
        if name in item.__dict__
    ]


@register_direction("forward")
@register_direction("gather")
def callbacks_direct(iterable: TypeIterable, name: str) -> LFMethodTuple:
    callbacks = extract_attrs(iterable, name)
    return tuple(callbacks)


@register_direction("backward")
def callbacks_reversed(iterable: TypeIterable, name: str) -> LFMethodTuple:
    callbacks = extract_attrs(iterable, name)
    callbacks.reverse()
    return tuple(callbacks)


def extract_bases(cls: type) -> Tuple[type, ...]:
    bases = cls.mro()

    bases = [
        # ===
        Base
        for Base in bases
        if Base not in constants.lifecycle_bases_blacklist
    ]

    lifecycle_disallowed_attrs = constants.lifecycle_disallowed_attrs
    for base in bases:
        clsdict = vars(base)
        for check_attribute, description in lifecycle_disallowed_attrs:
            if check_attribute in clsdict:
                message = f"Attribute {check_attribute} is not allowed"

                if description:
                    message = "%s. %s" % (message, description)

                raise ValueError(message, base)

    first = bases.pop(0)
    bases.append(first)
    return tuple(bases)


def separate_sync_async(iterable: LFMethodTuple) -> SeparatedLFMethods:
    callbacks_sync: List[LFMethodSync] = []
    callbacks_async: List[LFMethodAsync] = []

    for callback in iterable:
        assert isinstance(callback, function_types)
        if iscoroutinefunction(callback):
            callbacks_async.append(callback)
        else:
            callbacks_sync.append(callback)

    return SeparatedLFMethods(
        callbacks_sync=tuple(callbacks_sync),
        callbacks_async=tuple(callbacks_async),
    )
