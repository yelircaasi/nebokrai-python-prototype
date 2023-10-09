from typing import Any, Iterator, Optional, Union

from ...config import Config
from ...util import tabularize
from ..base.project import Project
from ..container.tasks import Tasks


class Projects:
    """
    Container class for multiple instances of the Project class.
    """

    def __init__(self, config: Config, projects: Optional[list[Project]] = None) -> None:
        self._projects: dict[tuple[str, str], Project] = {p.project_id: p for p in (projects or [])}
        self.config = config
        self._tasks: Tasks = self._get_tasks()

    @classmethod
    def from_dict(cls, config, roadmap_id: str, projects_dict: dict[str, Any]) -> "Projects":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """

        projects = cls(config)

        for project_code, project_dict in projects_dict.items():
            if project_dict:
                projects.add(Project.from_dict(config, roadmap_id, project_code, project_dict))

        return projects

    # @property
    # def project_list(self) -> list[Project]:
    #     return list(self._projects.values())

    # @project_list.setter
    # def projects(self, value):
    #     raise ValueError("Cannot directly set projects attribute.")

    def add(self, project: Project) -> None:
        self._projects.update({project.project_id: project})

    @property
    def tasks(self) -> Tasks:
        return self._tasks

    def _get_tasks(self) -> Tasks:
        tasks = Tasks(self.config)
        for _project in self._projects.values():
            for task in _project:
                tasks.add(task)
        return tasks

    @property
    def iter_by_priority(self) -> Iterator[Project]:
        return iter(
            sorted(list(self._projects.values()), key=lambda proj: proj.priority)
        )  # TODO: make iterate in order

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Projects instance.
        """

        def format_number(s: Any) -> str:
            return (len(str(s)) == 1) * " " + f" {s} │ "

        width = self.config.repr_width

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
        return iter(self._projects.values())  # TODO: make iterate in order

    def __len__(self) -> int:
        return len(self._projects)

    def __getitem__(self, __id: Union[str, tuple[str, str], tuple[str, str, str]]) -> Any:
        if isinstance(__id, str):
            roadmap_id = list(self._projects)[0][0]
            return self._projects[(roadmap_id, __id)]
        if len(__id) == 2:
            return self._projects[__id]  # type: ignore
        if len(__id) == 3:
            return self._tasks[__id]  # type: ignore
        raise KeyError(f"Invalid key for `Projects`: {__id}.")

    def __setitem__(
        self, __id: Union[tuple[str, str], tuple[str, str, str]], __value: Project
    ) -> None:
        if len(__id) == 2:
            self._projects.update({__id: __value})  # type: ignore
        elif len(__id) == 3:
            return self._tasks.update({__id: __value})  # type: ignore
        raise KeyError(f"Invalid key for `Projects`: {__id}.")

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
