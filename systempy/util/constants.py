from typing import Set, Dict, Tuple
from .typing import (
    LFMethod,
    # LFMethodT,
    LFTypeConfig,
    DirectionHandler,
    TargetTypeHandler,
    CheckHandler,
    LFHookRegistry,
    AddCFG,
    AnyHashable,
    # TargetType,
)

from .dataclasses import LFMethodsRegistered

lifecycle_additional_configuration: LFTypeConfig = {}

lifecycle_registered_methods: Dict[LFMethod, LFMethodsRegistered] = {}
apply_additional_config__cfg: Dict[AnyHashable, AddCFG] = {}

lifecycle_hooks_parents: Dict[LFMethod, LFMethod] = {}
lifecycle_hooks_before: LFHookRegistry = {}
lifecycle_hooks_after: LFHookRegistry = {}

handler_by_iscoroutinefunction: Dict[AnyHashable, TargetTypeHandler] = {}
handler_by_direction: Dict[AnyHashable, DirectionHandler] = {}
on_register_check_method_type: Dict[AnyHashable, CheckHandler] = {}

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
