from typing_extensions import deprecated

from .target import Target
from .util import mark_as_target


@deprecated("No reason to use since 0.1.0")
@mark_as_target
class Unit(Target, final=False): ...
