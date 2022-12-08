## Changelog

### 0.0.10 &#151 0.0.12

- A lot of fixes to make library running on MacOS

### 0.0.9

- Fix an error in mypy plugin to make it working

### 0.0.7 &#151 0.0.8

- A lot of small fixes around `__slots__` and dataclasses on python >= 3.10

### 0.0.6

- Fix invalid package build

### 0.0.5

- Refactor systempy's typing
- - Tested building via `mypyc`. It's almost ready
- Refactor and split REPL code
- - I found REPL have a lot of problems and
    [tried to fix it](../marginal_notes/repl_pain)
- Add [ptpython](https://github.com/prompt-toolkit/ptpython) REPL.
  [More about it](../../examples/self-hosted/repl#ptrepl-extension)
- Got an idea how to test

### 0.0.4

- Reformat code using black
- Add `py.typed` package hint
- Add some type hints

### 0.0.3

- Implement 90% of documentation

### 0.0.2

- Rename module. The lowerCamelCase makes me suffer. Current name is `systempy`
- Write initial docs

### 0.0.1

- Implementation complete. Library is installable and tested on my pet project
- No documentation yet. All in my mind
- No tests yet. Testing code on my ~~production~~ pet project
- No idea how to test the code. How to test daemon is started? Which lifecycle
  stages were worked? And which were **not**? How the daemon handled unix signal?
- - Maybe via socket, but there is a recursion: while we are running unit tests
    we are running also integration tests, and broken unit tests may lead to the
    false-positive integration test result
- - Maybe via checking subprocess result code and checking it's stdout/stderr
    logs. Anyway it's better then via socket and works good everywhere
- No examples yet (except my pet project which is closedsource, haha)

### 0.0.0

- Unfortunally, the name `lifecycle` is already used. Choosing the new name
- - New name is `systemPY`
- - The LULZ explanation is in the article
    [Why does it `systemPY`?](https://telegra.ph/Why-does-it-systemPY-08-12)
- Initial commit as independent project
- Pypi stub

## Ancient History

Fossil area. Be careful, don't trample the bones

### -0.1.0

- By the impression of systemd refactor the library, drop hardcoded stages,
  make implementation ultimately soft. Now all lifecycle stages are custom.
  It's possible to define any new custom stages and bind it to any previously
  defined stage (before or after it) without any limit
- Implement `gather` direction as arbitrary, handled by `asyncio.gather` core
- Implement experimental `reload_threadsafe`

### -0.2.0

- Drop `call super()` (anti)pattern. Right now while you are implementing the
  component you don't care about other components
- Implement basic daemon reload

### -0.3.0

- Initial idea, named `lifecycle`. You can find a lot of mentions in the code
