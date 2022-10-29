from dataclasses import dataclass
from typing import Optional, Type

from . import systempy_typing


@dataclass()
class LFMethodsRegistered:
    direction: Optional["systempy_typing.DirectionHandler"]
    direction_name: Optional["systempy_typing.TargetDirection"]
    interface: Optional[Type]

    __slots__ = (
        "direction",
        "direction_name",
        "interface",
    )
