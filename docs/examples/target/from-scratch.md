# Creating own Target from scratch

You may deside you need more (or less) startup and shutdown stages and they
doesn't match target, provided by systempy. It's time to define your own:

=== "naming"

    Here `TargetMeta` relies on class name, so it's important to make class name
    `str.endswith(("Target", "TargetABC"))`

    ```python
    from systempy import DIRECTION, TargetMeta, register_target_method

    class MySpecialTarget(metaclass=TargetMeta):
        @register_target_method(DIRECTION.FORWARD)
        def first_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        def second_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        def third_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        def fourth_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        async def fifth_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.GATHER)
        async def sixth_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.GATHER)
        async def seventh_startup_stage(self) -> None: ...

        # ===

        @register_target_method(DIRECTION.GATHER)
        async def first_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.GATHER)
        async def second_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        async def third_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def fourth_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def fifth_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def sixth_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def seventh_shutdown_stage(self) -> None: ...
    ```

=== "`role` kwarg"

    Here `TargetMeta` relies on explicit `role` kwarg and doesn't check class
    name, so you may give your class arbitrary name

    ```python
    from systempy import DIRECTION, ROLE, TargetMeta, register_target_method

    class MySpecialTarget(metaclass=TargetMeta, role=ROLE.TARGET):
        @register_target_method(DIRECTION.FORWARD)
        def first_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        def second_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        def third_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        def fourth_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.FORWARD)
        async def fifth_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.GATHER)
        async def sixth_startup_stage(self) -> None: ...

        @register_target_method(DIRECTION.GATHER)
        async def seventh_startup_stage(self) -> None: ...

        # ===

        @register_target_method(DIRECTION.GATHER)
        async def first_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.GATHER)
        async def second_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        async def third_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def fourth_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def fifth_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def sixth_shutdown_stage(self) -> None: ...

        @register_target_method(DIRECTION.BACKWARD)
        def seventh_shutdown_stage(self) -> None: ...
    ```

Here it's completely your business, how and why does these stages happens. You
may create stages, which will be executed only when any event is happened, but
not on init or shutdown
