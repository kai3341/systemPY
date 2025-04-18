from abc import ABCMeta
from dataclasses import Field, dataclass, field
from typing import Any, cast, dataclass_transform
from typing import final as typing_final

from .util.configuration import apply_additional_configuration

default_dataclass_kwargs: dict[str, bool] = {
    "kw_only": True,
}


target_meta_dataclass_fns = (
    dataclass(**default_dataclass_kwargs, init=False, repr=False, eq=False),
    dataclass(**default_dataclass_kwargs),
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
        new_cls = super().__new__(mcs, name, bases, classdict, **kwargs)

        if final:
            apply_additional_configuration(typing_final(new_cls))

        target_meta_dataclass = target_meta_dataclass_fns[final]
        return target_meta_dataclass(cast("type[TargetMeta]", new_cls))
