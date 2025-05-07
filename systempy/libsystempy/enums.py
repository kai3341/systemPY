from enum import Enum, unique


@unique
class DIRECTION(str, Enum):
    """
    Public enum containing supported directions. Rely on your IDE's help
    """

    FORWARD = "forward"
    BACKWARD = "backward"
    GATHER = "gather"


@unique
class TYPE(str, Enum):
    """
    Private internal enum
    """

    SYNC = "sync"
    ASYNC = "async"


@unique
class ROLE(str, Enum):
    APP = "app"
    UNIT = "unit"
    MIXIN = "mixin"
    TARGET = "target"
