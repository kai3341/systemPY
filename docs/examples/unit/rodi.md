# Rodi unit

FIXME: I don't use rodi

Lets's define this unit at `lib/unit/rodi_unit.py`, and then import it via
`from lib.unit import RodiUnit`. Don't forget to re-export it in `__init__.py`

```python
from dataclasses import field

from rodi import Container
from systempy import Target

class RodiUnit(Target, final=Flase):
    rodi_container: Container = field(default_factory=Container)

    # Also valid on pre_startup
```
