from functools import partial, lru_cache
from typing import Type, Callable
from .typing import TypeIterable
from . import extraction


def create_handler_generic(
    cls: type,
    bases: TypeIterable,
    name: str,
    reason: Callable,
    collect: Callable,
    compose: Callable,
) -> None:
    callbacks = collect(bases, name)
    handler = compose(cls, reason, callbacks)
    setattr(cls, name, handler)


@lru_cache(maxsize=None)
def create_partial_handler_generic(
    cls: Type,
) -> Callable[[str, Callable, Callable, Callable], None]:
    bases = extraction.extract_bases(cls)
    return partial(create_handler_generic, cls, bases)
