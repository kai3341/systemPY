# Redis / Valkey unit example

Both `Redis` or `Valkey` use `redis-py` connector

=== "contextvars"

    ```python
    from dataclasses import field
    from os import environ

    from redis.asyncio import Redis
    from systempy import Target

    from contexts import RedisCTX


    class RedisUnit(Target):
        redis_connection: Redis = field(init=False)

        def pre_startup(self) -> None:
            self.redis_connection = Redis.from_url(environ["REDIS_URI"])
            RedisCTX.set(self.redis_connection)

        async def on_startup(self) -> None:
            await self.redis_connection.initialize()

        async def on_shutdown(self) -> None:
            await self.redis_connection.close()
    ```

=== "rodi"

    FIXME: I don't use rodi

    ```python
    from dataclasses import field
    from os import environ

    from redis.asyncio import Redis
    from systempy import Target

    from lib.unit import RodiUnit


    class RedisUnit(RodiUnit):
        redis_connection: Redis = field(init=False)

        def pre_startup(self) -> None:
            self.redis_connection = Redis.from_url(environ["REDIS_URI"])
            self.rodi_container.add_instance(self.redis_connection)

        async def on_startup(self) -> None:
            await self.redis_connection.initialize()

        async def on_shutdown(self) -> None:
            await self.redis_connection.close()
    ```
