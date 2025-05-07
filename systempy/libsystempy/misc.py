from collections.abc import MutableMapping

from .local_typing import KT, VT


def get_key_or_create(
    the_dict: MutableMapping[KT, VT],
    key: KT,
    default_factory: type[VT],
) -> VT:
    """
    Like DefaultDict
    """
    if key in the_dict:
        return the_dict[key]
    value = default_factory()
    the_dict[key] = value
    return value
