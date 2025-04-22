from weakref import WeakKeyDictionary

from .enums import TYPE as _TYPE
from .local_typing import DisallowedAttrInfo, LFMetadata, LFRegistered, LFTypeConfig

lifecycle_additional_configuration: LFTypeConfig[type] = WeakKeyDictionary()
lifecycle_registered_methods: LFRegistered = WeakKeyDictionary()

sync_or_async = (_TYPE.SYNC, _TYPE.ASYNC)
handler_metadata: LFMetadata = WeakKeyDictionary()


lifecycle_disallowed_attrs: list[DisallowedAttrInfo] = [
    ("__init__", "Use `on_init` instead"),
    ("__post_init__", "Use `on_init` instead"),
]
