from inspect import isfunction, iscoroutinefunction

from . import constants
from .misc import create_dict_registerer, get_key_or_create
from .typing import TargetDirection


register_addition_cfg_applier = create_dict_registerer(
    constants.apply_additional_config__cfg,
)

register_direction = create_dict_registerer(
    # ===
    constants.handler_by_direction
)

register_handler_by_iscoroutinefunction = create_dict_registerer(
    constants.handler_by_iscoroutinefunction
)


register_check_method_type = create_dict_registerer(
    constants.on_register_check_method_type,
)


def mark_as_target(cls):
    constants.lifecycle_bases_blacklist.add(cls)
    return cls


def register_target_method(direction: TargetDirection):
    def inner(func):
        if not isfunction(func):
            raise ValueError(f"{func} is not a function")

        constants.lifecycle_registered_methods[func] = {
            "direction_name": direction,
            "direction": constants.handler_by_direction[direction],
        }
        return func

    return inner


def register_target(cls):
    mark_as_target(cls)

    lifecycle_registered_methods = constants.lifecycle_registered_methods
    handler_by_iscoroutinefunction = constants.handler_by_iscoroutinefunction
    for target in cls.__dict__.values():

        if not target in lifecycle_registered_methods:
            continue

        lifecycle_registered_this_methods = lifecycle_registered_methods[target]
        lifecycle_registered_this_methods["interface"] = cls
        direction_handler = lifecycle_registered_this_methods["direction"]
        direction_name = lifecycle_registered_this_methods["direction_name"]

        if direction_name in handler_by_iscoroutinefunction:
            method_type_name = direction_name
        else:
            method_async = iscoroutinefunction(target)
            method_type_name = constants.sync_or_async[method_async]

        if method_type_name in constants.on_register_check_method_type:
            checker = constants.on_register_check_method_type[method_type_name]
            checker(target)

        method_type_handler = handler_by_iscoroutinefunction[method_type_name]

        method_name = target.__name__

        current_cls_config = get_key_or_create(
            constants.lifecycle_additional_configuration,
            cls,
        )

        subconfig = get_key_or_create(
            current_cls_config,
            "stack_method",
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


def create_register_hook(lifecycle_hooks):
    lifecycle_hooks_parents = constants.lifecycle_hooks_parents

    def register_hook(lifecycle_method):
        registry = get_key_or_create(
            lifecycle_hooks,
            lifecycle_method,
            list,
        )

        if lifecycle_method in lifecycle_hooks_parents:
            lifecycle_method_parent = lifecycle_hooks_parents[lifecycle_method]
        else:
            lifecycle_method_parent = lifecycle_method

        parent_syncronous = not iscoroutinefunction(lifecycle_method_parent)

        def inner(func):
            if parent_syncronous and iscoroutinefunction(func):
                raise ValueError(register_hook_invalid_template % func)

            lifecycle_hooks_parents[func] = lifecycle_method_parent
            registry.append(func)
            return func

        return inner

    return register_hook


register_hook_before = create_register_hook(constants.lifecycle_hooks_before)
register_hook_after = create_register_hook(constants.lifecycle_hooks_after)

# === Just populate registries ===

from . import extraction

extraction.__package__

from . import handler_type

handler_type.__package__

from . import check

check.__package__
