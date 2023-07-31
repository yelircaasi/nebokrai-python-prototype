from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from ...util import Norg, PDate, Regexes, tabularize
from ..container.projects import Projects
from .project import Project


class Roadmap:
    def __init__(
        self,
        name: str,
        roadmap_id: str,
        projects: Projects,
        updated: PDate = PDate.today() + 7,
        categories: Iterable[str] = [],
    ) -> None:
        self.name = name
        self.roadmap_id = roadmap_id
        self._projects = projects
        self.updated = updated
        self.categories = categories

    @classmethod
    def from_norg_path(self, norg_path: Path) -> "Roadmap":
        norg = Norg.from_path(norg_path)
        projects = Projects()  # norg.title, norg.doc_id)
        for item in norg.items:
            item_id = item.item_id[-1] if item.item_id else None
            projects.add(
                Project(
                    item.name or "<Placeholder Project Name>",
                    project_id=(
                        norg.doc_id,
                        item_id or "<Placeholder Project ID>",
                    ),
                    tasks=[],  # TODO
                    priority=item.priority or 10,
                    start=item.start_date or PDate.today() + 7,
                    end=item.end_date or PDate.today() + 107,
                    interval=item.interval or 7,
                    cluster_size=item.cluster_size or 1,
                    duration=item.duration or 30,
                    tags=item.tags or set(),
                    description=item.description or "",
                    notes=item.notes or "",
                    path=item.path,
                    before=item.before or set(),
                    after=item.dependencies or set(),
                )
            )
        return Roadmap(norg.title, norg.doc_id, projects)

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"{self.name} (ID {self.roadmap_id})", width)
        empty = tabularize("", width)
        projects = map(
            lambda p: format_number(p.project_id) + f"{p.name}", iter(self._projects)
        )
        projects = map(lambda x: tabularize(x, width), projects)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(projects)
            + "\n"
            + empty
            + bottombeam
        )

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> Iterator[Project]:
        return iter(self._projects)

    