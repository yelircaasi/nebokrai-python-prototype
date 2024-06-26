import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional, Union

from .util import NKTime
from .util.serde.for_config import ConfigDictParsed, ConfigDictRaw, parse_config_dict


class PathManager:
    """
    Helper class to simplify working with paths in the data directory.
    """

    def __init__(self, root: Union[Path, str]) -> None:
        self.root = Path(root)

        self.declaration_dir = self.root / "declaration"
        self.derivation_dir = self.root / "derivation"
        self.backup_dir = self.root / "backup"
        self.tmp_dir = self.root / "tmp"
        self.tracking_dir = self.root / "tracking"

        self.calendar = self.declaration_dir / "calendar.json"
        self.config = self.declaration_dir / "config.json"
        self.roadmaps = self.declaration_dir / "roadmaps.json"
        self.routines = self.declaration_dir / "routines.json"
        self.tracking = self.declaration_dir / "tracking.json"

        self.plan = self.derivation_dir / "plan.json"
        self.schedules = self.derivation_dir / "schedules.json"
        self.txt_dir = self.derivation_dir / "txt"
        self.log_dir = self.derivation_dir / "log"

        self.txt_plan = self.txt_dir / "plan.txt"
        self.txt_schedules = self.txt_dir / "schedules.txt"
        self.txt_gantt = self.txt_dir / "gantt.txt"

        self.tracking_store = self.tracking_dir / "tracking_store.json"

    def backup(self, backup_name: str) -> Path:
        """
        Generates a path to a backup file ensuring that the backups folder exists.
        """
        backup_dir = self.root / "backups"
        if not backup_dir.exists():
            backup_dir.mkdir()
        return backup_dir / backup_name

    def backup_with_date(self, backup_name: str) -> Path:
        """
        Generates a path to a backup file containing a timestamp.
          Ensures that the backups folder exists.
        """
        backup_dir = self.root / "backups"
        if not backup_dir.exists():
            backup_dir.mkdir()
        split_list = backup_name.split(".")
        split_list[-2] += str(datetime.now()).split(".", maxsplit=1)[0].replace(" ", "_")
        backup_name = ".".join(split_list[:-1])
        return backup_dir / backup_name

    def _last_backup(self, backup_name: str) -> Path:
        backup_files = filter(lambda f: f.startswith(backup_name), os.listdir(self.backup_dir))
        return self.backup_dir / sorted(backup_files)[-1]

    @property
    def last_schedules_backup(self) -> Path:
        return self._last_backup("schedules")

    @property
    def last_plan_backup(self) -> Path:
        return self._last_backup("plan")

    def _backup(self, backup_name) -> Path:
        return self.backup_dir / f"{backup_name}_{self.timestamp}.json"

    @property
    def plan_backup(self) -> Path:
        return self._backup("plan")

    @property
    def schedules_backup(self) -> Path:
        return self._backup("schedules")

    @property
    def timestamp(self) -> str:
        """
        Creates a timestamp string corresponding to whenever this property is invoked, typically to
        record when a file was last written.
        """
        dt = datetime.now()
        return str(dt).split(".", maxsplit=1)[0].replace(" ", "_").replace(":", "-")

    def __str__(self) -> str:
        width = 100
        double_bar = width * "="
        single_bar = width * "-"
        return "\n".join(
            (
                double_bar,
                f"root:               {self.root}",
                single_bar,
                f"declaration_dir:    {self.declaration_dir}",
                f"derivation_dir:     {self.derivation_dir}",
                f"backup_dir:         {self.backup_dir}",
                f"tmp_dir:            {self.tmp_dir}",
                f"txt_dir:            {self.txt_dir}",
                f"log_dir:            {self.log_dir}",
                f"tracking_dir:       {self.tracking_dir}",
                single_bar,
                f"calendar:           {self.calendar}",
                f"config:             {self.config}",
                f"roadmaps:           {self.roadmaps}",
                f"routines:           {self.routines}",
                f"tracking:           {self.tracking}",
                single_bar,
                f"plan:               {self.plan}",
                f"schedules:          {self.schedules}",
                single_bar,
                f"txt_plan:           {self.txt_plan}",
                f"txt_schedules:      {self.txt_schedules}",
                f"txt_gantt:          {self.txt_gantt}",
                single_bar,
                f"tracking_store:     {self.tracking_store}",
                double_bar,
            )
        )

    def __repr__(self) -> str:
        return str(self)


