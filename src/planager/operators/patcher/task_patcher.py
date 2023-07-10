from typing import Optional

from ...config import ConfigType
from ...entity.base.task import Task
from ...entity.patch.task_patch import TaskPatch


class TaskPatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        self._config = config

    def __call__(self, task: Task, task_patch: Optional[TaskPatch]) -> Task:
        if not task_patch:
            return task
        return task  # TODO
