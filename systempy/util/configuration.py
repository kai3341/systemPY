from typing import Dict, Any, Hashable, Union

from .register import register_addition_cfg_applier
from .creation import create_partial_handler_generic
from .typing import SMConfig, TypeIterable


from .misc import get_key_or_create

from .constants import (
    apply_additional_config__cfg,
    lifecycle_additional_configuration,
)


@register_addition_cfg_applier
def stack_method(cls: type, config: SMConfig) -> None:
    create = create_partial_handler_generic(cls)

    for stage_name, stage_args in config.items():
        create(stage_name, *stage_args)


def apply_additional_config(cls: type, config: Dict[str, Dict]) -> None:
    for key, value in config.items():
        apply_cfg_handler = apply_additional_config__cfg[key]
        apply_cfg_handler(cls, value)


def apply_additional_configuration(this_cls: type) -> None:
    for cls, config in lifecycle_additional_configuration.items():
        assert isinstance(cls, type)
        if issubclass(this_cls, cls):
            apply_additional_config(this_cls, config)


def update_annotation(
    clsdict: Dict[Any, Any],
    bases: TypeIterable,
) -> None:
    annotations: Dict[str, Any] = get_key_or_create(
        clsdict,
        "__annotations__",
        dict,
    )

    for base in bases:
        basedict = base.__dict__

        if "__annotations__" not in basedict:
            continue

        annotations.update(basedict["__annotations__"])
