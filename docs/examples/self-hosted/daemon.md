# Daemon example

Unlike [`ScriptUnit`](./scripting.md), the `DaemonUnit` implements full lifecycle
with `reload()`, but **requires** for implementation  `main_sync()` and `stop()`
methods


## Run

Now you can run your daemon:

```sh
python my_daemon.py
```

## Reload

By default `reload` action bound to `signals.SIGHUP`. Let's try to reload:

```sh
kill -HUP $YOUR_DAEMON_PID
```
