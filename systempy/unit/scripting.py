from typing_extensions import ParamSpec

from ..libsystempy import ROLE
from ..target import SyncMixinABC

A = ParamSpec("A")


class ScriptUnit(SyncMixinABC[A], role=ROLE.MIXIN):
    def run_sync(self) -> None:
        with self:
            self.main_sync()
