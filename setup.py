from os import environ

from setuptools import setup

from setup_constants import DESCRIPTION, NAME, NAME_CANONICAL, VERSION

if "NO_MYPYC" in environ:
    ext_modules = []
else:
    from setup_mypycify import ext_modules


requirements = []

requirements_build = []

packages = [
    NAME,
    f"{NAME}.util",
    f"{NAME}.ext",
    f"{NAME}.repl",
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
