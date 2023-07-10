from typing import Optional

from ...entity import Schedule, SchedulePatch
from ...util import ConfigType


class SchedulePatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        self._config = config

    def __call__(
        self, schedule: Schedule, schedule_patches: Optional[SchedulePatch]
    ) -> Schedule:
        if not schedule_patches:
            return schedule  # TODO
        return schedule
