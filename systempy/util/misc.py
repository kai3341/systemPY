from typing import Union, Callable, Type, TypeVar, Dict, Any

T = TypeVar("T")
Named = Union[Callable, Type]
Inner = Callable[[Named], Named]
Outer = Callable[[Union[str, Named]], Union[Inner, Named]]


def create_dict_registerer(target_dict: Dict[str, Named]) -> Outer:
    def outer(name_or_target: Union[str, Named]):
        if isinstance(name_or_target, str):
            name = name_or_target
        else:
            name = name_or_target.__name__

        def registerer(target: Named) -> Named:
            target_dict[name] = target
            return target

        if isinstance(name_or_target, str):
            return registerer
        else:
            return registerer(name_or_target)

    return outer


def get_key_or_create(
    the_dict: Dict,
    key: Any,
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
