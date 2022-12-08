import sys

from typing import Callable
from .repl_typing import TRU


readline_available = False

handle_interrupt: Callable[[TRU], None]
setup_completer: Callable[[TRU], None]

__all__ = (
    "handle_interrupt",
    "setup_completer",
)


def handle_interrupt__fallback(unit: TRU) -> None:
    pass


def setup_completer__fallback(unit: TRU) -> None:
    pass


try:
    import readline

    readline_available = True
except ImportError:
    print(
        "Module readline not available. No tab complete available.",
        file=sys.stderr,
    )

else:
    import rlcompleter

    import ctypes
    from ctypes.util import find_library

    rl_library = find_library("readline")
    assert rl_library, "Module `readline` already imported"
    rl = ctypes.CDLL(rl_library)

    readline.parse_and_bind("tab: complete")

    try:
        rl_kill_full_line = rl.rl_kill_full_line
        rl_beg_of_line = rl.rl_beg_of_line
        rl_on_new_line = rl.rl_on_new_line
        rl_forced_update_display = rl.rl_forced_update_display
    except AttributeError:
        readline_available = False

    def handle_interrupt__readline(unit: TRU) -> None:
        sys.stderr.write("^C\n")
        rl_kill_full_line()
        rl_beg_of_line()
        rl_on_new_line()
        rl_forced_update_display()

    def setup_completer__readline(unit: TRU) -> None:
        unit.repl_completer = rlcompleter.Completer(unit.repl_env_full)
        readline.set_completer(unit.repl_completer.complete)


if readline_available:
    handle_interrupt = handle_interrupt__readline
    setup_completer = setup_completer__readline
else:
    handle_interrupt = handle_interrupt__fallback
    setup_completer = setup_completer__readline
