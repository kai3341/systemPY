from os import path
from ..repl.repl import ReplUnit
from ..util import mark_as_target

from mypy_extensions import trait


@mark_as_target
@trait
class PrettyReplUnit(ReplUnit):
    def repl_handle_banner(self, banner: str) -> str:
        caller_globals = self._repl_caller_frame[0].f_globals
        package = caller_globals["__package__"]

        filename = self._repl_caller_frame.filename
        basename = path.basename(filename)
        extension_idx = basename.rfind(".")

        if extension_idx > 0:
            basename = basename[:extension_idx]

        if package:
            self._module_qualname = f"{package}.{basename}"
        else:
            self._module_qualname = basename

        banner_lines = banner.split("\n")
        banner_lines.pop(-1)
        banner_lines.append("")
        banner_lines.append(f"Working on {self._module_qualname}")
        banner_lines.append(f"Variables: {sorted(self.repl_env)}")
        return "\n".join(banner_lines)
