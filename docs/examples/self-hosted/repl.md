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

So, I've started implementing REPL via fixing this anoying behavior

## Vanila asyncio repl `ReplUnit`. Implement the unit

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

## PrettyReplUnit extension

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

API reference is the same. This is my pet project code with minimal changes

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
