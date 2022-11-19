from typing import Generator, Dict, List, Tuple, Iterable
from .check import check_callback_signature

from .typing import CT

from .constants import (
    lifecycle_registered_methods,
    lifecycle_hooks_before,
    lifecycle_hooks_after,
)


def build_callback_plan_hook_iter(
    cls: type,
    reason: CT,
    hook_registry: Dict[CT, List[CT]],
) -> Generator[CT, None, None]:
    if reason in hook_registry:
        next_reasons = hook_registry[reason]
        for next_reason in next_reasons:
            next_registered_methods = lifecycle_registered_methods[next_reason]
            next_reason_interface = next_registered_methods.interface
            assert next_reason_interface

            if issubclass(cls, next_reason_interface):
                next_callback = getattr(cls, next_reason.__name__)
                check_callback_signature(next_reason, next_callback)
                yield from build_callback_plan_iter(
                    cls,
                    next_reason,
                    [next_callback],
                )


def build_callback_plan_iter(
    cls: type,
    reason: CT,
    callbacks: Iterable[CT] = (),
) -> Generator[CT, None, None]:
    yield from build_callback_plan_hook_iter(
        cls,
        reason,
        lifecycle_hooks_before,
    )

    yield from callbacks

    yield from build_callback_plan_hook_iter(
        cls,
        reason,
        lifecycle_hooks_after,
    )


def build_callback_plan(
    cls: type,
    reason: CT,
    callbacks: Iterable[CT],
) -> Tuple[CT, ...]:
    for func in callbacks:
        check_callback_signature(reason, func)

    callbacks_total = build_callback_plan_iter(cls, reason, callbacks)
    return tuple(callbacks_total)
