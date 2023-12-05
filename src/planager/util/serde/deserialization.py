import re
from dataclasses import dataclass
from typing import Annotated, Callable, Iterable, Literal, Protocol, TypeVar, Union

from ...configuration import config
from ...util.entity_ids import TaskID
from ...util.pdatetime.pdate import PDate
from ..elementary_types import Natural, T, TimeAmountRaw, TrueString, true_strings
from ..pdatetime.ptime import PTime
from .custom_dict_types import (
    ActivityDictParsed,
    ActivityDictRaw,
    CalendarDictParsed,
    CalendarDictRaw,
    ConfigDictParsed,
    ConfigDictRaw,
    DayDictParsed,
    DayDictRaw,
    DayLogDictParsed,
    DayLogDictRaw,
    DeclarationDictParsed,
    DeclarationDictRaw,
    EntryDictParsed,
    EntryDictRaw,
    PromptResponseParserDispatcher,
    PromptResponseType,
    RawPromptResponseType,
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
    RoutinesDictParsed,
    RoutinesDictRaw,
    TaskDictFullRaw,
    TaskDictParsed,
    TaskDictRaw,
    TimedDistance,
    TimedDistanceWithElevation,
    TrackingDictParsed,
    TrackingDictRaw,
)


def split_tag_sequence(tags: str) -> set[str]:
    return set(re.split(r", ?|,? ", tags))


def parse_declaration_dict(decl_dict: DeclarationDictRaw) -> DeclarationDictParsed:
    routines_dict: RoutinesDictRaw = decl_dict["routines"]
    return {
        "config": parse_config_dict(decl_dict["config"]),
        "routines": {k: parse_routine_dict(v) for k, v in routines_dict.items()},
        "tracking": parse_tracking_dict(decl_dict["tracking"]),
        "calendar": parse_calendar_dict(decl_dict["calendar"]),
        "roadmaps": parse_roadmaps_dict(decl_dict["roadmaps"]),
    }


def parse_config_dict(conf_dict: ConfigDictRaw) -> ConfigDictParsed:
    """ """
    return {
        "repr_width": conf_dict["repr_width"],
        "default_duration": conf_dict["default_duration"],
        "default_priority": conf_dict["default_priority"],
        "default_sleep_priority": conf_dict["default_sleep_priority"],
        "default_interval": conf_dict["default_interval"],
        "default_cluster_size": conf_dict["default_cluster_size"],
        "default_order": conf_dict["default_order"],
        "default_normaltime": conf_dict["default_normaltime"],
        "default_idealtime_factor": conf_dict["default_idealtime_factor"],
        "default_mintime_factor": conf_dict["default_mintime_factor"],
        "default_maxtime_factor": conf_dict["default_maxtime_factor"],
        "default_categories": conf_dict["default_categories"],
        "default_ismovable": conf_dict["default_ismovable"],
        "default_alignend": conf_dict["default_alignend"],
        "default_day_start": PTime.from_string(conf_dict["default_day_start"]),
        "default_day_end": PTime.from_string(conf_dict["default_day_end"]),
        "default_empty_blocks": split_tag_sequence(conf_dict["default_empty_blocks"]),
        "default_project_dates_missing_offset": conf_dict["default_project_dates_missing_offset"],
        "default_project_dates_missing_hashmod": conf_dict["default_project_dates_missing_hashmod"],
        "default_schedule_weight_interval_min": conf_dict["default_schedule_weight_interval_min"],
        "default_schedule_weight_interval_max": conf_dict["default_schedule_weight_interval_max"],
        "default_schedule_weight_transform_exponent": conf_dict[
            "default_schedule_weight_transform_exponent"
        ],
        "default_sleep_delta_min": conf_dict["default_sleep_delta_min"],
        "default_sleep_delta_max": conf_dict["default_sleep_delta_max"],
    }


def parse_routine_dict(routine_dict: "RoutineDictRaw") -> "RoutineDictParsed":
    return {
        "name": routine_dict["name"],
        "default_start": PTime.from_string(routine_dict["default_start"]),
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
        "dtype": activity_dict["dtype"],
        "desirable": activity_dict["desirable"],
        "prompt": activity_dict["prompt"].strip(" ") + "  ",
        "order": activity_dict.get("order") or config.default_order,
    }


