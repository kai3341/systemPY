from .register import register_addition_cfg_applier
from .creation import create_partial_handler_generic

from . import constants


@register_addition_cfg_applier
def stack_method(cls, config):
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
