# Daemon examples

Unlike [`scripting`](./scripting.md), daemon is long-living process, that's why
it provides some extra features:

* Built-in `stop()` and `reload()` methods

* Signal handling (by default `SIGHUP` forces `DaemonUnit` reload)

## `DaemonUnit`

Same as [`ScriptUnit`](./scripting.md), the `DaemonUnit` is **syncronous** unit
and **requires** for implementation `main_sync()`

```python
from systempy import DaemonUnit
from lib.unit import Example1Unit, Example2Unit, Example3Unit

class ExampleDaemonApp(
    Example1Unit,
    Example2Unit,
    Example3Unit,
    DaemonUnit,
):
    def main_sync(self) -> None: ...

if __name__ == "__main__":
    ExampleDaemonApp.launch()
```

## `LoopUnit`

is (almost) subclass of `DaemonUnit`, but configured to run **asyncronous**
long-living jobs. It **requires** for implementation `main_async()`

```python
from systempy import LoopUnit
from lib.unit import Example1Unit, Example2Unit, Example3Unit

class ExampleLoopApp(
    Example1Unit,
    Example2Unit,
    Example3Unit,
    LoopUnit,
):
    async def main_async(self) -> None: ...

if __name__ == "__main__":
    ExampleLoopApp.launch()
```

## `EventWaitUnit`

is a subclass of `LoopUnit`, but already have implementation of `main_async()`,
which is actually doing infinite wait. It's useful, when all your units have
only startup and shutdown, but does not have own `main`

```python
from systempy import LoopUnit
from lib.unit import Example1Unit, Example2Unit, Example3Unit

class ExampleInfiniteWaitApp(
    Example1Unit,
    Example2Unit,
    Example3Unit,
    EventWaitUnit,
): ...

if __name__ == "__main__":
    ExampleInfiniteWaitApp.launch()
```

# Run and Reload

Now you can run your daemon:

```sh
python my_daemon.py
```

By default `reload` action bound to `signals.SIGHUP`. Let's try to reload:

```sh
kill -HUP $YOUR_DAEMON_PID
```
