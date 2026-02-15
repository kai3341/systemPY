I wanted to start coding immediately, but I have one important thing for you
to say before: somewhy many ASGI frameworks implemented lifespan as side task
[[uvicorn](https://uvicorn.dev/concepts/lifespan/#lifespan-architecture),
[granian](https://github.com/emmett-framework/granian?tab=readme-ov-file#hooks)].
And this breaks an idea to use contextvars, but we can embed ASGI Web server
into our application.

Let's create a decorator, converting out ASGI App factory to ASGI Server factory:

Text below is incatual...


```python
# lib.asgi_app_to_server

from collections.abc import Callable
from typing import Any

from systempy.unit.asgi_server import ASGIServerFactory

from lib.asgi_server_implementation import server

ASGIApp = Callable
ASGIAppFactory = Callable[[], ASGIApp]

def asgi_app_to_server(
    host: str,
    port: int,
    **any_params: dict[str, Any],
) -> Callable[[ASGIAppFactory], ASGIServerFactory]:
    def inner (asgi_app_factory: ASGIAppFactory) -> ASGIServerFactory:
        return lambda: server(asgi_app_factory, host, port)
    
    return inner
```

Let's create server factories for different ASGI servers!

=== "uvicorn"

    ```python
    # lib.asgi_server_implementation
    from uvicorn import Config, Server

    def server(app_factory: ASGIAppFactory, host: str, port: int) -> Server:
        config = Config(app_factory, factory=True, host=host, port=port)
        return Server(config)
    ```

=== "granian"

    ```python
    # lib.asgi_server_implementation
    from granian.server.embed import Server
    from granian.constants import Interfaces

    def server(app_factory: ASGIAppFactory, host: str, port: int) -> Server:
        return Server(
            app_factory,
            interface=Interfaces.ASGI,
            factory=True,
            host=host,
            port=port,
        )
    ```
