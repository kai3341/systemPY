from typing import Set, Dict, Tuple, Hashable
from .dataclasses import LFMethodsRegistered
from .typing import (
    LFMethod,
    # LFMethodT,
    LFTypeConfig,
    DirectionHandler,
    TargetTypeHandler,
    CheckHandler,
    LFHookRegistry,
    AddCFG,
    # TargetType,
)

lifecycle_additional_configuration: LFTypeConfig = {}

lifecycle_registered_methods: Dict[LFMethod, LFMethodsRegistered] = {}
apply_additional_config__cfg: Dict[Hashable, AddCFG] = {}

lifecycle_hooks_parents: Dict[LFMethod, LFMethod] = {}
lifecycle_hooks_before: LFHookRegistry = {}
lifecycle_hooks_after: LFHookRegistry = {}

handler_by_iscoroutinefunction: Dict[Hashable, TargetTypeHandler] = {}
handler_by_direction: Dict[Hashable, DirectionHandler] = {}
on_register_check_method_type: Dict[Hashable, CheckHandler] = {}

sync_or_async: Tuple[str, str] = (
    "sync",
    "async",
)

# sync_or_async = TargetType.__args__
# "object" has no attribute "__args__"


lifecycle_disallowed_attrs = [
    ("__init__", "Use `on_init` instead"),
    ("__post_init__", "Use `on_init` instead"),
]

lifecycle_bases_blacklist: Set = set((object,))
