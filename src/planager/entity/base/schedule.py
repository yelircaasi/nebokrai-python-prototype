from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ...util import HTML, JSON, Norg, PDate, PTime, round5, tabularize
from ..container.entries import Entries
from ..container.routines import Routines
from ..container.tasks import Tasks
from .adhoc import AdHoc
from .entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from .plan import Plan


class Schedule:
    def __init__(
        self,
        date: Optional[PDate] = None,
        schedule: Optional[Entries] = None,
        width: int = 80,
        weight_interval_min: float = 0.8,
        weight_interval_max: float = 1.2,
    ) -> None:
        self.schedule = schedule or self.make_default_day()
        self.date: PDate = date or PDate.today() + 1
        self.width: int = width
        self.overflow: Entries = Entries()
        self.weight_interval_min = weight_interval_min
        self.weight_interval_max = weight_interval_max
        self.prio_transform: Callable = lambda x: (x / 100) ** 1.5

    def copy(self):
        newschedule = Schedule()
        newschedule.__dict__.update(self.__dict__)
        return newschedule

    @staticmethod
    def make_default_day() -> Entries:
        return Entries(
            [
                FIRST_ENTRY,
                Entry("Sleep", PTime(0), end=PTime(5), priority=70, ismovable=False),
                Empty(start=PTime(5), end=PTime(21)),
                Entry("Sleep", PTime(21), end=PTime(24), priority=70, ismovable=False),
                LAST_ENTRY,
            ]
        )

    @classmethod
    def from_norg(cls, path: Path) -> "Schedule":
        """ """
        schedule = cls()
        return schedule

    @classmethod
    def from_json(cls, path: Path) -> "Schedule":
        schedule = cls()
        return schedule

    @classmethod
    def from_html(cls, path: Path) -> "Schedule":
        schedule = cls()
        return schedule

    def to_norg(self, path: Path) -> None:
        norg = self.as_norg()
        with open(path, "w") as f:
            f.write(str(norg))

    def to_json(self, path: Path) -> None:
        json_obj = self.as_json()
        with open(path, "w") as f:
            f.write(json_obj.as_json_string())

    def to_html(self, path: Path) -> None:
        html_obj = self.as_html()
        with open(path, "w") as f:
            f.write(html_obj.as_html_string())

    def as_norg(self) -> Norg:
        return Norg()  # TODO

    def as_json(self) -> JSON:
        return JSON()  # TODO

    def as_html(self) -> HTML:
        return HTML()  # TODO

    def add(self, entry: Entry) -> None:
        """
        Top-level abstraction for adding an entry to the schedule.

        First checks for a block to add on top of, otherwise follows the default logic.
        """
        assert self.can_be_added(entry)  # TODO
        block_ind = min(self.schedule.get_inds_of_relevant_blocks(entry))
        if block_ind:
            self.schedule.add_to_block_by_index(entry, block_ind)
        else:
            self.schedule = self.allocate_in_time(self.schedule + [entry])

    def remove(self, entry: Entry) -> None:
        ...

    def names(self) -> List[str]:
        return [x.name for x in self.schedule]

    def starts(self) -> List[PTime]:
        return [x.start for x in self.schedule]

    def starts_strings(self) -> List[str]:
        return [str(x.start) for x in self.schedule]

    def add_routines(self, routines: Routines) -> None:  #  -> KEEP
        for routine in routines:
            if routine.valid_on(self.date):
                self.add(routine.as_entry(None))
                print(self)
            else:
                print(f"Not valid on {self.date}.")
        raise ValueError  # ---

    def add_from_plan(self, plan: Plan, tasks: Tasks) -> None:  #  -> KEEP
        for task_id in plan[self.date]:
            self.add(tasks[task_id].as_entry(None))

    def add_adhoc(self, adhoc: AdHoc) -> None:  #  -> KEEP
        for entry in adhoc[self.date]:
            self.add(entry)

    def can_be_added(
        self, entry: Entry
    ) -> bool:  # MOVE TO ENTRIES? NAH, GOOD TO HAVE ACCESSIBLE
        assert self.schedule.overlaps_are_movable(entry)
        if not entry.ismovable:
            overlaps = self.schedule.get_overlaps(entry)
            if not all(map(lambda x: x.ismovable, overlaps)):
                return False
        return sum(map(lambda x: x.mintime, self.schedule)) + entry.mintime < (24 * 60)

    def allocate_in_time(
        self, entries: Entries
    ) -> (
        Entries
    ):  # MOVE TO ENTRIES? NAH -> need to refactor this, make purely functional
        """
        Creates a schedule (i.e. entry list) from a list of entries. Steps:
          1) check whether the entries fit in a day
          2) get the compression factor, i.e. how much, on average, the entries need to be compacted in order to fit
          3) separate entries into fixed (immovable) and flex (movable)
          4) add the fixed entried to the schedule
          5) identify the gaps
          6) fill in the gaps with the flex items TODO
          7) resize between fixed points to remove small empty patches (where possible)
          TODO: add alignend functionality (but first get it working without)
        """
        assert Entries.entry_list_fits(entries)
        compression_factor = round(
            (24 * 60) / sum(map(lambda x: x.normaltime, entries)) - 0.01, 3
        )

        entries_fixed, entries_flex = self.schedule.get_fixed_and_flex()
        schedule = Entries([FIRST_ENTRY, *entries_fixed, LAST_ENTRY])

        schedule.fill_gaps(entries_flex, self.prio_weighting_function, compression_factor)
        schedule.smooth_between_fixed(self.prio_weighting_function)

        return schedule

    @property
    def prio_weighting_function(self) -> Callable[[Union[int, float]], float]:
        def time_weight_from_prio(prio: Union[int, float]) -> float:
            interval = self.weight_interval_max - self.weight_interval_min
            return self.weight_interval_min + interval * self.prio_transform(prio)

        return time_weight_from_prio

    def is_valid(self) -> bool:  # MAKE SIMILAR IN ENTRIES?
        """ """
        if len(self.schedule) == 1:
            adjacency = True
        else:
            adjacency = all(
                map(
                    lambda x: x[0].end == x[1].start,
                    zip(self.schedule.slice(None, -1), self.schedule.slice(1, None)),
                )
            )
        return (
            adjacency
            and (self.schedule[0].start == PTime())
            and (self.schedule[-1].end == PTime(24))
        )

    def __str__(self) -> str:
        """ """
        topbeam = "┏" + (self.width - 2) * "━" + "┓"
        date = tabularize(self.date.pretty(), self.width, thick=True)
        bottombeam = "┗" + (self.width - 2) * "━" + "┛"

        lines = []
        lines.append(topbeam)
        lines.append(date)
        for entry in self.schedule:
            if entry.priority >= 0:
                lines.append(entry.pretty(width=self.width))
        lines.append(bottombeam)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__repr__()
