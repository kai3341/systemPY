from .typing import LFTypeConfig

lifecycle_additional_configuration: LFTypeConfig = {}

lifecycle_registered_methods = {}
apply_additional_config__cfg = {}

lifecycle_hooks_parents = {}
lifecycle_hooks_before = {}
handler_by_iscoroutinefunction = {}
lifecycle_hooks_after = {}
handler_by_direction = {}
on_register_check_method_type = {}

sync_or_async = (
    "sync",
    "async",
)

lifecycle_disallowed_attrs = [
    ("__init__", "Use `on_init` instead"),
]

lifecycle_bases_blacklist = set((object,))
