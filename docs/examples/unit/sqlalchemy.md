# SQLAlchemy unit example

Each database in your project require to create own `Unit`:

=== "contextvars"

    ```python
    from contextvars import ContextVar
    from dataclasses import field
    from os import environ

    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        async_sessionmaker,
        create_async_engine,
    )
    from systempy import Target

    from models import FirstDBSessionCTX, SecondDBSessionCTX

    SessionMakerType = async_sessionmaker[AsyncSession]


    def _initialize_sa(
        uri: str, ctx: ContextVar[SessionMakerType]
    ) -> tuple[AsyncEngine, SessionMakerType]:
        engine = create_async_engine(uri, pool_pre_ping=True)
        session = async_sessionmaker(engine)
        ctx.set(session)
        return engine, session

    # FirstDB

    class FirstDBUnit(Target):
        __firstdb_engine: AsyncEngine = field(init=False)
        first_db: SessionMakerType = field(init=False)

        def pre_startup(self) -> None:
            self.__firstdb_engine, self.first_db = _initialize_sa(
                environ["FIRSTDB_URI"], FirstDBSessionCTX
            )

        async def on_shutdown(self) -> None:
            await self.__firstdb_engine.dispose()

    # SecondDB

    class SecondDBUnit(Target):
        __seconddb_engine: AsyncEngine = field(init=False)
        second_db: SessionMakerType = field(init=False)

        def pre_startup(self) -> None:
            self.__seconddb_engine, self.second_db = _initialize_sa(
                environ["SECONDDB_URI"], SecondDBSessionCTX
            )

        async def on_shutdown(self) -> None:
            await self.__seconddb_engine.dispose()
    ```

=== "rodi"

    FIXME: I don't use rodi

    ```python
    from dataclasses import field
    from os import environ

    from rodi import Container
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        async_sessionmaker,
        create_async_engine,
    )
    from systempy import Target

    from lib.unit import RodiUnit

    SessionMakerType = async_sessionmaker[AsyncSession]


    def _initialize_sa(
        uri: str, alias: str, container: Container
    ) -> tuple[AsyncEngine, SessionMakerType]:
        engine = create_async_engine(uri, pool_pre_ping=True)
        session = async_sessionmaker(engine)
        container.add_transient_by_factory(session)
        container.add_alias(alias, AsyncSession)
        return engine, session

    # FirstDB

    class FirstDBUnit(RodiUnit):
        __firstdb_engine: AsyncEngine = field(init=False)
        first_db: SessionMakerType = field(init=False)

        def pre_startup(self) -> None:
            self.__firstdb_engine, self.first_db = _initialize_sa(
                environ["FIRSTDB_URI"], "first_db", self.rodi_container
            )

        async def on_shutdown(self) -> None:
            await self.__firstdb_engine.dispose()

    # SecondDB

    class SecondDBUnit(RodiUnit):
        __seconddb_engine: AsyncEngine = field(init=False)
        second_db: SessionMakerType = field(init=False)

        def pre_startup(self) -> None:
            self.__seconddb_engine, self.second_db = _initialize_sa(
                environ["SECONDDB_URI"], "second_db", self.rodi_container
            )

        async def on_shutdown(self) -> None:
            await self.__seconddb_engine.dispose()
    ```
