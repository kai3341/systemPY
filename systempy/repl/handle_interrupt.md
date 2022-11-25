# Great fuck-up story

- `Readline` works fine
- Fallback doesn't work

## Fallback fuck-up story

- I tried to send exception to REPL thread:
- - Exception happens **after** pressing `Enter` in REPL
- - Commend line between pressing `Ctrl+C` and `Enter` is ignoring / dropping
- I tried to send signal to REPL thread, but it closes immediately
- I tried to find any API to clear input buffer via ctypes, but I don't see it
  is possible
- I tried to simulate key press via ctypes and X11, but got solution becomes a
  monster:
- - X11 is Linux-specific back-end
- - Wayland is Linux-specific back-end too require different solution
- - Normally it should be `readline` is installsed on Linux machines. That's why
    I think fallback implementation is a big time waste
- - I don't have MacOS device to check any solution
- - OK, I have a virtual machine with Windows
- - And it looks easier to install windows python version under wine

But what for? Just install `readline` and enjoy

So, I don't have a good solution in fallback mode
