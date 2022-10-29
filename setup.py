"""
Python application component initialization system
"""

from genericpath import isfile
import os
from setuptools import setup  # type: ignore
from inspect import cleandoc
from mypyc.build import mypycify

name_canonical = "systemPY"
name = name_canonical.lower()

description = cleandoc(__doc__)

requirements = []

packages = [
    name,
    f"{name}.util",
    f"{name}.ext",
]

package_data = {
    name: ["py.typed"],
}

keywords = [
    "asyncio",
    "graceful",
    "init",
    "initialization",
    "shutdown",
    "manager",
]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    # Programming Language
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    # Topic
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    # Typing
    "Typing :: Typed",
]

py_modules = [
    name,
]

names = [
    "systempy/util/constants.py",
    "systempy/util/extraction.py",
    "systempy/util/configuration.py",
    "systempy/util/check.py",
    "systempy/util/systempy_typing.py",
    "systempy/util/creation.py",
    "systempy/util/callback_plan.py",
    "systempy/util/misc.py",
    "systempy/util/register.py",
    "systempy/util/systempy_dataclasses.py",
    "systempy/util/handler_type.py",
    "systempy/target.py",
    # "systempy/unit.py",
    # "systempy/process.py",
    # "systempy/repl.py",
    # "systempy/mypy.py",
    # "systempy/loop.py",
    # "systempy/daemon.py",
]


# def mypycify_targets_iter(root: str):
#     for entry in os.listdir(root):
#         if entry.startswith("."):
#             continue

#         if entry.startswith("_"):
#             continue

#         path = os.path.join(root, entry)

#         if os.path.isdir(path):
#             if entry == "util":
#                 continue
#             yield from mypycify_targets_iter(path)

#         if entry.endswith(".py"):
#             # if entry == "setup.py"
#             if os.path.isfile(path):
#                 yield path


# ext_modules = mypycify_targets_iter(name)
# ext_modules = list(ext_modules)
ext_modules = mypycify(names)


with open("README.md") as readme_file:
    long_description = readme_file.read()


setup(
    classifiers=classifiers,
    description=description,
    install_requires=requirements,
    license="MIT",
    packages=packages,
    package_data=package_data,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=keywords,
    name=name_canonical,
    py_modules=py_modules,
    ext_modules=ext_modules,
    url="https://github.com/kai3341/systemPY",
    version="0.0.4",
    zip_safe=True,
)
