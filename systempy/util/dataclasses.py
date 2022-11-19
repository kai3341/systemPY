from dataclasses import dataclass
from typing import Optional, Callable

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
