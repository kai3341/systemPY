from inspect import iscoroutinefunction
from typing import Callable, Type

from .typing import (
    T,
    TargetDirection,
    FT,
    LFHookRegistry,
    Inner,
    Outer,
    LFDecorator,
)

from .dataclasses import LFMethodsRegistered
from .misc import create_dict_registerer, get_key_or_create

from .constants import (
    apply_additional_config__cfg,
    handler_by_direction,
    handler_by_iscoroutinefunction,
    on_register_check_method_type,
    lifecycle_bases_blacklist,
    lifecycle_registered_methods,
    lifecycle_additional_configuration,
    lifecycle_hooks_parents,
    lifecycle_hooks_before,
    lifecycle_hooks_after,
    sync_or_async,
)


register_addition_cfg_applier: Outer = create_dict_registerer(
    apply_additional_config__cfg,
)

register_direction: Outer = create_dict_registerer(
    # ===
    handler_by_direction,
)

register_handler_by_iscoroutinefunction: Outer = create_dict_registerer(
    handler_by_iscoroutinefunction,
)


register_check_method_type: Outer = create_dict_registerer(
    on_register_check_method_type,
)


def mark_as_target(cls: Type[T]) -> Type[T]:
    lifecycle_bases_blacklist.add(cls)
    return cls


def register_target_method(direction: TargetDirection) -> LFDecorator:
    def inner(func: FT) -> FT:
        if not callable(func):
            raise ValueError(f"{func} is not a callable")

        lifecycle_registered_methods[func] = LFMethodsRegistered(
            interface=None,
            direction_name=direction,
            direction=handler_by_direction[direction],
        )

        return func

    return inner


def register_target(cls: Type[T]) -> Type[T]:
    mark_as_target(cls)

    for target in cls.__dict__.values():
        if not callable(target):
            continue

        if target not in lifecycle_registered_methods:
            continue

        lifecycle_registered_this_methods = lifecycle_registered_methods[target]
        lifecycle_registered_this_methods.interface = cls
        direction_handler = lifecycle_registered_this_methods.direction
        direction_name = lifecycle_registered_this_methods.direction_name

        if direction_name in on_register_check_method_type:
            checker = on_register_check_method_type[direction_name]
            checker(target)

        method_async: bool = iscoroutinefunction(target)
        method_type_name = sync_or_async[method_async]

        method_type_handler = handler_by_iscoroutinefunction[method_type_name]

        method_name = target.__name__

        current_cls_config = get_key_or_create(
            lifecycle_additional_configuration,
            cls,
            dict,
        )

        subconfig = get_key_or_create(
            current_cls_config,
            "stack_method",
            dict,
        )

        subconfig[method_name] = (
            target,
            direction_handler,
            method_type_handler,
        )

    return cls


register_hook_invalid_template = (
    "You are trying to register executing asyncronous hook %s on the stage "
    "when event loop is not started or already stopped"
)


def create_register_hook(
    lifecycle_hooks: LFHookRegistry,
) -> Callable[[FT], Inner]:
    def register_hook(lifecycle_method: FT) -> Inner:
        registry: list = get_key_or_create(
            lifecycle_hooks,
            lifecycle_method,
            list,
        )

        lifecycle_method_parent = lifecycle_hooks_parents.get(
            lifecycle_method,
            lifecycle_method,
        )

        parent_syncronous = not iscoroutinefunction(lifecycle_method_parent)

        def inner(func: FT) -> FT:
            if parent_syncronous and iscoroutinefunction(func):
                raise ValueError(register_hook_invalid_template % func)

            lifecycle_hooks_parents[func] = lifecycle_method_parent
            registry.append(func)
            return func

        return inner

    return register_hook


register_hook_before = create_register_hook(lifecycle_hooks_before)
register_hook_after = create_register_hook(lifecycle_hooks_after)

# === Just populate registries ===

from . import extraction

extraction.__package__

from . import handler_type

handler_type.__package__

from . import check

check.__package__
