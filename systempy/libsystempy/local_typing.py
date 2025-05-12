from collections.abc import Callable, Coroutine, Iterable, MutableMapping
from types import BuiltinFunctionType, FunctionType
from typing import TYPE_CHECKING, TypeVar, Union
from weakref import WeakKeyDictionary, ref

from typing_extensions import ParamSpec, TypeAlias

if TYPE_CHECKING:
    from . import local_dataclasses

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")
A = ParamSpec("A")
KT = TypeVar("KT")
VT = TypeVar("VT")

function_types = (FunctionType, BuiltinFunctionType)

Named = Union[Callable, type]
PrimitiveHashable = Union[str, bytes, int, float, bool]

TT = TypeVar("TT", bound=type)  # pylint: disable=C0103

WeakTypeIterable = Iterable[ref[type]]

CTuple = tuple[Callable[P, R], ...]
Decorator = Callable[[Callable[P, R]], Callable[P, R]]

DirectionHandler = Callable[[WeakTypeIterable, Callable], "CTuple[P, R]"]

SMConfig = MutableMapping[str, "local_dataclasses.GenericHandlerSettings"]
LFTypeConfig = WeakKeyDictionary[TT, "local_dataclasses.ClsCFG"]
LFRegistered = MutableMapping[
    Callable[P, R],
    "local_dataclasses.LFMethodsRegistered[P, R]",
]
LFMetadata = MutableMapping[
    Callable[P, R],
    "local_dataclasses.CallbackMetadata",
]
MaybeCoro: TypeAlias = Union[R, Coroutine[R, None, None]]

DisallowedAttrInfo = tuple[str, str]
