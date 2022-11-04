from types import FunctionType
from typing import Union, Type, Dict, Hashable
from .typing import T, Named, Outer, Inner, Any, LFMethodT


named_types = (type, FunctionType)


def create_dict_registerer(target_dict: Dict[Hashable, Any]) -> Outer:
    def outer(named_or_hashable: Union[Hashable, Named]) -> Union[Inner, Named]:
        name = (
            named_or_hashable.__name__
            if isinstance(named_or_hashable, named_types)
            else named_or_hashable
        )

        def registerer(target: LFMethodT) -> LFMethodT:
            target_dict[name] = target
            return target

        return (
            registerer(named_or_hashable)
            if isinstance(named_or_hashable, named_types)
            else registerer
        )

    return outer


def get_key_or_create(
    the_dict: Dict[Hashable, T],
    key: Hashable,
    default_factory: Type[T],
) -> T:
    """
    Like DefaultDict
    """
    if key in the_dict:
        return the_dict[key]
    else:
        value = default_factory()
        the_dict[key] = value
        return value
