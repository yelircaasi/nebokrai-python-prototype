from pathlib import Path
from typing import Iterator, List

from ...util import Norg, tabularize
from ..base.routine import Routine


class Routines:
    """
    Container class for routines, designed to be

    """

    def __init__(self) -> None:
        self._routines: List[Routine] = []

    def __iter__(self) -> Iterator[Routine]:
        return iter(self._routines)

    def add(self, routine: Routine) -> None:
        self._routines.append(routine)

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        top = tabularize("Routines", width, pad=1)
        empty = tabularize("", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, ""))
            + "\n".join(map(str, self._routines))
            + bottombeam
        )

    def __getitem__(self, __name: str) -> Routine:
        return list(filter(lambda x: x.name == __name, self._routines))[0]

    # def __setitem__(self, __name: str, __value: Any) -> None:
    #     ...

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Routines":
        file = workspace_dir / "routines.norg"
        parsed = Norg.from_path(file)
        routines = Routines()
        for section in parsed.sections:
            title = section["title"]
            # attributes = Norg.parse_preasterix_attributes(section["text"])
            attributes = section["attributes"]
            # items = list(map(lambda x: x if isinstance(x, str) else x["title"], Norg.parse_subsections(section)))
            items = section["subsections"]
            routines.add(
                Routine(
                    title,
                    attributes,
                    items,
                )
            )
        for routine in routines:
            print(routine.priority)
        return routines
