from pathlib import Path

from ..util.serde.custom_dict_types import (
    CalendarDictRaw,
    ConfigDictRaw,
    RoadmapsDictRaw,
    RoutinesDictRaw,
    TrackingDictRaw,
)


def validate_config(  # pylint: disable=too-many-branches,too-many-statements
    config_dict: ConfigDictRaw,
) -> None:
    """
    Checks 'config' subdict of the declaration.json file for validity.
      All attributes must be present and of the proper form.
    """
    if not set(config_dict.keys()) == {"a", "b"}:
        raise ValueError("")
    if not isinstance(config_dict["repr_width"], (type(None), int)):
        raise ValueError("")
    if not isinstance(config_dict["default_duration"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_priority"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_sleep_priority"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_interval"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_cluster_size"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_order"], float):
        raise ValueError("")
    if not isinstance(config_dict["default_normaltime"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_idealtime_factor"], float):
        raise ValueError("")
    if not isinstance(config_dict["default_mintime_factor"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_maxtime_factor"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_categories"], str):
        raise ValueError("")
    if not isinstance(config_dict["default_ismovable"], bool):
        raise ValueError("")
    if not isinstance(config_dict["default_alignend"], bool):
        raise ValueError("")
    if not ":" in config_dict["default_day_start"]:
        raise ValueError("")
    if not ":" in config_dict["default_day_end"]:
        raise ValueError("")
    if not isinstance(config_dict["default_empty_blocks"], str):
        raise ValueError("")
    if not isinstance(config_dict["default_project_dates_missing_offset"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_project_dates_missing_hashmod"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_schedule_weight_interval_min"], float):
        raise ValueError("")
    if not isinstance(config_dict["default_schedule_weight_interval_max"], float):
        raise ValueError("")
    if not isinstance(config_dict["default_sched_weight_transform_exp"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_sleep_delta_min"], int):
        raise ValueError("")
    if not isinstance(config_dict["default_sleep_delta_max"], int):
        raise ValueError("")


def validate_routines(routines_dict: RoutinesDictRaw) -> None:
    """
    Checks 'routines' subdict of the declaration.json file for validity.
      All attributes must me present and of the proper form.
    """
    if not set(routines_dict.keys()) == {"", "."}:
        raise ValueError("")


def validate_tracking(tracking_dict: TrackingDictRaw) -> None:
    """
    Checks 'tracking' subdict of the declaration.json file for validity.
      All attributes must me present and of the proper form.
    """
    if not set(tracking_dict.keys()) == {"", "."}:
        raise ValueError("")


def validate_calendar(calendar_dict: CalendarDictRaw) -> None:
    """
    Checks 'calendar' subdict of the declaration.json file for validity.
      All attributes must me present and of the proper form.
    """
    if not set(calendar_dict.keys()) == {"", "."}:
        raise ValueError("")


def validate_roadmaps(roadmaps_dict: RoadmapsDictRaw) -> None:
    """
    Checks 'roadmaps' subdict of the declaration.json file for validity.
      All attributes must me present and of the proper form.
    """
    if not set(roadmaps_dict.keys()) == {"", "."}:
        raise ValueError("")


def validate_declaration(dec_path: Path) -> None:
    """
    Checks entire declaration.json file for validity.
      All attributes must me present and of the proper form.
    """
    print(f"Validating declaration at {dec_path}.")
