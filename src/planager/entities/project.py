from typing import Any, List, Optional

from planager.entities.task import TaskPatches, Tasks


class Project:
    def __init__(self) -> None:
        self.x = ...

    def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
        ...


class Projects:
    def __init__(self, projects: List[Project] = []) -> None:
        self._projects = projects

    def __getitem__(self, __name: str) -> Any:
        schedule = ...
        return schedule
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
        tasks = Tasks()
        for _project in self._projects:
            for task in _project.get_tasks():
                tasks.add(task)
        return tasks
    