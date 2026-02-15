from collections.abc import Callable
from dataclasses import field
from typing import Protocol, TypeVar

from systempy.unit.loop import LoopUnit

S = TypeVar("S")


class ASGIServerProtocol(Protocol):
    async def serve(self) -> None: ...
    async def shutdown(self) -> None: ...


ASGIServerFactory = Callable[[], ASGIServerProtocol]
ASGIApp = Callable
ASGIAppFactory = Callable[[], ASGIApp]


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


def asgi_server_factory_decorator(
    server_factory: Callable[[ASGIAppFactory, S], ASGIServerProtocol],
) -> Callable[[Callable[[], S]], Callable[[ASGIAppFactory], ASGIServerFactory]]:
    def outer(
        configure_server: Callable[[], S],
    ) -> Callable[[ASGIAppFactory], ASGIServerFactory]:
        def inner(asg_app_factory: ASGIAppFactory) -> ASGIServerFactory:
            return lambda: server_factory(asg_app_factory, configure_server())

        return inner

    return outer
