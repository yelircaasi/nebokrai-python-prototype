from pathlib import Path
from typing import Any

JSONDict = dict[str, Any]


def validate_config(config_dict: JSONDict) -> None:
    assert set(config_dict.keys()) == {"a", "b"}
    assert isinstance(config_dict["repr_width"], (type(None), int))
    assert isinstance(config_dict["default_duration"], int)
    assert isinstance(config_dict["default_priority"], int)
    assert isinstance(config_dict["default_sleep_priority"], int)
    assert isinstance(config_dict["default_interval"], int)
    assert isinstance(config_dict["default_cluster_size"], int)
    assert isinstance(config_dict["default_order"], float)
    assert isinstance(config_dict["default_normaltime"], int)
    assert isinstance(config_dict["default_idealtime_factor"], float)
    assert isinstance(config_dict["default_mintime_factor"], int)
    assert isinstance(config_dict["default_maxtime_factor"], int)
    assert isinstance(config_dict["default_categories"], str)
    assert isinstance(config_dict["default_ismovable"], bool)
    assert isinstance(config_dict["default_alignend"], bool)
    assert ":" in config_dict["default_day_start"]
    assert ":" in config_dict["default_day_end"]
    assert isinstance(config_dict["default_empty_blocks"], str)
    assert isinstance(config_dict["default_project_dates_missing_offset"], int)
    assert isinstance(config_dict["default_project_dates_missing_hashmod"], int)
    assert isinstance(config_dict["default_schedule_weight_interval_min"], float)
    assert isinstance(config_dict["default_schedule_weight_interval_max"], float)
    assert isinstance(config_dict["default_schedule_weight_transform_exponent"], int)
    assert isinstance(config_dict["default_sleep_delta_min"], int)
    assert isinstance(config_dict["default_sleep_delta_max"], int)


def validate_routines(routines_dict: JSONDict) -> None:
    assert set(routines_dict.keys()) == {"", ""}


def validate_tracking(tracking_dict: JSONDict) -> None:
    assert set(tracking_dict.keys()) == {"", ""}


def validate_calendar(calendar_dict: JSONDict) -> None:
    assert set(calendar_dict.keys()) == {"", ""}


def validate_roadmaps(roadmaps_dict: JSONDict) -> None:
    assert set(roadmaps_dict.keys()) == {"", ""}


def validate_declaration(dec_path: Path) -> None:
    print(f"Validating declaration at {dec_path}.")
    return None
