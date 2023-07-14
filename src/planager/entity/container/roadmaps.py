from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from ...util import Norg, PDate, tabularize
from ..base.project import Project
from ..base.roadmap import Roadmap
from ..container.projects import Projects


class Roadmaps:
    def __init__(
        self, roadmaps: List[Roadmap] = [], workspace_dir: Optional[Path] = None
    ) -> None:
        self.workspace_dir = workspace_dir
        self._roadmaps: Dict[str, Roadmap] = {
            roadmap.roadmap_id: roadmap for roadmap in roadmaps
        }

    def __iter__(self) -> Iterator[Roadmap]:
        return iter(self._roadmaps.values())

    def __getitem__(self, __key: str) -> Roadmap:
        return self._roadmaps[__key]

    def __setitem__(self, __name: str, __value: Any) -> None:
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
        top = tabularize("Roadmaps", width, pad=1)
        empty = tabularize("", width)
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        names = map(
            lambda x: tabularize(x.replace(" Roadmap", ""), width),
            map(
                lambda r: format_number(r.roadmap_id) + f"{r.name}",
                self._roadmaps.values(),
            ),
        )
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(names)
            + "\n"
            + empty
            + bottombeam
        )

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Roadmaps":
        file = workspace_dir / "roadmaps.norg"
        parsed = Norg.from_path(file)
        roadmap_list = []
        for item in parsed.items:
            _, link = Norg.parse_link(item.name)
            path = workspace_dir / link.replace("$/", "")
            roadmap_list.append(Roadmap.from_norg_path(path))
        return cls(roadmap_list, workspace_dir)

    def open_projects_norg(self) -> Projects:
        projects = Projects()
        for roadmap in self._roadmaps.values():
            for project in roadmap:
                _project = project.copy()
                # TODO project.update_from_norg()
                projects.add(project)
        return projects

    def get_projects(self) -> Dict[Tuple[str, str], Project]:
        projects: Dict[Tuple[str, str], Project] = {}
        for roadmap_id, roadmap in self._roadmaps.items():
            for project_id, project in roadmap._projects._projects.items():
                tuple_id: Tuple[str, str] = (
                    (roadmap_id, project_id)
                    if isinstance(project_id, int)
                    else project_id
                )
                projects.update({tuple_id: project})
        return projects
