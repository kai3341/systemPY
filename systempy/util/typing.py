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

from .. import target

T = TypeVar("T")

Self = TypeVar("Self", covariant=True)

Named = Union[FunctionType, type, Any]
Inner = Callable[[Named], Named]
Outer = Callable[[Union[Hashable, Named]], Union[Inner, Named]]

LFConfig = Dict[str, Any]
LFTypeConfig = Dict[Any, LFConfig]
TargetDirection = Literal["forward", "backward", "gather"]
TargetType = Literal["sync", "async"]

TypeIterable = Iterable[type]

LFMethodSync = Callable[[Any], None]
LFMethodAsync = Callable[[Any], Coroutine[Any, Any, None]]
LFMethod = Union[LFMethodSync, LFMethodAsync]
LFMethodT = TypeVar("LFMethodT", bound=LFMethod)
# LFMethod = FunctionType
LFMethodTuple = Tuple[LFMethodT, ...]
LFHookRegistry = Dict[LFMethodT, List[LFMethodT]]
LFDecorator = Callable[[LFMethodT], LFMethodT]

TargetTypeHandler = Callable[[Type, LFMethodT, LFMethodTuple], LFMethodT]
DirectionHandler = Callable[[TypeIterable, str], LFMethodTuple]
CheckHandler = Callable[[Named], None]

SMConfig = Dict[str, Tuple[LFMethodT, DirectionHandler, TargetTypeHandler]]

AddCFG = Callable[[type, SMConfig], None]
