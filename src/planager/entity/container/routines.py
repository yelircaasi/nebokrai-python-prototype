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

    @classmethod
    def from_norg_workspace(cls, workspace: Path) -> "Routines":
        return cls()

    def add(self, routine: Routine) -> None:
        self._routines.append(routine)

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        top = tabularize("Routines", width)
        empty = tabularize("", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, ""))
            + "\n".join(map(str, self._routines))
            + bottombeam
        )

    def __iter__(self) -> Iterator[Routine]:
        return iter(self._routines)

    def __getitem__(self, __name: str) -> Routine:
        return list(filter(lambda x: x.name == __name, self._routines))[0]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
