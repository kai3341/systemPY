# Custom target example

You may need extra lifecycle stages. You may extend existing stages with your own

=== "naming"

    Here `TargetMeta` relies on class name, so it's important to make class name
    `str.endswith(("Target", "TargetABC"))`

    ```python
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
    ```

=== "`role` kwarg"

    Here `TargetMeta` relies on explicit `role` kwarg and doesn't check class
    name, so you may give your class arbitrary name

    ```python
    from systempy import (
        DIRECTION,
        ROLE,
        Target,
        register_hook_after,
        register_hook_before,
    )

    class ExtTarget(Target, role=ROLE.TARGET):
        @register_hook_after(Target.on_startup, DIRECTION.FORWARD)
        async def post_startup(self) -> None: ...

        @register_hook_before(Target.on_shutdown, DIRECTION.BACKWARD)
        async def pre_shutdown(self) -> None: ...
    ```
