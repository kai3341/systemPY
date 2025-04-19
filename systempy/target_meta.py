from abc import ABCMeta
from dataclasses import Field, dataclass, field
from typing import Any, cast, dataclass_transform
from typing import final as typing_final

from .util.configuration import apply_additional_configuration
from .util.constants import _init_on_not_final_classes
from .util.register import mark_as_final

default_dataclass_kwargs: dict[str, bool] = {
    "kw_only": True,
}


target_meta_dataclass_fns = (
    dataclass(**default_dataclass_kwargs, init=False, repr=False, eq=False),
    dataclass(**default_dataclass_kwargs),
)

subclassing_final_caught = (
    "Subclassing of final classes {cls} is not allowed. "
    "Did you forget to pass it `final=False`?"
)


@dataclass_transform(
    field_specifiers=(Field, field),
    kw_only_default=True,
)
class TargetMeta(ABCMeta):
    @dataclass_transform(
        field_specifiers=(Field, field),
        kw_only_default=True,
    )
    def __new__(
        mcs: type["TargetMeta"],
        name: str,
        bases: tuple[type, ...],
        classdict: dict[str, Any],
        *,
        final: bool = True,
        **kwargs: Any,
    ) -> type["TargetMeta"]:
        for base in bases:
            if base in mark_as_final:
                raise TypeError(subclassing_final_caught.format(cls=base))

        if not final:
            classdict["__init__"] = _init_on_not_final_classes

        new_cls = super().__new__(mcs, name, bases, classdict, **kwargs)

        if final:
            # I'n not sure I can trust `typing.final` implementation
            apply_additional_configuration(mark_as_final(typing_final(new_cls)))

        target_meta_dataclass = target_meta_dataclass_fns[final]
        return target_meta_dataclass(cast("type[TargetMeta]", new_cls))
