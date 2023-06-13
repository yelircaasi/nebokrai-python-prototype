from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

from planager.entities.project import Project, Projects
from src.planager.utils.datetime_extensions import PDate, ZERODATE


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

    @classmethod
    def from_norg_workspace(self, workspace_dir: Path) -> "Roadmap":
        ...

    def __iter__(self) -> Iterator[Project]:
        return iter(self.projects)


class Roadmaps:
    def __init__(self) -> None:
        self.workspace_dir: Optional[Path] = None
        self.roadmaps = []
    
    def __getitem__(self, __name: str) -> Roadmap:
        roadmap = ...
        return roadmap
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
    
    def from_norg_workspace(self, workspace_dir: Path) -> "Roadmaps":
        ...

    def open_projects_norg(self) -> Projects:
        projects = Projects()
        for roadmap in self.roadmaps:
            for project in roadmap:
                _project = project.copy()
                project.update_from_norg()
                projects.add(project)
        return projects      
