from typing import Any, Callable, Iterable, Optional, Union

from ...util import PDate, PTime, round5, tabularize
from .entry import Entry
from ..container.entries import Entries
from .task import Task


class Routine:
    def __init__(
        self,
        name: str,
        start: PTime,
        items: Iterable[Entry] = [],
        priority: int = 80,
        notes: str = "",
        normaltime: Optional[int] = None,
        idealtime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        valid_dates: Union[Callable[[PDate], bool], set[PDate]] = lambda d: True,
    ) -> None:
        self.name = name
        self.start = start
        self.items = Entries(items)
        self.priority = int(priority) or 80
        self.notes = notes
        self.normaltime = normaltime or 60
        self.idealtime = idealtime or round5(self.normaltime * 1.5)
        self.mintime = mintime or round5(self.normaltime / 4)
        self.mintime = mintime or round5(self.normaltime * 1.5)
        self.maxtime = maxtime or round5(self.normaltime * 2)

        def validator(d: PDate) -> bool:
            ret: bool = (
                (d in valid_dates)
                if hasattr(valid_dates, "__contains__")
                else valid_dates(d)
            )
            return ret

        self.valid_dates = validator

    @classmethod
    def from_dict(cls, routine_dict: dict[str, Any]) -> "Routine":
        items: list[Entry] = []
        for item_dict in routine_dict["items"]:
            items.append(Entry.from_dict(item_dict))
        default_start = PTime.from_string(routine_dict["default_start"])
        normaltime = int(routine_dict.get("default_normaltime") or 60)
        return cls(
            routine_dict["name"],
            default_start,
            items,
            priority=int(routine_dict.get("default_priority") or 80),
            notes=routine_dict.get("default_notes", ""),
            normaltime=normaltime,
            idealtime=int(routine_dict.get("default_idealtime") or 1.5 * normaltime),
            mintime=int(routine_dict.get("default_mintime") or 0.25 * normaltime),
            maxtime=int(routine_dict.get("default_maxtime") or 2 * normaltime),
        )

    def valid_on(self, date: PDate) -> bool:
        return self.valid_dates(date)

    def as_entry(
        self,
        name: str,
        start: PTime,
        priority: int,
        normaltime: int,
        idealtime: int,
        mintime: int,
        maxtime: int,
    ) -> Entry:
        return Entry(
            self.name,
            start or self.start,
            priority=self.priority,
            normaltime=normaltime,
            idealtime=idealtime,
            mintime=mintime,
            maxtime=maxtime,
        )

    def pretty(self, width: int = 120) -> str:
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = (
            thickbeam
            + tabularize(f"{self.name}", width, thick=True)
            + "\n"
            + tabularize(f"  Priority: {self.priority}", width, thick=True)
            + thinbeam
        )
        format_number = lambda s: (len(str(s)) == 1) * " " + f"{s} │ "
        return header + "\n".join(
            [
                tabularize(
                    format_number(i) * (len(s.name) > 0) + s.name, width, thick=True
                )
                for i, s in enumerate(self.items, start=1)
            ]
        )

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
