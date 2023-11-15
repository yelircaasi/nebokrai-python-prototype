from typing import Any, Iterable, Iterator, Optional

from ...util import tabularize
from ..base.routine import Routine


class Routines:
    """
    Container class for multiple instances of the Routine class.
    """

    def __init__(self, routines: Optional[Iterable[Routine]] = None) -> None:
        self._routines: dict[str, Routine] = {
            rout.name.split(" ")[0].lower(): rout for rout in (routines or [])
        }

    @classmethod
    def from_dict(cls, routines_dict: dict[str, Any]) -> "Routines":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """

        routines = []
        for routine_dict in routines_dict.values():
            routines.append(Routine.from_dict(routine_dict))
        return cls(routines)

    def add(self, routine: Routine) -> None:
        self._routines.update({routine.name: routine})

    def pretty(self, width: int = 120) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Routines instance.
        """

        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        top = tabularize("Routines", width, thick=True)
        empty = tabularize("", width, thick=True)
        return (
            "\n".join(("", topbeam, empty, top, empty, ""))
            + "\n".join(map(str, self._routines.values()))
            + bottombeam
        )

    def __iter__(self) -> Iterator[Routine]:
        return iter(self._routines.values())

    def __getitem__(self, __name: str) -> Routine:
        return self._routines[__name.split(" ")[0].lower()]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
