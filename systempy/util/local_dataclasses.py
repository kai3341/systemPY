from dataclasses import dataclass, field
from typing import Optional, Callable, Tuple

from . import local_typing


@dataclass()
class LFMethodsRegistered:
    direction: Optional["local_typing.DirectionHandler"]
    direction_name: Optional["local_typing.TargetDirection"]
    interface: Optional[type]


@dataclass()
class GenericHandlerSettings:
    reason: Callable
    collect: Callable[["local_typing.TypeIterable", str], "local_typing.LFMethodTuple"]
    compose: Callable[[type, Callable, "local_typing.LFMethodTuple"], Callable]


@dataclass()
class SeparatedLFMethods:
    callbacks_sync: Tuple["local_typing.LFMethodSync", ...]
    callbacks_async: Tuple["local_typing.LFMethodAsync", ...]


@dataclass()
class ClsCFG:
    stack_method: "local_typing.SMConfig" = field(default_factory=dict)
