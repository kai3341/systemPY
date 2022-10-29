import traceback

from dataclasses import dataclass
from typing import Optional, Type, cast
from types import TracebackType

from . import target
from . import util
from .util import configuration as util_configuration


class UnitMeta(type):
    def __new__(
        cls: Type[type],
        name: str,
        bases: tuple,
        classdict: dict,
    ) -> "UnitMeta":
        util_configuration.update_annotation(classdict, bases)
        classdict["__slots__"] = tuple(classdict["__annotations__"])
        new_cls = type.__new__(cls, name, bases, classdict)
        util_configuration.apply_additional_configuration(new_cls)
        new_cls = dataclass(new_cls)
        return cast(UnitMeta, new_cls)


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
