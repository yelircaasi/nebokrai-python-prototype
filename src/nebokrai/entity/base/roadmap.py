from typing import Iterable, Iterator, List, Optional, Tuple

from nebokrai.util import color

from ...configuration import config
from ...util import NKDate, ProjectID, RoadmapID, TaskID, tabularize
from ...util.serde.custom_dict_types import RoadmapDictRaw
from ..container.projects import Projects
from .project import Project
from .task import Task


class Roadmap:
    """
    Container for a roadmap, which consists of projects, which in turn consist of tasks.
    """

    def __init__(
        self,
        name: str,
        roadmap_id: RoadmapID,
        projects: Projects,
        categories: Optional[Iterable[str]] = None,
    ) -> None:
        self.name = name
        self.roadmap_id = roadmap_id
        self._projects = projects
        self.categories = categories or set()

    @classmethod
    def deserialize(cls, roadmap_id: RoadmapID, roadmap_dict: RoadmapDictRaw) -> "Roadmap":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        name = roadmap_dict["name"]
        projects = Projects.deserialize(roadmap_id, roadmap_dict["projects"])

        return cls(name, roadmap_id, projects)

    def copy(self) -> "Roadmap":
        return Roadmap(
            name=self.name,
            roadmap_id=self.roadmap_id,
            projects=self._projects,
            categories=self.categories,
        )

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Entry instance.
        """
        width = config.repr_width
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        top = tabularize(f"{self.name} (ID {self.roadmap_id})", width, thick=True)
        empty = tabularize("", width, thick=True)
        projects = map(lambda p: f"{'-'.join(p.project_id): <9} │ {p.name}", iter(self._projects))
        projects = map(lambda x: tabularize(x, width, thick=True), projects)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(projects)
            + "\n"
            + empty
            + bottombeam
        )

    @property
    def start_date(self) -> NKDate:
        """
        Property returning the earliest date of any task contained in the
          consituent projects of the given roadmap.
        """
        if not self._projects:
            return NKDate.nonedate()
        return min(map(lambda p: p.start, self._projects))

    @property
    def end_date(self) -> NKDate:
        """
        Property returning the latest date of any task contained in the
          consituent projects of the given roadmap.
        """
        if not self._projects:
            return NKDate.nonedate()
        today = NKDate.today()
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

    @property
    def repr1(self) -> str:
        def stringify(project: Project) -> str:
            return f"{color.magenta(project.name[:20])} ({color.cyan(str(project.project_id))})"
        
        projects_string = ' | '.join(map(stringify, self._projects))
        return f"{color.magenta(self.name)}: start {color.green(self.start)}: {projects_string}"
