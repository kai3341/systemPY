import os, tomli

version = "0.0.14"
name_canonical = "systemPY"
name = name_canonical.lower()


pyproject_config = "pyproject.toml"
if os.path.isfile(pyproject_config):
    with open(pyproject_config, "rb") as ppfile:
        pyproject = tomli.load(ppfile)
else:
    pyproject = {}
