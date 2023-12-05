from typing import Callable, Literal, NotRequired, Optional, TypedDict, Union

from ..elementary_types import (
    DesirabilityString,
    Natural,
    PromptTypeName,
    StatusLiteral,
    T,
    TimeAmountRaw,
    TrackingActivityType,
    WeekdayLiteral,
)
from ..entity_ids import TaskID
from ..pdatetime.pdate import PDate
from ..pdatetime.ptime import PTime

RoutinesDictRaw = dict[str, "RoutineDictRaw"]
RoutinesDictParsed = dict[str, "RoutineDictParsed"]
PlanDictRaw = dict[str, list["TaskDictFullRaw"]]
PlanDictParsed = dict[PDate, "PlanTaskParsed"]
RoadmapsDictRaw = dict[str, "RoadmapDictRaw"]
RoadmapsDictParsed = dict[str, "RoadmapDictParsed"]
RoutinesInCalendarDictRaw = dict[str, "RoutineInCalendarDictRaw"]


class TimedDistance(TypedDict):
    seconds: float
    kilometers: float


class TimedDistanceWithElevation(TypedDict):
    seconds: float
    kilometers: float
    up: float
    down: float


PromptResponseType = Union[
    bool, int, Natural, list[Natural], str, float, TimedDistance, TimedDistanceWithElevation
]
RawPromptResponseType = Union[
    int, Natural, list[Natural], str, float, TimedDistance, TimedDistanceWithElevation
]


class PromptResponseParserDispatcher(TypedDict):
    boolean: Callable[[str], bool]
    natural: Callable[[Natural], Natural]
    natural_sequence: Callable[[list[Natural]], list[Natural]]
    string: Callable[[T], T]
    time: Callable[[str], PTime]
    time_amount: Callable[[TimeAmountRaw], Natural]
    timed_distance: Callable[[T], T]
    timed_distance_with_elevation: Callable[[T], T]
    # typed_list: Callable[[list[RawPromptResponseType]], list[PromptResponseType]]


# PromptTypeName = Literal[]


class DeclarationDictRaw(TypedDict):
    config: "ConfigDictRaw"
    routines: "RoutinesDictRaw"
    tracking: "TrackingDictRaw"
    calendar: "CalendarDictRaw"
    roadmaps: "RoadmapsDictRaw"


class DeclarationDictParsed(TypedDict):
    config: "ConfigDictParsed"
    routines: "RoutinesDictParsed"
    tracking: "TrackingDictParsed"
    calendar: "CalendarDictParsed"
    roadmaps: "RoadmapsDictParsed"


class ConfigDictRaw(TypedDict):
    repr_width: int
    default_duration: int
    default_priority: float
    default_sleep_priority: float
    default_interval: int
    default_cluster_size: int
    default_order: float
    default_normaltime: int
    default_idealtime_factor: float
    default_mintime_factor: float
    default_maxtime_factor: float
    default_categories: str
    default_ismovable: bool
    default_alignend: bool
    default_day_start: str
    default_day_end: str
    default_empty_blocks: str
    default_project_dates_missing_offset: int
    default_project_dates_missing_hashmod: int
    default_schedule_weight_interval_min: float
    default_schedule_weight_interval_max: float
    default_schedule_weight_transform_exponent: float
    default_sleep_delta_min: int
    default_sleep_delta_max: int


class ConfigDictParsed(TypedDict):
    repr_width: int
    default_duration: int
    default_priority: float
    default_sleep_priority: float
    default_interval: int
    default_cluster_size: int
    default_order: float
    default_normaltime: int
    default_idealtime_factor: float
    default_mintime_factor: float
    default_maxtime_factor: float
    default_categories: str
    default_ismovable: bool
    default_alignend: bool
    default_day_start: PTime
    default_day_end: PTime
    default_empty_blocks: set[str]
    default_project_dates_missing_offset: int
    default_project_dates_missing_hashmod: int
    default_schedule_weight_interval_min: float
    default_schedule_weight_interval_max: float
    default_schedule_weight_transform_exponent: float
    default_sleep_delta_min: int
    default_sleep_delta_max: int


