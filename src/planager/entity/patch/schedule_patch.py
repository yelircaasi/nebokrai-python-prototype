from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ...util import Norg, PDate, PTime, round5, tabularize


class SchedulePatch:
    def __init__(self) -> None:
        ...


class SchedulePatches:
    def __init__(self, schedule_patches: Dict[PDate, SchedulePatch] = {}) -> None:
        self._patches: Dict[PDate, SchedulePatch] = schedule_patches

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "SchedulePatches":
        return cls()

    @property
    def start_date(self) -> PDate:
        if not self._patches:
            return PDate.tomorrow()
        return min(self._patches)

    @property
    def end_date(self) -> PDate:
        if not self._patches:
            return PDate.tomorrow()
        return max(self._patches)

    def __getitem__(self, __key: Any) -> SchedulePatch:
        __key = PDate.ensure_is_pdate(__key)
        if not __key:
            raise ValueError(f"Date not in schedules: {str(__key)}")
        return self._patches.get(__key, SchedulePatch())
