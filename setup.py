"""
Python application component initialization system
"""


from setuptools import setup
from inspect import cleandoc

from setup_constants import name_canonical, name, version

# from setup_mypycify import ext_modules
ext_modules = []


description = cleandoc(__doc__)

requirements = [
    "mypy-extensions",
]

packages = [
    name,
    f"{name}.util",
    f"{name}.ext",
    f"{name}.repl",
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
    "setup_constants",
]

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
    version=version,
    zip_safe=True,
)
