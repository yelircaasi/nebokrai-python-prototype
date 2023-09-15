from typing import Callable, Optional, Union

from ...util import PDate, PTime, round5, tabularize
from .entry import Entry
from .task import Task


class Routine:
    def __init__(
        self,
        name: str,
        start: PTime,
        items: list = [],
        priority: int = 80,
        notes: str = "",
        normaltime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        valid_dates: Union[Callable[[PDate], bool], set[PDate]] = lambda d: True,
    ) -> None:
        self.name = name
        self.start = start
        self.items = items
        self.routine_id = ("routine", "", name)
        self.priority = int(priority) or 80
        self.notes = notes
        self.normaltime = normaltime or 60
        self.mintime = mintime or round5(self.normaltime / 4)
        self.maxtime = maxtime or round5(self.normaltime * 2)
        self.valid_dates = (
            valid_dates
            if callable(self.valid_dates)
            else (lambda d: d in self.valid_dates)
        )

    def valid_on(self, date: PDate) -> bool:
        return self.valid_dates(date)

    def as_entry(self, start: Optional[PTime] = None) -> Entry:
        return Entry(self.name, start or self.start, priority=self.priority)  # TODO

    def as_task(self) -> Task:
        return Task(self.name, self.routine_id, priority=self.priority)  # TODO

    def pretty(self, width: int = 80) -> str:
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = (
            thickbeam
            + tabularize(f"{self.name}", width)
            + "\n"
            + tabularize(f"  Priority: {self.priority}", width)
            + thinbeam
        )
        format_number = lambda s: (len(str(s)) == 1) * " " + f"{s} │ "
        return header + "\n".join(
            [
                tabularize(format_number(i) * (len(s) > 0) + s, width)
                for i, s in enumerate((self.items + [""]), start=1)
            ]
        )

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
