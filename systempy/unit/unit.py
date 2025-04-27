from typing_extensions import deprecated

from ..target import Target
from ..util import ROLE


@deprecated("No reason to use since 0.1.0")
class Unit(Target, role=ROLE.MIXIN): ...
