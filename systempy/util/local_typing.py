from types import FunctionType, BuiltinFunctionType
from typing import (
    Type,
    Dict,
    Tuple,
    List,
    TypeVar,
    Callable,
    Iterable,
    Any,
    Literal,
    Union,
    Coroutine,
    AnyStr,
    # TypedDict,
)

from . import local_dataclasses

T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")

function_types = (FunctionType, BuiltinFunctionType)
FunctionTypes = Union[FunctionType, BuiltinFunctionType]
named_types = (*function_types, type)

Named = Union[Callable, Type]
PrimitiveHashable = Union[AnyStr, int, float, bool]
AnyHashable = Union[PrimitiveHashable, Named]

CT = TypeVar("CT", bound=Callable)
FT = TypeVar("FT", bound=FunctionType)
BFT = TypeVar("BFT", bound=BuiltinFunctionType)
TT = TypeVar("TT", bound=type)
CFT = Union[CT, FT, BFT]
CTFT = Union[CT, FT, BFT, TT]

LFMethodSync = Callable[[T], None]
LFMethodAsync = Callable[[T], Coroutine[Any, Any, None]]
LFMethod = Union[LFMethodSync, LFMethodAsync]

TargetDirection = Literal["forward", "backward", "gather"]
TargetType = Literal["sync", "async"]

TypeIterable = Iterable[type]

LFMethodTuple = Tuple[LFMethod, ...]
LFHookRegistry = Dict[CFT, List[CFT]]
LFDecorator = Callable[[CFT], CFT]

TargetTypeHandler = Callable[[Type, CT, LFMethodTuple], CT]
DirectionHandler = Callable[[TypeIterable, str], LFMethodTuple]
CheckHandler = Callable[[CFT], None]

SMConfig = Dict[str, "local_dataclasses.GenericHandlerSettings"]
LFTypeConfig = Dict[TT, "local_dataclasses.ClsCFG"]
