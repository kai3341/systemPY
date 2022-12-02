from typing import Generator, Tuple, Iterable
from .local_typing import CTFT, function_types

from .check import check_callback_signature
from .misc import HookRegistry
from .constants import lifecycle_registered_methods
from .register import register_hook_before, register_hook_after


def build_callback_plan_hook_iter(
    cls: type,
    reason: CTFT,
    hook_registry: HookRegistry,
) -> Generator[CTFT, None, None]:
    if reason in hook_registry:
        next_reasons = hook_registry[reason]
        for next_reason in next_reasons:
            assert isinstance(next_reason, function_types)
            next_registered_methods = lifecycle_registered_methods[next_reason]
            next_reason_interface = next_registered_methods.interface
            assert next_reason_interface

            if issubclass(cls, next_reason_interface):
                next_callback = getattr(cls, next_reason.__name__)
                assert isinstance(next_callback, function_types)
                check_callback_signature(next_reason, next_callback)
                yield from build_callback_plan_iter(
                    cls,
                    next_reason,
                    (next_callback,),
                )


def build_callback_plan_iter(
    cls: type,
    reason: CTFT,
    callbacks: Iterable[CTFT] = (),
) -> Generator[CTFT, None, None]:
    yield from build_callback_plan_hook_iter(cls, reason, register_hook_before)
    yield from callbacks
    yield from build_callback_plan_hook_iter(cls, reason, register_hook_after)


def build_callback_plan(
    cls: type,
    reason: CTFT,
    callbacks: Iterable[CTFT],
) -> Tuple[CTFT, ...]:
    for func in callbacks:
        check_callback_signature(reason, func)

    callbacks_total = build_callback_plan_iter(cls, reason, callbacks)
    return tuple(callbacks_total)
