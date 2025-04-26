from typing import TYPE_CHECKING, Generic, ParamSpec

from ..target import ProcessMixinABC

A = ParamSpec("A")


class ProcessUnit(Generic[A], ProcessMixinABC):
    def run_sync(self) -> None:
        with self:
            self.main_sync()

    if TYPE_CHECKING:

        def __init__(self, *args: A.args, **kwargs: A.kwargs) -> None: ...

    @classmethod
    def launch(cls, *args: A.args, **kwargs: A.kwargs) -> None:
        self = cls(*args, **kwargs)
        self.run_sync()
