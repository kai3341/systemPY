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
    # Optional,
)

T = TypeVar("T")

AnyHashable = Union[Hashable, str, bytes, int, bool, FunctionType, type]

Named = Union[FunctionType, type, Any]
Inner = Callable[[Named], Named]
Outer = Callable[[Union[AnyHashable, Named]], Union[Inner, Named]]

LFConfig = Dict[str, Any]
LFTypeConfig = Dict[Any, LFConfig]
TargetDirection = Literal["forward", "backward", "gather"]
TargetType = Literal["sync", "async"]

TypeIterable = Iterable[type]

LFMethodSync = Callable[[Any], None]
LFMethodAsync = Callable[[Any], Coroutine[Any, Any, None]]
LFMethod = Union[LFMethodSync, LFMethodAsync]
LFMethodT = TypeVar("LFMethodT", bound=LFMethod)
LFMethodTuple = Tuple[LFMethodT, ...]
LFHookRegistry = Dict[LFMethodT, List[LFMethodT]]
LFDecorator = Callable[[LFMethodT], LFMethodT]

TargetTypeHandler = Callable[[Type, LFMethodT, LFMethodTuple], LFMethodT]
DirectionHandler = Callable[[TypeIterable, str], LFMethodTuple]
CheckHandler = Callable[[Named], None]

SMConfig = Dict[str, Tuple[LFMethodT, DirectionHandler, TargetTypeHandler]]

AddCFG = Callable[[type, SMConfig], None]
