from typing import Set, Dict, Tuple, Callable

from .local_typing import (
    LFTypeConfig,
    # LFHookRegistry,
)

from .local_dataclasses import LFMethodsRegistered

lifecycle_additional_configuration: LFTypeConfig = {}

lifecycle_registered_methods: Dict[Callable, LFMethodsRegistered] = {}

# lifecycle_hooks_parents: Dict[Callable, Callable] = {}
# lifecycle_hooks_before: LFHookRegistry = {}
# lifecycle_hooks_after: LFHookRegistry = {}


sync_or_async: Tuple[str, ...] = (
    "sync",
    "async",
)


lifecycle_disallowed_attrs = [
    ("__init__", "Use `on_init` instead"),
    ("__post_init__", "Use `on_init` instead"),
]

lifecycle_bases_blacklist: Set = set((object,))
