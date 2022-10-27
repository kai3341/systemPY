from os import path
from ..repl import ReplUnit


class PrettyReplUnit(ReplUnit):
    def repl_handle_banner(self, banner):
        caller_globals = self.repl_caller_frame[0].f_globals
        package = caller_globals["__package__"]

        filename = self.repl_caller_frame.filename
        basename = path.basename(filename)
        extension_idx = basename.rfind(".")

        if extension_idx > 0:
            basename = basename[:extension_idx]

        module_qualname = f"{package}.{basename}"

        banner_lines = banner.split("\n")
        banner_lines.pop(-1)
        banner_lines.append("")
        banner_lines.append(f"Working on {module_qualname}")
        banner_lines.append(f"Variables: {sorted(self.repl_env)}")
        return "\n".join(banner_lines)
