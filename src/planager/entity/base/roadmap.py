from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from ...util import ZERODATE, Norg, PDate, Regexes, tabularize
from ..container.projects import Projects
from .project import Project


class Roadmap:
    def __init__(
        self,
        name: str,
        roadmap_id: str,
        projects: Projects,
        updated: PDate = ZERODATE,
        categories: Iterable[str] = [],
    ) -> None:
        self.name = name
        self.roadmap_id = roadmap_id
        self._projects = projects
        self.updated = updated
        self.categories = categories

    # @classmethod
    # def from_norg_workspace(self, workspace_dir: Path) -> "Roadmap":
    #     ...

    @classmethod
    def from_norg_path(self, norg_path: Path) -> "Roadmap":
        norg = Norg.from_path(norg_path)
        projects = Projects()  # norg.title, norg.doc_id)
        for item in norg.items:
            projects.add(
                # Project(item, (norg.doc_id, str(item.item_id)), norg_path))
                Project(
                    item.get_name() or "<Placeholder Project Name>",
                    project_id=(
                        norg.doc_id,
                        item.get_id() or "<Placeholder Project ID>",
                    ),
                    tasks=[],  # TODO
                    priority=item.get_priority() or 10,
                    start=item.get_start_date() or PDate.today() + 7,
                    end=item.get_end_date() or PDate.today() + 107,
                    interval=item.get_interval() or 7,
                    cluster_size=item.get_cluster_size() or 1,
                    duration=item.get_duration() or 30,
                    tags=item.get_tags() or set(),
                    description=item.get_description() or "",
                    notes=item.get_notes(),
                    path=item.get_path(),
                    before=item.get_before() or set(),
                    after=item.get_after() or set(),
                )
            )
        return Roadmap(norg.title, norg.doc_id, projects)

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
        top = tabularize(f"{self.name} (ID {self.roadmap_id})", width, pad=1)
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
