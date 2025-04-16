# systemPY

![Logo](https://raw.githubusercontent.com/kai3341/systemPY/main/docs/images/systempy-logo.png)

Python application component initialization system

![python](https://img.shields.io/pypi/pyversions/systemPY)
![version](https://img.shields.io/pypi/v/systemPY)
![downloads](https://img.shields.io/pypi/dm/systemPY)
![format](https://img.shields.io/pypi/format/systemPY)
[![Documentation Status](https://readthedocs.org/projects/systempy/badge/?version=latest)](https://systempy.readthedocs.io/en/latest/?badge=latest)
![GitHub issues](https://img.shields.io/github/issues/kai3341/systemPY)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Full documantation is available at
[Read the Docs](https://systempy.readthedocs.io/en/latest/)

## The problem

The regular application contain many atomic components. Asyncio makes theirs
initializing a little bit complicated. It's OK, when you have single entrypoint
and initialize your application components via your framework. While you add
new components to your application iteratively, you don't see any problem

When you create any new entrypoint, you have to think a lot, how to initialize
application components again, which callbacks should be called and in which
order. But it's a half of the problem! You have to implement also graceful
shutdown

The most painful part is one-time scripts. It's kind of The Banana Gorilla
Problem: you wanted a banana but you have to initialize a gorilla holding the
banana and the entire jungle, and then graceful shutdown it

## Solution

This library allows you to implement application startup and shutdown in
declarative way. You have to implement a class for each your component,
write the startup and shutdown code. Then combine required components as
mixins into the current application `Unit` class. Then create an instance
and pass dependencies as keyword arguments. In case it's daemon run
`instance.run_sync()` methed

## Basic principles

There are 6 most significant stages of the application lifecycle:

- `on_init` executes exactly once on application startup

- `pre_startup` is called before event loop startup

- `on_startup` is called exactly when event loop started

- `on_shutdown` is called when application is going shutdown or reload but
  event loop still working

- `post_shutdown` is called after event loop stopped or drained. When
  application is going to reload, then it should be called `pre_startup`

- `on_exit` executes exactly once when application is stopping

You may to create `Unit` classes for each your application component where you
may put your code. Then you may combine these `Unit` class mixins into the
current worker class, which aggregate your defined callbacks and run in the
right order. Depending on application type, these callbacks may be called by
primary application or by you are
