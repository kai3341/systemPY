from dataclasses import dataclass
from .util import mark_as_target
from .unit_meta import UnitMeta

from mypy_extensions import trait


@mark_as_target
@trait
@dataclass()
class Unit(metaclass=UnitMeta):
    pass
