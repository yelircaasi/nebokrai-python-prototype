from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

from planager.entities import Project, Projects
from planager.utils.data.norg.norg_utils import Norg
from planager.utils.datetime_extensions import PDate, ZERODATE


class Roadmap:
    def __init__(
            self,
            projects: List[Dict] = [],
            updated: PDate = ZERODATE,
            categories: Iterable[str] = []
        ) -> None:
        self.projects = projects
        self.updated = updated
        self.categories = categories

    # @classmethod
    # def from_norg_workspace(self, workspace_dir: Path) -> "Roadmap":
    #     ...

    @classmethod
    def from_norg_path(self, norg_path: Path) -> "Roadmap":
        norg = Norg.from_path(norg_path)
        for item in norg["items"]:
            if "||" in item:
                ...
            else:
                _, link = Norg.parse_link(item)
                path = norg_path.parent / link.replace("$/", "")
                project = Project.from_norg(path)
            

    def __iter__(self) -> Iterator[Project]:
        return iter(self.projects)


class Roadmaps:
    def __init__(
        self, roadmaps: List[Roadmap] = [],
        workspace_dir: Optional[Path] = None
    
    ) -> None:
        self.workspace_dir = workspace_dir
        self.roadmaps = {roadmap.id: roadmap for roadmap in roadmaps}
    
    def __getitem__(self, __name: str) -> Roadmap:
        roadmap = ...
        return roadmap
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
    
    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Roadmaps":
        file = workspace_dir / "roadmaps.norg"
        parsed: Dict = Norg.from_path(file)
        roadmap_list = []
        for item in parsed["items"]:
            _, link = Norg.parse_link(item)
            path = workspace_dir / link.replace("$/", "")
            roadmap_list.append(Roadmap.from_norg_path(path))
        return cls(roadmap_list, workspace_dir)


    def open_projects_norg(self) -> Projects:
        projects = Projects()
        for roadmap in self.roadmaps:
            for project in roadmap:
                _project = project.copy()
                project.update_from_norg()
                projects.add(project)
        return projects      
