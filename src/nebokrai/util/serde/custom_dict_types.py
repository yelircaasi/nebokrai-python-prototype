from typing import Callable, Literal, NotRequired, Optional, TypedDict, Union

from ..elementary_types import (
    DesirabilityString,
    Natural,
    PromptTypeName,
    StatusLiteral,
    T,
    TimeAmountRaw,
    TimedDistance,
    TimedDistanceWithElevation,
    TrackingActivityResponseType,
    WeekdayLiteral,
)
from ..entity_ids import ProjectID, TaskID
from ..nkdatetime.nkdate import NKDate
from ..nkdatetime.nktime import NKTime

RoutinesDictRaw = dict[str, "RoutineDictRaw"]
RoutinesDictParsed = dict[str, "RoutineDictParsed"]
PlanDictRaw = dict[str, list["TaskFullDictRaw"]]
PlanDictParsed = dict[NKDate, "PlanTaskParsed"]
RoadmapsDictRaw = dict[str, "RoadmapDictRaw"]
RoadmapsDictParsed = dict[str, "RoadmapDictParsed"]
RoutinesInCalendarDictRaw = dict[str, "RoutineInCalendarDictRaw"]


PromptResponseType = Union[
    bool, int, Natural, list[Natural], str, float, TimedDistance, TimedDistanceWithElevation
]
RawPromptResponseType = Union[
    int, Natural, list[Natural], str, float, TimedDistance, TimedDistanceWithElevation
]


class PromptResponseParserDispatcher(TypedDict):
    """
    Implementation of (quasi) strategy pattern for dynamic selection of parser for different
      response types.
    """

    boolean: Callable[[str], bool]
    natural: Callable[[Natural], Natural]
    natural_sequence: Callable[[list[Natural]], list[Natural]]
    string: Callable[[T], T]
    time: Callable[[str], NKTime]
    time_amount: Callable[[TimeAmountRaw], Natural]
    timed_distance: Callable[[T], T]
    timed_distance_with_elevation: Callable[[T], T]


class DeclarationDictRaw(TypedDict):
    """
    Data type corresponding to a freshly-read declaration.json file.
    """

    config: "ConfigDictRaw"
    routines: "RoutinesDictRaw"
    tracking: "TrackingDictRaw"
    calendar: "CalendarDictRaw"
    roadmaps: "RoadmapsDictRaw"


class DeclarationDictParsed(TypedDict):
    """
    Data type corresponding to a freshly-read and type-converted declaration.json file.
    """

    config: "ConfigDictParsed"
    routines: "RoutinesDictParsed"
    tracking: "TrackingDictParsed"
    calendar: "CalendarDictParsed"
    roadmaps: "RoadmapsDictParsed"


class ConfigDictRaw(TypedDict):
    """
    Data type corresponding to a freshly-read 'config' subdict of a declaration.json file.
    """

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
    default_sched_weight_transform_exp: float
    default_sleep_delta_min: int
    default_sleep_delta_max: int


class ConfigDictParsed(TypedDict):
    """
    Data type corresponding to a freshly-read and type-converted 'config' subdict of a
      declaration.json file.
    """

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
    default_day_start: NKTime
    default_day_end: NKTime
    default_empty_blocks: set[str]
    default_project_dates_missing_offset: int
    default_project_dates_missing_hashmod: int
    default_schedule_weight_interval_min: float
    default_schedule_weight_interval_max: float
    default_sched_weight_transform_exp: float
    default_sleep_delta_min: int
    default_sleep_delta_max: int


class RoutineDictRaw(TypedDict):
    """
    Data type corresponding to a freshly-read routine subdict of the 'routines' subdict of a
      declaration.json file.
    """

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
    """
    Data type corresponding to a freshly-read routine subdict of the 'routines' subdict of a
      declaration.json file.
    """

    name: str
    default_start: NKTime
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
    """
    Data type corresponding to a freshly-read item dict of the 'routine' subdict of a
      declaration.json file.
    """

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
    """
    Data type corresponding to a freshly-read 'tracking' subdict of a declaration.json file.
    """

    activities: list["ActivityDictRaw"]


class TrackingDictParsed(TypedDict):
    """
    Data type corresponding to a freshly-read and type-converted 'tracking' subdict of a
      declaration.json file.
    """

    activities: list["ActivityDictParsed"]


