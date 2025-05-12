"""
Compatability layer. Windows does not support SIGHUP
"""

from platform import system
from signal import Signals

current_system = system()

default_reload_signals: tuple[Signals, ...]

default_reload_signals = (
    () if current_system == "Windows" else (Signals.SIGHUP,)  # type: ignore[attr-defined]
)
