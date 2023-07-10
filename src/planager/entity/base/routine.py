from typing import Optional

from ...util import PDate, PTime, round5, tabularize
from .entry import Entry
from .task import Task


class Routine:
    def __init__(
        self,
        name: str,
        routine_num: int,
        attributes: dict,
        items: list,
    ) -> None:
        self.name = name
        self.items = items
        self.id = (-1, 0, routine_num)

        if attributes:
            self.__dict__.update(attributes)
        self.priority = attributes.get("priority") or 80
        self.priority = int(self.priority)
        self.notes = attributes.get("notes") or ""
        self.normaltime = attributes.get("normaltime", 60)
        self.mintime = attributes.get("mintime", round5(self.normaltime / 4))
        self.mintime = attributes.get("mintime", round5(self.normaltime * 2))

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

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
                tabularize(format_number(i) * (len(s) > 0) + s, width, pad=1)
                for i, s in enumerate((self.items + [""]), start=1)
            ]
        )

    def valid_on(self, date: PDate) -> bool:
        # TODO
        return True

    def as_entry(self, start: Optional[PTime]) -> Entry:
        return Entry(self.name, start, priority=self.priority)  # TODO

    def as_task(self) -> Task:
        return Task(self.name, self.id, priority=self.priority)  # TODO
