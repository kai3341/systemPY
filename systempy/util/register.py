from inspect import iscoroutinefunction
from typing import Callable, Type

from .typing import (
    T,
    TargetDirection,
    CT,
    LFHookRegistry,
    LFDecorator,
    function_types,
)

from .dataclasses import LFMethodsRegistered, GenericHandlerSettings
from .misc import NamedRegistry, get_key_or_create

from .constants import (
    lifecycle_bases_blacklist,
    lifecycle_registered_methods,
    lifecycle_additional_configuration,
    lifecycle_hooks_parents,
    lifecycle_hooks_before,
    lifecycle_hooks_after,
    sync_or_async,
)

Inner = Callable[[CT], CT]

register_addition_cfg_applier = NamedRegistry()
register_direction = NamedRegistry()
register_handler_by_iscoroutinefunction = NamedRegistry()
register_check_method_type = NamedRegistry()


def mark_as_target(cls: Type[T]) -> Type[T]:
    lifecycle_bases_blacklist.add(cls)
    return cls


def register_target_method(direction: TargetDirection) -> LFDecorator:
    direction_handler = register_direction[direction]

    def inner(func: CT) -> CT:
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


def register_target(cls: Type[T]) -> Type[T]:
    mark_as_target(cls)

    # clsdict = cls.__dict__
    clsdict = vars(cls)

    for method_name__, target in clsdict.items():
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

        method_async: bool = iscoroutinefunction(target)
        method_type_name = sync_or_async[method_async]

        method_type_handler = register_handler_by_iscoroutinefunction[method_type_name]

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

        subconfig[method_name] = GenericHandlerSettings(
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
) -> Callable[[CT], Inner]:
    def register_hook(lifecycle_method: CT) -> Inner:
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

        def inner(func: CT) -> CT:
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
