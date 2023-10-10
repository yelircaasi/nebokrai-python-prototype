import re
from typing import Any

from .util import PTime


class Config:
    """
    Holds all config options passed in from declaration.
    """

    repr_width: int

    default_priority: int
    default_sleep_priority: int
    default_duration: int
    default_interval: int
    default_cluster_size: int
    default_order: int
    default_normaltime: int
    default_idealtime_factor: float
    default_mintime_factor: float
    default_maxtime_factor: float
    default_categories: set
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

    def __init__(
        self,
        repr_width: int,
        default_priority: int,
        default_duration: int,
        default_interval: int,
        default_cluster_size: int,
        default_order: int,
        default_normaltime: int,
        default_idealtime_factor: float,
        default_mintime_factor: float,
        default_maxtime_factor: float,
        default_categories: set,
        default_ismovable: bool,
        default_alignend: bool,
        default_day_start: PTime,
        default_day_end: PTime,
        default_empty_blocks: set[str],
        default_project_dates_missing_offset: int,
        default_project_dates_missing_hashmod: int,
        default_schedule_weight_interval_min: float,
        default_schedule_weight_interval_max: float,
        default_schedule_weight_transform_exponent: float,
        default_sleep_priority: int,
        default_sleep_delta_min: int,
        default_sleep_delta_max: int,
    ) -> None:
        self.repr_width = repr_width

        self.default_priority = default_priority
        self.default_duration = default_duration
        self.default_interval = default_interval
        self.default_cluster_size = default_cluster_size
        self.default_order = default_order
        self.default_normaltime = default_normaltime
        self.default_idealtime_factor = default_idealtime_factor
        self.default_mintime_factor = default_mintime_factor
        self.default_maxtime_factor = default_maxtime_factor
        self.default_categories = default_categories
        self.default_ismovable = default_ismovable
        self.default_alignend = default_alignend

        self.default_day_start = default_day_start
        self.default_day_end = default_day_end
        self.default_empty_blocks = default_empty_blocks
        self.default_project_dates_missing_offset = default_project_dates_missing_offset
        self.default_project_dates_missing_hashmod = default_project_dates_missing_hashmod
        self.default_schedule_weight_interval_min = default_schedule_weight_interval_min
        self.default_schedule_weight_interval_max = default_schedule_weight_interval_max
        self.default_schedule_weight_transform_exponent = default_schedule_weight_transform_exponent

        self.default_sleep_priority = default_sleep_priority
        self.default_sleep_delta_min = default_sleep_delta_min
        self.default_sleep_delta_max = default_sleep_delta_max

    @classmethod
    def from_dict(cls, cfg: dict) -> "Config":
        return cls(
            int(cfg["repr_width"]),
            int(cfg["default_priority"]),
            int(cfg["default_duration"]),
            int(cfg["default_interval"]),
            int(cfg["default_cluster_size"]),
            int(cfg["default_order"]),
            int(cfg["default_normaltime"]),
            float(cfg["default_idealtime_factor"]),
            float(cfg["default_mintime_factor"]),
            float(cfg["default_maxtime_factor"]),
            set(re.split(", ?", cfg["default_categories"])),
            cfg["default_ismovable"],
            cfg["default_alignend"],
            PTime.from_string(cfg["default_day_start"]),
            PTime.from_string(cfg["default_day_end"]),
            set(re.split(", ?", cfg["default_empty_blocks"])),
            int(cfg["default_project_dates_missing_offset"]),
            int(cfg["default_project_dates_missing_hashmod"]),
            float(cfg["default_schedule_weight_interval_min"]),
            float(cfg["default_schedule_weight_interval_max"]),
            float(cfg["default_schedule_weight_transform_exponent"]),
            int(cfg["default_sleep_priority"]),
            int(cfg["default_sleep_delta_min"]),
            int(cfg["default_sleep_delta_max"]),
        )

    @property
    def default_routine_dict(self) -> dict[str, dict]:
        return {}

    def __getitem__(self, __key: str) -> Any:
        return self.__dict__[__key]
