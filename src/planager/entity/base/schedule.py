from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Union

from ...util import HTML, JSON, Norg, PDate, PTime, round5, tabularize
from ..container.entries import Entries
from ..container.routines import Routines
from ..container.tasks import Tasks
from .calendar import Calendar
from .entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from .plan import Plan


class Schedule:
    def __init__(
        self,
        date: Optional[PDate] = None,
        schedule: Optional[Iterable[Entry]] = None,
        width: int = 80,
        weight_interval_min: float = 0.8,
        weight_interval_max: float = 1.2,
        prio_transform: Callable = lambda x: (x / 100) ** 1.5,
    ) -> None:
        self.schedule = Entries(schedule) if schedule is not None else self.make_default_day()
        self.date: PDate = date or PDate.today() + 1
        self.width: int = width
        self.overflow: Entries = Entries()
        self.weight_interval_min = weight_interval_min
        self.weight_interval_max = weight_interval_max
        self.prio_transform: Callable = prio_transform
        

    def copy(self):
        newschedule = Schedule()
        newschedule.__dict__.update(self.__dict__)
        return newschedule

    @classmethod
    def from_calendar(cls, calendar: Calendar, date: PDate) -> "Schedule":
        sched = cls(date)
        ...
        return sched

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

    # def to_norg(self, path: Path) -> None:
    #     norg = self.as_norg()
    #     with open(path, "w") as f:
    #         f.write(str(norg))

    def to_json(self, path: Path) -> None:
        json_obj = self.as_json()
        with open(path, "w") as f:
            f.write(json_obj.as_json_string())

    def to_html(self, path: Path) -> None:
        html_obj = self.as_html()
        with open(path, "w") as f:
            f.write(html_obj.as_html_string())

    # def as_norg(self) -> Norg:
    #     return Norg()  # TODO

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
            self.schedule = Entries.allocate_in_time(
                self.schedule + [entry], self.prio_weighting_function
            )

    def remove(self, entry: Entry) -> None:
        ...

    def names(self) -> list[str]:
        return [x.name for x in self.schedule]

    def starts(self) -> list[PTime]:
        return [x.start for x in self.schedule]

    def starts_strings(self) -> list[str]:
        return [str(x.start) for x in self.schedule]

    def add_routines(
        self, routines_list: list[str], routines: Routines
    ) -> None:  #  -> KEEP
        for routine_name in routines_list:
            routine = routines[routine_name]
            if routine.valid_on(self.date):
                self.add(routine.as_entry())
                print(self)
            else:
                print(f"Not valid on {self.date}.")
        raise ValueError  # ---

    def add_from_plan(self, plan: Plan, tasks: Tasks) -> None:  #  -> KEEP
        for task_id in plan[self.date]:
            self.add(tasks[task_id].as_entry(None))

    def can_be_added(
        self, entry: Entry
    ) -> bool:  # MOVE TO ENTRIES? NAH, GOOD TO HAVE ACCESSIBLE
        assert self.schedule.overlaps_are_movable(entry)
        if not entry.ismovable:
            overlaps = self.schedule.get_overlaps(entry)
            if not all(map(lambda x: x.ismovable, overlaps)):
                return False
        return sum(map(lambda x: x.mintime, self.schedule)) + entry.mintime < (24 * 60)

    @property
    def empty_time(self) -> int:
        return sum(
            map(
                lambda e: e.duration,
                filter(lambda e: isinstance(e, Empty), self.schedule),
            )
        )
    
    @property
    def total_available(self) -> int:
        return sum(map(lambda e: e.available, self.schedule))

    @property
    def available_dict(self) -> dict[str, int]:
        time_dict: dict[str, int] = {}
        time_dict.update({"empty": self.empty_time})
        time_dict.update({"total": self.total_available})
        for block in self.schedule.blocks:
            time_dict.update({block: self.schedule.available_for_block(block)})
        return time_dict

    @property
    def prio_weighting_function(self) -> Callable[[Union[int, float]], float]:
        def time_weight_from_prio(prio: Union[int, float]) -> float:
            interval = self.weight_interval_max - self.weight_interval_min
            return self.weight_interval_min + interval * self.prio_transform(prio)

        return time_weight_from_prio
    
    @property
    def entries(self) -> Entries:
        return Entries(filter(lambda x: isinstance(x, Entry), self.schedule))

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
