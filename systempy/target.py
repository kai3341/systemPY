from __future__ import annotations

import atexit
from abc import abstractmethod
from dataclasses import Field, fields
from typing import TYPE_CHECKING, Generic

from typing_extensions import ParamSpec, Self

from .libsystempy import DIRECTION, ROLE, handler_metadata, register_target_method
from .target_meta import TargetMeta

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import TracebackType

A = ParamSpec("A")


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


class _FieldIterMixin(InterfaceTarget):
    def __iter__(self) -> Iterator[Field]:
        yield from fields(self)


class Target(
    _InitMixin,
    _FieldIterMixin,
    role=ROLE.MIXIN,
): ...


class SyncMixinABC(Target, Generic[A]):
    if TYPE_CHECKING:

        def __init__(self, *args: A.args, **kwargs: A.kwargs) -> None: ...

    @classmethod
    def launch(cls, *args: A.args, **kwargs: A.kwargs) -> None:
        self = cls(*args, **kwargs)
        self.run_sync()

    @abstractmethod
    def main_sync(self) -> None: ...

    @abstractmethod
    def run_sync(self) -> None: ...

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


class AsyncMixinABC(Target):
    @abstractmethod
    async def main_async(self) -> None: ...
    @abstractmethod
    async def run_async(self) -> None: ...

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


__all__ = (
    "AsyncMixinABC",
    "SyncMixinABC",
    "Target",
)
