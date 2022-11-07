from types import FunctionType, MethodType
from typing import Union, Type, Dict
from .typing import T, Named, Outer, Inner, Any, AnyHashable


named_types = (type, FunctionType, MethodType)


def create_dict_registerer(target_dict: Dict[AnyHashable, Any]) -> Outer:
    def outer(named_or_hashable: Union[AnyHashable, Named]) -> Union[Inner, Named]:
        name = (
            named_or_hashable.__name__
            if isinstance(named_or_hashable, named_types)
            else named_or_hashable
        )

        def registerer(target: Named) -> Named:
            target_dict[name] = target
            return target

        return (
            registerer(named_or_hashable)
            if isinstance(named_or_hashable, named_types)
            else registerer
        )

    return outer


def get_key_or_create(
    the_dict: Dict[AnyHashable, T],
    key: AnyHashable,
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
