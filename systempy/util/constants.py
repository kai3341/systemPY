from typing import Set, Dict, Tuple
from .dataclasses import LFMethodsRegistered
from .typing import (
    LFMethod,
    LFTypeConfig,
    DirectionHandler,
    TargetTypeHandler,
    CheckHandler,
    # TargetType,
)

lifecycle_additional_configuration: LFTypeConfig = {}

lifecycle_registered_methods: Dict[LFMethod, LFMethodsRegistered] = {}
apply_additional_config__cfg: Dict[str, LFMethod] = {}

# FIXME!!!!
lifecycle_hooks_parents: Dict[str, None] = {}
lifecycle_hooks_before: Dict[str, None] = {}
lifecycle_hooks_after: Dict[str, None] = {}

handler_by_iscoroutinefunction: Dict[str, TargetTypeHandler] = {}
handler_by_direction: Dict[str, DirectionHandler] = {}
on_register_check_method_type: Dict[str, CheckHandler] = {}

sync_or_async: Tuple[str, ...] = (
    "sync",
    "async",
)

# sync_or_async = TargetType.__args__
# "object" has no attribute "__args__"


lifecycle_disallowed_attrs = [
    ("__init__", "Use `on_init` instead"),
]

lifecycle_bases_blacklist: Set = set((object,))
