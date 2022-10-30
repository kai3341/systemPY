from typing import Hashable

from .register import register_addition_cfg_applier
from .creation import create_partial_handler_generic
from .typing import SMConfig

from . import constants
from . import misc


@register_addition_cfg_applier
def stack_method(cls: Hashable, config: SMConfig):
    create = create_partial_handler_generic(cls)

    for stage_name, stage_args in config.items():
        create(stage_name, *stage_args)


def apply_additional_config(this_cls, config):
    for key, value in config.items():
        apply_cfg_handler = constants.apply_additional_config__cfg[key]
        apply_cfg_handler(this_cls, value)


def apply_additional_configuration(this_cls):
    for cls, config in constants.lifecycle_additional_configuration.items():
        if issubclass(this_cls, cls):
            apply_additional_config(this_cls, config)


def update_annotation(clsdict, bases):
    annotations = misc.get_key_or_create(clsdict, "__annotations__", dict)

    for base in bases:
        basedict = base.__dict__

        if "__annotations__" not in basedict:
            continue

        annotations.update(basedict["__annotations__"])
