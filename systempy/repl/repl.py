import asyncio
import asyncio.__main__ as amain  # type: ignore
import inspect
import rlcompleter
from typing import Dict, Tuple, Any

from .handle_interrupt import handle_interrupt, setup_completer

from ..process import ProcessUnit

from mypy_extensions import trait


@trait
class _ReplLocalsMixin:
    __slots__ = (
        "_repl_caller_frame",
        "repl_env_full",
        "repl_env",
    )

    _repl_caller_frame: inspect.FrameInfo
    repl_env_full: Dict[str, Any]
    _repl_variables: Dict[str, Any] = {}
    __repl_locals_keys_from_globals = (
        "__name__",
        "__package__",
        "__loader__",
        "__spec__",
        "__builtins__",
        "__file__",
    )

    def _repl_env_defaults(self) -> Dict[str, Any]:
        return {"asyncio": asyncio, "unit": self}

    def _setup_repl_env(self) -> None:
        repl_env = self._repl_env_defaults()
        repl_env.update(self._repl_variables)
        self.repl_env = repl_env
        self.repl_env_full = repl_env.copy()

        env = self._repl_caller_frame[0].f_globals

        for key in self.__repl_locals_keys_from_globals:
            self.repl_env_full[key] = env[key]

    def _setup_repl_caller_frame(self) -> None:
        "Firstly"
        frames = inspect.stack()
        self._repl_caller_frame = frames[-1]


@trait
class ReplUnit(_ReplLocalsMixin, ProcessUnit):
    _repl_variables: Dict[str, Any] = {}
    _repl_caller_frame: inspect.FrameInfo
    loop: asyncio.AbstractEventLoop
    console: amain.AsyncIOInteractiveConsole
    repl_completer: rlcompleter.Completer
    repl_thread: amain.REPLThread
    repl_env_full: Dict[str, Any]

    __slots__ = _ReplLocalsMixin.__slots__ + (
        "loop",
        "console",
        "repl_env_full",
        "repl_completer",
        "repl_thread",
    )

    def __setup_repl(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self._setup_repl_env()

        setup_completer(self)

        self.console = amain.AsyncIOInteractiveConsole(
            self.repl_env_full,
            self.loop,
        )

        self.__repr_console_interact()
        self.__repr_console_runsource()

        amain.repl_future = None
        amain.repl_future_interrupted = False
        amain.loop = self.loop
        amain.console = self.console

        self.repl_thread = amain.REPLThread()
        self.repl_thread.daemon = True
        self.repl_thread.start()

    def on_init(self) -> None:
        self._setup_repl_caller_frame()
        self.__setup_repl()

    def repl_handle_banner(self, banner: str) -> str:
        return banner

    def repl_handle_exitmsg(self, exitmsg: str) -> str:
        return exitmsg

    async def repl_handle_code(self, code: str) -> None:
        pass

    def __repr_console_interact(self) -> None:
        original_interact = self.console.interact

        def interact(banner: str, exitmsg: str) -> None:
            banner = self.repl_handle_banner(banner)
            exitmsg = self.repl_handle_exitmsg(exitmsg)
            original_interact(banner, exitmsg)

        self.console.interact = interact

    def __repr_console_runsource(self) -> None:
        original_runsource = self.console.runsource

        def runsource(
            source: str,
            *args: Tuple[str, ...],
            **kwargs: Dict[str, str],
        ) -> Any:
            coro = self.repl_handle_code(source)
            asyncio.run_coroutine_threadsafe(coro, self.loop)
            return original_runsource(source, *args, **kwargs)

        self.console.runsource = runsource

    def main_sync(self) -> None:
        self.loop.create_task(self.on_startup())
        while True:
            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                handle_interrupt(self)
                if amain.repl_future and not amain.repl_future.done():
                    amain.repl_future.cancel()
                    amain.repl_future_interrupted = True
                continue
            else:
                self.loop.run_until_complete(self.on_shutdown())
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                break

    # Experimental
    def __done_after_shutdown_asyncgens(self, result: Any) -> None:
        self.loop.call_soon_threadsafe(self.post_shutdown)
        self.loop.call_soon_threadsafe(self.pre_startup)
        asyncio.ensure_future(
            self.on_startup(),
            loop=self.loop,
        )

    def __done_after_on_shutdown(self, result: Any) -> None:
        future = asyncio.ensure_future(
            self.loop.shutdown_asyncgens(),
            loop=self.loop,
        )
        future.add_done_callback(self.__done_after_shutdown_asyncgens)

    def reload_threadsafe(self) -> None:
        future = asyncio.ensure_future(
            self.on_shutdown(),
            loop=self.loop,
        )
        future.add_done_callback(self.__done_after_on_shutdown)

    def reload(self) -> None:
        ...
