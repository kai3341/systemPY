"""
Welcome to Dead Code! It was try to build this project via mypyc. But:
https://mypyc.readthedocs.io/en/latest/native_classes.html#inheritance
It's critical besause all this project about inheritance

TODO: mypy plugin is very messy now and does not build. Refactor it
TODO: It looks all util module may be built successfuly
"""

import os
from mypyc.build import mypycify

from setup_constants import name


mypycify_structure = {
    name: {
        None: (
            # "mypy.py",
            "target.py",
            # "unit_meta.py",
            "unit.py",
            "process.py",
            "daemon.py",
            "repl.py",
            "loop.py",
        ),
        "util": {
            None: (
                "typing.py",
                "dataclasses.py",
                "constants.py",
                "extraction.py",
                "configuration.py",
                "check.py",
                "creation.py",
                "callback_plan.py",
                "misc.py",
                "register.py",
                "handler_type.py",
            ),
        },
        "ext": {
            None: (
                "pretty_repl.py",
                "target_ext.py",
                "starlette.py",
                "celery.py",
            ),
        },
    },
}


def walk(struct: dict, root=None):
    if root is None:
        for key, value in struct.items():
            if key is None:
                for item in value:
                    yield item
            else:
                yield from walk(value, key)
    else:
        for key, value in struct.items():
            if key is None:
                for item in value:
                    yield os.path.join(root, item)
            else:
                next_root = os.path.join(root, key)
                yield from walk(value, next_root)


ext_modules = walk(mypycify_structure)
ext_modules = list(ext_modules)
ext_modules = mypycify(ext_modules)


__all__ = ("ext_modules",)
