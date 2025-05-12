from collections.abc import Callable, Coroutine, MutableMapping, MutableSet
from dataclasses import dataclass, field
from typing import Generic, overload
from weakref import ref

from .enums import DIRECTION
from .local_typing import (
    KT,
    VT,
    CTuple,
    Decorator,
    DirectionHandler,
    P,
    PrimitiveHashable,
    R,
    SMConfig,
    WeakTypeIterable,
)


@dataclass()
class LFMethodsRegistered(Generic[P, R]):
    direction: "DirectionHandler[P, R]"
    direction_name: DIRECTION
    interface: ref[type] = field(init=False)


@dataclass()
class GenericHandlerSettings(Generic[P, R]):
    reason: ref[Callable]
    collect: ref[Callable[[WeakTypeIterable, Callable], "CTuple[P, R]"]]
    compose: ref[Callable[[type, WeakTypeIterable, Callable, "CTuple[P, R]"], Callable]]


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
    _registry: MutableMapping[KT, VT] = field(default_factory=dict)

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
    def __call__(self, named_or_hashable: PrimitiveHashable) -> "Decorator[P, R]": ...

    def __call__(
        self,
        named_or_hashable: "PrimitiveHashable | Callable[P, R]",
    ) -> "Decorator[P, R] | Callable[P, R]":
        if callable(named_or_hashable):
            name = named_or_hashable.__name__
            self._registry[name] = named_or_hashable
            return named_or_hashable

        def registerer(target: Callable[P, R]) -> Callable[P, R]:
            self._registry[named_or_hashable] = target
            return target

        return registerer


@dataclass()
class SetRegistry(Generic[VT]):
    regisrty: MutableSet[VT] = field(default_factory=set)

    def __call__(self, target: VT) -> VT:
        self.regisrty.add(target)
        return target

    def __contains__(self, target: VT) -> bool:
        return target in self.regisrty

    def add(self, *args: VT) -> None:
        for t in args:
            self(t)


@dataclass()
class CallbackMetadata:
    call_order: tuple[str, ...]
