from pathlib import Path
import re
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from planager.utils.misc import expand_task_segments, tabularize
from planager.utils.regex import Regexes
from .task import Task, TaskPatches, Tasks
from planager.utils.data.norg.norg_utils import Norg


class Project:
    def __init__(
        self, name: str, id: int, tasks: Union[List[str], str] = [], **kwargs
    ) -> None:
        self.name = name
        self.id = id
        self._tasks = Tasks.from_string_iterable(
            expand_task_segments(tasks) if isinstance(tasks, str) else tasks
        )

    def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
        ...

    def __getitem__(self, __key: int) -> Task:
        return self._tasks[__key]

    @classmethod
    def from_norg_path(cls, norg_path: Path, **kwargs) -> "Project":
        norg = Norg.from_path(norg_path)
        tasks = Tasks.from_norg_path(norg_path)

        return cls(name=norg.title, id=norg.id, tasks=tasks, path=norg_path, **kwargs)

    @classmethod
    def from_roadmap_item(cls, item: str, id: int, roadmap_path: Path) -> "Project":
        # norg = Norg.from_path(norg_path)
        regx = Regexes.first_line
        title = re.search(regx, item).groups()[0]
        attributes = Norg.get_attributes(item)
        priority = attributes.get("priority", 10)
        if "||" in title:
            name, tasks = re.split("\s*\|\|\s*", title)

            # tasks = map(lambda x: Task(x[1], x[0], priority=priority), enumerate(tasks))
            return cls(name, id, tasks, **attributes)
        else:
            _, link = Norg.parse_link(item)
            if link:
                path = roadmap_path.parent.parent / link.replace("$/", "")
                assert path.exists()
                return cls.from_norg_path(path, **attributes)
            else:
                raise ValueError(f"No path found in roadmap item: {item}.")

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"Project: {self.name} (ID {self.id})", width, pad=1)
        empty = tabularize("", width)
        tasks = map(
            lambda x: tabularize(
                f"{format_number(x.id)}{x.name} (priority {x.priority})", width
            ),
            self._tasks,
        )
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(tasks)
            + "\n"
            + empty
            + bottombeam
        )


class Projects:
    def __init__(self, projects: List[Project] = []) -> None:
        self._projects: Dict[Tuple, Project] = {
            project.id: project for project in projects
        }
        self._tasks: Tasks = self._get_tasks()

    @property
    def projects(self) -> List[Project]:
        return list(self._projects.values())

    @projects.setter
    def projects(self, value):
        raise ValueError("Cannot directly set projects attribute.")

    def add(self, project: Project) -> None:
        self._projects.update({project.id: project})

    def __iter__(self) -> Iterable[Project]:
        return iter(self._projects.values())

    def __getitem__(self, __id: Union[int, tuple]) -> Any:
        if isinstance(__id, int):
            return self._projects[__id]
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

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        top = tabularize("Projects", width, pad=1)
        empty = tabularize("", width)
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        names = map(
            lambda x: tabularize(x, width),
            map(lambda r: format_number(r.id) + f"{r.name}", self._projects.values()),
        )
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(names)
            + "\n"
            + empty
            + bottombeam
        )
