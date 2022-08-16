# Daemon

I suggest to make a daemon example with a bit complicated startup and shutdown
to make it less boring. Just imagine your daemon have a lot of dependencies
have to be initialized

## Custom `Target`

At the first we have to defive custom startup and shutdown lifecycle stages

```python
from systempy import util as systempy_util
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

    # Look, you may to add hooks just while you defining the `Target`
    @systempy_util.register_hook_after(also_after_post_shutdown)
    @systempy_util.register_target_method("backward")
    def after_also_after_post_shutdown(self): ...
```

## Daemon class

Then you have to subclass this `Target`. Optionally you may add more mixins.
Remember: combining a lot of `Target` mixins into current worker class is a
default usage scenario of this library

```python
import os
import asyncio

from systempy import Unit, LoopUnit, DaemonUnit
from somewhere_you_defined import ExampleDaemonTarget


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

Now you can run your daemon.

## Reload

By default `reload` action bound to `signals.SIGHUP`. Let's try to reload:

```sh
kill -HUP $YOUR_DAEMON_PID
```
