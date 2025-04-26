from collections.abc import Callable
from functools import partial
from weakref import ref

from . import extraction
from .local_dataclasses import GenericHandlerSettings
from .local_typing import WeakTypeIterable


def create_handler_generic(
    cls_ref: ref[type],
    bases: WeakTypeIterable,
    settings: GenericHandlerSettings,
) -> None:
    collect = settings.collect()
    reason = settings.reason()
    compose = settings.compose()
    cls = cls_ref()
    assert collect
    assert reason
    assert compose
    assert cls
    callbacks = collect(bases, reason)
    handler = compose(cls, bases, reason, callbacks)
    setattr(cls, reason.__name__, handler)


def create_partial_handler_generic(
    cls: type,
) -> Callable[[GenericHandlerSettings], None]:
    bases = extraction.extract_bases(cls)
    return partial(create_handler_generic, ref(cls), bases)
