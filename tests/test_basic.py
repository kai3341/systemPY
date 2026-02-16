from os import environ
from typing import TypeVar
from unittest import TestCase, skipIf

T = TypeVar("T")


class BasicTestCase(TestCase):
    def test_custom_target(self) -> None:
        from _util._cbutil import _method_async, _method_sync
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

    def test_custom_target_wrong_inheritence(self) -> None:
        from _util._cbutil import _method_async, _method_sync
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

        class ExampleDaemon2Unit(Target):
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

        class ExampleDaemonApp(
            ExampleDaemon1Unit,
            ExampleDaemon2Unit,
            LoopUnit,
        ):
            reload_signals = ()

            async def main_async(self) -> None:
                results_append("main_async")

        ExampleDaemonApp.launch()

        expected_result = [
            "before_on_init:1",
            "on_init:1",
            "on_init:2",
            "after_on_init:1",
            "before_pre_startup:1",
            "pre_startup:1",
            "pre_startup:2",
            "after_pre_startup:1",
            "on_startup:1",
            "on_startup:2",
            "main_async",
            "on_shutdown:2",
            "on_shutdown:1",
            "post_shutdown:2",
            "post_shutdown:1",
            "after_post_shutdown:1",
            "also_after_post_shutdown:1",
            "after_also_after_post_shutdown:1",
        ]

        self.assertListEqual(
            results,
            expected_result,
            "some ExampleDaemon2Unit methods have to be skipped",
        )

    def test_async_stop_reload(self) -> None:
        from threading import Thread
        from time import sleep

        from _util._cbutil import _method_async, _method_sync
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

    def test_sync_stop_reload(self) -> None:
        from threading import Thread
        from time import sleep

        from _util._cbutil import _method_sync
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

    def test_sync_script(self) -> None:
        from _util._cbutil import _method_sync
        from systempy import ScriptUnit, Target

        results: list[str] = []
        results_append = results.append

        _sync_1 = _method_sync(results_append, "1")

        class Example1Unit(Target):
            @_sync_1
            def on_init(self) -> None: ...

            @_sync_1
            def pre_startup(self) -> None: ...

            @_sync_1
            def post_shutdown(self) -> None: ...

        _sync_2 = _method_sync(results_append, "2")

        class Example2Unit(Target):
            @_sync_2
            def on_init(self) -> None: ...

            @_sync_2
            def pre_startup(self) -> None: ...

            @_sync_2
            def post_shutdown(self) -> None: ...

        _sync_3 = _method_sync(results_append, "3")

        class Example3Unit(Target):
            @_sync_3
            def on_init(self) -> None: ...

            @_sync_3
            def pre_startup(self) -> None: ...

            @_sync_3
            def post_shutdown(self) -> None: ...

        class ExampleScriptApp(
            Example1Unit,
            Example2Unit,
            Example3Unit,
            ScriptUnit,
        ):
            def main_sync(self) -> None:
                results_append("main_sync")

        ExampleScriptApp.launch()

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
        ]

        self.assertListEqual(results_expected, results)

    def test_sync_script_app_subclassing(self) -> None:
        from _util._cbutil import _method_sync
        from systempy import ScriptUnit, Target

        results: list[str] = []
        results_append = results.append

        _sync_1 = _method_sync(results_append, "1")

        class Example1Unit(Target):
            @_sync_1
            def on_init(self) -> None: ...

            @_sync_1
            def pre_startup(self) -> None: ...

            @_sync_1
            def post_shutdown(self) -> None: ...

        _sync_2 = _method_sync(results_append, "2")

        class Example2Unit(Target):
            @_sync_2
            def on_init(self) -> None: ...

            @_sync_2
            def pre_startup(self) -> None: ...

            @_sync_2
            def post_shutdown(self) -> None: ...

        _sync_3 = _method_sync(results_append, "3")

        class Example3Unit(Target):
            @_sync_3
            def on_init(self) -> None: ...

            @_sync_3
            def pre_startup(self) -> None: ...

            @_sync_3
            def post_shutdown(self) -> None: ...

        _sync_4 = _method_sync(results_append, "4")

        class ExampleScript4App(
            Example1Unit,
            Example2Unit,
            Example3Unit,
            ScriptUnit,
        ):
            def main_sync(self) -> None:
                results_append("main_sync")

            @_sync_4
            def on_init(self) -> None: ...

            @_sync_4
            def pre_startup(self) -> None: ...

            @_sync_4
            def post_shutdown(self) -> None: ...

        _sync_5 = _method_sync(results_append, "5")

        class ExampleScript5App(ExampleScript4App):
            @_sync_5
            def on_init(self) -> None: ...

            @_sync_5
            def pre_startup(self) -> None: ...

            @_sync_5
            def post_shutdown(self) -> None: ...

        _sync_6 = _method_sync(results_append, "6")

        class ExampleScript6App(ExampleScript5App):
            @_sync_6
            def on_init(self) -> None: ...

            @_sync_6
            def pre_startup(self) -> None: ...

            @_sync_6
            def post_shutdown(self) -> None: ...

        _sync_7 = _method_sync(results_append, "7")

        class ExampleScript7App(ExampleScript6App):
            @_sync_7
            def on_init(self) -> None: ...

            @_sync_7
            def pre_startup(self) -> None: ...

            @_sync_7
            def post_shutdown(self) -> None: ...

        ExampleScript7App.launch()

        results_expected = [
            "on_init:1",
            "on_init:2",
            "on_init:3",
            "on_init:4",
            "on_init:5",
            "on_init:6",
            "on_init:7",
            "pre_startup:1",
            "pre_startup:2",
            "pre_startup:3",
            "pre_startup:4",
            "pre_startup:5",
            "pre_startup:6",
            "pre_startup:7",
            "main_sync",
            "post_shutdown:7",
            "post_shutdown:6",
            "post_shutdown:5",
            "post_shutdown:4",
            "post_shutdown:3",
            "post_shutdown:2",
            "post_shutdown:1",
        ]

        self.assertListEqual(results_expected, results)

    def test_async_script(self) -> None:
        from _util._cbutil import _method_async, _method_sync
        from systempy import AsyncScriptUnit, Target

        results: list[str] = []
        results_append = results.append

        _sync_1 = _method_sync(results_append, "1")
        _async_1 = _method_async(results_append, "1")

        class Example1Unit(Target):
            @_sync_1
            def on_init(self) -> None: ...

            @_sync_1
            def pre_startup(self) -> None: ...

            @_async_1
            async def on_shutdown(self) -> None: ...

            @_async_1
            async def on_startup(self) -> None: ...

            @_sync_1
            def post_shutdown(self) -> None: ...

        _sync_2 = _method_sync(results_append, "2")
        _async_2 = _method_async(results_append, "2")

        class Example2Unit(Target):
            @_sync_2
            def on_init(self) -> None: ...

            @_sync_2
            def pre_startup(self) -> None: ...

            @_async_2
            async def on_shutdown(self) -> None: ...

            @_async_2
            async def on_startup(self) -> None: ...

            @_sync_2
            def post_shutdown(self) -> None: ...

        _sync_3 = _method_sync(results_append, "3")
        _async_3 = _method_async(results_append, "3")

        class Example3Unit(Target):
            @_sync_3
            def on_init(self) -> None: ...

            @_sync_3
            def pre_startup(self) -> None: ...

            @_async_3
            async def on_shutdown(self) -> None: ...

            @_async_3
            async def on_startup(self) -> None: ...

            @_sync_3
            def post_shutdown(self) -> None: ...

        class ExampleScriptApp(
            Example1Unit,
            Example2Unit,
            Example3Unit,
            AsyncScriptUnit,
        ):
            reload_signals = ()

            async def main_async(self) -> None:
                results_append("main_async")

        ExampleScriptApp.launch()

        results_expected = [
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
        ]

        self.assertListEqual(results_expected, results)

    def test_custom_event_loop(self) -> None:

        from asyncio import AbstractEventLoop, SelectorEventLoop

        from systempy import AsyncScriptUnit

        results: list[str] = []
        results_append = results.append

        def loop_factory() -> AbstractEventLoop:
            results_append("custom_event_loop")
            return SelectorEventLoop()

        class ExampleScriptApp(AsyncScriptUnit):
            reload_signals = ()

            async def main_async(self) -> None:
                results_append("main_async")

        ExampleScriptApp.launch(loop_factory=loop_factory)

        results_expected = [
            "custom_event_loop",
            "main_async",
        ]

        self.assertListEqual(results_expected, results)

    def test_target_from_scratch(self) -> None: ...

    @skipIf(
        "MEMORE_LEAK_ROUNDS" not in environ,
        "Variable `MEMORE_LEAK_ROUNDS` is not defined",
    )
    def test_zzz_memory_leak(self) -> None:
        from gc import collect
        from sys import version_info

        from systempy import register_hook_after, register_hook_before
        from systempy.libsystempy import class_role_registry

        # create many objects
        for _ in range(int(environ["MEMORE_LEAK_ROUNDS"])):
            self.test_custom_target()
            collect()
            self.test_sync_script_app_subclassing()
            collect()

        class_roles_expected = {
            "object": "ROLE.BUILTINS",
            "Generic": "ROLE.BUILTINS",
            "Protocol": "ROLE.BUILTINS",
            "InterfaceTarget": "ROLE.TARGET",
            "_InitMixin": "ROLE.MIXIN",
            "_FieldIterMixin": "ROLE.MIXIN",
            "Target": "ROLE.MIXIN",
            "SyncMixinABC": "ROLE.MIXIN",
            "AsyncMixinABC": "ROLE.MIXIN",
            "_BaseDaemonUnitABC": "ROLE.UNIT",
            "DaemonUnit": "ROLE.MIXIN",
            "LoopUnit": "ROLE.MIXIN" if version_info >= (3, 12) else "ROLE.UNIT",
            "EventWaitUnit": "ROLE.UNIT",
            "ScriptUnit": "ROLE.MIXIN",
            "ReplLocalsMixin": "ROLE.MIXIN",
            "ReplUnit": "ROLE.UNIT",
            "Unit": "ROLE.MIXIN",
            "ExtTarget": "ROLE.TARGET",
        }

        class_roles_found = {
            cls.__qualname__: str(role) for cls, role in class_role_registry.items()
        }

        self.assertDictEqual(
            class_roles_found,
            class_roles_expected,
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
