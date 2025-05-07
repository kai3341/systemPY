import sys
from dataclasses import field
from os import path
from typing import ParamSpec

from ptpython.repl import embed

from systempy import LoopUnit
from systempy.unit.repl.mixins import ReplLocalsMixin

A = ParamSpec("A")


class PTReplUnit(ReplLocalsMixin, LoopUnit[A]):
    _module_qualname: str = field(init=False)
    _banner: str = field(init=False)

    repl_history_filename: str | None = field(default=None)
    repl_head: str | None = field(default=None)

    def on_init(self) -> None:
        self._setup_repl_caller_frame()
        self._setup_repl_env()
        self._setup_banner(self.repl_head)

    def _setup_banner(self, head: str | None = None) -> None:
        caller_globals = self._repl_caller_frame[0].f_globals
        package = caller_globals["__package__"]
        filename = self._repl_caller_frame.filename
        basename = path.basename(filename)

        extension_idx = basename.rfind(".")

        if extension_idx > 0:
            basename = basename[:extension_idx]

        if package:
            self._module_qualname = f"{package}.{basename}"
        else:
            self._module_qualname = basename

        banner_lines = [
            f"Working on {self._module_qualname}",
            f"Variables: {sorted(self.repl_env)}",
        ]

        if head is not None:  # allow it to be empty str
            banner_lines.insert(0, head)

        self._banner = "\n".join(banner_lines)

    async def main_async(self) -> None:
        print(self._banner, file=sys.stderr)  # noqa: T201
        await embed(
            globals=self.repl_env_full,
            title=self._module_qualname,
            return_asyncio_coroutine=True,
            history_filename=self.repl_history_filename,
            patch_stdout=True,
        )
