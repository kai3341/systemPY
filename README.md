# systemPY

![Logo](docs/images/systempy-logo.png)

Python application component initialization system

![python](https://img.shields.io/pypi/pyversions/systemPY)
![version](https://img.shields.io/pypi/v/systemPY)
![downloads](https://img.shields.io/pypi/dm/systemPY)
![format](https://img.shields.io/pypi/format/systemPY)
[![Documentation Status](https://readthedocs.org/projects/systempy/badge/?version=latest)](https://systempy.readthedocs.io/en/latest/?badge=latest)
![GitHub issues](https://img.shields.io/github/issues/kai3341/systemPY)

## The problem

The regular application contain many atomic components. Asyncio makes theirs
initializing a little bit complicated. It's OK, when you have single entrypoint
and initialize your application components via your framework. While you add
new components to your application iteratively, you don't see any problem

When you create any new entrypoint, you have to think a lot, how to initialize
application components again, which callbacks should be called and in which
order. But it's a half of the problem! You have to implement also graceful
shutdown

The most painful part is one-time scripts. It's kind of The Banana Gorilla
Problem: you wanted a banana but you have to initialize a gorilla holding the
banana and the entire jungle, and then graceful shutdown it

## Solution

This library allows you to implement application startup and shutdown in
declarative way. You have to implement a class for each your component,
write the startup and shutdown code. Then combine required components as mixins
into the current application `Unit` class. Then create an instance and pass
dependencies as keyword arguments. In case it's daemon run `instance.run_sync()`
methed

It's possible to use `systemPY` in three scenarios:

* Secondary application, which is handled by another application like
`celery` or `starlette`

* Daemon or script -- self-hosted application

* Master application, handles other applications


## Short Stupid Example

Here it should be normal example, but I have only this:

```python
import os
import asyncio

from systempy import Unit, LoopUnit, DaemonUnit, util as systempy_util
from systempy.ext.target_ext import TargetExt


@systempy_util.register_target
class ExampleDaemonTarget(TargetExt):
    @systempy_util.register_hook_before(TargetExt.post_startup)
    @systempy_util.register_target_method("forward")
    def before_post_startup(self): ...

    @systempy_util.register_hook_before(TargetExt.pre_shutdown)
    @systempy_util.register_target_method("gather")
    async def before_pre_shutdown(self): ...

    @systempy_util.register_hook_after(TargetExt.post_shutdown)
    @systempy_util.register_target_method("backward")
    def after_post_shutdown(self): ...

    @systempy_util.register_hook_after(TargetExt.post_shutdown)
    @systempy_util.register_target_method("backward")
    def also_after_post_shutdown(self): ...

    @systempy_util.register_hook_after(also_after_post_shutdown)
    @systempy_util.register_target_method("backward")
    def after_also_after_post_shutdown(self): ...


class ExampleDaemon(
    Unit,
    LoopUnit,
    ExampleDaemonTarget,
    DaemonUnit,
):
    async def main_async(self):
        while True:
            await asyncio.sleep(5)

    def on_init(self) -> None:
        print("ON INIT")

    def pre_startup(self) -> None:
        print("\tPRE STARTUP")

    async def on_startup(self) -> None:
        print("\t\tON STARTUP")

    async def post_startup(self) -> None:
        print("\t\t\tPOST STARTUP")

    def before_post_startup(self):
        print("\t\t\tCUSTOM BEFORE POST STARTUP")

    async def before_pre_shutdown(self):
        print("\t\t\tCUSTOM BEFORE PRE SHUTDOWN")

    async def pre_shutdown(self) -> None:
        print("\t\t\tPRE SHUTDOWN")

    async def on_shutdown(self) -> None:
        print("\t\tON SHUTDOWN")

    def post_shutdown(self) -> None:
        print("\tPOST SHUTDOWN")

    def also_after_post_shutdown(self) -> None:
        print("\tALSO AFTER POST SHUTDOWN")

    def after_also_after_post_shutdown(self) -> None:
        print("\tAFTER ALSO AFTER POST SHUTDOWN")

    def on_exit(self) -> None:
        print("ON EXIT")


if __name__ == "__main__":
    print("PID: %s" % os.getpid())
    ExampleDaemon.launch()
```

## Bonus: REPL Example

Also require normal example, but I have only this

```python
from systempy import Unit
from systempy.ext.celery import CeleryUnit
from systempy.ext.starlette import StarletteUnit
from systempy.ext.pretty_repl import PrettyReplUnit

from my_project.my_systempy import (
    ConfigUnit,
    LoggerUnit,
    MyDatabaseUnit,
)


from . import instances
from . import config
from . import views
from . import tasks
from . import models


class AppReplUnit(
    ConfigUnit,
    LoggerUnit,
    CeleryUnit,
    StarletteUnit,
    MyDatabaseUnit,
    PrettyReplUnit,
    Unit,
):
    repl_variables = {
        "tasks": tasks,
        "config": config,
        "models": models,
        "views": views,
        "instances": instances,
    }


unit = AppReplUnit(
    # required by your LoggerUnit
    app_name='MyProjectRepl',
    # you rely on your config in your multiple units
    config=config.config,
    starlette_app=instances.starlette_app,
    # let's initialize Celery tasks to be able to run any task
    celery_app=instances.celery_app,
)


if __name__ == '__main__':
    unit.run_sync()
```

## Philosophy

Batteries are included, but use it as example first
