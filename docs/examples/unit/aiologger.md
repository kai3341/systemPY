# AIOLogger unit

=== "contextvars"

    ```python
    from dataclasses import field

    from aiologger import Logger, logger
    from aiologger.handlers import files as logger_file_handlers
    from systempy import Target

    from lib.logger import ExtraLogRecord, LoggerCTX


    class LoggerUnit(Target, final=False):
        logger_instance: Logger = field(init=False)

        def on_init(self) -> None:
            # Here is huge aiologger bug: it does not allow to set
            # own LogRecord type
            logger.LogRecord = ExtraLogRecord

        def pre_startup(self) -> None:
            self.logger_instance = Logger.with_default_handlers()
            LoggerCTX.set(self.logger_instance)

        async def on_shutdown(self) -> None:
            await self.logger_instance.shutdown()
    ```

=== "rodi"

    FIXME: I don't use rodi

    ```python
    from dataclasses import field

    from aiologger import Logger, logger
    from aiologger.handlers import files as logger_file_handlers
    from systempy import Target

    from lib.unit import RodiUnit
    from lib.logger import ExtraLogRecord, LoggerCTX


    class LoggerUnit(RodiUnit, final=False):
        logger_instance: Logger = field(init=False)

        def on_init(self) -> None:
            # Here is huge aiologger bug: it does not allow to set
            # own LogRecord type
            logger.LogRecord = ExtraLogRecord

        def pre_startup(self) -> None:
            self.logger_instance = Logger.with_default_handlers()
            self.rodi_container.add_instance(self.logger_instance)

        async def on_shutdown(self) -> None:
            await self.logger_instance.shutdown()
    ```
