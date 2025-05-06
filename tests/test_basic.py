from os import environ
from typing import TypeVar
from unittest import TestCase, skip, skipIf

T = TypeVar("T")


class BasicTestCase(TestCase):
    def test_custom_target(self) -> None:  # noqa: C901
        from gc import collect

        from _cbutil import _method_async, _method_sync

        from systempy import (
            DIRECTION,
            LoopUnit,
            register_hook_after,
            register_hook_before,
        )
        from systempy.unit.ext.target_ext import ExtTarget

        results: list[str] = []
        results_append = results.append

        class ExampleDaemonTarget(ExtTarget):
            @register_hook_before(ExtTarget.on_init, DIRECTION.FORWARD)
            def before_on_init(self) -> None: ...

            @register_hook_after(ExtTarget.on_init, DIRECTION.FORWARD)
            def after_on_init(self) -> None: ...

            @register_hook_before(ExtTarget.pre_startup, DIRECTION.FORWARD)
            def before_pre_startup(self) -> None: ...

            @register_hook_after(ExtTarget.pre_startup, DIRECTION.FORWARD)
            def after_pre_startup(self) -> None: ...

            @register_hook_before(ExtTarget.post_startup, DIRECTION.FORWARD)
            async def before_post_startup(self) -> None: ...

            @register_hook_after(ExtTarget.post_startup, DIRECTION.GATHER)
            async def after_post_startup(self) -> None: ...

            @register_hook_before(ExtTarget.pre_shutdown, DIRECTION.GATHER)
            async def before_pre_shutdown(self) -> None: ...

            @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
            def after_post_shutdown(self) -> None: ...

            @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
            def also_after_post_shutdown(self) -> None: ...

            @register_hook_after(also_after_post_shutdown, DIRECTION.BACKWARD)
            def after_also_after_post_shutdown(self) -> None: ...

        _gather = _method_async(results_append, "*")

        _sync_1 = _method_sync(results_append, "1")
        _async_1 = _method_async(results_append, "1")

        class ExampleDaemon1Unit(ExampleDaemonTarget):
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

        _sync_2 = _method_sync(results_append, "2")
        _async_2 = _method_async(results_append, "2")

        class ExampleDaemon2Unit(ExampleDaemonTarget):
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

        _sync_3 = _method_sync(results_append, "3")
        _async_3 = _method_async(results_append, "3")

        class ExampleDaemon3Unit(ExampleDaemonTarget):
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

        class ExampleDaemonApp(
            ExampleDaemon1Unit,
            ExampleDaemon2Unit,
            ExampleDaemon3Unit,
            LoopUnit,
        ):
            reload_signals = ()

            async def main_async(self) -> None:
                results_append("main_async")

        collect()  # Make sure we didn't leave any object without refs

        ExampleDaemonApp.launch()

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
            ExampleDaemonApp.on_init.__qualname__,
            "Sync[on_init]("
            "ExampleDaemon1Unit.before_on_init;"
            "ExampleDaemon2Unit.before_on_init;"
            "ExampleDaemon3Unit.before_on_init;"
            "ExampleDaemon1Unit.on_init;"
            "ExampleDaemon2Unit.on_init;"
            "ExampleDaemon3Unit.on_init;"
            "_BaseDaemonUnitABC.on_init;"
            "ExampleDaemon1Unit.after_on_init;"
            "ExampleDaemon2Unit.after_on_init;"
            "ExampleDaemon3Unit.after_on_init)",
        )

        self.assertEqual(
            ExampleDaemonApp.before_on_init.__qualname__,
            "Sync[before_on_init]("
            "ExampleDaemon1Unit.before_on_init;"
            "ExampleDaemon2Unit.before_on_init;"
            "ExampleDaemon3Unit.before_on_init)",
        )

    @skip("not ready")
    def test_custom_target_wrong_inheritence(self) -> None:  # noqa: C901
        from gc import collect

        from _cbutil import _method_async, _method_sync

        from systempy import (
            DIRECTION,
            LoopUnit,
            Target,
            register_hook_after,
            register_hook_before,
        )
        from systempy.unit.ext.target_ext import ExtTarget

        results: list[str] = []
        results_append = results.append

        class ExampleDaemonTarget(Target):
            @register_hook_before(ExtTarget.on_init, DIRECTION.FORWARD)
            def before_on_init(self) -> None: ...

            @register_hook_after(ExtTarget.on_init, DIRECTION.FORWARD)
            def after_on_init(self) -> None: ...

            @register_hook_before(ExtTarget.pre_startup, DIRECTION.FORWARD)
            def before_pre_startup(self) -> None: ...

            @register_hook_after(ExtTarget.pre_startup, DIRECTION.FORWARD)
            def after_pre_startup(self) -> None: ...

            @register_hook_before(ExtTarget.post_startup, DIRECTION.FORWARD)
            async def before_post_startup(self) -> None: ...

            @register_hook_after(ExtTarget.post_startup, DIRECTION.GATHER)
            async def after_post_startup(self) -> None: ...

            @register_hook_before(ExtTarget.pre_shutdown, DIRECTION.GATHER)
            async def before_pre_shutdown(self) -> None: ...

            @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
            def after_post_shutdown(self) -> None: ...

            @register_hook_after(ExtTarget.post_shutdown, DIRECTION.BACKWARD)
            def also_after_post_shutdown(self) -> None: ...

            @register_hook_after(also_after_post_shutdown, DIRECTION.BACKWARD)
            def after_also_after_post_shutdown(self) -> None: ...

        _gather = _method_async(results_append, "*")

        _sync_1 = _method_sync(results_append, "1")
        _async_1 = _method_async(results_append, "1")

        class ExampleDaemon1Unit(ExampleDaemonTarget):
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

        _sync_2 = _method_sync(results_append, "2")
        _async_2 = _method_async(results_append, "2")

        class ExampleDaemon2Unit(ExampleDaemonTarget):
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

        _sync_3 = _method_sync(results_append, "3")
        _async_3 = _method_async(results_append, "3")

        class ExampleDaemon3Unit(ExampleDaemonTarget):
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

        class ExampleDaemonApp(
            ExampleDaemon1Unit,
            ExampleDaemon2Unit,
            ExampleDaemon3Unit,
            LoopUnit,
        ):
            reload_signals = ()

            async def main_async(self) -> None:
                results_append("main_async")

        collect()  # Make sure we didn't leave any object without refs

        ExampleDaemonApp.launch()

        print(results)

    def test_async_stop_reload(self) -> None:  # noqa: C901
        from threading import Thread
        from time import sleep

        from _cbutil import _method_async, _method_sync

        from systempy import EventWaitUnit, Target

        results: list[str] = []
        results_append = results.append

        _sync_1 = _method_sync(results_append, "1")
        _async_1 = _method_async(results_append, "1")

        class ExampleDaemon1Unit(Target):
            @_sync_1
            def on_init(self) -> None: ...

            @_sync_1
            def pre_startup(self) -> None: ...

            @_async_1
            async def on_startup(self) -> None: ...

            @_async_1
            async def on_shutdown(self) -> None: ...

            @_sync_1
            def post_shutdown(self) -> None: ...

        _sync_2 = _method_sync(results_append, "2")
        _async_2 = _method_async(results_append, "2")

        class ExampleDaemon2Unit(Target):
            @_sync_2
            def on_init(self) -> None: ...

            @_sync_2
            def pre_startup(self) -> None: ...

            @_async_2
            async def on_startup(self) -> None: ...

            @_async_2
            async def on_shutdown(self) -> None: ...

            @_sync_2
            def post_shutdown(self) -> None: ...

        _sync_3 = _method_sync(results_append, "3")
        _async_3 = _method_async(results_append, "3")

        class ExampleDaemon3Unit(Target):
            @_sync_3
            def on_init(self) -> None: ...

            @_sync_3
            def pre_startup(self) -> None: ...

            @_async_3
            async def on_startup(self) -> None: ...

            @_async_3
            async def on_shutdown(self) -> None: ...

            @_sync_3
            def post_shutdown(self) -> None: ...

        class ExampleApp(
            ExampleDaemon1Unit,
            ExampleDaemon2Unit,
            ExampleDaemon3Unit,
            EventWaitUnit,
        ):
            async def main_async(self) -> None:
                results_append("main_async")
                return await super().main_async()

        unit = ExampleApp()

        thread = Thread(target=unit.run_sync)
        thread.start()
        thread_id = thread.ident
        assert thread_id
        sleep(0.2)
        unit.reload()
        sleep(0.2)
        unit.reload()
        sleep(0.2)
        unit.stop()
        thread.join(1)

        unit.remove_signal_handlers()

        self.assertEqual(thread.is_alive(), False)

        expected_result = [
            "on_init:1",
            "on_init:2",
            "on_init:3",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "on_startup:1",
            "on_startup:2",
            "on_startup:3",
            "main_async",
            "on_shutdown:3",
            "on_shutdown:2",
            "on_shutdown:1",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "on_startup:1",
            "on_startup:2",
            "on_startup:3",
            "main_async",
            "on_shutdown:3",
            "on_shutdown:2",
            "on_shutdown:1",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "on_startup:1",
            "on_startup:2",
            "on_startup:3",
            "main_async",
            "on_shutdown:3",
            "on_shutdown:2",
            "on_shutdown:1",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
        ]

        self.assertListEqual(results, expected_result, "lifecycle method order")

    def test_sync_stop_reload(self) -> None:  # noqa: C901
        from threading import Thread
        from time import sleep

        from _cbutil import _method_sync

        from systempy import DaemonUnit, Target

        results: list[str] = []
        results_append = results.append

        _sync_1 = _method_sync(results_append, "1")

        class ExampleDaemon1Unit(Target):
            @_sync_1
            def on_init(self) -> None: ...

            @_sync_1
            def pre_startup(self) -> None: ...

            @_sync_1
            def post_shutdown(self) -> None: ...

        _sync_2 = _method_sync(results_append, "2")

        class ExampleDaemon2Unit(Target):
            @_sync_2
            def on_init(self) -> None: ...

            @_sync_2
            def pre_startup(self) -> None: ...

            @_sync_2
            def post_shutdown(self) -> None: ...

        _sync_3 = _method_sync(results_append, "3")

        class ExampleDaemon3Unit(Target):
            @_sync_3
            def on_init(self) -> None: ...

            @_sync_3
            def pre_startup(self) -> None: ...

            @_sync_3
            def post_shutdown(self) -> None: ...

        class ExampleDaemonApp(
            ExampleDaemon1Unit,
            ExampleDaemon2Unit,
            ExampleDaemon3Unit,
            DaemonUnit,
        ):
            def main_sync(self) -> None:
                results_append("main_sync")
                while True:
                    sleep(0.05)

        unit = ExampleDaemonApp()

        thread = Thread(target=unit.run_sync)
        thread.start()
        thread_id = thread.ident
        assert thread_id
        sleep(0.1)
        unit.reload()

        sleep(0.2)
        unit.reload()
        sleep(0.2)
        unit.stop()
        thread.join(1)

        unit.remove_signal_handlers()

        self.assertEqual(thread.is_alive(), False)

        results_expected = [
            "on_init:1",
            "on_init:2",
            "on_init:3",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "main_sync",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "main_sync",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "main_sync",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
        ]

        self.assertListEqual(results, results_expected)

    def test_target_from_scratch(self) -> None: ...

    @skipIf(
        "MEMORE_LEAK_ROUNDS" not in environ,
        "Variable `MEMORE_LEAK_ROUNDS` is not defined",
    )
    def test_zzz_memory_leak(self) -> None:
        from gc import collect

        from systempy.libsystempy.register import (
            mark_as_final,
            mark_as_target,
            register_hook_after,
            register_hook_before,
        )

        # create many objects
        for _ in range(int(environ["MEMORE_LEAK_ROUNDS"])):
            self.test_custom_target()

        collect()

        self.assertEqual(len(mark_as_final.regisrty), 0)

        marked_as_target = {
            "Protocol",
            "DaemonUnit",
            "ExtTarget",
            "SyncMixinABC",
            "Target",
            "_FieldIterMixin",
            "object",
            "AsyncMixinABC",
            "_InitMixin",
            "InterfaceTarget",
            "ReplLocalsMixin",
            "Unit",
            "LoopUnit",
            "Generic",
            "ScriptUnit",
            "AsyncScriptUnit",
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
            "ExtTarget.post_startup": "InterfaceTarget.on_startup",
            "ExtTarget.pre_shutdown": "InterfaceTarget.on_shutdown",
        }

        self.assertDictEqual(hook_parents_names, hook_parents_names__expected)

        hook_names_after = {
            cb.__qualname__
            for cb in register_hook_after._registry  # noqa: SLF001
        }

        hook_names_after__expected = {
            "InterfaceTarget.on_init",
            "InterfaceTarget.on_startup",
            "InterfaceTarget.pre_startup",
            "ExtTarget.post_startup",
            "InterfaceTarget.post_shutdown",
        }

        self.assertSetEqual(hook_names_after, hook_names_after__expected)

        hook_names_before = {
            cb.__qualname__
            for cb in register_hook_before._registry  # noqa: SLF001
        }

        hook_names_before__expected = {
            "InterfaceTarget.on_shutdown",
            "InterfaceTarget.on_init",
            "ExtTarget.post_startup",
            "InterfaceTarget.pre_startup",
            "ExtTarget.pre_shutdown",
        }

        self.assertSetEqual(hook_names_before, hook_names_before__expected)
