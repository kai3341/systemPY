I wanted to start coding immediately, but I have one important thing for you
to say before: some why many ASGI frameworks implemented lifespan as side task
[[uvicorn](https://uvicorn.dev/concepts/lifespan/#lifespan-architecture),
[granian](https://github.com/emmett-framework/granian?tab=readme-ov-file#hooks)].
And this breaks an idea to use `contextvars`, but we can embed ASGI Web server
into our application, and `ASGIServerUnit` would help to do it

All this article is about how to use `contextvars` with ASGI servers. If you
use different DI solution use this article as just funny story

`ASGIServerUnit` is implementation-agnostic and depends on protocol only. Also
I've created useful `asgi_server_factory_decorator`, helping you to minify
boilerplate code

Let's create ASGI server factories!

=== "uvicorn"

    ```python
    # lib.create_asgi_server
    from typing import NotRequired, TypedDict, Any

    from systempy.unit.asgi_server import (
        asgi_server_factory_decorator,
        ASGIAppFactory,
        ASGIServerProtocol,
    )

    from uvicorn import Config, Server


    class ExampleConfigObject(TypedDict):
        # Hint: this may be ANY object, because you handle it by your code
        host: NotRequired[str]
        port: NotRequired[int]


    def create_settings(example_param: Any) -> ExampleConfigObject:
        # Hint: it may be useful to parametrize this function, and
        # `example_param` demonstrates it. Use partial to curry this function
        return {"port": 12345}


    @asgi_server_factory_decorator
    def create_asgi_server(
        app_factory: ASGIAppFactory,
        settings: ExampleConfigObject,
    ) -> ASGIServerProtocol:
        config = Config(
            app_factory,
            factory=True,
            **settings,
        )
        return Server(config)
    ```

=== "granian"

    ```python
    # lib.create_asgi_server
    from typing import NotRequired, TypedDict, Any

    from systempy.unit.asgi_server import (
        asgi_server_factory_decorator,
        ASGIAppFactory,
        ASGIServerProtocol,
    )
    from granian.server.embed import Server
    from granian.constants import Interfaces


    class ExampleConfigObject(TypedDict):
        # Hint: this may be ANY object, because you handle it by your code
        address: NotRequired[str]
        port: NotRequired[int]


    def create_settings(example_param: Any) -> ExampleConfigObject:
        # Hint: it may be useful to parametrize this function, and
        # `example_param` demonstrates it. Use partial to curry this function
        return {"port": 12345}


    @asgi_server_factory_decorator
    def create_asgi_server(
        app_factory: ASGIAppFactory,
        settings: ExampleConfigObject,
    ) -> ASGIServerProtocol:
        return Server(
            app_factory,
            interface=Interfaces.ASGI,
            factory=True,
            **settings
        )
    ```

And now we are ready to use it:

=== "FastAPI"

    ```python
    # web_app.py

    from functools import partial

    from fastapi import FastAPI
    from systempy.unit.asgi_server import ASGIServerUnit

    from lib.create_asgi_server import create_asgi_server, create_settings

    from .views import router


    # Hint: use `functools.partial` to curry your `create_settings` if required
    @create_asgi_server(partial(create_settings, "example_param_value"))
    def create_app() -> FastAPI:
        app = FastAPI()
        app.include_router(router)
        return app


    class ExampleWebApp(
        ASGIServerUnit,
        # ... more units
    ): ...


    if __name__ == '__main__':
        ExampleWebApp.launch(asgi_server_factory=create_app)
    ```

=== "Litestar"

    ```python
    # web_app.py

    from functools import partial

    from litestar import Litestar
    from systempy.unit.asgi_server import ASGIServerUnit

    from lib.create_asgi_server import create_asgi_server, create_settings

    from .views import router


    # Hint: use `functools.partial` to curry your `create_settings` if required
    @create_asgi_server(partial(create_settings, "example_param_value"))
    def create_app() -> Litestar:
        return Litestar(
            route_handlers=[router],
        )


    class ExampleWebApp(
        ASGIServerUnit,
        # ... more units
    ): ...


    if __name__ == '__main__':
        ExampleWebApp.launch(asgi_server_factory=create_app)
    ```
