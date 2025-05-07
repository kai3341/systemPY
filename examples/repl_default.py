"""
ReplUnit is deprecated. Please use PTReplUnit instead.
"""

from pathlib import Path
from sys import path

root_dir = Path(__file__).parent.parent
path.append(str(root_dir))

from _util._cbutil import _method_sync
from systempy import ReplUnit, Target

_sync_1 = _method_sync(print, "1")


class ExampleDaemon1Unit(Target):
    @_sync_1
    def on_init(self) -> None: ...

    @_sync_1
    def pre_startup(self) -> None: ...

    @_sync_1
    def post_shutdown(self) -> None: ...


_sync_2 = _method_sync(print, "2")


class ExampleDaemon2Unit(Target):
    @_sync_2
    def on_init(self) -> None: ...

    @_sync_2
    def pre_startup(self) -> None: ...

    @_sync_2
    def post_shutdown(self) -> None: ...


_sync_3 = _method_sync(print, "3")


class ExampleDaemon3Unit(Target):
    @_sync_3
    def on_init(self) -> None: ...

    @_sync_3
    def pre_startup(self) -> None: ...

    @_sync_3
    def post_shutdown(self) -> None: ...


class ExampleDefaultReplApp(
    ExampleDaemon1Unit,
    ExampleDaemon2Unit,
    ExampleDaemon3Unit,
    ReplUnit,
): ...


if __name__ == "__main__":
    ExampleDefaultReplApp.launch()
