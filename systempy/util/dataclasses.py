from dataclasses import dataclass
from typing import Optional

from .typing import DirectionHandler, TargetDirection


@dataclass()
class LFMethodsRegistered:
    direction: Optional[DirectionHandler]
    direction_name: Optional[TargetDirection]
    interface: Optional[type]


# LFMethodsRegistered.__slots__ = tuple(LFMethodsRegistered.__annotations__)
