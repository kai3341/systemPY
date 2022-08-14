# Example integration with Starlette or FastAPI

If you open FastAPI source code you find it's subclass of Starlette. That's why
I don't separate them

For example, the name of following file is `starlette_app.py`

```python
from systempy import Unit
from systempy.ext.starlette import StarletteUnit

# It's advice to define all your apps in separated file(s)
# having this instance and nothing else. I think it's the
# easiest way to avoid circular imports
from .starlette_instance import app as starlette_app

from . import views
# Linters somewhy don't know that imports has side effects
views.__package__


class  MyAppUnit(StarletteUnit, Unit):
    # Optionally you can define lifecycle actions
    # These actions you can split into your own mixins
    # Then you organize own mixins into own collection
    # and then your application Unit will be a combination
    # of 4-6 or more mixins. Congrats! This is the most
    # typical `systemPY` usage

    def on_init(self):
        """
        This method will be called exactly once on application
        initialization
        """
        # WARNING: NO super().on_init()

    def pre_startup(self):
        """
        Event loop should not be started, but depends on
        primary application
        """
        # WARNING: NO super().pre_startup()

    async def on_startup(self):
        """
        Event loop started
        """
        # WARNING: NO super().on_startup()

    async def on_shutdown(self):
        """
        Event loop still working
        """
        # WARNING: NO super().on_shutdown()

    def post_shutdown(self):
        """
        Event loop should be stoped
        """
        # WARNING: NO super().post_shutdown()

    def on_exit(self):
        """
        This method will be called exactly once on application
        shutdown
        """


# StarletteUnit relies on keyword argument starlette_app

unit = MyAppUnit(
    starlette_app=starlette_app,
)
```

Then run webserver:

```bash
uvicorn starlette_app:starlette_app
```