def parse_calendar_dict(calendar_dict: CalendarDictRaw) -> CalendarDictParsed:
    return {
        "days": {
            PDate.from_string(k): parse_calendar_day(v) for k, v in calendar_dict["days"].items()
        },
    }


def parse_calendar_day(day_dict: DayDictRaw) -> DayDictParsed:
    return {
        "weekday": day_dict["weekday"],
        "start": PTime.from_string(day_dict["start"]),
        "end": PTime.from_string(day_dict["end"]),
        "routines": list(map(parse_calendar_routine, day_dict["routines"])),
        "entries": list(map(parse_entry_dict, day_dict["entries"])),
    }


def parse_calendar_routine(
    cal_routine_dict: RoutineInCalendarDictRaw,
) -> RoutineInCalendarDictParsed:
    return {
        "name": cal_routine_dict["name"],
        "start": PTime.from_string(cal_routine_dict["start"]),
        "end": PTime.from_string(cal_routine_dict["end"]),
        "priority": cal_routine_dict["priority"],
        "normaltime": cal_routine_dict["normaltime"],
        "idealtime": cal_routine_dict["idealtime"],
        "mintime": cal_routine_dict["mintime"],
        "maxtime": cal_routine_dict["maxtime"],
        "ismovable": cal_routine_dict["ismovable"],
        "order": cal_routine_dict["order"],
    }


def parse_task_dict(task_dict: TaskDictRaw | TaskDictFullRaw) -> TaskDictParsed:
    def parse_id(s: str) -> TaskID:
        res = re.split(r"\W", s)
        return TaskID(res[0], res[1], res[2])

    deps_raw: str = task_dict.get("dependencies") or ""
    cats_raw: str = task_dict.get("categories") or ""
    dependencies = set(map(parse_id, filter(bool, deps_raw)))
    categories = set(filter(bool, cats_raw)) or set()

    return {
        "name": task_dict["name"],
        "id": task_dict["name"],
        "priority": task_dict.get("priority"),  # , config.default_priority),
        "notes": task_dict.get("notes") or "",
        "duration": task_dict.get("duration") or config.default_duration,
        "status": task_dict.get("status"),
        "status": task_dict.get("status"),
        "dependencies": dependencies,
        "categories": categories,
    }


def parse_entry_dict(entry_dict: EntryDictRaw | RoutineItemDictRaw) -> EntryDictParsed:
    normaltime = entry_dict["normaltime"]
    return {
        "name": entry_dict["name"],
        "priority": entry_dict["priority"],
        "normaltime": normaltime,
        "start": PTime.from_string(entry_dict.get("start")),
        "end": PTime.from_string(entry_dict.get("end")),
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
        "assigned_time": PTime.from_string(entry_dict.get("assigned_time")),
    }


def parse_roadmaps_dict(roadmaps_dict: RoadmapsDictRaw) -> RoadmapsDictParsed:
    return {k: parse_roadmap_dict(roadmaps_dict[k]) for k in roadmaps_dict}


def parse_roadmap_dict(roadmap_dict: RoadmapDictRaw) -> RoadmapDictParsed:
    return {"tmp": "placeholder"}


def identity(t: T) -> T:
    return t


def parse_day_log(log_dict: DayLogDictRaw) -> DayLogDictRaw:
    dispatch: PromptResponseParserDispatcher = {
        "boolean": parse_boolean,
        "natural": parse_natural,
        "natural_sequence": parse_natural_sequence,
        "string": identity,
        "time": PTime.from_string,
        "time_amount": parse_time_amount,
        "timed_distance": identity,
        "timed_distance_with_elevation": identity,
        # "typed_list": parse_typed_list,
    }
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
        time_amount if isinstance(time_amount, int) else PTime.from_string(time_amount).tominutes()
    )


# def parse_typed_list(raw_typed_list: list[RawPromptResponseType]) -> list[PromptResponseType]:
#     return []
