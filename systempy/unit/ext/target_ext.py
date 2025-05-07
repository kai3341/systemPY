from systempy import (
    DIRECTION,
    Target,
    register_hook_after,
    register_hook_before,
)


class ExtTarget(Target):
    @register_hook_after(Target.on_startup, DIRECTION.FORWARD)
    async def post_startup(self) -> None: ...

    @register_hook_before(Target.on_shutdown, DIRECTION.BACKWARD)
    async def pre_shutdown(self) -> None: ...
