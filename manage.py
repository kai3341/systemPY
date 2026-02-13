#!/usr/bin/env python

from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Generator
from dataclasses import dataclass
from os import environ
from pathlib import Path
from sys import executable, platform
from typing import ClassVar

root_dir = Path().absolute()

VENV_BIN = Path(executable).parent


BaseManagePYType = type["BaseManagePY"]


if platform == "win32":
    from subprocess import run
    from sys import stderr, stdout

    def execute_process(args: tuple[str, ...]) -> None:
        run(args, check=True, stdout=stdout, stderr=stderr, env=environ)  # noqa: S603

else:
    from os import execv

    def execute_process(args: tuple[str, ...]) -> None:
        execv(args[0], args)  # noqa: S606


@dataclass()
class BaseManagePY(ABC):
    namespace: Namespace
    parser: ClassVar
    _registry: ClassVar[dict[str, BaseManagePYType]]

    @abstractmethod
    def execute(self) -> None: ...

    def __init_subclass__(cls) -> None:
        cls._registry = {}

    @classmethod
    def register(
        cls,
        name: str,
    ) -> Callable[[BaseManagePYType], BaseManagePYType]:
        def inner(target: BaseManagePYType) -> BaseManagePYType:
            cls._registry[name] = target
            return target

        return inner

    @classmethod
    def main(cls, namespace: Namespace) -> None:
        self = cls(namespace)
        self.execute()


@dataclass()
class ManagePY(BaseManagePY):
    parser: ClassVar = ArgumentParser(
        description="Control panel of systempy",
    )

    subparsers: ClassVar = parser.add_subparsers(dest="root_subparser")

    @classmethod
    def launch(cls) -> None:
        namespace = cls.parser.parse_args()
        cls.main(namespace)

    def execute(self) -> None:
        root_subparser_name: str = self.namespace.root_subparser
        root_subparser = self._registry[root_subparser_name]
        root_subparser.main(self.namespace)


@ManagePY.register("doc-server")
@dataclass()
class DocWebSubparser(BaseManagePY):
    parser: ClassVar = ManagePY.subparsers.add_parser("doc-server")

    # === add_argument ===

    parser.add_argument(
        "--dev-addr",
        default="localhost:8000",
        help="Bind socket to this host:port",
    )

    # ===

    def collect_args_iter(self) -> Generator[str, None, None]:
        ns: Namespace = self.namespace
        yield from (str(VENV_BIN / "mkdocs"), "serve")
        dev_addr: str = ns.dev_addr
        yield from ("--dev-addr", dev_addr)
        yield from ("-w", "docs")

    def execute(self) -> None:
        args = tuple(self.collect_args_iter())
        execute_process(args)


@ManagePY.register("test")
@dataclass()
class TestsSubparser(BaseManagePY):
    parser: ClassVar = ManagePY.subparsers.add_parser("test")

    # === add_argument ===

    parser.add_argument(
        "--memory-leak-rounds",
        help="Configure optional `test_zzz_memory_leak`",
        type=int,
        default=2,
    )

    parser.add_argument(
        "tests",
        nargs="*",
        help="Test names to execute",
    )

    # ===

    def collect_args_iter(self) -> Generator[str, None, None]:
        ns: Namespace = self.namespace

        if ns.memory_leak_rounds:
            memory_leak_rounds: int = ns.memory_leak_rounds
            if memory_leak_rounds < 1:
                raise ValueError

            environ["MEMORE_LEAK_ROUNDS"] = str(memory_leak_rounds)

        yield from (executable, "-m", "unittest")

        if ns.tests:
            for test in ns.tests:
                yield f"tests.{test}"
        else:
            yield from ("discover", "-v", "tests")

    def execute(self) -> None:
        # new_env = {"PYTHONPATH": str(root_dir)}
        args = tuple(self.collect_args_iter())
        execute_process(args)


if __name__ == "__main__":
    ManagePY.launch()
