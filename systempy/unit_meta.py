from dataclasses import dataclass, field, Field

from sys import version_info
from typing import Type, Dict, Any, Tuple, cast

from typing_extensions import dataclass_transform

from .util.configuration import (
    update_annotation,
    apply_additional_configuration,
)

MetaClassType = Type[type]

default_dataclass_kwargs: Dict[str, bool] = {
    "kw_only": True,
}

if version_info >= (3, 11):
    default_dataclass_kwargs["slots"] = True
    default_dataclass_kwargs["weakref_slot"] = True


unit_meta_dataclass = dataclass(**default_dataclass_kwargs)


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
        new_cls = type.__new__(cls, name, bases, classdict, **kwargs)
        apply_additional_configuration(new_cls)
        new_cls = unit_meta_dataclass(new_cls)
        return cast(UnitMeta, new_cls)
