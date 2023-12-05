from ..pdatetime.ptime import PTime
from .custom_dict_types import ConfigDictParsed, ConfigDictRaw
from .util import split_tag_sequence


def parse_config_dict(conf_dict: ConfigDictRaw) -> ConfigDictParsed:
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
        "default_sched_weight_transform_exp": conf_dict["default_sched_weight_transform_exp"],
        "default_sleep_delta_min": conf_dict["default_sleep_delta_min"],
        "default_sleep_delta_max": conf_dict["default_sleep_delta_max"],
    }
