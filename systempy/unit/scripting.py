from asyncio import run

from typing_extensions import ParamSpec

from ..libsystempy import ROLE
from ..target import AsyncMixinABC, SyncMixinABC

A = ParamSpec("A")


class ScriptUnit(SyncMixinABC[A], role=ROLE.MIXIN):
    def run_sync(self) -> None:
        with self:
            self.main_sync()


class AsyncScriptUnit(ScriptUnit[A], AsyncMixinABC, role=ROLE.MIXIN):
    def main_sync(self) -> None:
        run(self.run_async())

    async def run_async(self) -> None:
        async with self:
            await self.main_async()
