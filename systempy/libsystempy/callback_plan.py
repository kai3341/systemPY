from collections.abc import Callable, Generator, Iterable
from typing import TYPE_CHECKING

from .check import check_callback_signature
from .constants import lifecycle_registered_methods
from .local_typing import P, R, WeakTypeIterable
from .register import register_hook_after, register_hook_before

if TYPE_CHECKING:
    from .hook_registry import HookRegistry


def build_callback_plan_hook_iter(
    cls: type,
    bases: WeakTypeIterable,
    reason: Callable[P, R],
    hook_registry: "HookRegistry[P, R]",
) -> Generator[Callable[P, R], None, None]:
    if reason in hook_registry:
        next_reasons = hook_registry[reason]
        for next_reason in next_reasons:
            assert callable(next_reason)
            next_registered_methods = lifecycle_registered_methods[next_reason]
            next_reason_interface = next_registered_methods.interface()
            direction_handler = next_registered_methods.direction
            assert next_reason_interface

            if issubclass(cls, next_reason_interface):
                next_callbacks = direction_handler(bases, next_reason)

                for next_callback in next_callbacks:
                    check_callback_signature(next_reason, next_callback)

                yield from build_callback_plan_iter(
                    cls,
                    bases,
                    next_reason,
                    next_callbacks,
                )


def build_callback_plan_iter(
    cls: type,
    bases: WeakTypeIterable,
    reason: Callable[P, R],
    callbacks: Iterable[Callable[P, R]] = (),
) -> Generator[Callable[P, R], None, None]:
    yield from build_callback_plan_hook_iter(cls, bases, reason, register_hook_before)
    yield from callbacks
    yield from build_callback_plan_hook_iter(cls, bases, reason, register_hook_after)


def build_callback_plan(
    cls: type,
    bases: WeakTypeIterable,
    reason: Callable[P, R],
    callbacks: Iterable[Callable[P, R]],
) -> tuple[Callable[P, R], ...]:
    for func in callbacks:
        check_callback_signature(reason, func)

    callbacks_total = build_callback_plan_iter(cls, bases, reason, callbacks)
    return tuple(callbacks_total)