class RoutineDictRaw(TypedDict):
    name: str
    default_start: str
    default_priority: float
    default_notes: str
    default_normaltime: int
    default_idealtime: int
    default_mintime: int
    default_maxtime: int
    default_blocks: str
    default_order: float
    items: list["RoutineItemDictRaw"]


class RoutineDictParsed(TypedDict):
    name: str
    default_start: PTime
    default_priority: float
    default_notes: str
    default_normaltime: int
    default_idealtime: int
    default_mintime: int
    default_maxtime: int
    default_blocks: str
    default_order: float
    items: list["RoutineItemDictParsed"]


class RoutineItemDictRaw(TypedDict):
    name: str
    id: str
    priority: float
    start: NotRequired[str]
    end: NotRequired[str]
    desirable: NotRequired[DesirabilityString]
    prompt: NotRequired[str]
    dtype: NotRequired[PromptResponseType]
    normaltime: NotRequired[int]
    mintime: NotRequired[int]
    maxtime: NotRequired[int]
    idealtime: NotRequired[int]
    blocks: NotRequired[str]
    categories: NotRequired[str]
    notes: NotRequired[str]
    alignend: NotRequired[bool]
    order: NotRequired[float]
    subentries: NotRequired[list["EntryDictRaw"]]
    assigned_time: NotRequired[str]
    ismovable: NotRequired[bool]


RoutineItemDictParsed = RoutineItemDictRaw


class TrackingDictRaw(TypedDict):
    activities: list["ActivityDictRaw"]


class TrackingDictParsed(TypedDict):
    activities: list["ActivityDictParsed"]


class ActivityDictRaw(TypedDict):
    name: str
    dtype: PromptTypeName
    desirable: DesirabilityString
    prompt: str
    error_prompt: NotRequired[str]
    response: NotRequired[TrackingActivityType]
    order: NotRequired[float]


class ActivityDictParsed(TypedDict):
    name: str
    dtype: PromptTypeName
    desirable: DesirabilityString
    prompt: str
    error_prompt: NotRequired[str]
    response: NotRequired[TrackingActivityType]
    order: float


class PromptDispatcherType(TypedDict):
    sequence: Callable[[str, str, PromptTypeName], list]
    time: Callable[[str, str, str], PTime]
    integer: Callable[[str, str, str], int]
    integer_sequence: Callable[[str, str, str], list[int]]
    natural: Callable[[str, str, str], Natural]
    time_amount: Callable[[str, str, str], float]
    boolean: Callable[[str, str, str], bool]
    natural_sequence: Callable[[str, str, str], list[Natural]]
    text: Callable[[str, str, str], str]
    timed_distance: Callable[[str, str, str], TimedDistance]
    timed_distance_with_elevation: Callable[[str, str, str], TimedDistanceWithElevation]


class CalendarDictRaw(TypedDict):
    days: dict[str, "DayDictRaw"]


class CalendarDictParsed(TypedDict):
    days: dict[PDate, "DayDictParsed"]


class DayDictRaw(TypedDict):
    start: str
    end: str
    weekday: WeekdayLiteral
    routines: list["RoutineInCalendarDictRaw"]
    entries: list["EntryDictRaw"]


class DayDictParsed(TypedDict):
    start: PTime
    end: PTime
    weekday: WeekdayLiteral
    routines: list["RoutineInCalendarDictParsed"]
    entries: list["EntryDictParsed"]


class RoutineInCalendarDictRaw(TypedDict):
    name: str
    start: str
    end: str
    priority: NotRequired[float]
    normaltime: NotRequired[int]
    idealtime: NotRequired[int]
    mintime: NotRequired[int]
    maxtime: NotRequired[int]
    ismovable: NotRequired[bool]
    order: NotRequired[float]


