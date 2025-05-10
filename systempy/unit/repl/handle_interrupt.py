import sys
from collections.abc import Callable
from typing import Any

handle_interrupt: Callable[[Any], None]
setup_completer: Callable[[Any], None]

__all__ = (
    "handle_interrupt",
    "setup_completer",
)


def handle_interrupt__fallback(unit: Any) -> None: ...


def setup_completer__fallback(unit: Any) -> None: ...


handle_interrupt = handle_interrupt__fallback
setup_completer = setup_completer__fallback

try:
    import ctypes
    import readline
    import rlcompleter
    from ctypes.util import find_library

    rl_library = find_library("readline")
    assert rl_library, "Module `readline` already imported"
    rl = ctypes.CDLL(rl_library)

    readline.parse_and_bind("tab: complete")  # type: ignore[attr-defined]

    rl_kill_full_line = rl.rl_kill_full_line
    rl_beg_of_line = rl.rl_beg_of_line
    rl_on_new_line = rl.rl_on_new_line
    rl_forced_update_display = rl.rl_forced_update_display

    def handle_interrupt__readline(_unit: Any) -> None:
        sys.stderr.write("^C\n")
        rl_kill_full_line()
        rl_beg_of_line()
        rl_on_new_line()
        rl_forced_update_display()

    def setup_completer__readline(unit: Any) -> None:
        unit.repl_completer = rlcompleter.Completer(unit.repl_env_full)
        readline.set_completer(unit.repl_completer.complete)  # type: ignore[attr-defined]

except:  # noqa: E722
    print(  # noqa: T201
        "Module readline not available. No tab complete available.",
        file=sys.stderr,
    )

else:
    handle_interrupt = handle_interrupt__readline
    setup_completer = setup_completer__readline
