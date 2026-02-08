from collections.abc import Callable
from dataclasses import dataclass
from sys import version_info
from typing import TypeVar

from typing_extensions import NamedTuple

from .configuration import apply_additional_configuration
from .register import lifecycle_disallowed_method_exempt, register_target

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


def role_app(cls: type) -> type:
    cls = final(apply_additional_configuration(cls))
    clsdict = cls.__dict__
    for name in ("__init__", "__post_init__"):
        if method := clsdict.get(name):
            lifecycle_disallowed_method_exempt(method)
    return cls


class_role = ClassRole(
    role_app,
    nonfinal,
    nonfinal,
    lambda cls: nonfinal(register_target(cls)),
)
