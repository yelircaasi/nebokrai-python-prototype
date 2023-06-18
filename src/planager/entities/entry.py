# from datetime import time

from pathlib import Path
from typing import Optional, Tuple
from planager.utils.datetime_extensions import PTime
from planager.utils.misc import tabularize


class Entry:
    def __init__(
        self,
        name: str,
        start: PTime,
        end: Optional[PTime] or None,
        priority: int = 0,
        ismovable: bool = True,
        notes: str = "",
        normaltime: Optional[int] = None,
        idealtime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        alignend: bool = False,
    ) -> None:
        self.__dict__.update(locals())
        if normaltime and (not end):
            self.end = start + normaltime
        elif end and (not normaltime):
            self.normaltime = start.timeto(end)
        else:
            self.normaltime = 30
        if idealtime is None:
            self.idealtime = int(1.5 * self.normaltime)
        if mintime is None:
            self.mintime = int(0.333 * self.normaltime)
        if maxtime is None:
            self.maxtime = int(2 * self.normaltime)

    def copy(self) -> "Entry":
        return Entry(
            self.name,
            start=self.start,
            end=self.end,
            priority=self.priority,
            ismovable=self.ismovable,
            notes=self.notes,
            normaltime=self.normaltime,
            idealtime=self.idealtime,
            mintime=self.mintime,
            maxtime=self.maxtime,
            alignend=self.alignend,
        )

    @classmethod
    def from_norg(cls, path: Path) -> "Entry":
        # dict = read_norg_day(path)
        entry = cls()
        return entry

    @classmethod
    def from_json(cls, path: Path) -> "Entry":
        schedule = cls()
        return schedule

    def to_norg(self, path: Path) -> None:
        ...

    def to_json(self, path: Path) -> None:
        ...

    def timespan(self) -> Tuple[PTime, PTime]:
        return (self.start, self.end)

    def __eq__(self, entry2: "Entry") -> bool:
        return self.__str__() == str(entry2)

    def duration(self) -> int:
        return self.start.timeto(self.end)

    def hasmass(self) -> bool:
        return (self.priority > 0) or (self.name in {"First", "Last"})

    def before(self, entry2: "Entry") -> bool:
        return self.end <= entry2.start

    def after(self, entry2: "Entry") -> bool:
        return self.start >= entry2.end

    def overlaps(self, entry2: "Entry") -> bool:
        return (self.start <= entry2.start < self.end) or (
            entry2.start < self.start <= entry2.end
        )

    def overlaps_first(self, entry2: "Entry") -> bool:
        return self.start <= entry2.start < self.end <= entry2.end

    def overlaps_second(self, entry2: "Entry") -> bool:
        return entry2.start <= self.start < entry2.end <= self.end

    def surrounds(self, entry2: "Entry") -> bool:
        return self.start < entry2.start < entry2.end < self.end

    def surrounded(self, entry2: "Entry") -> bool:
        return entry2.start < self.start < self.end < entry2.end

    def shares_start_shorter(self, entry2: "Entry") -> bool:
        return (self.start == entry2.start) and (self.end < entry2.end)

    def shares_start_longer(self, entry2: "Entry") -> bool:
        return (self.start == entry2.start) and (self.end > entry2.end)

    def shares_end_shorter(self, entry2: "Entry") -> bool:
        return (self.start > entry2.start) and (self.end == entry2.end)

    def shares_end_longer(self, entry2: "Entry") -> bool:
        return (self.start < entry2.start) and (self.end == entry2.end)

    def iscovered(self, entry2: "Entry") -> bool:
        return (self.start >= entry2.start) and (self.end <= entry2.end)

    def precedes(self, entry2: "Entry") -> bool:
        return self.priority > entry2.priority

    def temporal_relationship(self, entry2: "Entry") -> str:
        if self.before(entry2):
            return "before"
        elif self.after(entry2):
            return "after"
        elif self.overlaps_first(entry2):
            return "overlaps_first"
        elif self.overlaps_second(entry2):
            return "overlaps_second"
        elif self.surrounds(entry2):
            return "surrounds"
        elif self.surrounded(entry2):
            return "surrounded"

    def pretty(self, width: int = 80) -> str:
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = thickbeam + tabularize(f"{self.start} - {self.end}", width) + thinbeam
        return header + "\n".join(
            (
                tabularize(s, width, pad=1)
                for s in (self.name, f"Priority: {self.priority}", self.notes)
            )
        )

    def __repr__(self) -> str:
        return self.pretty()


class Empty(Entry):
    def __init__(self, start: PTime, end: PTime, time: Optional[int] = None):
        super().__init__(
            "Empty", start=start, end=end, priority=-1.0, normaltime=time, mintime=0
        )


# ent = Entry(PTime(5,30), PTime(6,20), "Workout", priority=30, notes="Running, pullups, pushups, medecine ball")
# print(ent.pretty())

FIRST_ENTRY = Entry(
    "First", start=PTime(), end=PTime(), ismovable=False, priority=-1.0, mintime=0
)
LAST_ENTRY = Entry(
    "Last", start=PTime(24), end=PTime(24), ismovable=False, priority=-1.0, mintime=0
)
