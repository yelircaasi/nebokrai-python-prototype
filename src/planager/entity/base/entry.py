from pathlib import Path
from typing import Optional, Set, Tuple, Union

from ...util import PTime, round5, tabularize, wrap_string


class Entry:
    PRIORITY_DEFAULT = 10
    ORDER_DEFAULT = 50
    NORMALTIME_DEFAULT = 30
    IDEALTIME_FACTOR = 1.5
    MINTIME_FACTOR = 0.5
    MAXTIME_FACTOR = 2

    def __init__(
        self,
        name: str,
        start: Optional[PTime],
        end: Optional[PTime] = None,
        priority: Union[float, int] = PRIORITY_DEFAULT,
        ismovable: bool = True,
        blocks: Set[str] = set(),
        categories: Set[str] = set(),
        notes: str = "",
        normaltime: Optional[int] = None,
        idealtime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        alignend: bool = False,
        order: int = ORDER_DEFAULT,
    ) -> None:
        self.name = name
        self.start: PTime = start or PTime()
        self.priority = priority
        self.ismovable = ismovable
        self.blocks = blocks
        self.categories = categories.union({"wildcard"})
        self.notes = notes

        if normaltime:
            self.normaltime = normaltime
        elif start and end:
            self.normaltime = start.timeto(end)
        elif idealtime:
            self.normaltime = round5(idealtime / self.IDEALTIME_FACTOR)
        elif mintime:
            self.normaltime = round5(mintime / self.MINTIME_FACTOR)
        elif maxtime:
            self.normaltime = round5(maxtime / self.MAXTIME_FACTOR)
        else:
            self.normaltime = self.NORMALTIME_DEFAULT

        self.end: PTime = end or (self.start + self.normaltime)
        self.idealtime: int = idealtime or int(self.IDEALTIME_FACTOR * self.normaltime)
        self.mintime: int = mintime or int(self.MINTIME_FACTOR * self.normaltime)
        self.maxtime: int = maxtime or int(self.MAXTIME_FACTOR * self.normaltime)
        self.alignend: bool = alignend
        self.order: int = order

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

    @property
    def duration(self) -> int:
        return self.start.timeto(self.end)

    def timespan(self) -> Tuple[PTime, PTime]:
        return (self.start, self.end)

    def as_norg(
        self,
        path: Path,
        head_prefix: str = "-",
        attr_prefix: str = "  -- ",
        width: int = 80,
    ) -> str:
        lines = (
            f"{head_prefix}{self.start}-{self.end} | {self.name}"
            f"{attr_prefix}priority:   {self.priority}"
            if self.priority != 10
            else "" f"{attr_prefix}ismovable:  {str(self.ismovable).lower()}"
            if not self.ismovable
            else "" f"{attr_prefix}blocks:     {', '.join(self.blocks)}"
            if self.blocks
            else "" f"{attr_prefix}categories: {', '.join(self.categories)}"
            if self.categories
            else ""
            f"{attr_prefix}notes:      {wrap_string(self.notes, width=(width - 14 - len(attr_prefix)), trailing_spaces=19)}"
            if self.notes
            else ""
            f"{attr_prefix}normaltime: {self.normaltime}"
            f"{attr_prefix}idealtime:  {self.idealtime}"
            if self.idealtime != (1.5 * self.normaltime)
            else "" f"{attr_prefix}mintime:    {self.mintime}"
            if self.mintime != (0.5 * self.normaltime)
            else "" f"{attr_prefix}maxtime:    {self.maxtime}"
            if self.maxtime != (2 * self.normaltime)
            else "" f"{attr_prefix}alignend:   {str(self.alignend).lower()}"
            if self.alignend
            else "" f"{attr_prefix}order:      {self.order}"
            if self.order != 50
            else ""
        )

    def as_json(self, path: Path) -> str:
        ...

    def as_html(self, path: Path) -> str:
        ...

    def hasmass(self) -> bool:
        return (self.priority > 0) or (self.name in {"First", "Last"})

    def isbefore(self, entry2: "Entry") -> bool:
        return self.end <= entry2.start

    def isafter(self, entry2: "Entry") -> bool:
        return self.start >= entry2.end

    def isbefore_by_start(self, entry2: "Entry") -> bool:
        return self.start < entry2.start

    def isafter_by_start(self, entry2: "Entry") -> bool:
        return self.start >= entry2.start

    def overlaps(self, entry2: "Entry") -> bool:
        return (self.start <= entry2.start < self.end) or (
            entry2.start <= self.start < entry2.end
        )

    def overlaps_first(self, entry2: "Entry") -> bool:
        return (self.start < entry2.start < self.end <= entry2.end) or (
            self.start <= entry2.start < self.end < entry2.end
        )

    def overlaps_second(self, entry2: "Entry") -> bool:
        return (entry2.start < self.start < entry2.end <= self.end) or (
            entry2.start <= self.start < entry2.end < self.end
        )

    def surrounds(self, entry2: "Entry") -> bool:
        return self.start < entry2.start < entry2.end < self.end

    def surrounded_by(self, entry2: "Entry") -> bool:
        return entry2.start < self.start < self.end < entry2.end

    def shares_start_shorter(self, entry2: "Entry") -> bool:
        return (self.start == entry2.start) and (self.end < entry2.end)

    def shares_start_longer(self, entry2: "Entry") -> bool:
        return (self.start == entry2.start) and (self.end > entry2.end)

    def shares_end_shorter(self, entry2: "Entry") -> bool:
        return (self.start > entry2.start) and (self.end == entry2.end)

    def shares_end_longer(self, entry2: "Entry") -> bool:
        return (self.start < entry2.start) and (self.end == entry2.end)

    def covers(self, entry2: "Entry") -> bool:
        return (entry2.start >= self.start) and (entry2.end <= self.end)

    def iscovered(self, entry2: "Entry") -> bool:
        return (self.start >= entry2.start) and (self.end <= entry2.end)

    def trumps(self, entry2: "Entry") -> bool:
        return self.priority > entry2.priority

    def fits_in(self, __entry: "Entry", ratio: float = 1.0) -> bool:
        return self.duration >= max(__entry.mintime, ratio * __entry.normaltime)

    def accommodates(self, __entry: "Entry", ratio: float = 1.0) -> bool:
        return __entry.fits_in(self, ratio=ratio)

    def pretty(self, width: int = 80) -> str:
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = thickbeam + tabularize(f"{self.start} - {self.end}", width) + thinbeam
        return header + "\n".join(
            (
                tabularize(s, width, thick=True)
                for s in (self.name, f"Priority: {self.priority}", self.notes)
            )
        )

    def __eq__(self, entry2: "Entry") -> bool:  # type: ignore
        return self.__str__() == str(entry2)

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.pretty()


class Empty(Entry):
    def __init__(self, start: PTime, end: PTime, time: Optional[int] = None):
        _time = time or 30
        super().__init__(
            "Empty",
            start=start,
            end=end,
            priority=-1.0,
            blocks={"wildcard"},
            normaltime=_time,
            mintime=0,
        )


FIRST_ENTRY = Entry(
    "First", start=PTime(), end=PTime(), ismovable=False, priority=-1.0, mintime=0
)
LAST_ENTRY = Entry(
    "Last",
    start=PTime(24),
    end=PTime(24),
    ismovable=False,
    priority=-1.0,
    mintime=0,
)
