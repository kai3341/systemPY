from __future__ import annotations

from abc import ABCMeta
from dataclasses import Field, field
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    NamedTuple,
    TypeVar,
    cast,
)

from typing_extensions import ParamSpec, dataclass_transform

from .libsystempy import (
    ROLE,
    check_on_subclassing,
    class_role,
    class_role_registry,
)

if TYPE_CHECKING:
    from collections.abc import Callable


A = ParamSpec("A")
T = TypeVar("T")


class ErrorMessages(NamedTuple):
    instantiate_not_ready: str
    subclassed_baked: str


def _role_autodetect(cls: type) -> ROLE:
    clsname_endswith = cls.__name__.endswith
    if clsname_endswith("App"):
        return ROLE.APP
    if clsname_endswith(("Mixin", "MixinABC")):
        return ROLE.MIXIN
    if clsname_endswith(("Unit", "UnitABC")):
        return ROLE.UNIT
    if clsname_endswith(("Target", "TargetABC")):
        return ROLE.TARGET

    raise KeyError(cls)


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
        if role is None:
            role = _role_autodetect(cls)

        class_role_registry[cls] = role
        return getattr(class_role, role)

    @dataclass_transform(
        field_specifiers=(Field, field),
        kw_only_default=True,
    )
    def __new__(
        mcs: type[TargetMeta],
        name: str,
        bases: tuple[type, ...],
        classdict: dict[str, Any],
        *,
        role: ROLE | None = None,
        **kwargs: Any,
    ) -> type[TargetMeta]:
        for base in bases:
            if class_role_registry[base] == ROLE.APP:
                msg = mcs.__systempy_error_messages__.subclassed_baked.format(cls=base)
                raise TypeError(msg)

            check_on_subclassing(base)

        new_cls = cast(
            "type[TargetMeta]",
            super().__new__(mcs, name, bases, classdict, **kwargs),
        )
        return mcs.__systempy_criteria__(new_cls, role)(new_cls)

    def __call__(cls, *args: A.args, **kwargs: A.kwargs) -> TargetMeta[A]:
        cls_role = class_role_registry[cls]
        if cls_role != ROLE.APP:
            msg = cls.__systempy_error_messages__.instantiate_not_ready.format(cls=cls)
            raise TypeError(msg)
        return super().__call__(*args, **kwargs)

    def __init_subclass__(cls) -> None:
        class_role_registry[cls] = ROLE.METACLASS
        return super().__init_subclass__()
