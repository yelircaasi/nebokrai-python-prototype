from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from planager.entities import TaskPatches, Tasks
from planager.utils.data.norg.norg_utils import Norg


class Project:
    def __init__(self) -> None:
        self.x = ...

    def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
        ...

    @classmethod
    def from_norg_path(self, norg_path: Path) -> "Project":
        norg = Norg.from_path(norg_path)
        for item in norg["items"]:
            if "||" in item:
                ...
            else:
                _, link = Norg.parse_link(item)
                path = norg_path.parent / link.replace("$/", "")
                project = Project.from_norg(path)


class Projects:
    def __init__(self, projects: List[Project] = []) -> None:
        self._projects: Dict[Tuple, Project] = {project.id: project for project in projects}
        self._tasks: Tasks = self._get_tasks()

    @property
    def projects(self) -> List[Project]:
        return list(self._projects.values())
    
    @projects.setter
    def projects(self, value):
        raise ValueError("Cannot directly set projects attribute.")
    
    def add(self, project: Project) -> None:
        self.projects.update({project.id: project})

    def __getitem__(self, __id: tuple) -> Any:
        if len(__id) == 2:
            return self._projects[__id]
        elif len(__id) == 3:
            return self._tasks[__id]
        else:
            raise KeyError(f"Invalid key for `Projects`: {__id}.")
    
    def __setitem__(self, __id: str, __value: Any) -> None:
        if len(__id) == 2:
            self._projects.update({__id: __value})
        elif len(__id) == 3:
            return self._tasks.update({__id: __value})
        else:
            raise KeyError(f"Invalid key for `Projects`: {__id}.")

    def _get_tasks(self) -> Tasks:
        tasks = Tasks()
        for _project in self._projects:
            for task in _project.get_tasks():
                tasks.add(task)
        return tasks
    
    def patch_tasks(self, task_patches: Optional[TaskPatches] = None):
        ...
    
    def order_by_dependency(self) -> None:
        ...

    