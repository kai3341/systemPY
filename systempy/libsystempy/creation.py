from collections.abc import Callable
from functools import partial
from weakref import WeakKeyDictionary, WeakValueDictionary, ref

from . import extraction
from .constants import created_handlers, handler_metadata, original_methods
from .local_dataclasses import CallbackMetadata, GenericHandlerSettings
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

    if maybe_original := cls.__dict__.get(reason.__name__):
        if maybe_original not in created_handlers:
            original_methods[cls][reason] = maybe_original

    callbacks = collect(bases, reason)
    handler = compose(cls, bases, reason, callbacks)
    created_handlers.add(handler)
    handler_metadata[handler] = CallbackMetadata(
        call_order=tuple(c.__qualname__ for c in callbacks),
    )
    setattr(cls, reason.__name__, handler)


__create_partial_handler_generic_cache = WeakKeyDictionary[
    type,
    Callable[[GenericHandlerSettings], None],
]()


def create_partial_handler_generic(
    cls: type,
) -> Callable[[GenericHandlerSettings], None]:
    if maybe_cached := __create_partial_handler_generic_cache.get(cls):
        return maybe_cached

    bases = extraction.extract_bases(cls)
    original_methods[cls] = WeakValueDictionary()

    generic_handler = partial(create_handler_generic, ref(cls), bases)
    __create_partial_handler_generic_cache[cls] = generic_handler
    return generic_handler
