from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from ...util import tabularize
from ..base.project import Project
from ..container.tasks import Tasks
from ..patch.task_patch import TaskPatches


class Projects:
    def __init__(self, projects: List[Project] = []) -> None:
        self._projects: Dict[Tuple[str, str], Project] = {
            p.project_id: p for p in projects
        }
        self._tasks: Tasks = self._get_tasks()
        self._order: List[Tuple[str, str]] = list(self._projects.values())
        

    @property
    def projects(self) -> List[Project]:
        return list(self._projects.values())

    @projects.setter
    def projects(self, value):
        raise ValueError("Cannot directly set projects attribute.")

    def add(self, project: Project) -> None:
        self._projects.update({project.project_id: project})

    def patch_tasks(self, task_patches: Optional[TaskPatches] = None):
        ...

    def order_by_dependency(self) -> None:
        ...

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        top = tabularize("Projects", width)
        empty = tabularize("", width)
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        names = map(
            lambda x: tabularize(x, width),
            map(
                lambda p: format_number(p.project_id) + f"{p.name}",
                self._projects.values(),
            ),
        )
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(names)
            + "\n"
            + empty
            + bottombeam
        )

    def __iter__(self) -> Iterator[Project]:
        return iter(self._projects.values())

    def __getitem__(self, __id: Union[Tuple[str, str], Tuple[str, str, str]]) -> Any:
        if len(__id) == 2:
            return self._projects[__id]  # type: ignore
        elif len(__id) == 3:
            return self._tasks[__id]  # type: ignore
        else:
            raise KeyError(f"Invalid key for `Projects`: {__id}.")

    def __setitem__(
        self, __id: str, __value: Union[Tuple[str, str], Tuple[str, str, str]]
    ) -> None:
        if len(__id) == 2:
            self._projects.update({__id: __value})  # type: ignore
        elif len(__id) == 3:
            return self._tasks.update({__id: __value})  # type: ignore
        else:
            raise KeyError(f"Invalid key for `Projects`: {__id}.")

    def _get_tasks(self) -> Tasks:
        tasks = Tasks()
        for _project in self._projects.values():
            for task in _project._tasks:
                tasks.add(task)
        return tasks

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
