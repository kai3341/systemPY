from typing import Set, Dict, Tuple, Callable, List

from .local_typing import LFTypeConfig, DisallowedAttrInfo
from .local_dataclasses import LFMethodsRegistered


lifecycle_additional_configuration: LFTypeConfig = {}
lifecycle_registered_methods: Dict[Callable, LFMethodsRegistered] = {}
lifecycle_bases_blacklist: Set[type] = set((object,))


sync_or_async: Tuple[str, ...] = (
    "sync",
    "async",
)


lifecycle_disallowed_attrs: List[DisallowedAttrInfo] = [
    ("__init__", "Use `on_init` instead"),
    ("__post_init__", "Use `on_init` instead"),
]
