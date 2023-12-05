import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional, Union

from .util import PTime
from .util.serde.custom_dict_types import ConfigDictParsed, ConfigDictRaw
from .util.serde.deserialization import parse_config_dict


class PathManager:  # only supports JSON for now
    """
    Helper class to simplify working with paths in the data directory.
    """

    declaration: Path
    derivation: Path
    tracking: Path
    edit_times: Path
    txt: Path

    def __init__(self, root: Union[Path, str]) -> None:
        self.root = Path(root)
        self.declaration = self.root / "declaration.json"
        self.derivation_dir = self.root / "derivation"
        self.backup_dir = self.root / "backup"
        self.plan = self.derivation_dir / "plan.json"
        self.schedules = self.derivation_dir / "schedules.json"
        self.tracking_dir = self.root / "tracking"
        self.tracking = self.tracking_dir / "tracking.json"
        self.edit_times = self.root / "edit_times.json"
        self.txt = self.root / "txt"
        self.txt_plan = self.txt / "plan.txt"
        self.txt_schedules = self.txt / "schedules.txt"
        self.txt_gantt = self.txt / "gantt.txt"
        self.tmp = self.root / "tmp"
        self.tmp_declaration = self.tmp / "declaration.json"

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
        default_day_start: PTime,
        default_day_end: PTime,
        default_empty_blocks: set[str],
        default_project_dates_missing_offset: int,
        default_project_dates_missing_hashmod: int,
        default_schedule_weight_interval_min: float,
        default_schedule_weight_interval_max: float,
        default_schedule_weight_transform_exponent: float,
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
        self.default_schedule_weight_transform_exponent = default_schedule_weight_transform_exponent

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
            set(re.split(", ?", cfg["default_categories"])),
            cfg["default_ismovable"],
            cfg["default_alignend"],
            cfg["default_day_start"],
            cfg["default_day_end"],
            cfg["default_empty_blocks"],
            int(cfg["default_project_dates_missing_offset"]),
            int(cfg["default_project_dates_missing_hashmod"]),
            float(cfg["default_schedule_weight_interval_min"]),
            float(cfg["default_schedule_weight_interval_max"]),
            float(cfg["default_schedule_weight_transform_exponent"]),
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
            "default_schedule_weight_transform_exponent": self.default_schedule_weight_transform_exponent,
            "default_sleep_priority": self.default_sleep_priority,
            "default_sleep_delta_min": self.default_sleep_delta_min,
            "default_sleep_delta_max": self.default_sleep_delta_max,
        }

    @staticmethod
    def comma_join(string_iterable: Iterable[str]) -> str:
        return ",".join(sorted(string_iterable))

    @property
    def default_routine_dict(self) -> dict[str, dict]:
        return {}

    def __getitem__(self, __key: str) -> Any:
        return self.__dict__[__key]


str_path_to_dirpath_file: Optional[str] = os.environ.get("PLANAGER_CONFIG_FILE")
if not str_path_to_dirpath_file:
    path_to_dirpath_file = Path.home() / ".config/planager/path.txt"
else:
    path_to_dirpath_file = Path(str_path_to_dirpath_file)

if not path_to_dirpath_file.exists():
    raise ValueError(f"No configuration file given; should be at {path_to_dirpath_file}.")
path_to_dir = Path(path_to_dirpath_file)

with open(path_to_dir, encoding="ascii") as f:
    planager_root = Path(f.read().strip())

path_manager = PathManager(planager_root)

with open(path_manager.declaration, encoding="utf-8") as f:
    config_dict: ConfigDictParsed = parse_config_dict(json.load(f)["config"])
config = Config.deserialize(config_dict)

__all__ = ["config", "path_manager"]
