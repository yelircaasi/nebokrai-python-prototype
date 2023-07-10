from typing import Optional

from planager.config import ConfigType
from planager.entity.base.schedule import Schedule
from planager.entity.patch.schedule_patch import SchedulePatch


class SchedulePatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        self._config = config

    def __call__(
        self, schedule: Schedule, schedule_patches: Optional[SchedulePatch]
    ) -> Schedule:
        if not schedule_patches:
            return schedule  # TODO
        return schedule
