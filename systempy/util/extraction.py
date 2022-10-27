from typing import Iterable
from .register import register_direction
from . import constants

TypeIterable = Iterable[type]


def extract_attrs(iterable: TypeIterable, name: str):
    return (
        # ===
        getattr(item, name)
        for item in iterable
        if name in item.__dict__
    )


@register_direction("forward")
@register_direction("gather")
def callbacks_direct(iterable: TypeIterable, name: str):
    callbacks = extract_attrs(iterable, name)
    return tuple(callbacks)


@register_direction("backward")
def callbacks_reversed(iterable: TypeIterable, name: str):
    callbacks = extract_attrs(iterable, name)
    callbacks = list(callbacks)
    callbacks.reverse()
    return tuple(callbacks)


def extract_bases(cls: type):
    bases = cls.mro()

    bases = [Base for Base in bases if Base not in constants.lifecycle_bases_blacklist]

    lifecycle_disallowed_attrs = constants.lifecycle_disallowed_attrs
    for base in bases:
        for check_attribute, description in lifecycle_disallowed_attrs:
            if check_attribute in base.__dict__:
                message = f"Attribute {check_attribute} is not allowed"

                if description:
                    message = "%s. %s" % (message, description)

                raise ValueError(message, base)

    first = bases.pop(0)
    bases.append(first)
    return tuple(bases)
