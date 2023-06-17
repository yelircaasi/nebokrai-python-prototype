from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

from planager.entities import Project, Projects
from planager.utils.data.norg.norg_utils import Norg
from planager.utils.datetime_extensions import PDate, ZERODATE
from planager.utils.misc import tabularize


class Roadmap:
    def __init__(
            self,
            name: str,
            id: int,
            projects: Projects,
            updated: PDate = ZERODATE,
            categories: Iterable[str] = []
        ) -> None:
        self.name = name
        self.id = id
        self.projects = projects
        self.updated = updated
        self.categories = categories

    # @classmethod
    # def from_norg_workspace(self, workspace_dir: Path) -> "Roadmap":
    #     ...

    @classmethod
    def from_norg_path(self, norg_path: Path) -> "Roadmap":
        norg = Norg.from_path(norg_path)
        projects = Projects() #norg.title, norg.id)
        for id, item in enumerate(norg.items):
            projects.add(Project.from_roadmap_item(item, id, norg_path))
        return Roadmap(norg.title, norg.id, projects)
            
    def __iter__(self) -> Iterator[Project]:
        return iter(self.projects)
    
    def __str__(self) -> str:
        return self.pretty()
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def pretty(self, width: int = 80) -> str:
        
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        #thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"{self.name} (ID {self.id})", width, pad=1)
        empty = tabularize("", width)
        #projects = map(lambda x: tabularize(x, width), map(lambda r: format_number(r.id) + f"{r.name}", self.projects))
        #for p in self.projects._projects.items():
        #    print(p)
        projects = list(map(lambda r: format_number(r.id) + f"{r.name}", self.projects.projects))
        #print(projects)
        projects = map(lambda x: tabularize(x, width), projects)
        return "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, "")) + "\n".join(projects) + '\n' + empty + bottombeam



class Roadmaps:
    def __init__(
        self, roadmaps: List[Roadmap] = [],
        workspace_dir: Optional[Path] = None
    
    ) -> None:
        self.workspace_dir = workspace_dir
        self._roadmaps = {roadmap.id: roadmap for roadmap in roadmaps}
    
    def __getitem__(self, __key: int) -> Roadmap:
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
        #thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        top = tabularize("Roadmaps", width, pad=1)
        empty = tabularize("", width)
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        names = map(lambda x: tabularize(x.replace(" Roadmap", ""), width), map(lambda r: format_number(r.id) + f"{r.name}", self._roadmaps.values()))
        return "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, "")) + "\n".join(names) + '\n' + empty + bottombeam

    
    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Roadmaps":
        file = workspace_dir / "roadmaps.norg"
        parsed = Norg.from_path(file)
        roadmap_list = []
        for item in parsed.items:
            #print(item)
            _, link = Norg.parse_link(item)
            path = workspace_dir / link.replace("$/", "")
            roadmap_list.append(Roadmap.from_norg_path(path))
        return cls(roadmap_list, workspace_dir)


    def open_projects_norg(self) -> Projects:
        projects = Projects()
        for roadmap in self._roadmaps:
            for project in roadmap:
                _project = project.copy()
                project.update_from_norg()
                projects.add(project)
        return projects      
