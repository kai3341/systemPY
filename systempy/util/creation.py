from collections.abc import Callable
from functools import cache, partial

from . import extraction
from .local_dataclasses import GenericHandlerSettings
from .local_typing import TypeIterable


def create_handler_generic(
    cls: type,
    bases: TypeIterable,
    name: str,
    settings: GenericHandlerSettings,
) -> None:
    callbacks = settings.collect(bases, name)
    handler = settings.compose(cls, settings.reason, callbacks)
    setattr(cls, name, handler)


@cache
def create_partial_handler_generic(
    cls: type,
) -> Callable[[str, GenericHandlerSettings], None]:
    bases = extraction.extract_bases(cls)
    return partial(create_handler_generic, cls, bases)
