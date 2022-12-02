from inspect import iscoroutinefunction

from .misc import NamedRegistry, HookRegistry, get_key_or_create

from .local_typing import (
    TargetDirection,
    TT,
    CFT,
    LFDecorator,
    function_types,
)

from .local_dataclasses import (
    LFMethodsRegistered,
    GenericHandlerSettings,
    ClsCFG,
)

from .constants import (
    lifecycle_bases_blacklist,
    lifecycle_registered_methods,
    lifecycle_additional_configuration,
    sync_or_async,
)

register_addition_cfg_applier = NamedRegistry()
register_direction = NamedRegistry()
register_handler_by_aio = NamedRegistry()
register_check_method_type = NamedRegistry()

register_hook_before = HookRegistry()
register_hook_after = HookRegistry()


def mark_as_target(cls: TT) -> TT:
    lifecycle_bases_blacklist.add(cls)
    return cls


def register_target_method(direction: TargetDirection) -> LFDecorator:
    direction_handler = register_direction[direction]

    def inner(func: CFT) -> CFT:
        if not callable(func):
            raise ValueError(f"{func} is not a callable")

        registered_method = LFMethodsRegistered(
            interface=None,
            direction_name=direction,
            direction=direction_handler,
        )

        lifecycle_registered_methods[func] = registered_method

        return func

    return inner


def register_target(cls: TT) -> TT:
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

        method_async = iscoroutinefunction(target)
        method_type_name = sync_or_async[method_async]

        method_type_handler = register_handler_by_aio[method_type_name]

        method_name = target.__name__

        clscfg = get_key_or_create(
            lifecycle_additional_configuration,
            cls,
            ClsCFG,
        )

        clscfg.stack_method[method_name] = GenericHandlerSettings(
            target,
            direction_handler,
            method_type_handler,
        )

    return cls


# === Just populate registries ===

from . import extraction

extraction.__package__

from . import handler_type

handler_type.__package__

from . import check

check.__package__

__all__ = (
    "register_addition_cfg_applier",
    "register_direction",
    "register_handler_by_aio",
    "register_check_method_type",
    "mark_as_target",
    "register_target_method",
    "register_target",
    "register_hook_before",
    "register_hook_after",
)
