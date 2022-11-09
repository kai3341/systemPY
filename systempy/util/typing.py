from types import FunctionType
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
    Hashable,
    Protocol,
    # Optional,
)


T = TypeVar("T")

Named = Union[FunctionType, type]
AnyHashable = Union[Hashable, str, bytes, int, bool, FunctionType, type]

FT = TypeVar("FT", bound=FunctionType)

LFMethodSync = Callable[[T], None]
LFMethodAsync = Callable[[T], Coroutine[Any, Any, None]]

Inner = Callable[[FT], FT]
Outer = Callable[[Union[AnyHashable, FT]], Union[Inner, FT]]

LFConfig = Dict[str, Any]
LFTypeConfig = Dict[Any, LFConfig]
TargetDirection = Literal["forward", "backward", "gather"]
TargetType = Literal["sync", "async"]

TypeIterable = Iterable[type]

LFMethoduple = Tuple[FT, ...]
LFHookRegistry = Dict[FT, List[FT]]
LFDecorator = Callable[[FT], FT]

TargetTypeHandler = Callable[[Type, FT, LFMethoduple], FT]
DirectionHandler = Callable[[TypeIterable, str], LFMethoduple]
CheckHandler = Callable[[Named], None]

SMConfig = Dict[str, Tuple[FT, DirectionHandler, TargetTypeHandler]]

AddCFG = Callable[[type, SMConfig], None]
