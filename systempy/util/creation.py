from functools import partial, lru_cache
from typing import Type, Callable
from .typing import TypeIterable
from .dataclasses import GenericHandlerSettings
from . import extraction


def create_handler_generic(
    cls: type,
    bases: TypeIterable,
    name: str,
    settings: GenericHandlerSettings,
) -> None:
    callbacks = settings.collect(bases, name)
    handler = settings.compose(cls, settings.reason, callbacks)
    setattr(cls, name, handler)


@lru_cache(maxsize=None)
def create_partial_handler_generic(
    cls: Type,
) -> Callable[[str, GenericHandlerSettings], None]:
    bases = extraction.extract_bases(cls)
    return partial(create_handler_generic, cls, bases)
