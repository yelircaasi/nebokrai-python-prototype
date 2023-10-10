from typing import Any, Iterable, Iterator, List, Optional, Tuple

from ...config import Config
from ...util import PDate, ProjectID, RoadmapID, TaskID, tabularize
from ..container.projects import Projects
from .project import Project
from .task import Task


class Roadmap:
    """
    Container for a roadmap, which consists of projects, which in turn consist of tasks.
    """

    def __init__(
        self,
        config: Config,
        name: str,
        roadmap_id: RoadmapID,
        projects: Projects,
        categories: Optional[Iterable[str]] = None,
    ) -> None:
        self.config = config
        self.name = name
        self.roadmap_id = roadmap_id
        self._projects = projects
        self.categories = categories or set()

    @classmethod
    def from_dict(
        cls, config: Config, roadmap_id: RoadmapID, roadmap_dict: dict[str, Any]
    ) -> "Roadmap":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        projects = Projects.from_dict(config, roadmap_id, roadmap_dict["projects"])

        return cls(config, roadmap_dict["name"], roadmap_id, projects)

    def copy(self) -> "Roadmap":
        return Roadmap(
            self.config,
            name=self.name,
            roadmap_id=self.roadmap_id,
            projects=self._projects,
            categories=self.categories,
        )

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Entry instance.
        """
        width = self.config.repr_width
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        # format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"{self.name} (ID {self.roadmap_id})", width, thick=True)
        empty = tabularize("", width, thick=True)
        projects = map(lambda p: f"{'-'.join(p.project_id): <9} │ {p.name}", iter(self._projects))
        # projects = map(lambda x: tabularize(x.name, width, thick=True), projects)
        projects = map(lambda x: tabularize(x, width, thick=True), projects)
        # projects = map(str, projects)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(projects)
            + "\n"
            + empty
            + bottombeam
        )

    @property
    def start_date(self) -> PDate:
        """
        Property returning the earliest date of any task contained in the
          consituent projects of the given roadmap.
        """
        if not self._projects:
            return PDate.nonedate()
        return min(map(lambda p: p.start, self._projects))

    @property
    def end_date(self) -> PDate:
        """
        Property returning the latest date of any task contained in the
          consituent projects of the given roadmap.
        """
        if not self._projects:
            return PDate.nonedate()
        today = PDate.today()
        return max(map(lambda p: p.end or today, self._projects))

    def items(self) -> List[Tuple[ProjectID, Project]]:
        return [(proj.project_id, proj) for proj in self._projects]

    def get_task(self, task_id: TaskID) -> Task:
        if isinstance(task_id, TaskID):
            return self._projects[task_id.project_id][task_id]
        raise KeyError(f"Invalid task_id for Roadmap object: {task_id}")

    def __iter__(self) -> Iterator[Project]:
        return iter(self._projects)

    def __len__(self) -> int:
        return len(self._projects)

    def __getitem__(self, __key: ProjectID) -> Project:
        if isinstance(__key, ProjectID):
            return self._projects[__key]
        raise KeyError(f"Invalid key for Roadmap object: {__key}")

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
