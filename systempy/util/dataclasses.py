from dataclasses import dataclass, field
from typing import Optional, Callable, Tuple

from . import typing as _typing


@dataclass()
class LFMethodsRegistered:
    direction: Optional["_typing.DirectionHandler"]
    direction_name: Optional["_typing.TargetDirection"]
    interface: Optional[type]


@dataclass()
class GenericHandlerSettings:
    reason: Callable
    collect: Callable[["_typing.TypeIterable", str], "_typing.LFMethodTuple"]
    compose: Callable[[type, Callable, "_typing.LFMethodTuple"], Callable]


@dataclass()
class SeparatedLFMethods:
    callbacks_sync: Tuple["_typing.LFMethodSync", ...]
    callbacks_async: Tuple["_typing.LFMethodAsync", ...]


@dataclass()
class ClsCFG:
    stack_method: "_typing.SMConfig" = field(default_factory=dict)
