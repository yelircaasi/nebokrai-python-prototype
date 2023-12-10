from dataclasses import dataclass
from typing import Annotated, Literal, Optional, Protocol, TypedDict, TypeVar, Union

from .pdatetime.ptime import PTime

T = TypeVar("T")


class SupportsGe(Protocol):
    def __ge__(self: T, __other: T) -> bool:
        ...


class SupportsGt(Protocol):
    def __gt__(self: T, __other: T) -> bool:
        ...


@dataclass(frozen=True)
class BaseMetadata:
    """Base class for all metadata.

    This exists mainly so that implementers
    can do `isinstance(..., BaseMetadata)` while traversing field annotations.
    """

    __slots__ = ()


@dataclass(frozen=True)
class Ge(BaseMetadata):
    """Ge(ge=x) implies that the value must be greater than or equal to x.

    It can be used with any type that supports the ``>=`` operator,
    including numbers, dates and times, strings, sets, and so on.
    """

    ge: SupportsGe


@dataclass(frozen=True)
class Gt(BaseMetadata):
    """Gt(gt=x) implies that the value must be greater than or equal to x.

    It can be used with any type that supports the ``>=`` operator,
    including numbers, dates and times, strings, sets, and so on.
    """

    gt: SupportsGt


class TimedDistance(TypedDict):
    """
    Data type intended primarily for recording run/walk information.
    """

    seconds: float
    kilometers: float


class TimedDistanceWithElevation(TypedDict):
    """
    Data type intended primarily for recording run/walk information, with positive and negative
      elevation recorded separately.
    """

    seconds: float
    kilometers: float
    up: float
    down: float


DesirabilityString = Literal["yes", "no"]
WeekdayLiteral = Literal["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
StatusLiteral = Literal["todo", "done"]
Natural = Annotated[int, Ge(ge=0)]
Nonnegative = Annotated[float, Ge(ge=0)]
Positive = Annotated[float, Gt(gt=0)]
TrackingActivityResponseType = Union[
    int,
    list[int],
    str,
    float,
    TimedDistance,
    TimedDistanceWithElevation,
    Natural,
    bool,
    list[Natural],
    PTime,
    None,
    list["TrackingActivityResponseType"],
    dict[str, "TrackingActivityResponseType"],
]
TimeAmountRaw = Union[str, int]
TrueString = Literal["y", "yes", "✔"]
true_strings = set(["y", "yes", "✔"])
PromptTypeName = Optional[
    Literal[
        "boolean",
        "float",
        "integer_sequence",
        "integer",
        "nonnegative",
        "natural_sequence",
        "natural",
        "text",
        "time_amount",
        "time",
    ]
]
prompt_type_mapping: dict[PromptTypeName, str] = {
    "boolean": "bool",
    "float": "float",
    "integer_sequence": "list[int]",
    "integer": "int",
    "nonnegative": "list[float] where float >= 0",
    "natural_sequence": "list[int] where int > 0",
    "natural": "int, where int > 0",
    "text": "str",
    "time_amount": "float",
    "time": "PTime",
}
