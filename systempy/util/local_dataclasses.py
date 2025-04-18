from collections.abc import Callable, Coroutine, MutableMapping
from dataclasses import dataclass, field
from inspect import iscoroutinefunction
from typing import (
    ClassVar,
    Generic,
    overload,
)

from .enums import CONST
from .local_typing import (
    KT,
    VT,
    CTuple,
    Decorator,
    DirectionHandler,
    Named,
    P,
    PrimitiveHashable,
    R,
    SMConfig,
    TypeIterable,
)
from .misc import get_key_or_create


@dataclass()
class LFMethodsRegistered(Generic[P, R]):
    direction: DirectionHandler[P, R] | None
    direction_name: CONST | None
    interface: type | None


@dataclass()
class GenericHandlerSettings(Generic[P, R]):
    reason: Callable
    collect: Callable[[TypeIterable, str], CTuple[P, R]]
    compose: Callable[[type, Callable, CTuple[P, R]], Callable]


@dataclass()
class SeparatedLFMethods(Generic[P, R]):
    callbacks_sync: tuple[Callable[P, R], ...]
    callbacks_async: tuple[Callable[P, Coroutine[R, None, None]], ...]


@dataclass()
class ClsCFG(Generic[P, R]):
    stack_method: SMConfig = field(default_factory=dict)


# ===


@dataclass()
class BaseRegistry(Generic[KT, VT]):
    _registry: MutableMapping[KT, VT] = field(init=False, default_factory=dict)

    def __getitem__(self, key: KT) -> VT:
        return self._registry[key]

    def __contains__(self, key: KT) -> bool:
        return key in self._registry

    def get_or_raise(self, *keys: KT) -> VT:
        registry = self._registry
        for key in keys:
            if key in registry:
                return registry[key]

        raise KeyError(keys)


@dataclass()
class NamedRegistry(BaseRegistry[PrimitiveHashable, Callable[P, R]]):
    @overload
    def __call__(self, named_or_hashable: Callable[P, R]) -> Callable[P, R]: ...

    @overload
    def __call__(self, named_or_hashable: PrimitiveHashable) -> Decorator[P, R]: ...

    def __call__(
        self,
        named_or_hashable: PrimitiveHashable | Callable[P, R],
    ) -> Decorator[P, R] | Callable[P, R]:
        if callable(named_or_hashable):
            name = named_or_hashable.__name__
            self._registry[name] = named_or_hashable
            return named_or_hashable

        def registerer(target: Callable[P, R]) -> Callable[P, R]:
            self._registry[named_or_hashable] = target
            return target

        return registerer


@dataclass()
class HookRegistry(BaseRegistry[Callable[P, R], list[Callable[P, R]]]):
    hook_parents: ClassVar[MutableMapping[Named, Named]] = {}

    __hook_invalid_template = (
        "You are trying to register executing asyncronous hook %s on the stage "
        "when event loop is not started or already stopped"
    )

    def __call__(self, reason: Callable[P, R]) -> Decorator[P, R]:
        registry: list[Callable] = get_key_or_create(self._registry, reason, list)
        lifecycle_method_parent = self.hook_parents.get(reason, reason)
        parent_syncronous = not iscoroutinefunction(lifecycle_method_parent)

        def inner(func: Callable[P, R]) -> Callable[P, R]:
            if parent_syncronous and iscoroutinefunction(func):
                raise ValueError(self.__hook_invalid_template % func)

            self.hook_parents[func] = lifecycle_method_parent
            registry.append(func)
            return func

        return inner
