from . import target
from . import util
from .unit_meta import UnitMeta

from mypy_extensions import trait


# @util.mark_as_target
@trait
class Unit(target.Target, metaclass=UnitMeta):
    pass


util.mark_as_target(Unit)
