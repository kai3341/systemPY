# Example integration with Starlette or FastAPI

If you open FastAPI source code you find it's subclass of Starlette. That's why
I don't separate them

## Implementing `Unit` class

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
    """
    Optionally you can define lifecycle actions. These actions you can split
    into your own mixins. Then you organize own mixins into own collection and
    then your application `Unit` will be a combination of 4-6 or more mixins.
    Congrats! This is the most typical `systemPY` usage
    """


# StarletteUnit relies on keyword argument starlette_app
unit = MyAppUnit(
    starlette_app=starlette_app,
)
```

## Running the app

Then run webserver:

```sh
uvicorn starlette_app:starlette_app
```
