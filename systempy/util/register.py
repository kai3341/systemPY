from collections.abc import Callable
from inspect import iscoroutinefunction

from .constants import (
    lifecycle_additional_configuration,
    lifecycle_bases_blacklist,
    lifecycle_registered_methods,
    sync_or_async,
)
from .enums import CONST
from .local_dataclasses import (
    ClsCFG,
    GenericHandlerSettings,
    HookRegistry,
    LFMethodsRegistered,
    NamedRegistry,
)
from .local_typing import (
    TT,
    CTuple,
    Decorator,
    T,
    TypeIterable,
    function_types,
)
from .misc import get_key_or_create

register_addition_cfg_applier: NamedRegistry[[type, ClsCFG], None] = NamedRegistry()
register_direction: NamedRegistry[[TypeIterable, str], CTuple] = NamedRegistry()
register_handler_by_aio: NamedRegistry[[type, Callable, CTuple], Callable] = (
    NamedRegistry()
)
register_check_method_type: NamedRegistry[[Callable], None] = NamedRegistry()

register_hook_before: HookRegistry = HookRegistry()
register_hook_after: HookRegistry = HookRegistry()


def mark_as_target(cls: TT) -> TT:
    lifecycle_bases_blacklist.add(cls)
    return cls


def register_target_method(direction: CONST) -> Decorator:
    direction_handler = register_direction[direction]

    def inner(func: Callable) -> Callable:
        if not callable(func):
            raise TypeError(f"{func} is not a callable")  # noqa: EM102, TRY003

        lifecycle_registered_methods[func] = LFMethodsRegistered(
            interface=None,
            direction_name=direction,
            direction=direction_handler,
        )

        return func

    return inner


def register_target(cls: type[T]) -> type[T]:
    mark_as_target(cls)

    clsdict = vars(cls)

    for target in clsdict.values():
        if not isinstance(target, function_types):
            continue

        if target not in lifecycle_registered_methods:
            continue

        lifecycle_registered_this_methods = lifecycle_registered_methods[target]
        lifecycle_registered_this_methods.interface = cls
        direction_handler = lifecycle_registered_this_methods.direction
        direction_name = lifecycle_registered_this_methods.direction_name

        assert direction_name
        assert direction_handler

        if direction_name in register_check_method_type:
            checker = register_check_method_type[direction_name]
            checker(target)

        # register_handler_by_aio: GATHER or (A)SYNC
        method_type_handler = register_handler_by_aio.get_or_raise(
            direction_name,
            sync_or_async[iscoroutinefunction(target)],
        )

        clscfg = get_key_or_create(
            lifecycle_additional_configuration,
            cls,
            ClsCFG,
        )

        clscfg_stack_method = clscfg.stack_method
        target_name = target.__name__

        # I think it would be good enough to crash on developer's machine but
        # don't do this check on the production
        assert target_name not in clscfg_stack_method, "It's not allowed to "

        clscfg_stack_method[target_name] = GenericHandlerSettings(
            target,
            direction_handler,
            method_type_handler,
        )

    return cls


# === Just populate registries ===
from . import check, extraction, handler_type  # noqa: E402, F401

__all__ = (
    "mark_as_target",
    "register_addition_cfg_applier",
    "register_check_method_type",
    "register_direction",
    "register_handler_by_aio",
    "register_hook_after",
    "register_hook_before",
    "register_target",
    "register_target_method",
)
