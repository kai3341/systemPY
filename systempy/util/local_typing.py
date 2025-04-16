from collections.abc import Callable, Coroutine, Iterable
from types import BuiltinFunctionType, FunctionType
from typing import (
    TYPE_CHECKING,
    ParamSpec,
    TypeAlias,
    TypeVar,
)

if TYPE_CHECKING:
    from . import local_dataclasses

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")
A = ParamSpec("A")
KT = TypeVar("KT")
VT = TypeVar("VT")

function_types = (FunctionType, BuiltinFunctionType)

Named = Callable | type
PrimitiveHashable = str | bytes | int | float | bool

TT = TypeVar("TT", bound=type)  # pylint: disable=C0103

TypeIterable = Iterable[type]

CTuple = tuple[Callable[P, R], ...]
Decorator = Callable[[Callable[P, R]], Callable[P, R]]

DirectionHandler = Callable[[TypeIterable, str], CTuple[P, R]]

SMConfig = dict[str, "local_dataclasses.GenericHandlerSettings"]
LFTypeConfig = dict[TT, "local_dataclasses.ClsCFG"]
LFRegistered = dict[Callable, "local_dataclasses.LFMethodsRegistered"]
MaybeCoro: TypeAlias = R | Coroutine[R, None, None]

DisallowedAttrInfo = tuple[str, str]
