from typing import TYPE_CHECKING, Generic, ParamSpec

from .target import ProcessTargetABC
from .util import mark_as_target

A = ParamSpec("A")


@mark_as_target
class ProcessUnit(Generic[A], ProcessTargetABC, final=False):
    def run_sync(self) -> None:
        with self:
            self.main_sync()

    if TYPE_CHECKING:

        def __init__(self, *args: A.args, **kwargs: A.kwargs) -> None: ...

    @classmethod
    def launch(cls, *args: A.args, **kwargs: A.kwargs) -> None:
        self = cls(*args, **kwargs)
        self.run_sync()
