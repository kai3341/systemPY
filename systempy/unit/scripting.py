from typing_extensions import ParamSpec

from ..libsystempy import ROLE
from ..target import SyncMixinABC
from .loop import LoopUnit

A = ParamSpec("A")


class ScriptUnit(SyncMixinABC[A], role=ROLE.MIXIN):
    def run_sync(self) -> None:
        with self:
            self.main_sync()


class AsyncScriptUnit(ScriptUnit[A], LoopUnit[A], role=ROLE.MIXIN):
    async def run_async(self) -> None:
        async with self:
            await self.main_async()
