from typing import TYPE_CHECKING, Generic

from .target import ProcessTargetABC
from .util import mark_as_target
from .util.local_typing import A


@mark_as_target
class ProcessUnit(ProcessTargetABC, Generic[A], final=False):
    def run_sync(self) -> None:
        with self:
            self.main_sync()

    if TYPE_CHECKING:

        def __init__(self, *args: A.args, **kwargs: A.kwargs) -> None: ...

    @classmethod
    def launch(cls, *args: A.args, **kwargs: A.kwargs) -> None:
        self = cls(*args, **kwargs)
        self.run_sync()
