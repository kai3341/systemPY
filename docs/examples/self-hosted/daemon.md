# Daemon Example

I suggest to make a daemon example with a bit complicated startup and shutdown
to make it less boring. Just imagine your daemon have a lot of dependencies
have to be initialized

## Custom `Target`

At the first we have to defive custom startup and shutdown lifecycle stages. I
think the most interesting and useful for you it would be to define lifecycle
stages with `GATHER` direction to speedup your application startup and shutdown.
Keep in mind `GATHER`ing stages executes simultaneously

```python
# example_daemon_target.py
from systempy.util import (
    DIRECTION,
    register_hook_before,
    register_hook_after,
)
from systempy.unit.ext.target_ext import ExtTarget


class ExampleDaemonTarget(ExtTarget):
    @register_hook_before(ExtTarget.post_startup, DIRECTION.FORWARD)
    async def before_post_startup(self): ...

    @register_hook_after(ExtTarget.post_startup, DIRECTION.GATHER)
    async def after_post_startup(self): ...

    @register_hook_before(ExtTarget.pre_shutdown, DIRECTION.GATHER)
    async def before_pre_shutdown(self): ...

    @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
    def after_post_shutdown(self): ...

    @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
    def also_after_post_shutdown(self): ...

    # Look, you may to add hooks just while you defining the `Target`
    @register_hook_after(also_after_post_shutdown, DIRECTION.BACKWARD)
    def after_also_after_post_shutdown(self): ...
```

## Daemon Unit classes

Then you have to subclass this `Target` to define the code should be executed on
the stages you have just defined. In your real code you will subclass this
`Target` multiple times. Youe IDE should help you and highlight method names
you have just defined in your `ExampleDaemonTarget`

```python
# example_daemon_unit_1
from time import sleep
from asyncio import sleep as asleep
from example_daemon_target import ExampleDaemonTarget

class ExampleDaemonUnit1(ExampleDaemonTarget):
    def on_init(self) -> None:
        print("1 ON INIT START")
        sleep(1)
        print("1 ON INIT DONE")

    def pre_startup(self) -> None:
        print("\t1 PRE STARTUP START")
        sleep(1)
        print("\t1 PRE STARTUP DONE")

    async def on_startup(self) -> None:
        print("\t\t1 ON STARTUP START")
        await asleep(1)
        print("\t\t1 ON STARTUP DONE")

    async def post_startup(self) -> None:
        print("\t\t\t1 POST STARTUP START")
        await asleep(1)
        print("\t\t\t1 POST STARTUP DONE")

    def before_post_startup(self):
        print("\t\t\t1 CUSTOM BEFORE POST STARTUP START")
        sleep(1)
        print("\t\t\t1 CUSTOM BEFORE POST STARTUP DONE")

    async def before_pre_shutdown(self):
        print("\t\t\t1 CUSTOM BEFORE PRE SHUTDOWN START")
        await asleep(1)
        print("\t\t\t1 CUSTOM BEFORE PRE SHUTDOWN DONE")

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
```

## Daemon class

Optionally you may add more mixins.
Remember: combining a lot of `Target` mixins into current worker class is a
default usage scenario of this library

Create the file, for example, `my_daemon.py`

```python
#!/usr/bin/env python

import os
import asyncio

from systempy import Unit, LoopUnit, DaemonUnit
from somewhere_you_defined import ExampleDaemonTarget


class ExampleDaemon(
    ExampleDaemonUnit_1,
    DaemonUnit,
    Unit,
):
    async def main_async(self):
        while True:
            await asyncio.sleep(5)


if __name__ == "__main__":
    print("PID: %s" % os.getpid())
    ExampleDaemon.launch()
```

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
