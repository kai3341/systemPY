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

from .libsystempy.class_role import class_role
from .libsystempy.constants import lifecycle_disallowed_attrs
from .libsystempy.enums import ROLE
from .libsystempy.register import (
    class_role_registry,
    lifecycle_disallowed_method_exempt,
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

            clsdict = vars(base)
            for check_attribute, description in lifecycle_disallowed_attrs:
                if check_attribute in clsdict:
                    if clsdict[check_attribute] in lifecycle_disallowed_method_exempt:
                        continue

                    message = f"Attribute {check_attribute} is not allowed"

                    if description:
                        message = f"{message}. {description}"

                    raise ValueError(message, base)

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
