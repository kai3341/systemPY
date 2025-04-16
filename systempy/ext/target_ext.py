from ..target import Target
from ..util import (
    CONST,
    register_hook_after,
    register_hook_before,
    register_target,
    register_target_method,
)


@register_target
class TargetExt(Target, final=False):
    @register_hook_after(Target.on_startup)
    @register_target_method(CONST.FORWARD)
    async def post_startup(self) -> None:
        pass

    @register_hook_before(Target.on_shutdown)
    @register_target_method(CONST.BACKWARD)
    async def pre_shutdown(self) -> None:
        pass
