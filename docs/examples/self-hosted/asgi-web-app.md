I wanted to start coding immediately, but I have one important thing for you
to say before: somewhy many ASGI frameworks implemented lifespan as side task
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


    class UvicornKwargs(TypedDict):
        host: NotRequired[str]
        port: NotRequired[int]


    def create_settings(example_param: Any) -> UvicornKwargs:
        return {"port": 12345}


    @asgi_server_factory_decorator
    def create_asgi_server(
        app_factory: ASGIAppFactory,
        settings: UvicornKwargs,
    ) -> ASGIServerProtocol:
        config = Config(app_factory, factory=True, **settings)
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


    class GranianKwargs(TypedDict):
        address: NotRequired[str]
        port: NotRequired[int]


    def create_settings(example_param: Any) -> GranianKwargs:
        return {"port": 12345}


    @asgi_server_factory_decorator
    def create_asgi_server(
        app_factory: ASGIAppFactory,
        settings: GranianKwargs,
    ) -> ASGIServerProtocol:
        return Server(
            app_factory,
            interface=Interfaces.ASGI,
            factory=True,
            **settings
        )
    ```

And now we are ready to use it:

```python
# web_app.py

from functools import partial

from fastapi import FastAPI  # for example
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
