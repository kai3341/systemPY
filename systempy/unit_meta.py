from dataclasses import dataclass
from typing import Type, Dict, Any, Tuple, cast

from .util import configuration as util_configuration


class UnitMeta(type):
    def __new__(
        cls: Type[type],
        name: str,
        bases: Tuple[type, ...],
        classdict: Dict[str, Any],
    ) -> "UnitMeta":
        util_configuration.update_annotation(classdict, bases)
        classdict["__slots__"] = tuple(classdict["__annotations__"])
        new_cls = type.__new__(cls, name, bases, classdict)
        util_configuration.apply_additional_configuration(new_cls)
        new_cls = dataclass(new_cls)
        return cast(UnitMeta, new_cls)
