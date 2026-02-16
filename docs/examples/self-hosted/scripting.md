# Scripting example

Both `ScriptUnit` and `LoopUnit` provide handy abstraction to write one
time scripts. Both of them has defined `@abc.abstractmethod`s

Maybe you need something smarter? Please check [`DaemonUnit`](./daemon.md)

## `ScriptUnit`

aimed to help writing **syncronous** scripts. It **requires** to override
`main_sync` method

```python
from systempy import ScriptUnit
from lib.unit import Example1Unit, Example2Unit, Example3Unit

class ExampleScriptApp(
    Example1Unit,
    Example2Unit,
    Example3Unit,
    ScriptUnit,
):
    def main_sync(self) -> None: ...

if __name__ == "__main__":
    ExampleScriptApp.launch()
```

## `LoopUnit`

is aimed to help writing **asyncronous** scripts and daemons.
It **requires** to override `main_async` method
Also you may pass `loop_factory` in kwargs. This feature is tested and wirks on
all supported python versions despite different implementation

```python
from systempy import LoopUnit
from lib.unit import Example1Unit, Example2Unit, Example3Unit

class ExampleAsyncScriptApp(
    Example1Unit,
    Example2Unit,
    Example3Unit,
    LoopUnit,
):
    async def main_async(self) -> None: ...

if __name__ == "__main__":
    ExampleAsyncScriptApp.launch()
```
