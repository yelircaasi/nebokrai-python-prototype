from typing import Iterable, Union

from ...configuration import config
from ...util.entity_ids import ProjectID, TaskID
from ...util.nkdatetime.nkdate import NKDate
from ..elementary_types import Natural, T, TimeAmountRaw, true_strings
from ..nkdatetime.nktime import NKTime, NoneTime
from .custom_dict_types import (
    ActivityDictParsed,
    ActivityDictRaw,
    CalendarDictParsed,
    CalendarDictRaw,
    DayDictParsed,
    DayDictRaw,
    DayLogDictRaw,
    DeclarationDictParsed,
    DeclarationDictRaw,
    EntryDictParsed,
    EntryDictRaw,
    PromptResponseParserDispatcher,
    RoadmapDictParsed,
    RoadmapDictRaw,
    RoadmapsDictParsed,
    RoadmapsDictRaw,
    RoutineDictParsed,
    RoutineDictRaw,
    RoutineInCalendarDictParsed,
    RoutineInCalendarDictRaw,
    RoutineItemDictParsed,
    RoutineItemDictRaw,
    RoutinesDictRaw,
    TaskDictParsed,
    TaskDictRaw,
    TaskFullDictRaw,
    TrackingDictParsed,
    TrackingDictRaw,
)
from .for_config import parse_config_dict
from .util import split_tag_sequence


def parse_declaration_dict(decl_dict: DeclarationDictRaw) -> DeclarationDictParsed:
    routines_dict: RoutinesDictRaw = decl_dict["routines"]
    return {
        "config": parse_config_dict(decl_dict["config"]),
        "routines": {k: parse_routine_dict(v) for k, v in routines_dict.items()},
        "tracking": parse_tracking_dict(decl_dict["tracking"]),
        "calendar": parse_calendar_dict(decl_dict["calendar"]),
        "roadmaps": parse_roadmaps_dict(decl_dict["roadmaps"]),
    }


def parse_routine_dict(routine_dict: "RoutineDictRaw") -> "RoutineDictParsed":
    return {
        "name": routine_dict["name"],
        "default_start": NKTime.from_string(routine_dict["default_start"]),
        "default_priority": routine_dict["default_priority"],
        "default_notes": routine_dict["default_notes"],
        "default_normaltime": routine_dict["default_normaltime"],
        "default_idealtime": routine_dict["default_idealtime"],
        "default_mintime": routine_dict["default_mintime"],
        "default_maxtime": routine_dict["default_maxtime"],
        "default_blocks": routine_dict["default_blocks"],
        "default_order": routine_dict["default_order"],
        "items": list(map(parse_routine_item, routine_dict["items"])),
    }


def parse_routine_item(item_dict: RoutineItemDictRaw) -> RoutineItemDictParsed:
    return {
        "name": item_dict["name"],
        "id": item_dict["id"],
        "priority": item_dict["priority"],
        "normaltime": item_dict["normaltime"],
        "idealtime": item_dict["idealtime"],
        "mintime": item_dict["mintime"],
        "maxtime": item_dict["maxtime"],
        "order": item_dict["order"],
    }


def parse_tracking_dict(tracking_dict: TrackingDictRaw) -> TrackingDictParsed:
    return {
        "activities": list(map(parse_activity_dict, tracking_dict["activities"])),
    }


def parse_activity_dict(activity_dict: ActivityDictRaw) -> ActivityDictParsed:
    return {
        "name": activity_dict["name"],
        "dtype": activity_dict.get("dtype"),
        "prompt": activity_dict["prompt"].strip(" ") + "  ",
        "scoring": activity_dict["scoring"],
        "order": activity_dict.get("order") or config.default_order,
    }


def parse_calendar_dict(calendar_dict: CalendarDictRaw) -> CalendarDictParsed:
    return {
        NKDate.from_string(k): parse_calendar_day(v) for k, v in calendar_dict.items()
    }


def parse_calendar_day(day_dict: DayDictRaw) -> DayDictParsed:
    return {
        "weekday": day_dict["weekday"],
        "start": NKTime.from_string(day_dict["start"]),
        "end": NKTime.from_string(day_dict["end"]),
        "routines": list(map(parse_calendar_routine, day_dict["routines"])),
        "entries": list(map(parse_entry_dict, day_dict["entries"])),
    }


