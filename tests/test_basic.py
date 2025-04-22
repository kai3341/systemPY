from collections.abc import Callable, Coroutine
from functools import wraps
from typing import TypeVar
from unittest import TestCase

T = TypeVar("T")


def _method_sync(
    results: list[str],
    postfix: str,
) -> Callable[[Callable[[T], None]], Callable[[T], None]]:
    def outer(target: Callable[[T], None]) -> Callable[[T], None]:
        result = f"{target.__name__}:{postfix}"

        @wraps(target)
        def inner(self: T) -> None:  # noqa: ARG001
            results.append(result)

        return inner

    return outer


def _method_async(
    results: list[str],
    postfix: str,
) -> Callable[
    [Callable[[T], Coroutine[None, None, None]]],
    Callable[[T], Coroutine[None, None, None]],
]:
    def outer(
        target: Callable[[T], Coroutine[None, None, None]],
    ) -> Callable[[T], Coroutine[None, None, None]]:
        result = f"{target.__name__}:{postfix}"

        @wraps(target)
        async def inner(self: T) -> None:  # noqa: ARG001
            results.append(result)

        return inner

    return outer


class BasicTestCase(TestCase):
    def test_basic(self) -> None:
        from systempy import LoopUnit, ProcessUnit, Target

        on_init_results: list[int] = []
        pre_startup_results: list[int] = []
        on_startup_results: list[int] = []
        on_shutdown_results: list[int] = []
        post_shutdown_results: list[int] = []

        main_async_result: list[str] = []

        class C0(Target, final=False): ...

        # ===

        class C1(Target, final=False):
            def on_init(self) -> None:
                on_init_results.append(1)

            def pre_startup(self) -> None:
                pre_startup_results.append(1)

            def post_shutdown(self) -> None:
                post_shutdown_results.append(1)

        # ===

        class C2(Target, final=False):
            def on_init(self) -> None:
                on_init_results.append(2)

            async def on_startup(self) -> None:
                on_startup_results.append(2)

        # ===

        class C3(Target, final=False):
            async def on_shutdown(self) -> None:
                on_shutdown_results.append(3)

        # ===

        class Result(C0, C1, C2, C3, LoopUnit, ProcessUnit):
            reload_signals = ()

            async def main_async(self) -> None:
                main_async_result.append("result")

        Result.launch()

        self.assertListEqual(on_init_results, [1, 2])
        self.assertListEqual(pre_startup_results, [1])
        self.assertListEqual(on_startup_results, [2])
        self.assertListEqual(on_shutdown_results, [3])
        self.assertListEqual(post_shutdown_results, [1])
        self.assertListEqual(main_async_result, ["result"])

        del Result

    def test_custom_target(self) -> None:  # noqa: C901
        from gc import collect

        from systempy import (
            DIRECTION,
            LoopUnit,
            ProcessUnit,
            register_hook_after,
            register_hook_before,
            register_target,
            register_target_method,
        )
        from systempy.unit.ext.target_ext import TargetExt

        results: list[str] = []

        @register_target
        class ExampleDaemonTarget(TargetExt, final=False):
            @register_hook_before(TargetExt.on_init)
            @register_target_method(DIRECTION.FORWARD)
            def before_on_init(self) -> None: ...

            @register_hook_after(TargetExt.on_init)
            @register_target_method(DIRECTION.FORWARD)
            def after_on_init(self) -> None: ...

            @register_hook_before(TargetExt.pre_startup)
            @register_target_method(DIRECTION.FORWARD)
            def before_pre_startup(self) -> None: ...

            @register_hook_after(TargetExt.pre_startup)
            @register_target_method(DIRECTION.FORWARD)
            def after_pre_startup(self) -> None: ...

            @register_hook_before(TargetExt.post_startup)
            @register_target_method(DIRECTION.FORWARD)
            async def before_post_startup(self) -> None: ...

            @register_hook_after(TargetExt.post_startup)
            @register_target_method(DIRECTION.GATHER)
            async def after_post_startup(self) -> None: ...

            @register_hook_before(TargetExt.pre_shutdown)
            @register_target_method(DIRECTION.GATHER)
            async def before_pre_shutdown(self) -> None: ...

            @register_hook_after(TargetExt.post_shutdown)
            @register_target_method(DIRECTION.BACKWARD)
            def after_post_shutdown(self) -> None: ...

            @register_hook_after(TargetExt.post_shutdown)
            @register_target_method(DIRECTION.BACKWARD)
            def also_after_post_shutdown(self) -> None: ...

            @register_hook_after(also_after_post_shutdown)
            @register_target_method(DIRECTION.BACKWARD)
            def after_also_after_post_shutdown(self) -> None: ...

        _gather = _method_async(results, "*")

        _sync_1 = _method_sync(results, "1")
        _async_1 = _method_async(results, "1")

        class ExampleDaemonUnit1(ExampleDaemonTarget, final=False):
            @_sync_1
            def before_on_init(self) -> None: ...

            @_sync_1
            def on_init(self) -> None: ...

            @_sync_1
            def after_on_init(self) -> None: ...

            @_sync_1
            def before_pre_startup(self) -> None: ...

            @_sync_1
            def pre_startup(self) -> None: ...

            @_sync_1
            def after_pre_startup(self) -> None: ...

            @_async_1
            async def on_startup(self) -> None: ...

            @_async_1
            async def post_startup(self) -> None: ...

            @_async_1
            async def before_post_startup(self) -> None: ...

            @_gather
            async def after_post_startup(self) -> None: ...

            @_gather
            async def before_pre_shutdown(self) -> None: ...

            @_async_1
            async def pre_shutdown(self) -> None: ...

            @_async_1
            async def on_shutdown(self) -> None: ...

            @_sync_1
            def post_shutdown(self) -> None: ...

            @_sync_1
            def after_post_shutdown(self) -> None: ...

            @_sync_1
            def also_after_post_shutdown(self) -> None: ...

            @_sync_1
            def after_also_after_post_shutdown(self) -> None: ...

        _sync_2 = _method_sync(results, "2")
        _async_2 = _method_async(results, "2")

        class ExampleDaemonUnit2(ExampleDaemonTarget, final=False):
            @_sync_2
            def before_on_init(self) -> None: ...

            @_sync_2
            def on_init(self) -> None: ...

            @_sync_2
            def after_on_init(self) -> None: ...

            @_sync_2
            def before_pre_startup(self) -> None: ...

            @_sync_2
            def pre_startup(self) -> None: ...

            @_sync_2
            def after_pre_startup(self) -> None: ...

            @_async_2
            async def on_startup(self) -> None: ...

            @_async_2
            async def post_startup(self) -> None: ...

            @_async_2
            async def before_post_startup(self) -> None: ...

            @_gather
            async def after_post_startup(self) -> None: ...

            @_gather
            async def before_pre_shutdown(self) -> None: ...

            @_async_2
            async def pre_shutdown(self) -> None: ...

            @_async_2
            async def on_shutdown(self) -> None: ...

            @_sync_2
            def post_shutdown(self) -> None: ...

            @_sync_2
            def after_post_shutdown(self) -> None: ...

            @_sync_2
            def also_after_post_shutdown(self) -> None: ...

            @_sync_2
            def after_also_after_post_shutdown(self) -> None: ...

        _sync_3 = _method_sync(results, "3")
        _async_3 = _method_async(results, "3")

        class ExampleDaemonUnit3(ExampleDaemonTarget, final=False):
            @_sync_3
            def before_on_init(self) -> None: ...

            @_sync_3
            def on_init(self) -> None: ...

            @_sync_3
            def after_on_init(self) -> None: ...

            @_sync_3
            def before_pre_startup(self) -> None: ...

            @_sync_3
            def pre_startup(self) -> None: ...

            @_sync_3
            def after_pre_startup(self) -> None: ...

            @_async_3
            async def on_startup(self) -> None: ...

            @_async_3
            async def post_startup(self) -> None: ...

            @_async_3
            async def before_post_startup(self) -> None: ...

            @_gather
            async def after_post_startup(self) -> None: ...

            @_gather
            async def before_pre_shutdown(self) -> None: ...

            @_async_3
            async def pre_shutdown(self) -> None: ...

            @_async_3
            async def on_shutdown(self) -> None: ...

            @_sync_3
            def post_shutdown(self) -> None: ...

            @_sync_3
            def after_post_shutdown(self) -> None: ...

            @_sync_3
            def also_after_post_shutdown(self) -> None: ...

            @_sync_3
            def after_also_after_post_shutdown(self) -> None: ...

        class ExampleDaemon(
            ExampleDaemonUnit1,
            ExampleDaemonUnit2,
            ExampleDaemonUnit3,
            LoopUnit,
            ProcessUnit,
        ):
            reload_signals = ()

            async def main_async(self) -> None:
                results.append("main_async")

        collect()  # Make sure we didn't leave any object without refs

        ExampleDaemon.launch()

        expected_result = [
            "before_on_init:1",
            "before_on_init:2",
            "before_on_init:3",
            "on_init:1",
            "on_init:2",
            "on_init:3",
            "after_on_init:1",
            "after_on_init:2",
            "after_on_init:3",
            "before_pre_startup:1",
            "before_pre_startup:2",
            "before_pre_startup:3",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "after_pre_startup:1",
            "after_pre_startup:2",
            "after_pre_startup:3",
            "on_startup:1",
            "on_startup:2",
            "on_startup:3",
            "before_post_startup:1",
            "before_post_startup:2",
            "before_post_startup:3",
            "post_startup:1",
            "post_startup:2",
            "post_startup:3",
            "after_post_startup:*",
            "after_post_startup:*",
            "after_post_startup:*",
            "main_async",
            "before_pre_shutdown:*",
            "before_pre_shutdown:*",
            "before_pre_shutdown:*",
            "pre_shutdown:3",
            "pre_shutdown:2",
            "pre_shutdown:1",
            "on_shutdown:3",
            "on_shutdown:2",
            "on_shutdown:1",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
            "after_post_shutdown:3",
            "after_post_shutdown:2",
            "after_post_shutdown:1",
            "also_after_post_shutdown:3",
            "also_after_post_shutdown:2",
            "also_after_post_shutdown:1",
            "after_also_after_post_shutdown:3",
            "after_also_after_post_shutdown:2",
            "after_also_after_post_shutdown:1",
        ]

        self.assertListEqual(results, expected_result, "lifecycle method order")

        self.assertEqual(
            ExampleDaemon.on_init.__qualname__,
            "Sync[on_init]("
            "ExampleDaemonUnit1.before_on_init;"
            "ExampleDaemonUnit2.before_on_init;"
            "ExampleDaemonUnit3.before_on_init;"
            "ExampleDaemonUnit1.on_init;"
            "ExampleDaemonUnit2.on_init;"
            "ExampleDaemonUnit3.on_init;"
            "DaemonUnitBase.on_init;"
            "ExampleDaemonUnit1.after_on_init;"
            "ExampleDaemonUnit2.after_on_init;"
            "ExampleDaemonUnit3.after_on_init)",
        )

        self.assertEqual(
            ExampleDaemon.before_on_init.__qualname__,
            "Sync[before_on_init]("
            "ExampleDaemonUnit1.before_on_init;"
            "ExampleDaemonUnit2.before_on_init;"
            "ExampleDaemonUnit3.before_on_init)",
        )

    def test_memory_leak(self) -> None:
        from gc import collect

        from systempy.util.register import (
            mark_as_final,
            mark_as_target,
            register_hook_after,
            register_hook_before,
        )

        # create many objects
        for _ in range(20):
            self.test_custom_target()

        collect()

        self.assertEqual(len(mark_as_final.regisrty), 0)

        marked_as_target = {
            "TargetExt",
            "Unit",
            "Target",
            "Generic",
            "DaemonTargetABC",
            "ProcessUnit",
            "_TargetFieldIter",
            "DaemonUnit",
            "object",
            "Protocol",
            "_TargetInit",
            "TargetInterface",
            "ProcessTargetABC",
            "_TargetCtxMgrAsync",
            "_TargetCtxMgrSync",
        }

        self.assertSetEqual(
            {c.__name__ for c in mark_as_target.regisrty},
            marked_as_target,
        )

        hook_parents_names = {
            fk.__qualname__: fv.__qualname__
            for fk, fv in register_hook_after.hook_parents.items()
        }

        hook_parents_names__expected = {
            "TargetExt.post_startup": "TargetInterface.on_startup",
            "TargetExt.pre_shutdown": "TargetInterface.on_shutdown",
        }

        self.assertDictEqual(hook_parents_names, hook_parents_names__expected)

        hook_names_after = {
            cb.__qualname__
            for cb in register_hook_after._registry  # noqa: SLF001
        }

        hook_names_after__expected = {
            "TargetInterface.on_init",
            "TargetInterface.on_startup",
            "TargetInterface.pre_startup",
            "TargetExt.post_startup",
            "TargetInterface.post_shutdown",
        }

        self.assertSetEqual(hook_names_after, hook_names_after__expected)

        hook_names_before = {
            cb.__qualname__
            for cb in register_hook_before._registry  # noqa: SLF001
        }

        hook_names_before__expected = {
            "TargetInterface.on_shutdown",
            "TargetInterface.on_init",
            "TargetExt.post_startup",
            "TargetInterface.pre_startup",
            "TargetExt.pre_shutdown",
        }

        self.assertSetEqual(hook_names_before, hook_names_before__expected)
