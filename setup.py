from collections.abc import Sequence
from os import getenv

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel

from setup_constants import NAME

if getenv("USE_MYPYC"):
    from setup_mypycify import ext_modules

else:
    ext_modules = []


class BDistWheel(bdist_wheel):
    MAX_TAGS = 1

    def get_tag(self) -> Sequence[str]:
        interpret = self.__get_platform_interpret()
        tag = interpret if getenv("USE_MYPYC") else self.python_tag
        return (tag, interpret, self.__get_platform_tags())

    def __get_platform_interpret(self) -> str:
        if not getenv("USE_MYPYC"):
            return "none"

        from packaging.tags import interpreter_name, interpreter_version

        return f"{interpreter_name()}{interpreter_version()}"

    def __get_platform_tags(self) -> str:
        if not getenv("USE_MYPYC"):
            return "any"

        from packaging.tags import platform_tags

        all_tags = tuple(platform_tags())
        if len(all_tags) > self.MAX_TAGS:
            all_tags = all_tags[: self.MAX_TAGS]

        return ".".join(all_tags)


requirements: list[str] = []


packages = [
    NAME,
    f"{NAME}.libsystempy",
    f"{NAME}.unit",
    f"{NAME}.unit.ext",
    f"{NAME}.unit.repl",
]

package_data = {
    NAME: ["py.typed"],
}


py_modules = [
    NAME,
    # "setup_constants",
]

with open("README.md", encoding="utf-8") as readme_file:  # noqa: PTH123
    long_description = readme_file.read()


setup(
    install_requires=requirements,
    cmdclass={"bdist_wheel": BDistWheel},
    packages=packages,
    package_data=package_data,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    py_modules=py_modules,
    ext_modules=ext_modules,
    url="https://github.com/kai3341/systemPY",
    zip_safe=True,
)