class Config:
    """
    Holds all config options passed in from declaration.
    """

    repr_width: int

    default_priority: float
    default_sleep_priority: float
    default_duration: int
    default_interval: int
    default_cluster_size: int
    default_order: float
    default_normaltime: int
    default_idealtime_factor: float
    default_mintime_factor: float
    default_maxtime_factor: float
    default_categories: set
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

    def __init__(
        self,
        repr_width: int,
        default_priority: float,
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
        default_day_start: NKTime,
        default_day_end: NKTime,
        default_empty_blocks: set[str],
        default_project_dates_missing_offset: int,
        default_project_dates_missing_hashmod: int,
        default_schedule_weight_interval_min: float,
        default_schedule_weight_interval_max: float,
        default_sched_weight_transform_exp: float,
        default_sleep_priority: float,
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
        self.default_sched_weight_transform_exp = default_sched_weight_transform_exp

        self.default_sleep_priority = default_sleep_priority
        self.default_sleep_delta_min = default_sleep_delta_min
        self.default_sleep_delta_max = default_sleep_delta_max

    @classmethod
    def deserialize(cls, cfg: ConfigDictParsed) -> "Config":
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
            cls.comma_split(
                cfg["default_categories"]
            ),  # set(re.split(", ?", cfg["default_categories"])),
            cfg["default_ismovable"],
            cfg["default_alignend"],
            cfg["default_day_start"],
            cfg["default_day_end"],
            cfg["default_empty_blocks"],
            int(cfg["default_project_dates_missing_offset"]),
            int(cfg["default_project_dates_missing_hashmod"]),
            float(cfg["default_schedule_weight_interval_min"]),
            float(cfg["default_schedule_weight_interval_max"]),
            float(cfg["default_sched_weight_transform_exp"]),
            int(cfg["default_sleep_priority"]),
            int(cfg["default_sleep_delta_min"]),
            int(cfg["default_sleep_delta_max"]),
        )

    def serialize(self) -> ConfigDictRaw:
        print("Not yet implemented")
        return {
            "repr_width": self.repr_width,
            "default_priority": self.default_priority,
            "default_duration": self.default_duration,
            "default_interval": self.default_interval,
            "default_cluster_size": self.default_cluster_size,
            "default_order": self.default_order,
            "default_normaltime": self.default_normaltime,
            "default_idealtime_factor": self.default_idealtime_factor,
            "default_mintime_factor": self.default_mintime_factor,
            "default_maxtime_factor": self.default_maxtime_factor,
            "default_categories": self.comma_join(self.default_categories),
            "default_ismovable": self.default_ismovable,
            "default_alignend": self.default_alignend,
            "default_day_start": str(self.default_day_start),
            "default_day_end": str(self.default_day_end),
            "default_empty_blocks": self.comma_join(self.default_empty_blocks),
            "default_project_dates_missing_offset": self.default_project_dates_missing_offset,
            "default_project_dates_missing_hashmod": self.default_project_dates_missing_hashmod,
            "default_schedule_weight_interval_min": self.default_schedule_weight_interval_min,
            "default_schedule_weight_interval_max": self.default_schedule_weight_interval_max,
            "default_sched_weight_transform_exp": self.default_sched_weight_transform_exp,
            "default_sleep_priority": self.default_sleep_priority,
            "default_sleep_delta_min": self.default_sleep_delta_min,
            "default_sleep_delta_max": self.default_sleep_delta_max,
        }

    def comma_join(self, string_iterable: Iterable[str]) -> str:
        # string_list = self.comma_split(comma_sep_string)
        # print(f"{string_list=}")
        return ",".join(sorted(string_iterable))

    @staticmethod
    def comma_split(comma_sep_string: str) -> set[str]:
        return set(filter(bool, re.split(" ?, ?", comma_sep_string.strip())))

    @property
    def default_routine_dict(self) -> dict[str, dict]:
        return {}

    def __getitem__(self, __key: str) -> Any:
        return self.__dict__[__key]


str_path_to_dirpath_file: Optional[str] = os.environ.get("NEBOKRAI_ROOT_FILE")
if not str_path_to_dirpath_file:
    path_to_dirpath_file = Path.home() / ".config/nebokrai/path.txt"
else:
    path_to_dirpath_file = Path(str_path_to_dirpath_file)

if not path_to_dirpath_file.exists():
    raise ValueError(f"No configuration file given; should be at {path_to_dirpath_file}.")
path_to_dir = Path(path_to_dirpath_file)

with open(path_to_dir, encoding="ascii") as f:
    nebokrai_root = Path(f.read().strip())

path_manager = PathManager(nebokrai_root)

with open(path_manager.config, encoding="utf-8") as f:
    config_dict: ConfigDictParsed = parse_config_dict(json.load(f))
config = Config.deserialize(config_dict)

__all__ = ["config", "path_manager"]
