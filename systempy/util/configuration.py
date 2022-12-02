from dataclasses import fields
from typing import Dict, Any

from .register import register_addition_cfg_applier
from .creation import create_partial_handler_generic
from .local_typing import SMConfig, TypeIterable
from .local_dataclasses import ClsCFG


from .misc import get_key_or_create

from .constants import lifecycle_additional_configuration
from .register import register_addition_cfg_applier


@register_addition_cfg_applier
def stack_method(cls: type, config: SMConfig) -> None:
    create = create_partial_handler_generic(cls)

    for stage_name, stage_config in config.items():
        create(stage_name, stage_config)


def apply_additional_config(cls: type, config: ClsCFG) -> None:
    for clscfg_field in fields(config):
        key = clscfg_field.name
        value = getattr(config, key)
        apply_cfg_handler = register_addition_cfg_applier[key]
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
        basedict = vars(base)

        if "__annotations__" not in basedict:
            continue

        target_annotations: dict[str, Any] = basedict["__annotations__"]
        annotations.update(target_annotations)

        for key, value in target_annotations.items():
            if key in basedict:
                clsdict[key] = value
