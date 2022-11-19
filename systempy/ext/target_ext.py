from ..target import Target
from ..util import (
    register_target,
    register_hook_after,
    register_hook_before,
    register_target_method,
)

from mypy_extensions import trait


@register_target
@trait
class TargetExt(Target):
    @register_hook_after(Target.on_startup)
    @register_target_method("forward")
    async def post_startup(self) -> None:
        pass

    @register_hook_before(Target.on_shutdown)
    @register_target_method("backward")
    async def pre_shutdown(self) -> None:
        pass
