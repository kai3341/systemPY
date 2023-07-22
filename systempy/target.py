# import abc
import atexit

from typing import Optional, Type
from types import TracebackType

from mypy_extensions import trait
from typing_extensions import Self, dataclass_transform

from .util import register_target, register_target_method, mark_as_target


@register_target
@dataclass_transform()
class TargetInterface:
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


@mark_as_target
@trait
class _TargetInit(TargetInterface):
    def __post_init__(self) -> None:
        atexit.register(self.on_exit)
        self.on_init()


@mark_as_target
@trait
class _TargetCtxMgrSync(TargetInterface):
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


@mark_as_target
@trait
class _TargetCtxMgrAsync(TargetInterface):
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
class Target(_TargetInit, _TargetCtxMgrSync, _TargetCtxMgrAsync):
    ...


@mark_as_target
class ProcessTargetABC(Target):
    "Unfortunally `abc` can not be used because can not use 2 metaclasses"

    def main_sync(self) -> None:
        raise NotImplementedError()

    def run_sync(self) -> None:
        raise NotImplementedError()

    def reload(self) -> None:
        raise NotImplementedError()


@mark_as_target
class DaemonTargetABC(Target):
    "Unfortunally `abc` can not be used because can not use 2 metaclasses"

    async def main_async(self) -> None:
        raise NotImplementedError()

    async def run_async(self) -> None:
        raise NotImplementedError()

    def stop(self) -> None:
        raise NotImplementedError()


__all__ = (
    "Target",
    "ProcessTargetABC",
    "DaemonTargetABC",
)
