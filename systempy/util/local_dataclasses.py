from sys import version_info
from dataclasses import dataclass, field
from typing import Optional, Callable, Tuple, Dict

from . import local_typing


dataclass_kwargs: Dict[str, bool] = {}

if version_info > (3, 10):
    dataclass_kwargs["slots"] = True


@dataclass(**dataclass_kwargs)
class LFMethodsRegistered:
    direction: Optional["local_typing.DirectionHandler"]
    direction_name: Optional["local_typing.TargetDirection"]
    interface: Optional[type]


@dataclass(**dataclass_kwargs)
class GenericHandlerSettings:
    reason: Callable
    collect: Callable[["local_typing.TypeIterable", str], "local_typing.LFMethodTuple"]
    compose: Callable[[type, Callable, "local_typing.LFMethodTuple"], Callable]


@dataclass(**dataclass_kwargs)
class SeparatedLFMethods:
    callbacks_sync: Tuple["local_typing.LFMethodSync", ...]
    callbacks_async: Tuple["local_typing.LFMethodAsync", ...]


@dataclass(**dataclass_kwargs)
class ClsCFG:
    stack_method: "local_typing.SMConfig" = field(default_factory=dict)
