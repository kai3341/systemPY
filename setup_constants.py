import tomllib

NAME_CANONICAL = "systemPY"
NAME: str = NAME_CANONICAL.lower()
PYPROJECT_CONFIG = "pyproject.toml"

with open(PYPROJECT_CONFIG, "rb") as ppfile:  # noqa: PTH123
    pyproject = tomllib.load(ppfile)

VERSION = pyproject["project"]["version"]
DESCRIPTION = pyproject["project"]["description"]
