# Scripting example

Both `ScriptUnit` and `AsyncScriptUnit` provide handy abstraction to write one
time scripts. Both of them has defined `@abc.abstractmethod`s

Maybe you need something more smart? Please check [`DaemonUnit`](./daemon.md)

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

## `AsyncScriptUnit`

is a subclass of `ScriptUnit` and aimed to help writing **asyncronous** scripts.
It **requires** to override `main_async` method

```python
from systempy import ScriptUnit
from lib.unit import Example1Unit, Example2Unit, Example3Unit

class ExampleAsyncScriptApp(
    Example1Unit,
    Example2Unit,
    Example3Unit,
    AsyncScriptUnit,
):
    async def main_async(self) -> None: ...

if __name__ == "__main__":
    ExampleAsyncScriptApp.launch()
```
