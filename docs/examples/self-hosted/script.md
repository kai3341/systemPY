# Script example

Very simiral to [daemon](./daemon.md). Look there first

## Implement the `Unit`

Let's begin from creating, for example, `my_script.py`

```python
#!/usr/bin/env python

from systempy import Unit, LoopUnit, DaemonUnit


class ExampleScript(
    Unit,
    LoopUnit,
    DaemonUnit,
):
    async def main_async(self):
        """
        Write your code here. Easy to use, isn't it?
        """


if __name__ == "__main__":
    ExampleScript.launch()
```

## Run it

```sh
python my_script.py
```
