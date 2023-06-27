from typing import (
    Callable,
    Optional,
    Type as TypingType,
)

from mypy.nodes import TypeInfo

from mypy.plugin import (
    ClassDefContext,
    Plugin,
)

from mypy.plugins import dataclasses


UNITMETA_FULLNAME = "systempy.unit_meta.UnitMeta"


def plugin(version: str) -> "TypingType[Plugin]":
    """
    `version` is the mypy version string

    We might want to use this to print a warning if the mypy version being used is
    newer, or especially older, than we expect (or need).
    """
    return SystemPYPlugin


class SystemPYPlugin(Plugin):
    def get_base_class_hook(
        self,
        fullname: str,
    ) -> "Optional[Callable[[ClassDefContext], None]]":
        sym = self.lookup_fully_qualified(fullname)

        if not sym:
            return None

        if not isinstance(sym.node, TypeInfo):
            return None

        declared_metaclass = sym.node.declared_metaclass

        if not declared_metaclass:
            return None

        declared_metaclass_type = declared_metaclass.type

        if declared_metaclass_type.fullname != UNITMETA_FULLNAME:
            return None

        return self._on_base_class_hook

    def _on_base_class_hook(self, ctx: ClassDefContext) -> None:
        dataclasses.dataclass_class_maker_callback(ctx)
