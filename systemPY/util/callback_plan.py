from . import constants
from .check import check_callback_signature


def build_callback_plan_hook_iter(cls, reason, hook_registry):
    lifecycle_registered_methods = constants.lifecycle_registered_methods
    if reason in hook_registry:
        next_reasons = hook_registry[reason]
        for next_reason in next_reasons:
            next_registered_methods = lifecycle_registered_methods[next_reason]
            next_reason_interface = next_registered_methods["interface"]

            if issubclass(cls, next_reason_interface):
                next_callback = getattr(cls, next_reason.__name__)
                check_callback_signature(next_reason, next_callback)
                yield from build_callback_plan_iter(
                    cls,
                    next_reason,
                    [next_callback],
                )


def build_callback_plan_iter(cls, reason, callbacks=()):
    yield from build_callback_plan_hook_iter(
        cls,
        reason,
        constants.lifecycle_hooks_before,
    )

    yield from callbacks

    yield from build_callback_plan_hook_iter(
        cls,
        reason,
        constants.lifecycle_hooks_after,
    )


def build_callback_plan(cls, reason, callbacks):
    for func in callbacks:
        check_callback_signature(reason, func)

    callbacks_total = build_callback_plan_iter(cls, reason, callbacks)
    callbacks_total = tuple(callbacks_total)

    return callbacks_total
