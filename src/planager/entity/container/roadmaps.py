from pathlib import Path
from typing import Any, Iterator, Optional, Union

from ...configuration import config
from ...util import PDate, ProjectID, RoadmapID, TaskID, tabularize
from ..base.project import Project
from ..base.roadmap import Roadmap
from ..base.task import Task
from ..container.projects import Projects
from ..container.tasks import Tasks


class Roadmaps:
    """
    Container class for multiple instances of the Roadmap class.
    """

    def __init__(
        self,
        roadmaps: Optional[list[Roadmap]] = None,
        workspace_dir: Optional[Path] = None,
    ) -> None:
        self.workspace_dir = workspace_dir
        self._roadmaps: dict[RoadmapID, Roadmap] = {
            roadmap.roadmap_id: roadmap for roadmap in (roadmaps or [])
        }

    @classmethod
    def from_dict(cls, roadmaps_dict: dict[str, Any]) -> "Roadmaps":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        ret = cls()
        for roadmap_code, roadmap_dict in roadmaps_dict.items():
            roadmap_id = RoadmapID(roadmap_code)
            ret.add(Roadmap.from_dict(roadmap_id, roadmap_dict))
        return ret

    @property
    def projects(self) -> Projects:
        """
        Returns all projects contained in the current instance, in the form of a Projects instance.
        """
        projects: Projects = Projects()
        for _, roadmap in self._roadmaps.items():
            for _, project in roadmap.items():
                projects.add(project)
        return projects

    @property
    def tasks(self) -> Tasks:
        """
        Returns all tasks contained in the projects contained in the current instance,
          in the form of a Tasks instance.
        """
        _tasks: Tasks = Tasks()
        for _, roadmap in self._roadmaps.items():
            for _, project in roadmap.items():
                _tasks.update(project.tasks)
        return _tasks

    @property
    def start_date(self) -> PDate:
        return min(roadmap.start_date for roadmap in self._roadmaps.values())

    @property
    def end_date(self) -> PDate:
        return max(roadmap.end_date for roadmap in self._roadmaps.values())

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Roadmaps instance.
        """

        width = config.repr_width

        empty = "\n" + tabularize("", width, thick=True)
        names = map(
            lambda x: tabularize(x.replace(" Roadmap", ""), width, thick=True),
            map(
                lambda r: f" {r.roadmap_id: <4} │ {r.name}",
                self._roadmaps.values(),
            ),
        )
        return (
            "\n"
            + "┏"
            + (width - 2) * "━"
            + "┓"
            + empty
            + tabularize(" Roadmaps", width, thick=True)
            + empty
            + "┠"
            + (width - 2) * "─"
            + "┨"
            + empty
            + "\n"
            + "\n".join(names)
            + empty
            + "\n┗"
            + (width - 2) * "━"
            + "┛"
        )

    def add(self, __roadmap: Roadmap) -> None:
        assert __roadmap.roadmap_id not in self._roadmaps
        self._roadmaps.update({__roadmap.roadmap_id: __roadmap})

    def get_project(self, project_id: ProjectID) -> Project:
        if isinstance(project_id, ProjectID):
            return self._roadmaps[project_id.roadmap_id][project_id]
        raise KeyError(f"Invalid project_id for Roadmaps object: {project_id}")

    def get_task(self, task_id: TaskID) -> Task:
        if isinstance(task_id, TaskID):
            return self._roadmaps[task_id.roadmap_id][task_id.project_id][task_id]
        raise KeyError(f"Invalid task_id for Roadmaps object: {task_id}")

    def __len__(self) -> int:
        return len(self._roadmaps)

    def __iter__(self) -> Iterator[Roadmap]:
        return iter(self._roadmaps.values())

    def __getitem__(self, __key: Union[RoadmapID, ProjectID, TaskID]) -> Roadmap:
        if isinstance(__key, RoadmapID):
            return self._roadmaps[__key]
        raise KeyError(f"Invalid key for Roadmaps object: {__key}")

    def __setitem__(self, __id: RoadmapID, __roadmap: Roadmap) -> None:
        self._roadmaps.update({__id: __roadmap})

    @property
    def summary(self) -> str:
        return "Plan.summary property is not yet implemented."

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
