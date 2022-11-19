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
)

from . import dataclasses as _dataclasses

T = TypeVar("T")

function_types = (FunctionType, BuiltinFunctionType)
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
CF = Union[Callable, FunctionType, BuiltinFunctionType]

LFMethodSync = Callable[[T], None]
LFMethodAsync = Callable[[T], Coroutine[Any, Any, None]]
LFMethod = Union[LFMethodSync, LFMethodAsync]

LFConfig = Dict[str, Any]
LFTypeConfig = Dict[AnyHashable, LFConfig]
TargetDirection = Literal["forward", "backward", "gather"]
TargetType = Literal["sync", "async"]

TypeIterable = Iterable[type]

LFMethodTuple = Tuple[LFMethod, ...]
LFHookRegistry = Dict[CT, List[CT]]
LFDecorator = Callable[[CT], CT]

TargetTypeHandler = Callable[[Type, CT, LFMethodTuple], CT]
DirectionHandler = Callable[[TypeIterable, str], LFMethodTuple]
CheckHandler = Callable[[CT], None]

SMConfig = Dict[str, "_dataclasses.GenericHandlerSettings"]

AddCFG = Callable[[PrimitiveHashable, SMConfig], None]
