# Scripting example

TODO: INACTUAL

The `ProcessUnit` implements `run_sync()` method, which handles `pre_startup()`
and `post_shutdown()` and **requires** for implementation `main_sync()` method.
Designed for simle run syncronous code. Used by [`ReplUnit`](./repl.md)
(deprecated. Use [`PTReplUnit`](./repl.md#ptrepl-extension) instead)

Maybe you need something more smart? Please check [`DaemonUnit`](./daemon.md)
