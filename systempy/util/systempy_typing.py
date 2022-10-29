from typing import Type, Dict, Tuple, TypeVar, Callable, Iterable, Any, Literal

T = TypeVar("T")
LFConfig = Dict[str, Any]
LFTypeConfig = Dict[type, LFConfig]
TargetDirection = Literal["forward", "backward", "gather"]
TargetType = Literal["sync", "async"]

TypeIterable = Iterable[type]

LFMethod = Callable[[T], None]
LFMethodTuple = Tuple[LFMethod, ...]

TargetTypeHandler = Callable[[Type, LFMethod, LFMethodTuple], LFMethod]
DirectionHandler = Callable[[TypeIterable, str], LFMethodTuple]
CheckHandler = Callable[[LFMethod], None]

SMConfig = Dict[str, Tuple[LFMethod, DirectionHandler, TargetTypeHandler]]
