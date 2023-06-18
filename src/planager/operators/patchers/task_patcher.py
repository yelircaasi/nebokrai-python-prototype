from typing import Optional

from planager import entities
from planager.config import ConfigType


class TaskPatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        self._config = config

    def __call__(
        self, task: entities.Task, task_patch: Optional[entities.TaskPatch]
    ) -> entities.Task:
        if not task_patch:
            return task
        return task  # TODO
