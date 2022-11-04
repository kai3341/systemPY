"""
Python application component initialization system
"""

import os
from setuptools import setup
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


mypycify_structure = {
    name: {
        None: (
            "mypy.py",
            "target.py",
            # "unit_meta.py",
            "unit.py",
            "process.py",
            "daemon.py",
            "repl.py",
            "loop.py",
        ),
        "util": {
            None: (
                "constants.py",
                "extraction.py",
                "configuration.py",
                "check.py",
                "typing.py",
                "creation.py",
                "callback_plan.py",
                "misc.py",
                "register.py",
                "dataclasses.py",
                "handler_type.py",
            ),
        },
        "ext": {
            None: (
                "pretty_repl.py",
                "target_ext.py",
                "starlette.py",
                "celery.py",
            ),
        },
    },
}


def walk(struct: dict, root=None):
    if root is None:
        for key, value in struct.items():
            if key is None:
                for item in value:
                    yield item
            else:
                yield from walk(value, key)
    else:
        for key, value in struct.items():
            if key is None:
                for item in value:
                    yield os.path.join(root, item)
            else:
                next_root = os.path.join(root, key)
                yield from walk(value, next_root)


ext_modules = walk(mypycify_structure)
ext_modules = list(ext_modules)
ext_modules = mypycify(ext_modules)


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
