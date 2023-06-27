import abc
import atexit

from typing import Optional, Type, Dict, Any
from types import TracebackType

from mypy_extensions import trait
from typing_extensions import Self, dataclass_transform

from .util import register_target, register_target_method, mark_as_target


@register_target
@dataclass_transform()
@trait
class Target:
    def __post_init__(self) -> None:
        atexit.register(self.on_exit)
        self.on_init()

    @register_target_method("forward")
    def on_init(self) -> None:
        pass

    @register_target_method("forward")
    def pre_startup(self) -> None:
        pass

    @register_target_method("forward")
    async def on_startup(self) -> None:
        pass

    @register_target_method("backward")
    async def on_shutdown(self) -> None:
        pass

    @register_target_method("backward")
    def post_shutdown(self) -> None:
        pass

    @register_target_method("backward")
    def on_exit(self) -> None:
        pass

    def __enter__(self: Self) -> Self:
        self.pre_startup()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        self.post_shutdown()
        return True

    async def __aenter__(self: Self) -> Self:
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


@mark_as_target
@trait
class ProcessTargetABC:  # (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def main_sync(self) -> None:
        pass

    @abc.abstractmethod
    def run_sync(self) -> None:
        pass

    @abc.abstractmethod
    def reload(self) -> None:
        pass

    @classmethod
    def launch(cls, **kwargs: Dict[str, Any]) -> None:
        self = cls(**kwargs)
        self.run_sync()


@mark_as_target
@trait
class DaemonTargetABC:  # (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def main_async(self) -> None:
        pass

    @abc.abstractmethod
    async def run_async(self) -> None:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        pass


__all__ = (
    "Target",
    "ProcessTargetABC",
    "DaemonTargetABC",
)
