from asyncio import CancelledError, Event
from contextlib import suppress
from dataclasses import field
from typing import ParamSpec

from .loop import LoopUnit

A = ParamSpec("A")


class EventWaitUnit(LoopUnit[A]):
    """
    Infinite wait unit
    """

    __event: Event = field(init=False)

    async def on_startup(self) -> None:
        self.__event = Event()

    async def main_async(self) -> None:
        with suppress(CancelledError):
            await self.__event.wait()
