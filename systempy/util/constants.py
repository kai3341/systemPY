from typing import Any

from .enums import TYPE as _TYPE
from .local_typing import DisallowedAttrInfo, LFRegistered, LFTypeConfig

lifecycle_additional_configuration: LFTypeConfig[type] = {}
lifecycle_registered_methods: LFRegistered = {}

sync_or_async = (_TYPE.SYNC, _TYPE.ASYNC)


init_on_not_final_class_error = (
    "Caught attempt to instantiate class {cls} marked `final=False`"
)


def _init_on_not_final_classes(self: object, *_args: Any, **_kwargs: Any) -> None:
    raise TypeError(init_on_not_final_class_error.format(cls=type(self)))


lifecycle_disallowed_attrs: list[DisallowedAttrInfo] = [
    ("__init__", "Use `on_init` instead", ({_init_on_not_final_classes}).__contains__),
    ("__post_init__", "Use `on_init` instead", lambda _: False),
]
