import traceback

from typing import Optional, Type
from types import TracebackType

from . import target
from . import util
from .unit_meta import UnitMeta


@util.mark_as_target
class Unit(target.Target, metaclass=UnitMeta):
    def lifecycle_exception_handler(self, error: Exception) -> None:
        traceback.print_exc()

    # === context management ===

    def __enter__(self):
        self.pre_startup()
        return self

    async def __aenter__(self):
        await self.on_startup()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        await self.on_shutdown()
        return True

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        self.post_shutdown()
        return True
