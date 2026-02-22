# Great fuck-up story

- `Readline` works fine
- Fallback doesn't work

## Fallback fuck-up story

- I tried to send exception to REPL thread:
- - Exception happens **after** pressing `Enter` in REPL
- - Command line between pressing `Ctrl+C` and `Enter` is ignoring / dropping
- I tried to send signal to REPL thread, but it closes immediately
- I tried to find any API to clear input buffer via ctypes, but:
- - Linux uses `fgets` libc API. I don't see it's possible to clear the buffer
- - Windows uses `ReadConsoleW` API. Stackoverflow tells it's possible, but I
    haven't check it
- I tried to write `\n` directly into process stdin, but it has no effect
- - On Linux it's simple because of `procfs`
- - MacOS does not have `procfs`
- - Windows have different API
- I tried to simulate key press via ctypes and X11, but got solution becomes a
  monster:
- - X11 is Linux-specific back-end
- - Wayland is Linux-specific back-end too require different solution
- - Normally it should be `readline` is installed on Linux machines. That's why
    I think fallback implementation is a big time waste
- - I don't have MacOS device to check any solution
- - OK, I have a virtual machine with Windows
- - And it looks easier to install windows python version under wine

But what for? Just install `readline` and enjoy

So, I don't have a good solution in fallback mode

UPD: I asked people how does default `asyncio` REPL work on different platforms
and found that on Windows `Ctrl+C` stops REPL process. It's awful, and I
can't fix it

UPD2: That's why I added
[PTRepl Extension](../../examples/self-hosted/repl.md/#ptrepl-extension)
