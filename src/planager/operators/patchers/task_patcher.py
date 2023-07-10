from typing import Optional

from planager.config import ConfigType
from planager.entity.base.task import Task
from planager.entity.patch.task_patch import TaskPatch


class TaskPatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        self._config = config

    def __call__(self, task: Task, task_patch: Optional[TaskPatch]) -> Task:
        if not task_patch:
            return task
        return task  # TODO
