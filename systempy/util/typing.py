from typing import Dict, TypeVar, Any, Literal

T = TypeVar("T")
LFConfig = Dict[str, Any]
LFTypeConfig = Dict[type, LFConfig]
TargetDirection = Literal["forward", "backward", "gather"]
