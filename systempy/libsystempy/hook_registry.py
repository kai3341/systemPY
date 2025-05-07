from collections.abc import Callable
from dataclasses import dataclass
from inspect import iscoroutinefunction
from typing import (
    ClassVar,
)
from weakref import WeakKeyDictionary

from . import register
from .enums import DIRECTION
from .local_dataclasses import BaseRegistry
from .local_typing import (
    Decorator,
    Named,
    P,
    R,
)
from .misc import get_key_or_create
from .weak_queue import WeakQueue


@dataclass()
class HookRegistry(BaseRegistry[Callable[P, R], WeakQueue[Callable[P, R]]]):
    hook_parents: ClassVar = WeakKeyDictionary[Named, Named]()

    __hook_invalid_template = (
        "You are trying to register executing asyncronous hook %s on the stage "
        "when event loop is not started or already stopped"
    )

    def __call__(
        self,
        reason: Callable[P, R],
        direction: DIRECTION | None = None,
    ) -> Decorator[P, R]:
        registry = get_key_or_create(self._registry, reason, WeakQueue)
        lifecycle_method_parent = self.hook_parents.get(reason, reason)
        parent_syncronous = not iscoroutinefunction(lifecycle_method_parent)

        def inner(func: Callable[P, R]) -> Callable[P, R]:
            if parent_syncronous and iscoroutinefunction(func):
                raise ValueError(self.__hook_invalid_template % func)

            if direction is not None:
                register.register_target_method(direction)(func)
            self.hook_parents[func] = lifecycle_method_parent
            registry.append(func)
            return func

        return inner
