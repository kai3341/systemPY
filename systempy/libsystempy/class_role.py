from collections.abc import Callable
from dataclasses import dataclass
from sys import version_info
from typing import TypeVar
from typing import final as typing_final

from typing_extensions import NamedTuple

from .configuration import apply_additional_configuration
from .register import register_target

T = TypeVar("T")


class ClassRole(NamedTuple):
    app: Callable[[type[T]], type[T]]
    unit: Callable[[type[T]], type[T]]
    mixin: Callable[[type[T]], type[T]]
    target: Callable[[type[T]], type[T]]


default_dataclass_kwargs: dict[str, bool] = {}

if version_info >= (3, 10):
    default_dataclass_kwargs["kw_only"] = True


nonfinal = dataclass(**default_dataclass_kwargs, init=False, repr=False, eq=False)
final = dataclass(**default_dataclass_kwargs)


class_role = ClassRole(
    lambda cls: final(apply_additional_configuration(typing_final(cls))),
    nonfinal,
    nonfinal,
    lambda cls: nonfinal(register_target(cls)),
)
