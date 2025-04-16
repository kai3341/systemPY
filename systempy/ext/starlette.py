from starlette.applications import Starlette

from ..target import Target


class StarletteUnit(Target, final=False):
    starlette_app: Starlette

    def on_init(self) -> None:
        add_event_handler = self.starlette_app.add_event_handler

        add_event_handler("startup", self.pre_startup)
        add_event_handler("startup", self.on_startup)
        add_event_handler("shutdown", self.on_shutdown)
        add_event_handler("shutdown", self.post_shutdown)
