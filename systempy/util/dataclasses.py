from dataclasses import dataclass
from typing import Optional

from . import typing as _typing


@dataclass()
class LFMethodsRegistered:
    direction: Optional["_typing.DirectionHandler"]
    direction_name: Optional["_typing.TargetDirection"]
    interface: Optional[type]

    __slots__ = (
        "direction",
        "direction_name",
        "interface",
    )
