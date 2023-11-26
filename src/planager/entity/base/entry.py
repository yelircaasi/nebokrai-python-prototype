import re
from typing import Any, Iterable, Optional, Union

from ...configuration import config
from ...util import PTime, round5, tabularize


class Entry:
    """
    A single schedule entry to be a part of Day, Routine, or another instance of Entry.
    """

    def __init__(
        self,
        name: str,
        start: Optional[PTime],
        end: Optional[PTime] = None,
        priority: Optional[Union[float, int]] = None,
        blocks: Optional[set[str]] = None,
        categories: Optional[set[str]] = None,
        notes: str = "",
        normaltime: Optional[int] = None,
        idealtime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        ismovable: bool = True,
        alignend: bool = False,
        order: Optional[float] = None,
        subentries: Optional[Iterable["Entry"]] = None,
    ) -> None:
        self.subentries: list[Entry] = list(subentries or [])

        # meta / info
        self.name = name
        self.notes = notes

        # algo
        self.start: PTime = start if isinstance(start, PTime) else PTime.nonetime()
        self.priority = config.default_priority if priority is None else priority
        self.blocks = blocks or set([])
        self.categories = (categories or set([])).union(config.default_categories)
        self.ismovable = ismovable

        if normaltime:
            self.normaltime = normaltime
        elif start and end:
            self.normaltime = start.timeto(end)
        elif idealtime:
            self.normaltime = round5(idealtime / config.default_idealtime_factor)
        elif mintime:
            self.normaltime = round5(mintime / config.default_mintime_factor)
        elif maxtime:
            self.normaltime = round5(maxtime / config.default_maxtime_factor)
        else:
            self.normaltime = config.default_normaltime

        self.idealtime: int = idealtime or round5(config.default_idealtime_factor * self.normaltime)
        self.mintime: int = mintime or round5(config.default_mintime_factor * self.normaltime)
        self.maxtime: int = maxtime or round5(config.default_maxtime_factor * self.normaltime)
        self.end: PTime = end or (self.start + self.normaltime)
        self.alignend: bool = alignend
        self.order: float = config.default_order if order is None else order
        self.assigned_time: Optional[int] = None

    @classmethod
    def from_dict(cls, entry_dict: dict[str, Any]) -> "Entry":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        normaltime = int(entry_dict.get("normaltime", config.default_normaltime))
        idealtime = (
            int(entry_dict["idealtime"])
            if "idealtime" in entry_dict
            else int(config.default_idealtime_factor * normaltime)
        )

        bool_helper = {None: True, False: False}

        return cls(
            entry_dict["name"],
            PTime.from_string(entry_dict.get("start") or "nonetime"),
            PTime.from_string(entry_dict.get("end") or "nonetime"),
            priority=entry_dict["priority"],
            blocks=set(re.split("[^A-z] ?", entry_dict["blocks"]))
            if "blocks" in entry_dict
            else set(),
            categories=set(re.split("[^A-z] ?", entry_dict["categories"])).union(
                config.default_categories
            )
            if "categories" in entry_dict
            else set(),
            notes=entry_dict.get("notes", ""),
            normaltime=normaltime,
            idealtime=idealtime,
            mintime=(
                int(entry_dict["mintime"])
                if "mintime" in entry_dict
                else int(config.default_mintime_factor * normaltime)
            ),
            maxtime=(
                int(entry_dict["maxtime"])
                if "maxtime" in entry_dict
                else int(config.default_maxtime_factor * normaltime)
            ),
            ismovable=bool_helper[entry_dict.get("ismovable")],
            alignend=bool_helper[entry_dict.get("alignend")],
            order=entry_dict.get("order") or config.default_order,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "start": str(self.start),
            "end": str(self.end),
            "NOTES": "Entry.as_dict() IS UNFINISHED",
        }

    @classmethod
    def first_entry(cls) -> "Entry":
        """
        Creates the opening bookend entry for padding and placeholding purposes.
        """
        return Entry(
            "First",
            start=PTime(),
            end=PTime(),
            ismovable=False,
            priority=-1.0,
            mintime=0,
            maxtime=0,
            idealtime=0,
        )

    @classmethod
    def last_entry(cls) -> "Entry":
        """
        Creates the opening bookend entry for padding and placeholding purposes.
        """
        return Entry(
            "Last",
            start=PTime(24),
            end=PTime(24),
            ismovable=False,
            priority=-1.0,
            mintime=0,
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

    def hasmass(self) -> bool:
        return (self.priority > 0) or (self.name in {"First", "Last"})

    def overlaps(self, entry2: "Entry") -> bool:
        return (self.start <= entry2.start < self.end) or (entry2.start <= self.start < entry2.end)

    def fits_into(self, __entry: "Entry", ratio: float = 1.0) -> bool:
        return self.mintime <= max(__entry.mintime, ratio * __entry.normaltime)

    def accommodates(self, __entry: "Entry", ratio: float = 1.0) -> bool:
        return __entry.fits_into(self, ratio=ratio)

    def add_subentry(self, subentry: "Entry") -> list["Entry"]:
        """
        Adds another entry to be part of self. Only works if self is a block,
          i.e. `self.blocks` is not empty.
        """
        self.assert_subentry_category(subentry)
        self.subentries.append(subentry)
        excess = self.pop_low_prio_subentries()
        self.subentries.sort(key=lambda e: (e.order, -e.priority))
        self.adjust_subentry_times()

        return excess

    def assert_subentry_category(self, subentry: "Entry") -> None:
        if not self.blocks.intersection(subentry.categories):
            raise ValueError(f"Invalid subentry '{subentry.name}' for entry '{self}'")

    def pop_low_prio_subentries(self) -> list["Entry"]:
        """
        Handle case where subentry does not fit - pop lowest-priority
        """
        excess: list[Entry] = []
        self.subentries.sort(key=lambda e: -e.priority)
        while sum(map(lambda se: se.duration, self.subentries)) > self.duration:
            excess.append(self.subentries.pop())
        if excess:
            print(f"The following entries do not fit in {self}: \n{excess}.")
        return excess

    def adjust_subentry_times(self) -> None:
        """
        Adjust times for subentries.
        """
        temp = self.start.copy()
        for subentry_ in self.subentries:
            subentry_.start = temp
            temp += subentry_.normaltime  # can change to use idealtime
            subentry_.end = temp

    @property
    def available(self) -> int:
        return self.duration - sum(map(lambda e: e.duration, self.subentries)) if self.blocks else 0

    @property
    def unavailable(self) -> int:
        return self.duration - self.available

    def subentry_string(self) -> str:
        """
        Creates a string representation for the subentries, to be
        """
        if not self.subentries:
            return ""
        width = config.repr_width
        top = "┠─┬─────────────┬" + (width - 18) * "─" + "┨"
        bottom = "┠─┴─────────────┴" + (width - 18) * "─" + "┨"
        middle = "\n┠─┼─────────────┼" + (width - 18) * "─" + "┨\n"
        body = middle.join(
            map(
                lambda sub: tabularize(f"│ {sub.start}-{sub.end} │ {sub.name}", width, thick=True),
                self.subentries,
            )
        )

        free = ""
        sub_end = self.subentries[-1].end
        if sub_end < self.end:
            free = tabularize(f"│ {sub_end}-{self.end} │ ", width, thick=True)
        if free:
            body += middle + free

        return "\n".join(("", top, body, bottom))

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Entry instance.
        """
        width = config.repr_width
        thickbeam = "┣━━━━━━━━━━━━━┯" + (width - 16) * "━" + "┫\n"
        thinbeam = "\n┠─────────────┴" + (width - 16) * "─" + "┨\n"
        header = (
            thickbeam
            + tabularize(f"{self.start}-{self.end} │ {self.name}", width, thick=True)
            + thinbeam
        )
        timestring = f"{self.normaltime}  ({self.mintime}-{self.maxtime}, ideal: {self.idealtime})"

        return (
            header
            + "\n".join(
                (
                    tabularize(s, width, thick=True, trailing_spaces=16)
                    for s in (
                        f"notes:        {self.notes}" if self.notes else "",
                        f"priority:     {self.priority}"
                        if self.priority != config.default_priority
                        else "",
                        f"time:         {timestring}",
                        f"blocks:       {', '.join(sorted(self.blocks))}" if self.blocks else "",
                        f"categories:   {', '.join(sorted(self.categories))}"
                        if self.categories != config.default_categories
                        else "",
                        f"ismovable:    {str(self.ismovable).lower()}"
                        if not self.ismovable == config.default_ismovable
                        else "",
                        f"alignend:     {str(self.alignend).lower()}"
                        if not self.alignend == config.default_alignend
                        else "",
                        f"order:        {int(self.order)}"
                        if not self.order == config.default_order
                        else "",
                    )
                    if s
                )
            )
            + self.subentry_string()
        )

    def __hash__(self) -> int:
        return hash((self.name, id(self)))

    def __eq__(self, entry2: "Entry") -> bool:  # type: ignore
        return self.__str__() == str(entry2)

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.pretty()


class Empty(Entry):
    """
    An entry representating a time slot with no assigned activity, i.e. a gap in the schedule.
    Used in scheduling algorithms.
    """

    def __init__(self, start: PTime, end: PTime):
        super().__init__(
            "Empty",
            start=start,
            end=end,
            priority=-1.0,
            blocks={"wildcard"},
            mintime=0,
        )

    @property
    def available(self) -> int:
        return self.duration
