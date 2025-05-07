from pathlib import Path
from sys import path

root_dir = Path(__file__).parent.parent
path.append(str(root_dir))

from _util._cbutil import _method_async, _method_sync
from systempy import (
    DIRECTION,
    EventWaitUnit,
    register_hook_after,
    register_hook_before,
)
from systempy.unit.ext.target_ext import ExtTarget


class ExampleDaemonTarget(ExtTarget):
    @register_hook_before(ExtTarget.on_init, DIRECTION.FORWARD)
    def before_on_init(self) -> None: ...

    @register_hook_after(ExtTarget.on_init, DIRECTION.FORWARD)
    def after_on_init(self) -> None: ...

    @register_hook_before(ExtTarget.pre_startup, DIRECTION.FORWARD)
    def before_pre_startup(self) -> None: ...

    @register_hook_after(ExtTarget.pre_startup, DIRECTION.FORWARD)
    def after_pre_startup(self) -> None: ...

    @register_hook_before(ExtTarget.post_startup, DIRECTION.FORWARD)
    async def before_post_startup(self) -> None: ...

    @register_hook_after(ExtTarget.post_startup, DIRECTION.GATHER)
    async def after_post_startup(self) -> None: ...

    @register_hook_before(ExtTarget.pre_shutdown, DIRECTION.GATHER)
    async def before_pre_shutdown(self) -> None: ...

    @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
    def after_post_shutdown(self) -> None: ...

    @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
    def also_after_post_shutdown(self) -> None: ...

    @register_hook_after(also_after_post_shutdown, DIRECTION.BACKWARD)
    def after_also_after_post_shutdown(self) -> None: ...


_gather = _method_async(print, "*")

_sync_1 = _method_sync(print, "1")
_async_1 = _method_async(print, "1")


class ExampleDaemon1Unit(ExampleDaemonTarget):
    @_sync_1
    def before_on_init(self) -> None: ...

    @_sync_1
    def on_init(self) -> None: ...

    @_sync_1
    def after_on_init(self) -> None: ...

    @_sync_1
    def before_pre_startup(self) -> None: ...

    @_sync_1
    def pre_startup(self) -> None: ...

    @_sync_1
    def after_pre_startup(self) -> None: ...

    @_async_1
    async def on_startup(self) -> None: ...

    @_async_1
    async def post_startup(self) -> None: ...

    @_async_1
    async def before_post_startup(self) -> None: ...

    @_gather
    async def after_post_startup(self) -> None: ...

    @_gather
    async def before_pre_shutdown(self) -> None: ...

    @_async_1
    async def pre_shutdown(self) -> None: ...

    @_async_1
    async def on_shutdown(self) -> None: ...

    @_sync_1
    def post_shutdown(self) -> None: ...

    @_sync_1
    def after_post_shutdown(self) -> None: ...

    @_sync_1
    def also_after_post_shutdown(self) -> None: ...

    @_sync_1
    def after_also_after_post_shutdown(self) -> None: ...


_sync_2 = _method_sync(print, "2")
_async_2 = _method_async(print, "2")


class ExampleDaemon2Unit(ExampleDaemonTarget):
    @_sync_2
    def before_on_init(self) -> None: ...

    @_sync_2
    def on_init(self) -> None: ...

    @_sync_2
    def after_on_init(self) -> None: ...

    @_sync_2
    def before_pre_startup(self) -> None: ...

    @_sync_2
    def pre_startup(self) -> None: ...

    @_sync_2
    def after_pre_startup(self) -> None: ...

    @_async_2
    async def on_startup(self) -> None: ...

    @_async_2
    async def post_startup(self) -> None: ...

    @_async_2
    async def before_post_startup(self) -> None: ...

    @_gather
    async def after_post_startup(self) -> None: ...

    @_gather
    async def before_pre_shutdown(self) -> None: ...

    @_async_2
    async def pre_shutdown(self) -> None: ...

    @_async_2
    async def on_shutdown(self) -> None: ...

    @_sync_2
    def post_shutdown(self) -> None: ...

    @_sync_2
    def after_post_shutdown(self) -> None: ...

    @_sync_2
    def also_after_post_shutdown(self) -> None: ...

    @_sync_2
    def after_also_after_post_shutdown(self) -> None: ...


_sync_3 = _method_sync(print, "3")
_async_3 = _method_async(print, "3")


class ExampleDaemon3Unit(ExampleDaemonTarget):
    @_sync_3
    def before_on_init(self) -> None: ...

    @_sync_3
    def on_init(self) -> None: ...

    @_sync_3
    def after_on_init(self) -> None: ...

    @_sync_3
    def before_pre_startup(self) -> None: ...

    @_sync_3
    def pre_startup(self) -> None: ...

    @_sync_3
    def after_pre_startup(self) -> None: ...

    @_async_3
    async def on_startup(self) -> None: ...

    @_async_3
    async def post_startup(self) -> None: ...

    @_async_3
    async def before_post_startup(self) -> None: ...

    @_gather
    async def after_post_startup(self) -> None: ...

    @_gather
    async def before_pre_shutdown(self) -> None: ...

    @_async_3
    async def pre_shutdown(self) -> None: ...

    @_async_3
    async def on_shutdown(self) -> None: ...

    @_sync_3
    def post_shutdown(self) -> None: ...

    @_sync_3
    def after_post_shutdown(self) -> None: ...

    @_sync_3
    def also_after_post_shutdown(self) -> None: ...

    @_sync_3
    def after_also_after_post_shutdown(self) -> None: ...


class ExampleDaemonApp(
    ExampleDaemon1Unit,
    ExampleDaemon2Unit,
    ExampleDaemon3Unit,
    EventWaitUnit,
):
    async def main_async(self) -> None:
        print("main_async")  # noqa: T201
        return await super().main_async()


if __name__ == "__main__":
    ExampleDaemonApp.launch()