class SubitemDictRaw(TypedDict):
    """
    Data type corresponding to a freshly-read activity subdict of 'tracking' subdict of a
      declaration.json file.
    """

    name: str
    dtype: PromptTypeName
    prompt: NotRequired[str]
    error_prompt: NotRequired[str]
    quit_string: NotRequired[str]
    components: NotRequired[dict[str, "ActivityDictParsed"]]
    subitem: NotRequired["ActivityDictParsed"]


class SubitemDictParsed(TypedDict):
    """
    Data type corresponding to a freshly-read and type-converted activity subdict of the 'tracking'
      subdict of a declaration.json file.
    """

    name: str
    dtype: PromptTypeName
    prompt: NotRequired[str]
    error_prompt: NotRequired[str]
    quit_string: NotRequired[str]
    components: NotRequired[dict[str, "ActivityDictParsed"]]
    subitem: NotRequired["ActivityDictParsed"]


ComponentDictRaw = dict[str, SubitemDictRaw]
ComponentDictParsed = dict[str, SubitemDictParsed]


class ActivityDictRaw(TypedDict):
    """
    Data type corresponding to a freshly-read activity subdict of 'tracking' subdict of a
      declaration.json file.
    """

    name: str
    dtype: PromptTypeName
    desirable: DesirabilityString
    prompt: NotRequired[str]
    error_prompt: NotRequired[str]
    quit_string: NotRequired[str]
    response: NotRequired[TrackingActivityResponseType]
    order: NotRequired[float]
    components: NotRequired[ComponentDictRaw]
    subitem: NotRequired[SubitemDictRaw]


class ActivityDictParsed(TypedDict):
    """
    Data type corresponding to a freshly-read and type-converted activity subdict of the 'tracking'
      subdict of a declaration.json file.
    """

    name: str
    dtype: PromptTypeName
    desirable: DesirabilityString
    prompt: NotRequired[str]
    error_prompt: NotRequired[str]
    quit_string: NotRequired[str]
    response: NotRequired[TrackingActivityResponseType]
    order: float
    components: NotRequired[ComponentDictParsed]
    subitem: NotRequired[SubitemDictParsed]


class PromptDispatcherType(TypedDict):
    """
    Implementation of (quasi) strategy pattern for dynamic selection of prompter, according to
      data type specified for a given activity.
    """

    sequence: Callable[[str, str, PromptTypeName], list]
    time: Callable[[str, str, str], NKTime]
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
    """
    Data type corresponding to a freshly-read 'calendar' subdict a declaration.json file.
    """

    days: dict[str, "DayDictRaw"]


class CalendarDictParsed(TypedDict):
    days: dict[NKDate, "DayDictParsed"]


class DayDictRaw(TypedDict):
    """
    Data type corresponding to a freshly-read day subdict of a 'calendar' subdict a
      declaration.json file.
    """

    start: str
    end: str
    weekday: WeekdayLiteral
    routines: list["RoutineInCalendarDictRaw"]
    entries: list["EntryDictRaw"]


class DayDictParsed(TypedDict):
    start: NKTime
    end: NKTime
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
    start: NKTime
    end: NKTime
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
    start: NKTime
    end: NKTime
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
    assigned_time: Optional[NKTime]


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
    start: NKDate
    end: NKDate
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
    project_id: NotRequired[Optional[str]]
    project_name: NotRequired[Optional[str]]
    priority: NotRequired[float]
    status: NotRequired[StatusLiteral]
    duration: NotRequired[int]
    dependencies: NotRequired[str]
    categories: NotRequired[str]
    notes: NotRequired[str]


class TaskFullDictRaw(TypedDict):
    name: str
    id: str
    priority: float
    project_id: Optional[str]
    project_name: Optional[str]
    status: StatusLiteral
    duration: int
    dependencies: str
    notes: str
    categories: str


class TaskDictParsed(TypedDict):
    name: str
    id: str
    project_id: Optional[ProjectID]
    project_name: Optional[str]
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
    date: NKDate
    entries: list["ScheduleEntryParsed"]


class ScheduleEntryRaw(TypedDict):
    tmp: Literal["placeholder"]


class ScheduleEntryParsed(TypedDict):
    tmp: Literal["placeholder"]
