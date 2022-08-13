# systemPY

Python application component initialization system

![python](https://img.shields.io/pypi/pyversions/systemPY)
![version](https://img.shields.io/pypi/v/systemPY)
![downloads](https://img.shields.io/pypi/dm/systemPY)
![format](https://img.shields.io/pypi/format/systemPY)
![GitHub issues](https://img.shields.io/github/issues/kai3341/systemPY)

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

It's possible to use `systemPY` in three scenarios:

* Secondary application, which is handled by another application like
`celery` or `starlette`

* Daemon or script -- self-hosted application

* Master application, handles other applications
