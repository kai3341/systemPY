from typing import Union, Type, Callable, Dict, overload

from .typing import (
    T,
    CT,
    TT,
    FT,
    BFT,
    CTFT,
    AnyHashable,
    PrimitiveHashable,
    named_types,
)

Inner = Callable[[CTFT], CTFT]
Outer = Callable[[Union[PrimitiveHashable, CT]], Union[Inner, CT]]


class NamedRegistry:
    __registry: Dict[PrimitiveHashable, Callable]
    __getitem__: Callable
    __contains__: Callable

    __slots__ = (
        "__registry",
        "__getitem__",
        "__contains__",
    )

    def __init__(self) -> None:
        registry: Dict[PrimitiveHashable, Callable] = {}
        self.__registry = registry
        self.__getitem__ = registry.__getitem__
        self.__contains__ = registry.__contains__

    @overload
    def __call__(self, named_or_hashable: FT) -> FT:
        ...

    @overload
    def __call__(self, named_or_hashable: BFT) -> BFT:
        ...

    @overload
    def __call__(self, named_or_hashable: TT) -> TT:
        ...

    @overload
    def __call__(self, named_or_hashable: CT) -> CT:
        ...

    @overload
    def __call__(self, named_or_hashable: PrimitiveHashable) -> Inner:
        ...

    def __call__(
        self,
        named_or_hashable: Union[PrimitiveHashable, CTFT],
    ) -> Union[Inner, CTFT]:
        name = (
            named_or_hashable.__name__
            if isinstance(named_or_hashable, named_types)
            else named_or_hashable
        )

        def registerer(target: CTFT) -> CTFT:
            self.__registry[name] = target
            return target

        return (
            # //
            registerer(named_or_hashable)
            if isinstance(named_or_hashable, named_types)
            else registerer
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__registry}>"


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
