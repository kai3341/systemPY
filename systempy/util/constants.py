from typing import Generic, Protocol

from .enums import TYPE as _TYPE
from .local_typing import DisallowedAttrInfo, LFRegistered, LFTypeConfig

lifecycle_additional_configuration: LFTypeConfig[type] = {}
lifecycle_registered_methods: LFRegistered = {}
lifecycle_bases_blacklist: set[type] = {object, Generic, Protocol}  # type: ignore[arg-type]

sync_or_async = (_TYPE.SYNC, _TYPE.ASYNC)


lifecycle_disallowed_attrs: list[DisallowedAttrInfo] = [
    ("__init__", "Use `on_init` instead"),
    ("__post_init__", "Use `on_init` instead"),
]
