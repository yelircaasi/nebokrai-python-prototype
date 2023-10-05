from pathlib import Path
import re
from typing import Any, Iterable, Optional, Union


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
        blocks: set[str] = set(),
        categories: set[str] = set(),
        notes: str = "",
        normaltime: Optional[int] = None,
        idealtime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        ismovable: bool = True,
        alignend: bool = False,
        order: int = ORDER_DEFAULT,
    ) -> None:
        self.name = name
        self.start: PTime = start or PTime()
        self.priority = priority
        self.blocks = blocks
        self.categories = categories.union({"wildcard"})
        self.notes = notes
        self.ismovable = ismovable

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

        self.subentries: list[Entry] = []

    @classmethod
    def from_dict(cls, entry_dict: dict[str, Any]) -> "Entry":
        normaltime = int(entry_dict.get("notes", "30"))
        idealtime = (
            int(entry_dict["idealtime"])
            if "idealtime" in entry_dict
            else int(1.5 * normaltime)
        )
        mintime = (
            int(entry_dict["mintime"])
            if "mintime" in entry_dict
            else int(0.5 * normaltime)
        )
        maxtime = (
            int(entry_dict["maxtime"])
            if "maxtime" in entry_dict
            else int(2 * normaltime)
        )
        return cls(
            entry_dict["name"],
            PTime.from_string(entry_dict["start"]),
            PTime.from_string(entry_dict["end"]),
            priority=entry_dict["priority"],
            blocks=set(re.split("[^A-z] ?", entry_dict["blocks"]))
            if "blocks" in entry_dict
            else set(),
            categories=set(re.split("[^A-z] ?", entry_dict["categories"]))
            if "categories" in entry_dict
            else set(),
            notes=entry_dict.get("notes", ""),
            normaltime=normaltime,
            idealtime=idealtime,
            mintime=mintime,
            maxtime=maxtime,
            ismovable=entry_dict.get("ismovable") or True,
            alignend=entry_dict.get("alignend") or True,
            order=entry_dict.get("order") or cls.ORDER_DEFAULT,
        )

    def copy(self) -> "Entry":
        return Entry(
            self.name,
            start=self.start,
            end=self.end,
            priority=self.priority,
            ismovable=self.ismovable,
            blocks=self.blocks,
            categories=self.categories,
            notes=self.notes,
            normaltime=self.normaltime,
            idealtime=self.idealtime,
            mintime=self.mintime,
            maxtime=self.maxtime,
            alignend=self.alignend,
            order=self.order,
        )

    @property
    def duration(self) -> int:
        return self.start.timeto(self.end)

    @property
    def timespan(self) -> tuple[PTime, PTime]:
        return (self.start, self.end)

    def as_norg(
        self,
        # path: Optional[Path] = None,
        head_prefix: str = "~ ",
        attr_prefix: str = "  -- ",
        width: int = 80,
    ) -> str:
        lines = "".join(
            (
                f"{head_prefix}{self.start}-{self.end} | {self.name}\n",
                f"{attr_prefix}notes:      {wrap_string(self.notes, width=(width - 14 - len(attr_prefix)), trailing_spaces=19)}\n"
                if self.notes
                else "",
                f"{attr_prefix}priority:   {self.priority}\n"
                if self.priority != 10
                else "",
                f"{attr_prefix}blocks:     {', '.join(sorted(self.blocks))}\n"
                if self.blocks
                else "",
                f"{attr_prefix}categories: {', '.join(sorted(self.categories))}\n"
                if self.categories != {"wildcard"}
                else "",
                f"{attr_prefix}normaltime: {self.normaltime}\n",
                f"{attr_prefix}idealtime:  {self.idealtime}\n"
                if self.idealtime != (1.5 * self.normaltime)
                else "",
                f"{attr_prefix}mintime:    {self.mintime}\n"
                if self.mintime != (0.5 * self.normaltime)
                else "",
                f"{attr_prefix}maxtime:    {self.maxtime}\n"
                if self.maxtime != (2 * self.normaltime)
                else "",
                f"{attr_prefix}ismovable:  {str(self.ismovable).lower()}\n"
                if not self.ismovable
                else "",
                f"{attr_prefix}order:      {self.order}\n" if self.order != 50 else "",
                f"{attr_prefix}alignend:   {str(self.alignend).lower()}\n"
                if self.alignend
                else "",
            )
        ).strip("\n")
        return lines

    def as_json(self, path: Path) -> str:
        return ""

    def as_html(self, path: Path) -> str:
        return ""

    def hasmass(self) -> bool:
        return (self.priority > 0) or (self.name in {"First", "Last"})

    def isbefore(self, entry2: "Entry") -> bool:
        return self.end <= entry2.start

    def isafter(self, entry2: "Entry") -> bool:
        return self.start >= entry2.end

    def isbefore_by_start(self, entry2: "Entry") -> bool:
        return self.start < entry2.start

    def isafter_by_start(self, entry2: "Entry") -> bool:
        return self.start > entry2.start

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
        return self.mintime <= max(__entry.mintime, ratio * __entry.normaltime)

    def accommodates(self, __entry: "Entry", ratio: float = 1.0) -> bool:
        return __entry.fits_in(self, ratio=ratio)

    def add_subentry(self, subentry: "Entry") -> None:
        if not self.blocks.intersection(subentry.categories):
            raise ValueError(f"")
        if self.accommodates(subentry):
            self.subentries.append(subentry)
            self.subentries.sort(key=lambda e: (e.order, e.priority))
        else:
            raise ValueError(f"Entry {subentry} does not fit in {self}.")

    @property
    def available(self) -> int:
        return (
            self.start.timeto(self.end)
            - sum(map(lambda e: e.duration, self.subentries))
            if self.blocks
            else 0
        )

    def pretty(self, width: int = 80) -> str:
        thickbeam = "┣━━━━━━━━━━━━━┯" + (width - 16) * "━" + "┫\n"
        thinbeam = "\n┠─────────────┴" + (width - 16) * "─" + "┨\n"
        header = (
            thickbeam
            + tabularize(f"{self.start}-{self.end} │ {self.name}", width, thick=True)
            + thinbeam
        )
        return header + "\n".join(
            (
                tabularize(s, width, thick=True, trailing_spaces=16)
                for s in (
                    f"notes:        {self.notes}" if self.notes else "",
                    f"priority:     {self.priority}" if self.priority != 10 else "",
                    f"time:         {self.normaltime}  ({self.mintime}-{self.maxtime}, ideal: {self.idealtime})",
                    f"blocks:       {', '.join(sorted(self.blocks))}"
                    if self.blocks
                    else "",
                    f"categories:   {', '.join(sorted(self.categories))}"
                    if self.categories != {"wildcard"}
                    else "",
                    f"ismovable:    {str(self.ismovable).lower()}"
                    if not self.ismovable
                    else "",
                    f"alignend:     {str(self.alignend).lower()}"
                    if self.alignend
                    else "",
                    f"order:        {self.order}" if not self.order == 50 else "",
                )
                if s
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

    @property
    def available(self) -> int:
        return self.duration


# class Block(Entry):
#     def __init__(
#         self, name: str, start: PTime, end: PTime, entries: Iterable[Entry]
#     ) -> None:
#         self.name = name
#         self.start = start
#         self.end = end
#         self.entries = list(entries)

#     # @property

#     @property
#     def available(self) -> int:
#         return self.start.timeto(self.end) - sum(map(lambda e: e.duration, self.entries))


# class RoutineEntry(Entry):
#     def __init__(self, routine: Routine)


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
