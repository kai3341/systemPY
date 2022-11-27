# REPL examples

Before starting. You know python already have an asyncio REPL:

```sh
python -m asyncio
asyncio REPL 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Use "await" directly instead of "asyncio.run()".
Type "help", "copyright", "credits" or "license" for more information.
>>> import asyncio
>>> |
```

Is it OK? It's a little buggy. Try to press `Ctrl+C` to send KeyboardInterrupt.
Does it handles correctly? Then press `Tab`. When you have `readline` library
it should complete the command line, but it does not work too

There are some tries to fix this anoying behavior. Right now the best solution
is [PTRepl Extension](#ptrepl-extension) -- it works fine on Linux, MacOS and
Windows

## Vanila asyncio repl `ReplUnit`. Implement the unit

This solution does not requires external libraries and uses `ctypes`. On Linux
and MacOS when library `readline` is available, this solution is good enough,
but on Windows it's the same awful as built-in `asyncio` REPL. My other variants
are drop-in replacements of `ReplUnit` and everything you read here is relevant
for other implementations

Start from creating file, for example, `my_repl.py`:

```python
from systempy import Unit, ReplUnit


class MyReplUnit(ReplUnit, Unit):
    """
    Just add your component mixins. For example, initialize models and other
    components. Also you may add your custom variables into repl globals.
    It's useful to pre-import some modules, like models or tasks
    """

    repl_variables = {
        "my_variable": "my_value",
    }


unit = MyReplUnit()


if __name__ == '__main__':
    unit.run_sync()
```

## Run the REPL

Now you are able to use this REPL:

```sh
python -m my_repl
```

## PrettyReplUnit Extension

This is a subclass of `ReplUnit` but having a little bit changed banner:

```sh
(venv) kai@asus-ux360c:~/Projects/my-pet-project$ python -m petproject.mymodule.repl
asyncio REPL 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Use "await" directly instead of "asyncio.run()".
Type "help", "copyright", "credits" or "license" for more information.

Working on petproject.mymodule.repl
Variables: ['asyncio', 'config', 'models', 'othermodule_service', 'singleton', 'tasks', 'unit', 'views']
>>> |
```

API reference is the same, and problems are the same too. This is my pet project
code with minimal changes

```python
from systempy import Unit
from systempy.ext.celery import CeleryUnit
from systempy.ext.starlette import StarletteUnit
from systempy.ext.pretty_repl import PrettyReplUnit

from petproject.common.systempy import (
    ConfigUnit,
    LoggerUnit,
    LoggingUnit,
    SQLAlchemyMariaDBUnit,
    MyFirstDatabaseUnit,
)

from . import config
from . import singleton
from . import views

from petproject.common import models
from petproject.common.service import othermodule as othermodule_service
from petproject.othermodule import tasks


class MyPrettyReplUnit(
    ConfigUnit,
    LoggerUnit,
    LoggingUnit,
    CeleryUnit,
    StarletteUnit,
    SQLAlchemyMariaDBUnit,
    MyFirstDatabaseUnit,
    PrettyReplUnit,
    Unit,
):
    repl_variables = {
        "views": views,
        "singleton": singleton,
        "config": config,
        "models": models,
        "othermodule_service": othermodule_service,
        "tasks": tasks,
    }


unit = MyPrettyReplUnit(
    config=config.config,
)


if __name__ == '__main__':
    unit.run_sync()
```

## PTRepl Extension

This is drop-in replacement of
[PrettyReplUnit Extension](#prettyreplunit-extension), but it implemented in
absolutelly different way and relien on
[ptpython](https://github.com/prompt-toolkit/ptpython) library.
It works fine on Linux, MacOS and Windows, and I like it's hints and syntax
highliting. Before starting you have to install this requirement:

```sh
pip install ptpython
```

Finally you can change the [PrettyReplUnit Extension](#prettyreplunit-extension)
and replace import statement:

```python
from systempy.ext.starlette import StarletteUnit
# from systempy.ext.pretty_repl import PrettyReplUnit
from systempy.ext.ptrepl import PTRepl as PrettyReplUnit
```

If you like this REPL implementation, you may remove old import and refactor
your code
