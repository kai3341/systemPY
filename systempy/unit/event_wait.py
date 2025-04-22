from asyncio import CancelledError, Event
from contextlib import suppress
from dataclasses import field

from .loop import LoopUnit


class EventWaitUnit(LoopUnit, final=False):
    """
    Infinite wait unit
    """

    __event: Event = field(init=False)

    def on_startup(self) -> None:
        self.__event = Event()

    async def main_async(self) -> None:
        with suppress(CancelledError):
            await self.__event.wait()
