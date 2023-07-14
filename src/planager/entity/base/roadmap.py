from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from ...util import ZERODATE, Norg, PDate, tabularize
from ..container.projects import Projects
from .project import Project


class Roadmap:
    def __init__(
        self,
        name: str,
        id: str,
        projects: Projects,
        updated: PDate = ZERODATE,
        categories: Iterable[str] = [],
    ) -> None:
        self.name = name
        self.id = id
        self._projects = projects
        self.updated = updated
        self.categories = categories

    # @classmethod
    # def from_norg_workspace(self, workspace_dir: Path) -> "Roadmap":
    #     ...

    @classmethod
    def from_norg_path(self, norg_path: Path) -> "Roadmap":
        norg = Norg.from_path(norg_path)
        projects = Projects()  # norg.title, norg.id)
        for id, item in enumerate(norg.items):
            projects.add(Project.from_roadmap_item(item, (norg.id, str(id)), norg_path))
        return Roadmap(norg.title, norg.id, projects)

    def __iter__(self) -> Iterator[Project]:
        return iter(self._projects)

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"{self.name} (ID {self.id})", width, pad=1)
        empty = tabularize("", width)
        projects = map(
            lambda r: format_number(r.id) + f"{r.name}", iter(self._projects)
        )
        projects = map(lambda x: tabularize(x, width), projects)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(projects)
            + "\n"
            + empty
            + bottombeam
        )