def parse_calendar_routine(
    cal_routine_dict: RoutineInCalendarDictRaw,
) -> RoutineInCalendarDictParsed:
    return {
        "name": cal_routine_dict["name"],
        "start": NKTime.from_string(cal_routine_dict["start"]),
        "end": NKTime.from_string(cal_routine_dict["end"]),
        "priority": cal_routine_dict["priority"],
        "normaltime": cal_routine_dict["normaltime"],
        "idealtime": cal_routine_dict["idealtime"],
        "mintime": cal_routine_dict["mintime"],
        "maxtime": cal_routine_dict["maxtime"],
        "ismovable": cal_routine_dict["ismovable"],
        "order": cal_routine_dict["order"],
    }


def parse_task_dict(task_dict: TaskDictRaw | TaskFullDictRaw) -> TaskDictParsed:
    deps_raw: str = task_dict.get("dependencies") or ""
    cats_raw: str = task_dict.get("categories") or ""
    dependencies = set(map(TaskID.from_string, filter(bool, deps_raw)))
    categories = set(filter(bool, cats_raw)) or set()

    project_id_str = task_dict.get("project_id")

    return {
        "name": task_dict["name"],
        "id": task_dict["name"],
        "project_name": task_dict.get("project_name"),
        "project_id": ProjectID.from_string(project_id_str) if project_id_str else None,
        "priority": task_dict.get("priority"),
        "notes": task_dict.get("notes") or "",
        "duration": task_dict.get("duration") or config.default_duration,
        "status": task_dict.get("status"),
        "dependencies": dependencies,
        "categories": categories,
    }


def parse_entry_dict(entry_dict: EntryDictRaw | RoutineItemDictRaw) -> EntryDictParsed:
    start: Union[NKTime, NoneTime] = NKTime.from_string(str(entry_dict.get("start")))
    end: Union[NKTime, NoneTime] = NKTime.from_string(str(entry_dict.get("end")))
    normaltime = entry_dict.get("normaltime") or start.timeto(end) if (start and end) else config.default_normaltime
    return {
        "name": entry_dict["name"],
        "priority": entry_dict["priority"],
        "normaltime": normaltime,
        "start": NKTime.from_string(str(entry_dict.get("start"))),
        "end": NKTime.from_string(str(entry_dict.get("end"))),
        "mintime": entry_dict.get("mintime") or int(config.default_mintime_factor * normaltime),
        "maxtime": entry_dict.get("maxtime") or int(config.default_maxtime_factor * normaltime),
        "idealtime": entry_dict.get("idealtime")
        or int(config.default_idealtime_factor * normaltime),
        "categories": split_tag_sequence(entry_dict.get("categories") or "")
        or config.default_categories,
        "notes": entry_dict.get("notes") or "",
        "alignend": entry_dict.get("alignend") or config.default_alignend,
        "order": entry_dict.get("order") or config.default_order,
        "subentries": list(map(parse_entry_dict, entry_dict.get("subentries") or [])),
        "blocks": split_tag_sequence(entry_dict.get("blocks") or ""),
        "ismovable": entry_dict.get("ismovable") or config.default_ismovable,
        "assigned_time": NKTime.from_string(str(entry_dict.get("assigned_time"))),
    }


def parse_roadmaps_dict(roadmaps_dict: RoadmapsDictRaw) -> RoadmapsDictParsed:
    return {k: parse_roadmap_dict(roadmaps_dict[k]) for k in roadmaps_dict}


def parse_roadmap_dict(roadmap_dict: RoadmapDictRaw) -> RoadmapDictParsed:
    print(roadmap_dict)
    return {"tmp": "placeholder"}


def identity(t: T) -> T:
    return t


def parse_day_log(log_dict: DayLogDictRaw) -> DayLogDictRaw:
    dispatch: PromptResponseParserDispatcher = {
        "boolean": parse_boolean,
        "natural": parse_natural,
        "natural_sequence": parse_natural_sequence,
        "string": identity,
        "time": NKTime.from_string,
        "time_amount": parse_time_amount,
        "timed_distance": identity,
        "timed_distance_with_elevation": identity,
    }
    print(log_dict)
    print(dispatch)
    return {}


def parse_boolean(s: str) -> bool:
    return s.lower() in true_strings


def parse_natural(n: Natural) -> Natural:
    assert n >= 0
    return n


def parse_natural_sequence(natural_sequence: Iterable[Natural]) -> list[Natural]:
    return list(map(parse_natural, natural_sequence))


def parse_time_amount(time_amount: TimeAmountRaw) -> int:
    return (
        time_amount if isinstance(time_amount, int) else NKTime.from_string(time_amount).tominutes()
    )
