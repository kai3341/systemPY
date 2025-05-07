# Celery integration example

Celery application is very similar to Starlette. Advice to handle asyncio jobs
via [celery-pool-asyncio](https://pypi.org/project/celery-pool-asyncio/)
library

## Writing `Unit`

First you have to create file, for example, `celery_app.py`

```python
from systempy import Unit
from systempy.unit.ext.celery import CeleryUnit

from .config import config

from .app import app as celery_app  # Advice to create an instencies of apps
# in separated file(s) to avoid circular imports

from . import tasks
tasks.__package__

class MyWorkerApp(CeleryUnit):
    ...


# Remember `CeleryUnit` require an `celery_app` and `config` kwargs
# Also remember: use `CeleryUnit` as an example of your own `Unit`

unit = MyWorkerApp(
    config=config,
    celery_app=celery_app,
)
```

## Running it

Now run the Celery:

```sh
celery worker -A celery_app:celery_app
```
