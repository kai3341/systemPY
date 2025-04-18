import atexit
from abc import abstractmethod
from collections.abc import Iterator
from dataclasses import Field, dataclass, fields
from types import TracebackType
from typing import Self

from .target_meta import TargetMeta
from .util import CONST, mark_as_target, register_target, register_target_method


@mark_as_target
class _TargetBase(metaclass=TargetMeta): ...


@register_target
class TargetInterface(_TargetBase):
    @register_target_method(CONST.FORWARD)
    def on_init(self) -> None: ...

    @register_target_method(CONST.FORWARD)
    def pre_startup(self) -> None: ...

    @register_target_method(CONST.FORWARD)
    async def on_startup(self) -> None: ...

    @register_target_method(CONST.BACKWARD)
    async def on_shutdown(self) -> None: ...

    @register_target_method(CONST.BACKWARD)
    def post_shutdown(self) -> None: ...

    @register_target_method(CONST.BACKWARD)
    def on_exit(self) -> None: ...


@mark_as_target
class _TargetInit(TargetInterface, final=False):
    def __post_init__(self) -> None:
        atexit.register(self.on_exit)
        self.on_init()


@mark_as_target
class _TargetCtxMgrSync(TargetInterface, final=False):
    def __enter__(self) -> Self:
        self.pre_startup()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        self.post_shutdown()


@mark_as_target
@dataclass()
class _TargetFieldIter(TargetInterface, final=False):
    def __iter__(self) -> Iterator[Field]:
        yield from fields(self)


@mark_as_target
class _TargetCtxMgrAsync(TargetInterface, final=False):
    async def __aenter__(self) -> Self:
        await self.on_startup()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        await self.on_shutdown()


@mark_as_target
class Target(
    _TargetInit,
    _TargetCtxMgrSync,
    _TargetCtxMgrAsync,
    _TargetFieldIter,
    final=False,
):
    pass


@mark_as_target
class ProcessTargetABC(Target, final=False):
    @abstractmethod
    def main_sync(self) -> None: ...

    @abstractmethod
    def run_sync(self) -> None: ...

    @abstractmethod
    def reload(self) -> None: ...


@mark_as_target
class DaemonTargetABC(Target, final=False):
    @abstractmethod
    async def main_async(self) -> None: ...

    @abstractmethod
    async def run_async(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...


__all__ = (
    "DaemonTargetABC",
    "ProcessTargetABC",
    "Target",
)
