from typing_extensions import deprecated

from ..libsystempy import ROLE
from ..target import Target


@deprecated("No reason to use since 0.1.0")
class Unit(Target, role=ROLE.MIXIN): ...
