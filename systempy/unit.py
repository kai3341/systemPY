from .target import Target
from .util import mark_as_target
from .unit_meta import UnitMeta

# from mypy_extensions import trait


# @trait
@mark_as_target
class Unit(Target, metaclass=UnitMeta):
    pass
