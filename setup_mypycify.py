"""
Welcome to Dead Code! It was try to build this project via mypyc. But:
https://mypyc.readthedocs.io/en/latest/native_classes.html#inheritance
It's critical besause all this project about inheritance

TODO: mypy plugin is very messy now and does not build. Refactor it
TODO: It looks all util module may be built successfuly
"""

import os
from mypyc.build import mypycify

from setup_constants import name, pyproject

from typing import Dict, Tuple, Union, Literal, Generator

STRUCT_LEAF = Tuple[str, ...]
STRUCT_LEAF_NODE = Dict[Literal[None], STRUCT_LEAF]
STRUCT = Union[STRUCT_LEAF_NODE, Dict[str, "STRUCT"]]

mypy_config = pyproject.get("tool", {}).get("mypy", {})

mypycify_structure: STRUCT = {
    name: {
        None: (
            "mypy.py",
            # "target.py",
            # "unit_meta.py",
            # "unit.py",
            # "process.py",
            # "daemon.py",
            # "loop.py",
        ),
        "repl": {
            None: (
                # " __init__.py",
                "handle_interrupt.py",
                # "mixins.py",
                # "repl.py",
                "repl_typing.py",
                "util.py",
            )
        },
        "util": {
            None: (
                "local_typing.py",
                "local_dataclasses.py",
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
        # "ext": {
        #     None: (
        #         "pretty_repl.py",
        #         "target_ext.py",
        #         "starlette.py",
        #         "celery.py",
        #     ),
        # },
    },
}


def _walk_next(struct: STRUCT, root: str) -> Generator[str, None, None]:
    for key, value in struct.items():
        if key is None:
            value_leaf: STRUCT_LEAF = value
            for item in value_leaf:
                yield os.path.join(root, item)
        else:
            value_struct: STRUCT = value
            next_root = os.path.join(root, key)
            yield from _walk_next(value_struct, next_root)


def walk(struct: STRUCT) -> Generator[str, None, None]:
    for key, value in struct.items():
        if key is None:
            value_leaf: STRUCT_LEAF = value
            for item in value_leaf:
                yield item
        else:
            value_struct: STRUCT = value
            yield from _walk_next(value_struct, key)


ext_modules = walk(mypycify_structure)
ext_modules = list(ext_modules)

if "custom_typeshed_dir" in mypy_config:
    custom_typeshed_dir = mypy_config["custom_typeshed_dir"]
    custom_typeshed_dir = "--custom-typing-module='%s'" % custom_typeshed_dir
    ext_modules.insert(0, custom_typeshed_dir)

ext_modules = mypycify(ext_modules)


__all__ = ("ext_modules",)
