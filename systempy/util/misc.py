from inspect import iscoroutinefunction
from typing import (
    Union,
    Type,
    Callable,
    Dict,
    MutableMapping,
    List,
    ClassVar,
    overload,
)

from .local_typing import (
    KT,
    VT,
    CT,
    TT,
    FT,
    BFT,
    CTFT,
    PrimitiveHashable,
    FunctionTypes,
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
        self.__registry = {}
        self.__getitem__ = self.__registry.__getitem__
        self.__contains__ = self.__registry.__contains__

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


class HookRegistry:
    """
    A little bit different then NamedRegistry:
    * class variable `hook_parents`
    * * TODO: It may be the same attribute as registry
    * * * So, it may require 2 registries
    * A little different registration logic
    """

    hook_parents: ClassVar[Dict[CTFT, CTFT]] = {}
    __registry: Dict[FunctionTypes, List[CTFT]]
    __getitem__: Callable
    __contains__: Callable

    _hook_invalid_template = (
        "You are trying to register executing asyncronous hook %s on the stage "
        "when event loop is not started or already stopped"
    )

    __slots__ = (
        "__registry",
        "__getitem__",
        "__contains__",
    )

    def __init__(self) -> None:
        self.__registry = {}
        self.__getitem__ = self.__registry.__getitem__
        self.__contains__ = self.__registry.__contains__

    def __call__(self, reason: CTFT) -> Inner:
        registry: list = get_key_or_create(self.__registry, reason, list)
        lifecycle_method_parent = self.hook_parents.get(reason, reason)
        parent_syncronous = not iscoroutinefunction(lifecycle_method_parent)

        def inner(func: CTFT) -> CTFT:
            if parent_syncronous and iscoroutinefunction(func):
                raise ValueError(self._hook_invalid_template % func)

            self.hook_parents[func] = lifecycle_method_parent
            registry.append(func)
            return func

        return inner

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__registry}>"


def get_key_or_create(
    the_dict: MutableMapping[KT, VT],
    key: KT,
    default_factory: Type[VT],
) -> VT:
    """
    Like DefaultDict
    """
    if key in the_dict:
        return the_dict[key]
    else:
        value = default_factory()
        the_dict[key] = value
        return value
