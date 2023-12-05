from typing import Any, Iterator, Optional, Union

from ...configuration import config
from ...util import ProjectID, RoadmapID, TaskID, tabularize
from ...util.serde.custom_dict_types import ProjectDictRaw
from ..base.project import Project
from ..base.task import Task
from ..container.tasks import Tasks


class Projects:
    """
    Container class for multiple instances of the Project class.
    """

    def __init__(self, projects: Optional[list[Project]] = None) -> None:
        self._projects: dict[ProjectID, Project] = {p.project_id: p for p in (projects or [])}
        self._tasks: Tasks = self._get_tasks()

    @classmethod
    def deserialize(
        cls, roadmap_id: RoadmapID, projects_dict: dict[str, ProjectDictRaw]
    ) -> "Projects":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """

        projects = cls()

        for project_code, project_dict in projects_dict.items():
            project_id = roadmap_id.project_id(project_code)
            if project_dict:
                projects.add(Project.deserialize(project_id, project_dict))

        return projects

    def add(self, project: Project) -> None:
        self._projects.update({project.project_id: project})

    @property
    def tasks(self) -> Tasks:
        return self._tasks

    def _get_tasks(self) -> Tasks:
        tasks = Tasks()
        for _project in self._projects.values():
            for task in _project:
                tasks.add(task)
        return tasks

    @property
    def iter_by_priority(self) -> Iterator[Project]:
        return iter(sorted(list(self._projects.values()), key=lambda proj: proj.priority))

    def get_task(self, task_id: TaskID) -> Task:
        if isinstance(task_id, TaskID):
            return self._projects[task_id.project_id][task_id]
        raise KeyError(f"Invalid task_id for Roadmap object: {task_id}")

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Projects instance.
        """

        def format_number(s: Any) -> str:
            return (len(str(s)) == 1) * " " + f" {s} │ "

        width = config.repr_width

        empty = "\n" + tabularize("", width)
        names = map(
            lambda x: tabularize(x, width),
            map(
                lambda p: format_number(p.project_id) + f"{p.name}",
                self._projects.values(),
            ),
        )
        return "".join(
            (
                "\n",
                "┏",
                (width - 2) * "━",
                "┓",
                empty,
                tabularize("Projects", width),
                empty,
                "┠",
                (width - 2) * "─",
                "┨",
                empty,
                "\n",
                "\n".join(names),
                empty,
                "\n┗",
                (width - 2) * "━",
                "┛",
            )
        )

    def __iter__(self) -> Iterator[Project]:
        return iter(sorted(self._projects.values(), key=lambda p: p.start))

    def __len__(self) -> int:
        return len(self._projects)

    def __getitem__(self, __key: ProjectID) -> Any:
        if isinstance(__key, ProjectID):
            return self._projects[__key]
        raise KeyError(f"Invalid key for Projects object: {__key}")

    def __setitem__(self, __id: Union[ProjectID, TaskID], __value: Project) -> None:
        if len(__id) == 2:
            self._projects.update({__id: __value})  # type: ignore
        elif len(__id) == 3:
            return self._tasks.update({__id: __value})  # type: ignore
        raise KeyError(f"Invalid key for `Projects`: {__id}.")

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
