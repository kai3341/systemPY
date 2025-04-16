"""
Welcome to Dead Code! It was try to build this project via mypyc. But:
https://mypyc.readthedocs.io/en/latest/native_classes.html#inheritance
It's critical besause all this project about inheritance

TODO: mypy plugin is very messy now and does not build. Refactor it
TODO: It looks all util module may be built successfuly
"""

import os
from collections.abc import Generator
from typing import Literal

from mypyc.build import mypycify

from setup_constants import NAME, pyproject

StructLeaf = tuple[str, ...]
StructLeafNode = dict[Literal[None], StructLeaf]
Struct = StructLeafNode | dict[str, "Struct"]

mypy_config: dict[str, str] = pyproject.get("tool", {}).get("mypy", {})


mypycify_structure: Struct = {  # pyright: ignore[reportAssignmentType]
    NAME: {
        None: (
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
                "util.py",
            ),
        },
        "util": {
            None: (
                "local_typing.py",
                # "local_dataclasses.py",  # https://github.com/python/mypy/issues/13304  # noqa: E501, ERA001
                "constants.py",
                "extraction.py",
                # "enums.py",
                "configuration.py",
                "check.py",
                "creation.py",
                "callback_plan.py",
                "misc.py",
                # "register.py",
                "handler_type.py",
            ),
        },
        # "ext": {  # noqa: ERA001
        #     None: (
        #         "pretty_repl.py",
        #         "target_ext.py",
        #         "starlette.py",
        #         "celery.py",
        #     ),
        # },
    },
}


def _walk_next(struct: Struct, root: str) -> Generator[str, None, None]:
    for key, value in struct.items():
        if key is None:
            value_leaf: StructLeaf = value
            for item in value_leaf:
                yield os.path.join(root, item)  # noqa: PTH118
        else:
            value_struct: Struct = value
            next_root = os.path.join(root, key)  # noqa: PTH118
            yield from _walk_next(value_struct, next_root)


def walk(struct: Struct) -> Generator[str, None, None]:
    for key, value in struct.items():
        if key is None:
            value_leaf: StructLeaf = value
            yield from value_leaf
        else:
            value_struct: Struct = value
            yield from _walk_next(value_struct, key)


ext_modules = walk(mypycify_structure)
ext_modules = list(ext_modules)

if "custom_typeshed_dir" in mypy_config:
    custom_typeshed_dir = mypy_config["custom_typeshed_dir"]
    # pylint: disable-next=C0209
    custom_typeshed_dir = f"--custom-typing-module='{custom_typeshed_dir}'"
    ext_modules.insert(0, custom_typeshed_dir)

ext_modules = mypycify(ext_modules)


__all__ = ("ext_modules",)
