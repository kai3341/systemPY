from dataclasses import dataclass

# from sys import version_info
from typing import Type, Dict, Any, Tuple, cast

from .util.configuration import (
    update_annotation,
    apply_additional_configuration,
)

default_dataclass_kwargs: Dict[str, Any] = {}

# if version_info >= (3, 10):
#     default_dataclass_kwargs["slots"] = True


class UnitMeta(type):
    def __new__(
        cls: Type[type],
        name: str,
        bases: Tuple[type, ...],
        classdict: Dict[str, Any],
        /,
        **kwargs: Dict[str, Any],
    ) -> "UnitMeta":
        update_annotation(classdict, bases)
        # classdict["__slots__"] = tuple(classdict["__annotations__"])
        new_cls = type.__new__(cls, name, bases, classdict, **kwargs)
        # if hasattr(new_cls, "__annotations__"):
        # new_cls.__slots__ = tuple(new_cls.__annotations__)
        apply_additional_configuration(new_cls)
        new_cls = dataclass(**default_dataclass_kwargs)(new_cls)
        return cast(UnitMeta, new_cls)
