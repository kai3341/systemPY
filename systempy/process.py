# from mypy_extensions import trait

from .target import ProcessTargetABC
from .util import mark_as_target

from typing import Any


@mark_as_target
# @trait
class ProcessUnit(ProcessTargetABC):
    def run_sync(self) -> None:
        with self:
            self.main_sync()

    @classmethod
    def launch(cls, **kwargs: Any) -> None:
        self = cls(**kwargs)
        self.run_sync()
