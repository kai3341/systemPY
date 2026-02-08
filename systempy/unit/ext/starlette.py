from starlette.applications import Starlette
from typing_extensions import deprecated

from systempy import Target


@deprecated("Will be removed into separated package")
class StarletteUnit(Target):
    starlette_app: Starlette

    def on_init(self) -> None:
        add_event_handler = self.starlette_app.add_event_handler

        add_event_handler("startup", self.pre_startup)
        add_event_handler("startup", self.on_startup)
        add_event_handler("shutdown", self.on_shutdown)
        add_event_handler("shutdown", self.post_shutdown)