class RoutineInCalendarDictParsed(TypedDict):
    name: str
    start: PTime
    end: PTime
    priority: float
    normaltime: int
    idealtime: int
    mintime: int
    maxtime: int
    ismovable: bool
    order: float


class EntryDictRaw(TypedDict):
    name: str
    start: str
    end: str
    priority: float
    ismovable: bool
    normaltime: NotRequired[int]
    mintime: NotRequired[int]
    maxtime: NotRequired[int]
    idealtime: NotRequired[int]
    blocks: NotRequired[str]
    categories: NotRequired[str]
    notes: NotRequired[str]
    alignend: NotRequired[bool]
    order: NotRequired[float]
    subentries: NotRequired[list["EntryDictRaw"]]
    assigned_time: NotRequired[str]


class EntryDictParsed(TypedDict):
    name: str
    start: PTime
    end: PTime
    priority: float
    blocks: set[str]
    ismovable: bool
    normaltime: int
    mintime: int
    maxtime: int
    idealtime: int
    categories: set[str]
    notes: str
    alignend: bool
    order: float
    subentries: list["EntryDictParsed"]
    assigned_time: Optional[PTime]


class RoadmapDictRaw(TypedDict):
    name: str
    categories: str
    projects: dict[str, "ProjectDictRaw"]


class RoadmapDictParsed(TypedDict):
    tmp: Literal["placeholder"]


class ProjectDictRaw(TypedDict):
    name: str
    task_string: str
    priority: float
    start: str
    end: NotRequired[str]
    duration: NotRequired[int]
    interval: NotRequired[int]
    cluster_size: NotRequired[int]
    tags: NotRequired[str]
    description: NotRequired[str]
    notes: NotRequired[str]
    dependencies: NotRequired[str]
    categories: NotRequired[str]
    tasks: list["TaskDictRaw"]


class ProjectDictParsed(TypedDict):
    name: str
    task_string: str
    priority: float
    start: PDate
    end: PDate
    duration: int
    tags: set[str]
    description: str
    notes: str
    dependencies: set[str]
    categories: set[str]
    tasks: list["TaskDictParsed"]


class TaskDictRaw(TypedDict):
    name: str
    id: str
    priority: NotRequired[float]
    status: NotRequired[StatusLiteral]
    duration: NotRequired[int]
    dependencies: NotRequired[str]
    categories: NotRequired[str]
    notes: NotRequired[str]


class TaskDictFullRaw(TypedDict):
    name: str
    id: str
    priority: float
    status: StatusLiteral
    duration: int
    project_id: str
    project_name: str
    dependencies: str
    notes: str
    categories: str


class TaskDictParsed(TypedDict):
    name: str
    id: str
    priority: Optional[float]
    status: Optional[StatusLiteral]
    notes: str
    duration: Optional[int]
    categories: set[str]
    dependencies: set[TaskID]


DayLogDictRaw = dict[str, ActivityDictRaw]
DayLogDictParsed = dict[str, ActivityDictParsed]


class PlanTaskRaw(TypedDict):
    name: str
    project_name: str
    id: str
    priority: float
    duration: int
    dependencies: str
    notes: str
    status: StatusLiteral
    categories: str


class PlanTaskParsed(TypedDict):
    name: str
    project_name: str
    id: TaskID
    priority: float
    duration: int
    dependencies: set[str]
    notes: str
    status: StatusLiteral
    categories: set[str]


class ScheduleDictRaw(TypedDict):
    date: str
    entries: list["EntryDictRaw"]


class ScheduleDictParsed(TypedDict):
    date: PDate
    entries: list["ScheduleEntryParsed"]


class ScheduleEntryRaw(TypedDict):
    tmp: Literal["placeholder"]


class ScheduleEntryParsed(TypedDict):
    tmp: Literal["placeholder"]
