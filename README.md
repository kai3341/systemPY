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
[Read the Docs](https://systempy.readthedocs.io/latest/)

## The problem

The regular application contains many atomic components. Asyncio makes their
initializing a little bit complicated. It's OK, when you have a single entrypoint
and initialize your application components via your framework. While you add
new components to your application iteratively, you don't see any problem

When you create any new entrypoint, you have to think a lot, how to initialize
application components again, which callbacks should be called and in which
order. But it's a half of the problem! You also have to implement a graceful
shutdown

The most painful part is one-time scripts. It's kind of The Banana Gorilla
Problem: you just want a banana but you have to initialize a gorilla holding the
banana and the entire jungle, and then gracefully shutdown it

## Solution

This library allows you to implement application startup and shutdown in a
declarative way. You have to implement a class for each your component,
write the startup and shutdown code. Then you have to combine required
components as mixins into the current application `App` class. Then create an
instance and pass dependencies as keyword arguments. In case it's a self-hosted
app you have to call the `instance.run_sync()` method

## Basic principles

There are 6 the most significant stages of the application lifecycle:

- `on_init` is called exactly once on the application startup

- `pre_startup` is called before the event loop is started

- `on_startup` is called exactly when the event loop has started

- `on_shutdown` is called when the application is going to shutdown or reload
  but the event loop is still working

- `post_shutdown` is called after event loop has stopped or drained. When
  application is going to reload, next it would be called `pre_startup`

- `on_exit` is called exactly once when application is going to stop

You may to create `Unit` classes for each your application component where you
may put your code. Then you may combine these `Unit` class mixins into the
current `App` class, which composes your defined callbacks and runs in the
right order. Depending on application type, these callbacks may be called by
primary application or by yourself
