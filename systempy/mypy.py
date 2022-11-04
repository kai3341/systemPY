# import sys
# from configparser import ConfigParser
from typing import (
    # Any,
    Callable,
    # Dict,
    List,
    Optional,
    # Set,
    Tuple,
    Type as TypingType,
    # Union,
)

# from mypy.errorcodes import ErrorCode
from mypy.nodes import (
    # ARG_NAMED,
    # ARG_NAMED_OPT,
    # ARG_OPT,
    ARG_POS,
    ARG_STAR2,
    MDEF,
    Argument,
    # AssignmentStmt,
    Block,
    # CallExpr,
    # ClassDef,
    # Context,
    Decorator,
    # EllipsisExpr,
    # FuncBase,
    FuncDef,
    # JsonDict,
    # MemberExpr,
    NameExpr,
    PassStmt,
    # PlaceholderNode,
    # RefExpr,
    # StrExpr,
    # SymbolNode,
    SymbolTableNode,
    # TempNode,
    TypeInfo,
    # TypeVarExpr,
    Var,
)

# from mypy.options import Options
from mypy.plugin import (
    # CheckerPluginInterface,
    ClassDefContext,
    # FunctionContext,
    # MethodContext,
    Plugin,
    # SemanticAnalyzerPluginInterface,
)

from mypy.plugins import dataclasses
from mypy.semanal import set_callable_name

# from mypy.server.trigger import make_wildcard_trigger
from mypy.types import (
    AnyType,
    CallableType,
    # Instance,
    NoneType,
    # Overloaded,
    Type,
    TypeOfAny,
    TypeType,
    # TypeVarType,
    # UnionType,
    # get_proper_type,
)

from mypy.typevars import fill_typevars
from mypy.util import get_unique_redefinition_name
from mypy.version import __version__ as mypy_version

try:
    from mypy.types import TypeVarDef  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    # Backward-compatible with TypeVarDef from Mypy 0.910.
    from mypy.types import TypeVarType as TypeVarDef

UNITMETA_FULLNAME = "systempy.unit.UnitMeta"


def parse_mypy_version(version: str) -> Tuple[int, ...]:
    return tuple(int(part) for part in version.split("+", 1)[0].split("."))


MYPY_VERSION_TUPLE = parse_mypy_version(mypy_version)
BUILTINS_NAME = "builtins" if MYPY_VERSION_TUPLE >= (0, 930) else "__builtins__"


def plugin(version: str) -> "TypingType[Plugin]":
    """
    `version` is the mypy version string

    We might want to use this to print a warning if the mypy version being used is
    newer, or especially older, than we expect (or need).
    """
    return SystemPYPlugin


class SystemPYPlugin(Plugin):
    def get_base_class_hook(
        self, fullname: str
    ) -> "Optional[Callable[[ClassDefContext], None]]":
        sym = self.lookup_fully_qualified(fullname)

        if not sym:
            return None

        if not isinstance(sym.node, TypeInfo):
            return None

        declared_metaclass = sym.node.declared_metaclass

        if not declared_metaclass:
            return None

        if declared_metaclass.type.fullname != UNITMETA_FULLNAME:
            return None

        return self._on_base_class_hook

    def _on_base_class_hook(self, ctx: ClassDefContext) -> None:
        init_arguments = [
            Argument(Var("kwargs"), AnyType(TypeOfAny.explicit), None, ARG_STAR2)
        ]
        add_method(ctx, "__init__", init_arguments, NoneType())
        dataclasses.DataclassTransformer(ctx).transform()


# === UTIL ===


def add_method(
    ctx: ClassDefContext,
    name: str,
    args: List[Argument],
    return_type: Type,
    self_type: Optional[Type] = None,
    tvar_def: Optional[TypeVarDef] = None,
    is_classmethod: bool = False,
    is_new: bool = False,
    # is_staticmethod: bool = False,
) -> None:
    """
    Adds a new method to a class.

    This can be dropped if/when https://github.com/python/mypy/issues/7301 is merged
    """
    info = ctx.cls.info

    # First remove any previously generated methods with the same name
    # to avoid clashes and problems in the semantic analyzer.
    if name in info.names:
        sym = info.names[name]
        if sym.plugin_generated and isinstance(sym.node, FuncDef):
            ctx.cls.defs.body.remove(sym.node)  # pragma: no cover

    self_type = self_type or fill_typevars(info)
    if is_classmethod or is_new:
        first = [
            Argument(Var("_cls"), TypeType.make_normalized(self_type), None, ARG_POS)
        ]
    # elif is_staticmethod:
    #     first = []
    else:
        self_type = self_type or fill_typevars(info)
        first = [Argument(Var("__pydantic_self__"), self_type, None, ARG_POS)]
    args = first + args
    arg_types, arg_names, arg_kinds = [], [], []
    for arg in args:
        assert arg.type_annotation, "All arguments must be fully typed."
        arg_types.append(arg.type_annotation)
        arg_names.append(arg.variable.name)
        arg_kinds.append(arg.kind)

    function_type = ctx.api.named_type(f"{BUILTINS_NAME}.function")
    signature = CallableType(
        arg_types, arg_kinds, arg_names, return_type, function_type
    )
    if tvar_def:
        signature.variables = [tvar_def]

    func = FuncDef(name, args, Block([PassStmt()]))
    func.info = info
    func.type = set_callable_name(signature, func)
    func.is_class = is_classmethod
    # func.is_static = is_staticmethod
    func._fullname = info.fullname + "." + name
    func.line = info.line

    # NOTE: we would like the plugin generated node to dominate, but we still
    # need to keep any existing definitions so they get semantically analyzed.
    if name in info.names:
        # Get a nice unique name instead.
        r_name = get_unique_redefinition_name(name, info.names)
        info.names[r_name] = info.names[name]

    if is_classmethod:  # or is_staticmethod:
        func.is_decorated = True
        v = Var(name, func.type)
        v.info = info
        v._fullname = func._fullname
        # if is_classmethod:
        v.is_classmethod = True
        dec = Decorator(func, [NameExpr("classmethod")], v)
        # else:
        #     v.is_staticmethod = True
        #     dec = Decorator(func, [NameExpr('staticmethod')], v)

        dec.line = info.line
        sym = SymbolTableNode(MDEF, dec)
    else:
        sym = SymbolTableNode(MDEF, func)
    sym.plugin_generated = True

    info.names[name] = sym
    info.defn.defs.body.append(func)
