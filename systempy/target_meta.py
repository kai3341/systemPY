from abc import ABCMeta
from collections.abc import Callable
from dataclasses import Field, field
from typing import (
    Any,
    ClassVar,
    Generic,
    NamedTuple,
    ParamSpec,
    TypeVar,
    cast,
    dataclass_transform,
)

from .libsystempy.class_role import class_role
from .libsystempy.enums import ROLE
from .libsystempy.register import mark_as_final

A = ParamSpec("A")
T = TypeVar("T")


class ErrorMessages(NamedTuple):
    instantiate_not_ready: str
    subclassed_baked: str


@dataclass_transform(
    field_specifiers=(Field, field),
    kw_only_default=True,
)
class TargetMeta(ABCMeta, Generic[A]):
    __systempy_error_messages__: ClassVar = ErrorMessages(
        instantiate_not_ready="Caught attempt to instantiate class {cls}, but "
        "its name doesn't match `.*App`. You have to rename it or subclass it",
        subclassed_baked="Subclassing of `*.App` classes {cls} is not allowed",
    )

    def __systempy_criteria__(
        cls: type,
        role: ROLE | None,
    ) -> Callable[[type[T]], type[T]]:
        if role is not None:
            return getattr(class_role, role)

        clsname_endswith = cls.__name__.endswith
        if clsname_endswith("App"):
            return class_role.app
        if clsname_endswith(("Mixin", "MixinABC")):
            return class_role.mixin
        if clsname_endswith(("Unit", "UnitABC")):
            return class_role.unit
        if clsname_endswith(("Target", "TargetABC")):
            return class_role.target

        raise KeyError(cls)

    @dataclass_transform(
        field_specifiers=(Field, field),
        kw_only_default=True,
    )
    def __new__(
        mcs: type["TargetMeta"],
        name: str,
        bases: tuple[type, ...],
        classdict: dict[str, Any],
        *,
        role: ROLE | None = None,
        **kwargs: Any,
    ) -> type["TargetMeta"]:
        for base in bases:
            if base in mark_as_final:
                msg = mcs.__systempy_error_messages__.subclassed_baked.format(cls=base)
                raise TypeError(msg)

        new_cls = cast(
            "type[TargetMeta]",
            super().__new__(mcs, name, bases, classdict, **kwargs),
        )
        return mcs.__systempy_criteria__(new_cls, role)(new_cls)

    def __call__(cls, *args: A.args, **kwargs: A.kwargs) -> "TargetMeta[A]":
        if cls not in mark_as_final:
            msg = cls.__systempy_error_messages__.instantiate_not_ready.format(cls=cls)
            raise TypeError(msg)
        return super().__call__(*args, **kwargs)
