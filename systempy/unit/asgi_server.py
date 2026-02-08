from collections.abc import Callable
from dataclasses import field
from typing import Protocol

from systempy.unit.loop import LoopUnit


class ASGIServerProtocol(Protocol):
    async def serve(self) -> None: ...
    async def shutdown(self) -> None: ...


ASGIServerFactory = Callable[[], ASGIServerProtocol]


class ASGIServerUnit(LoopUnit):
    asgi_server_factory: ASGIServerFactory
    __asgi_server: ASGIServerProtocol = field(init=False, repr=False)

    def pre_startup(self) -> None:
        self.__asgi_server = self.asgi_server_factory()

    async def main_async(self) -> None:
        await self.__asgi_server.serve()

    async def on_shutdown(self) -> None:
        await self.__asgi_server.shutdown()

    def post_shutdown(self) -> None:
        del self.__asgi_server
