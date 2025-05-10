"""
Welcome to Dead Code! It was try to build this project via mypyc. But:
https://mypyc.readthedocs.io/en/latest/native_classes.html#inheritance
It's critical besause all this project about inheritance

TODO: mypy plugin is very messy now and does not build. Refactor it
TODO: It looks all util module may be built successfuly
"""

import os
from collections.abc import Generator, Mapping
from typing import Union

from mypyc.build import mypycify

from setup_constants import NAME, pyproject

StructLeaf = tuple[str, ...]
Struct = Mapping[str | None, Union[StructLeaf, "Struct"]]

mypy_config: dict[str, str] = pyproject.get("tool", {}).get("mypy", {})


mypycify_structure: Struct = {
    NAME: {
        None: (
            # "target.py",
            # "unit_meta.py",
        ),
        "unit": {
            None: (
                # "unit.py",
                # "scripting.py",
                # "daemon.py",
                # "loop.py",
            ),
            "repl": {
                None: (
                    # " __init__.py",
                    "handle_interrupt.py",
                    # "mixins.py",
                    # "repl.py",
                ),
            },
            "ext": {
                None: (
                    # "pretty_repl.py",
                    # "target_ext.py",
                    # "starlette.py",
                    # "celery.py",
                ),
            },
        },
        "libsystempy": {
            None: (
                "callback_plan.py",
                "check.py",
                "class_role.py",
                "configuration.py",
                "constants.py",
                "creation.py",
                "extraction.py",
                # "enums.py",
                "handler_type.py",
                # "hook_registry.py",
                # "local_dataclasses.py",  # https://github.com/python/mypy/issues/13304  # noqa: E501, ERA001
                "local_typing.py",
                "misc.py",
                # "register.py",
                "thread_exception.py",
                # "weak_queue.py",
            ),
        },
    },
}


def _walk_next(struct: Struct, root: str) -> Generator[str, None, None]:
    for key, value in struct.items():
        if key is None:
            assert isinstance(value, tuple)
            value_leaf: StructLeaf = value
            for item in value_leaf:
                yield os.path.join(root, item)  # noqa: PTH118
        else:
            assert isinstance(value, dict)
            value_struct: Struct = value
            next_root = os.path.join(root, key)  # noqa: PTH118
            yield from _walk_next(value_struct, next_root)


def walk(struct: Struct) -> Generator[str, None, None]:
    for key, value in struct.items():
        if key is None:
            assert isinstance(value, tuple)
            value_leaf: StructLeaf = value
            yield from value_leaf
        else:
            assert isinstance(value, dict)
            value_struct: Struct = value
            yield from _walk_next(value_struct, key)


ext_modules_paths = list(walk(mypycify_structure))

if "custom_typeshed_dir" in mypy_config:
    custom_typeshed_dir = mypy_config["custom_typeshed_dir"]
    # pylint: disable-next=C0209
    custom_typeshed_dir = f"--custom-typing-module='{custom_typeshed_dir}'"
    ext_modules_paths.insert(0, custom_typeshed_dir)

ext_modules = mypycify(ext_modules_paths)


__all__ = ("ext_modules",)
