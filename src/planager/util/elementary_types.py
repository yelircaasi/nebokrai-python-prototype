from dataclasses import dataclass
from typing import Annotated, Literal, Protocol, TypedDict, TypeVar, Union

from .pdatetime.ptime import PTime

# from .serde.custom_dict_types import TimedDistance

T = TypeVar("T")


class SupportsGe(Protocol):
    def __ge__(self: T, __other: T) -> bool:
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
TrackingActivityType = Union[
    int, list[int], str, float, TimedDistance, Natural, bool, list[Natural], PTime, None
]
# int | list[int] | str | float |
TimeAmountRaw = Union[str, int]
TrueString = Literal["y", "yes", "✔"]
true_strings = set(["y", "yes", "✔"])
PromptTypeName = Literal[
    "boolean",
    "integer_sequence",
    "integer",
    "natural_sequence",
    "natural",
    "text",
    "time_amount",
    "time",
    "timed_distance_with_elevation",
    "timed_distance",
]
# typed_list: Callable[[list[RawPromptResponseType]], list[PromptResponseType]]
