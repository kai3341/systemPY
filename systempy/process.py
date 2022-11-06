# from mypy_extensions import trait

from .target import ProcessTargetABC, Target
from .util import mark_as_target


# @trait
@mark_as_target
class ProcessUnit(Target, ProcessTargetABC):
    def run_sync(self) -> None:
        with self:
            self.main_sync()
