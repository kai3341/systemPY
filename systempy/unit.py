import atexit
import traceback

from typing import Optional, Type
from types import TracebackType

from . import target
from . import util
from .util import configuration as util_configuration


@util.mark_as_target
class Unit(target.Target):
    def lifecycle_exception_handler(self, error: Exception) -> None:
        traceback.print_exc()

    # === __magic__ ===

    def __init__(self, **kwargs):
        atexit.register(self.on_exit)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.on_init()

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        util_configuration.apply_additional_configuration(cls)

    # === context management ===

    def __enter__(self):
        self.pre_startup()

    async def __aenter__(self):
        await self.on_startup()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        await self.on_shutdown()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        self.post_shutdown()
