from functools import partial, lru_cache
from typing import Type, Iterable, Callable
from .systempy_typing import T
from . import extraction


def create_handler_generic(
    cls: T,
    bases: Iterable[T],
    name: str,
    reason: Callable,
    collect: Callable,
    compose: Callable,
):
    callbacks = collect(bases, name)
    handler = compose(cls, reason, callbacks)
    setattr(cls, name, handler)


@lru_cache(maxsize=None)
def create_partial_handler_generic(
    cls: Type,
) -> Callable[[str, Callable, Callable, Callable], None]:
    bases = extraction.extract_bases(cls)
    return partial(create_handler_generic, cls, bases)
