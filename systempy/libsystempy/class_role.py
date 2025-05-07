from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, NamedTuple, TypeVar
from typing import final as typing_final

from .configuration import apply_additional_configuration
from .register import mark_as_final, mark_as_target, register_target

T = TypeVar("T")


class ClassRole(NamedTuple, Generic[T]):
    app: Callable[[T], T]
    unit: Callable[[T], T]
    mixin: Callable[[T], T]
    target: Callable[[T], T]


default_dataclass_kwargs: dict[str, bool] = {
    "kw_only": True,
}

nonfinal = dataclass(**default_dataclass_kwargs, init=False, repr=False, eq=False)
final = dataclass(**default_dataclass_kwargs)


class_role = ClassRole[type](
    lambda cls: final(apply_additional_configuration(mark_as_final(typing_final(cls)))),
    nonfinal,
    lambda cls: nonfinal(mark_as_target(cls)),
    lambda cls: nonfinal(register_target(cls)),
)
