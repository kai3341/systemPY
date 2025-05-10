from collections.abc import Callable
from inspect import iscoroutinefunction
from typing import Generic, Protocol, TypeVar
from weakref import WeakKeyDictionary, WeakSet, WeakValueDictionary, ref

from typing_extensions import ParamSpec

from .constants import (
    lifecycle_additional_configuration,
    lifecycle_registered_methods,
    sync_or_async,
)
from .enums import DIRECTION
from .hook_registry import HookRegistry
from .local_dataclasses import (
    ClsCFG,
    GenericHandlerSettings,
    LFMethodsRegistered,
    NamedRegistry,
    SetRegistry,
)
from .local_typing import (
    CTuple,
    Decorator,
    T,
    WeakTypeIterable,
    function_types,
)
from .misc import get_key_or_create

P = ParamSpec("P")
R = TypeVar("R")

register_addition_cfg_applier: "NamedRegistry[[type, ClsCFG], None]" = NamedRegistry(
    WeakValueDictionary(),
)
register_direction: "NamedRegistry[[WeakTypeIterable, Callable], CTuple]" = (
    NamedRegistry(
        WeakValueDictionary(),
    )
)
register_handler_by_aio: "NamedRegistry[[type, WeakTypeIterable, Callable, CTuple],Callable]" = NamedRegistry(  # noqa: E501
    WeakValueDictionary(),
)
register_check_method_type: "NamedRegistry[[Callable], None]" = NamedRegistry(
    WeakValueDictionary(),
)

register_hook_before: HookRegistry = HookRegistry(WeakKeyDictionary())
register_hook_after: HookRegistry = HookRegistry(WeakKeyDictionary())
mark_as_target = SetRegistry[type](WeakSet())

# According to `typing.final` implementation I can't trust to `__final__` class
# attribure
mark_as_final = SetRegistry[type](WeakSet())

mark_as_target.add(object, Generic, Protocol)  # type:ignore[arg-type]


msg_not_callable = "{func} is not a callable"


def register_target_method(direction: DIRECTION) -> Decorator:
    direction_handler = register_direction[direction]

    def inner(func: Callable[P, R]) -> Callable[P, R]:
        if not callable(func):
            raise TypeError(msg_not_callable.format(func=func))

        lifecycle_registered_methods[func] = LFMethodsRegistered(
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
        lifecycle_registered_this_methods.interface = ref(cls)
        direction_handler = lifecycle_registered_this_methods.direction
        direction_name = lifecycle_registered_this_methods.direction_name

        assert direction_name

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
        assert target_name not in clscfg_stack_method, (
            "It's not allowed to override "
            f"'{clscfg_stack_method[target_name].reason()}' on '{cls}'"
        )

        clscfg_stack_method[target_name] = GenericHandlerSettings(
            ref(target),
            ref(direction_handler),
            ref(method_type_handler),
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
