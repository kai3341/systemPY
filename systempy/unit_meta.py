from dataclasses import dataclass, field, Field

# from sys import version_info
from typing import TypeVar, Type, Dict, Any, Tuple, cast

from typing_extensions import dataclass_transform

from .util.configuration import (
    update_annotation,
    apply_additional_configuration,
)

MetaClassType = Type[type]

default_dataclass_kwargs: Dict[str, Any] = {
    "kw_only": True,
}

# if version_info >= (3, 10):
#     default_dataclass_kwargs["slots"] = True


@dataclass_transform(
    field_specifiers=(Field, field),
    kw_only_default=True,
)
class UnitMeta(type):
    def __new__(
        cls: MetaClassType,
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
