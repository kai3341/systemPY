from collections.abc import Callable, Generator, Iterable

from .check import check_callback_signature
from .constants import lifecycle_registered_methods
from .local_dataclasses import HookRegistry
from .local_typing import P, R, function_types
from .register import register_hook_after, register_hook_before


def build_callback_plan_hook_iter(
    cls: type,
    reason: Callable[P, R],
    hook_registry: HookRegistry[P, R],
) -> Generator[Callable[P, R], None, None]:
    if reason in hook_registry:
        next_reasons = hook_registry[reason]
        for next_reason in next_reasons:
            assert callable(next_reason)
            next_registered_methods = lifecycle_registered_methods[next_reason]
            next_reason_interface = next_registered_methods.interface
            assert next_reason_interface

            if issubclass(cls, next_reason_interface):
                next_callback: Callable[P, R] = getattr(cls, next_reason.__name__)
                assert isinstance(next_callback, function_types)
                check_callback_signature(next_reason, next_callback)
                yield from build_callback_plan_iter(
                    cls,
                    next_reason,
                    (next_callback,),
                )


def build_callback_plan_iter(
    cls: type,
    reason: Callable[P, R],
    callbacks: Iterable[Callable[P, R]] = (),
) -> Generator[Callable[P, R], None, None]:
    yield from build_callback_plan_hook_iter(cls, reason, register_hook_before)
    yield from callbacks
    yield from build_callback_plan_hook_iter(cls, reason, register_hook_after)


def build_callback_plan(
    cls: type,
    reason: Callable[P, R],
    callbacks: Iterable[Callable[P, R]],
) -> tuple[Callable[P, R], ...]:
    for func in callbacks:
        check_callback_signature(reason, func)

    callbacks_total = build_callback_plan_iter(cls, reason, callbacks)
    return tuple(callbacks_total)
