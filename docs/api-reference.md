# API Reference

## `Target`

## `SyncMixinABC`

## `AsyncMixinABC`

## `ScriptUnit`

## `AsyncScriptUnit` (removed. Now it's just `LoopUnit`)

## `DaemonUnit`

## `LoopUnit`

All `LoopUnit` subclasses accept optional `loop_factory` kwarg:
`Callable[[], AbstractEventLoop]`. Tested with python versions 3.9 &#151 3.14

## `EventWaitUnit`

## `ReplUnit` (deprecated)

## `ASGIServerUnit` and `asgi_server_factory_decorator`

Please check [ASGI Web Server](examples/self-hosted/asgi-web-app.md) article

## `ext.celery.CeleryUnit`

## `ext.pretty_repl.PrettyReplUnit`

## `ext.starlette.StarletteUnit`

## `ext.target_ext.ExtTarget`

## `register_target_method`

## `register_hook_before`

## `register_hook_after`
