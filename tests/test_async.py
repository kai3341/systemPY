from unittest import IsolatedAsyncioTestCase


class Test(IsolatedAsyncioTestCase):
    async def test_subprocess_async_reload_signal(self) -> None:
        from asyncio import create_subprocess_exec, sleep
        from asyncio.subprocess import PIPE
        from pathlib import Path
        from signal import SIGHUP, SIGINT
        from sys import executable

        current_dir = Path(__file__).parent

        process = await create_subprocess_exec(
            executable,
            (str(current_dir / "async_reload_signal.py")),
            stdout=PIPE,
            stderr=PIPE,
        )

        await sleep(0.4)

        self.assertEqual(process.returncode, None, "Process dead unexpectedly")

        process.send_signal(SIGHUP)
        await sleep(0.3)

        self.assertEqual(process.returncode, None, "Process dead unexpectedly")

        process.send_signal(SIGHUP)
        await sleep(0.2)

        self.assertEqual(process.returncode, None, "Process dead unexpectedly")

        process.send_signal(SIGINT)
        await sleep(0.2)

        self.assertEqual(process.returncode, 0)

        result = await process.communicate()
        stdout = result[0].decode()
        lines = stdout.split("\n")
        lines.pop()

        lines_expected = [
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

        self.assertListEqual(lines, lines_expected)

    async def test_subprocess_sync_reload_signal(self) -> None:
        from asyncio import create_subprocess_exec, sleep
        from asyncio.subprocess import PIPE
        from pathlib import Path
        from signal import SIGHUP, SIGINT
        from sys import executable

        current_dir = Path(__file__).parent

        process = await create_subprocess_exec(
            executable,
            (str(current_dir / "sync_reload_signal.py")),
            stdout=PIPE,
            stderr=PIPE,
        )

        await sleep(0.4)

        self.assertEqual(process.returncode, None, "Process dead unexpectedly")

        process.send_signal(SIGHUP)
        await sleep(0.3)

        self.assertEqual(process.returncode, None, "Process dead unexpectedly")

        process.send_signal(SIGHUP)
        await sleep(0.2)

        self.assertEqual(process.returncode, None, "Process dead unexpectedly")

        process.send_signal(SIGINT)
        await sleep(0.2)

        self.assertEqual(process.returncode, 0)

        result = await process.communicate()
        stdout = result[0].decode()
        lines = stdout.split("\n")
        lines.pop()

        lines_expected = [
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

        self.assertListEqual(lines, lines_expected)
