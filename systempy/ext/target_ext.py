from ..target import Target
from .. import util


@util.register_target
class TargetExt(Target):
    @util.register_hook_after(Target.on_startup)
    @util.register_target_method("forward")
    async def post_startup(self) -> None:
        ...

    @util.register_hook_before(Target.on_shutdown)
    @util.register_target_method("backward")
    async def pre_shutdown(self) -> None:
        ...
