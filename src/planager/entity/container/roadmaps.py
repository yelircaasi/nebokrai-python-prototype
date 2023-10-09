from pathlib import Path
from typing import Any, Iterator, Optional

from ...config import Config
from ...util import PDate, tabularize
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
        config: Config,
        roadmaps: Optional[list[Roadmap]] = None,
        workspace_dir: Optional[Path] = None,
    ) -> None:
        self.config = config
        self.workspace_dir = workspace_dir
        self._roadmaps: dict[str, Roadmap] = {
            roadmap.roadmap_id: roadmap for roadmap in (roadmaps or [])
        }

    @classmethod
    def from_dict(cls, config: Config, roadmaps_dict: dict[str, Any]) -> "Roadmaps":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        ret = cls(config)
        for rmid, rmdict in roadmaps_dict.items():
            ret.add(Roadmap.from_dict(config, rmid, rmdict))
        return ret

    # @classmethod
    # def from_norg_workspace(cls, workspace_dir: Path) -> "Roadmaps":
    #     file = workspace_dir / "roadmaps.norg"
    #     norg = Norg.from_path(file)
    #     roadmap_list = []
    #     for item in norg.items:
    #         if item.path:
    #             roadmap_list.append(Roadmap.from_norg_path(item.path))
    #         else:
    #             raise ValueError(f"Roadmap item must have a path link: {str(item)}")
    #     return cls(roadmap_list, workspace_dir)

    # def open_projects_norg(self) -> Projects:
    #     projects = Projects()
    #     for roadmap in self._roadmaps.values():
    #         for project in roadmap:
    #             _project = project.copy()
    #             # TODO project.update_from_norg()
    #             projects.add(_project)
    #     return projects

    @property
    def projects(self) -> Projects:  # Dict[tuple[str, str], Project]:
        """
        Returns all projects contained in the current instance, in the form of a Projects instance.
        """
        projects: Projects = Projects(self.config)  # Dict[tuple[str, str], Project] = {}
        for roadmap_id, roadmap in self._roadmaps.items():
            for project_id, project in roadmap.items():
                tuple_id: tuple[str, str] = (
                    (roadmap_id, project_id) if isinstance(project_id, int) else project_id
                )
                project.project_id = tuple_id
                projects.add(project)
        # projects.order_by_dependency()
        return projects

    @property
    def tasks(self) -> Tasks:
        """
        Returns all tasks contained in the projects contained in the current instance,
          in the form of a Tasks instance.
        """
        _tasks: Tasks = Tasks(self.config)
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

        width = self.config.repr_width

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
        assert not __roadmap.roadmap_id in self._roadmaps
        self._roadmaps.update({__roadmap.roadmap_id: __roadmap})

    def get_task(self, task_id: tuple[str, str, str]) -> Task:
        roadmap_code, project_code, task_code = task_id
        return self._roadmaps[roadmap_code][project_code][task_code]

    def __len__(self) -> int:
        return len(self._roadmaps)

    def __iter__(self) -> Iterator[Roadmap]:
        return iter(self._roadmaps.values())

    def __getitem__(self, __key: str) -> Roadmap:
        return self._roadmaps[__key]

    def __setitem__(self, __id: str, __roadmap: Any) -> None:
        self._roadmaps.update({__id: __roadmap})

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
