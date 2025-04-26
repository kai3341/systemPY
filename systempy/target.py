import atexit
from abc import abstractmethod
from collections.abc import Iterator
from dataclasses import Field, fields
from types import TracebackType
from typing import Self

from .target_meta import TargetMeta
from .util import DIRECTION, handler_metadata, register_target_method


class InterfaceTarget(metaclass=TargetMeta):
    @register_target_method(DIRECTION.FORWARD)
    def on_init(self) -> None: ...

    @register_target_method(DIRECTION.FORWARD)
    def pre_startup(self) -> None: ...

    @register_target_method(DIRECTION.FORWARD)
    async def on_startup(self) -> None: ...

    @register_target_method(DIRECTION.BACKWARD)
    async def on_shutdown(self) -> None: ...

    @register_target_method(DIRECTION.BACKWARD)
    def post_shutdown(self) -> None: ...

    @register_target_method(DIRECTION.BACKWARD)
    def on_exit(self) -> None: ...


class _InitMixin(InterfaceTarget):
    def __post_init__(self) -> None:
        on_exit_meta = handler_metadata[type(self).on_exit]

        if on_exit_meta.call_order:
            atexit.register(self.on_exit)

        self.on_init()


class _CtxMgrSyncMixin(InterfaceTarget):
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


class _FieldIterMixin(InterfaceTarget):
    def __iter__(self) -> Iterator[Field]:
        yield from fields(self)


class _CtxMgrAsyncMixin(InterfaceTarget):
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


class Target(
    _InitMixin,
    _CtxMgrSyncMixin,
    _CtxMgrAsyncMixin,
    _FieldIterMixin,
): ...


class ProcessMixinABC(Target):
    @abstractmethod
    def main_sync(self) -> None: ...

    @abstractmethod
    def run_sync(self) -> None: ...

    @abstractmethod
    def reload(self) -> None: ...


class DaemonMixinABC(Target):
    @abstractmethod
    async def main_async(self) -> None: ...

    @abstractmethod
    async def run_async(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...


__all__ = (
    "DaemonMixinABC",
    "ProcessMixinABC",
    "Target",
)
