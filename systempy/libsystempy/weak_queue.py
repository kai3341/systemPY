from collections.abc import Collection, Iterator
from dataclasses import InitVar, dataclass, field
from typing import ParamSpec, TypeVar
from weakref import ref

P = ParamSpec("P")
T = TypeVar("T")


@dataclass()
class WeakQueue(Collection[T]):
    initial: InitVar[Collection[T] | None] = field(default=None)

    __weaklist: list[ref[T]] = field(init=False, default_factory=list)

    def __post_init__(self, initial: Collection[T] | None) -> None:
        if initial:
            self.__weaklist.extend(map(self.__ref, initial))

    def __ref(self, o: T) -> ref[T]:
        return ref(o, self.__on_discard)

    def __on_discard(self, r: ref[T]) -> None:
        self.__weaklist.remove(r)

    def __contains__(self, value: object) -> bool:
        weaklist = self.__weaklist
        idx = 0
        while idx < len(weaklist):
            val = weaklist[idx]()

            if val is None:
                weaklist.pop(idx)
            else:
                if val == value:
                    return True

                idx += 1

        return False

    def append(self, value: T) -> None:
        return self.__weaklist.append(self.__ref(value))

    def __iter__(self) -> Iterator[T]:
        weaklist = self.__weaklist
        idx = 0
        while idx < len(weaklist):
            val = weaklist[idx]()

            if val is None:
                weaklist.pop(idx)
            else:
                yield val

                idx += 1

    def __len__(self) -> int:
        return len(self.__weaklist)
