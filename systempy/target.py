import abc

from . import util


@util.register_target
class Target:
    @util.register_target_method("forward")
    def on_init(self) -> None:
        ...

    @util.register_target_method("forward")
    def pre_startup(self) -> None:
        ...

    @util.register_target_method("forward")
    async def on_startup(self) -> None:
        ...

    @util.register_target_method("backward")
    async def on_shutdown(self) -> None:
        ...

    @util.register_target_method("backward")
    def post_shutdown(self) -> None:
        ...

    @util.register_target_method("backward")
    def on_exit(self) -> None:
        ...


@util.mark_as_target
class ProcessTargetABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def main_sync(self) -> None:
        ...

    @abc.abstractmethod
    def run_sync(self) -> None:
        ...

    @abc.abstractmethod
    def reload(self, *args) -> None:
        ...

    @classmethod
    def launch(cls, **kwargs):
        self = cls(**kwargs)
        self.run_sync()


@util.mark_as_target
class DaemonTargetABC(ProcessTargetABC):
    @abc.abstractmethod
    async def main_async(self) -> None:
        ...

    @abc.abstractmethod
    async def run_async(self) -> None:
        ...

    @abc.abstractmethod
    def stop(self) -> None:
        ...


__all__ = (
    "Target",
    "ProcessTargetABC",
    "DaemonTargetABC",
)
