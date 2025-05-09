from collections.abc import Sequence
from os import getenv

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel

from setup_constants import DESCRIPTION, NAME, NAME_CANONICAL, VERSION

requirements_build: list[str] = []

if getenv("USE_MYPYC"):
    from setup_mypycify import ext_modules

    requirements_build.append("mypyc")
else:
    ext_modules = []


class BDistWheel(bdist_wheel):
    MAX_TAGS = 10

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

keywords = [
    "asyncio",
    "graceful",
    "init",
    "initialization",
    "shutdown",
    "manager",
]

classifiers__python_versions = (
    "3 :: Only",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
)

classifiers__programming_language = tuple(
    f"Programming Language :: Python :: {i}"
    # ===
    for i in classifiers__python_versions
)

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    *classifiers__programming_language,
    # Topic
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    # Typing
    "Typing :: Typed",
]

py_modules = [
    NAME,
    # "setup_constants",
]

with open("README.md", encoding="utf-8") as readme_file:  # noqa: PTH123
    long_description = readme_file.read()


setup(
    classifiers=classifiers,
    description=DESCRIPTION,
    install_requires=requirements,
    extras_require={
        "dev": requirements_build,
    },
    cmdclass={"bdist_wheel": BDistWheel},
    license="MIT",
    packages=packages,
    package_data=package_data,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=keywords,
    name=NAME_CANONICAL,
    py_modules=py_modules,
    ext_modules=ext_modules,
    url="https://github.com/kai3341/systemPY",
    version=VERSION,
    zip_safe=True,
)
