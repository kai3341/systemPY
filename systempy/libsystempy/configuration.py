from dataclasses import fields
from typing import Any

from .constants import lifecycle_additional_configuration
from .creation import create_partial_handler_generic
from .local_dataclasses import ClsCFG
from .local_typing import WeakTypeIterable
from .misc import get_key_or_create
from .register import register_addition_cfg_applier


@register_addition_cfg_applier
def stack_method(cls: type, config: ClsCFG) -> None:
    sm_cfg = config.stack_method
    create = create_partial_handler_generic(cls)

    for stage_config in sm_cfg.values():
        create(stage_config)


def apply_additional_config(cls: type, config: ClsCFG) -> None:
    for clscfg_field in fields(config):
        key = clscfg_field.name
        apply_cfg_handler = register_addition_cfg_applier[key]
        apply_cfg_handler(cls, config)


def apply_additional_configuration(this_cls: type) -> type:
    for cls, config in lifecycle_additional_configuration.items():
        if issubclass(this_cls, cls):
            apply_additional_config(this_cls, config)
    return this_cls


def update_annotation(
    clsdict: dict[str, Any],
    bases: WeakTypeIterable,
) -> None:
    annotations: dict[str, type] = get_key_or_create(
        clsdict,
        "__annotations__",
        dict,
    )

    for base in bases:
        basedict = vars(base)

        if "__annotations__" not in basedict:
            continue

        target_annotations: dict[str, type] = basedict["__annotations__"]
        annotations.update(target_annotations)

        for key in target_annotations:
            if key in basedict:
                clsdict[key] = basedict[key]
