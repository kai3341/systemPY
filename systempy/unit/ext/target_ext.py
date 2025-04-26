from systempy import (
    DIRECTION,
    Target,
    register_hook_after,
    register_hook_before,
    register_target_method,
)


class ExtTarget(Target):
    @register_hook_after(Target.on_startup)
    @register_target_method(DIRECTION.FORWARD)
    async def post_startup(self) -> None: ...

    @register_hook_before(Target.on_shutdown)
    @register_target_method(DIRECTION.BACKWARD)
    async def pre_shutdown(self) -> None: ...
