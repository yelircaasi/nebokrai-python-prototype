from typing import Callable, Iterable, Optional, Union

from ...configuration import config
from ...util import PDate, PTime, tabularize
from ..container.entries import Entries
from .calendar import Calendar
from .entry import Empty, Entry
from .plan import Plan


class Schedule:
    """
    Contains entries assigned to times.
    """

    def __init__(
        self,
        date: PDate,
        schedule: Iterable[Entry],
        weight_interval_min: Optional[float] = None,
        weight_interval_max: Optional[float] = None,
        schedule_weight_transform_exponent: Optional[float] = None,
    ) -> None:
        self.width: int = config.repr_width

        self.schedule = Entries(schedule)

        # meta / info
        self.date: PDate = date

        # algo
        self.weight_interval_min = (
            weight_interval_min or config.default_schedule_weight_interval_min
        )
        self.weight_interval_max = (
            weight_interval_max or config.default_schedule_weight_interval_max
        )
        self.schedule_weight_transform_exponent = (
            schedule_weight_transform_exponent or config.default_schedule_weight_transform_exponent
        )

        # record
        self.overflow: Entries = Entries()

    def copy(self):
        newschedule = Schedule(config, self.date, [])
        newschedule.__dict__.update(self.__dict__)
        return newschedule

    @classmethod
    def from_calendar(cls, calendar: Calendar, date: PDate) -> "Schedule":
        return cls(date, calendar[date].entries)

    def remove(self, entry: Entry) -> None:
        self.schedule.remove(entry)

    def names(self) -> list[str]:
        return [x.name for x in self.schedule]

    def starts(self) -> list[PTime]:
        return [x.start for x in self.schedule]

    def starts_strings(self) -> list[str]:
        return [str(x.start) for x in self.schedule]

    def can_be_added(self, entry: Entry) -> bool:
        """
        Checks whether the given entry can be added.
        """
        if not entry.start:
            return True
        if not self.schedule.overlaps_are_movable(entry):
            return False
        if not entry.ismovable:
            overlaps = self.schedule.get_overlaps(entry)
            if not all(map(lambda x: x.ismovable, overlaps)):
                return False
        return sum(map(lambda x: x.mintime, self.schedule)) + entry.mintime < (24 * 60)

    @property
    def empty_time(self) -> int:
        """
        Returns the amount of empty time remaining in the schedule.
        """
        empties = filter(lambda e: isinstance(e, Empty), self.schedule)
        return sum(map(lambda e: e.duration, empties))

    @property
    def total_available(self) -> int:
        return sum(map(lambda e: e.available, self.schedule))

    @property
    def available_dict(self) -> dict[str, int]:
        """
        Returns a dictionary containing the time available for each block,
          for miscellaneous entries (i.e. empty time), and in total.
        """
        time_dict: dict[str, int] = {}
        time_dict.update({"empty": self.empty_time})
        time_dict.update({"total": self.total_available})
        for block in self.schedule.blocks:
            time_dict.update({block: self.schedule.available_for_block(block)})
        return time_dict

    @property
    def prio_weighting_function(self) -> Callable[[Union[int, float]], float]:
        """
        Returns a function used to divide time between entries when compression is required.
          It does so my mapping the respective priority values to relative time weights.
        """

        def time_weight_from_prio(prio: Union[int, float]) -> float:
            interval = self.weight_interval_max - self.weight_interval_min
            return (
                self.weight_interval_min + interval * prio / 100
            ) ** self.schedule_weight_transform_exponent

        return time_weight_from_prio

    @property
    def flex_list_and_fixed_clusters(self) -> tuple[list[Entry], list[list[Entry]]]:  # REFACTOR
        """
        Gets a list of movable entries and a list of lists (clusters) of adjacent fixed entries.
        """
        flex = sorted([e for e in self.schedule if e.ismovable], key=lambda e: e.start)
        fixed = sorted([e for e in self.schedule if not e.ismovable], key=lambda e: e.start)
        fixed_clusters = [[fixed.pop(0)]]
        while fixed:
            next_entry = fixed.pop(0)
            if fixed_clusters[-1][-1].end == next_entry.start:
                fixed_clusters[-1].append(next_entry)
            else:
                fixed_clusters.append([next_entry])

        return flex, fixed_clusters

    @property
    def entries(self) -> Entries:
        return Entries(filter(lambda x: isinstance(x, Entry), self.schedule))

    @property
    def is_valid(self) -> bool:
        """
        Checks whether all entries partition the time in the day.
        """
        return self.schedule.ispartitioned

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
                lines.append(entry.pretty())
        lines.append(bottombeam)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__repr__()


# TODO:  refactor
def add_from_plan_and_excess(
    schedule: Schedule, plan: Optional[Plan], excess: Entries
) -> tuple[Schedule, "Entries"]:  # REFACTOR
    """
    Adds all tasks planned for this day, converting tasks to entries.
    """
    if plan is None:
        raise ValueError("'plan' must already be defined when scheduling.")
    # combine entries from plan with excess
    entries = Entries(map(lambda t: t.as_entry(), plan[schedule.date]))
    entries.extend(excess)

    # first, add to blocks where possible
    to_remove = []
    for entry in entries:
        for block in schedule.schedule:
            if entry.categories.intersection(block.blocks) and entry not in to_remove:
                block.add_subentry(entry)
                to_remove.append(entry)
    for entry in to_remove:
        entries.remove(entry)

    flex_entries, fixed_clusters = schedule.flex_list_and_fixed_clusters

    entries.extend(flex_entries)
    entries.sort(key=lambda e: (e.order, -e.priority))

    new_entries = Entries()
    next_entry = entries.pop(0)
    new_entries.extend(fixed_clusters.pop(0))
    new_entries.append(next_entry)

    # heavy-lifting loop
    while fixed_clusters:
        hard_start = new_entries.last_fixed.start
        hard_end = fixed_clusters[0][0].start
        while entries and (
            (new_entries.fixed_to_end.total_normaltime + next_entry.normaltime)
            < hard_start.timeto(hard_end)
        ):
            # 1) attempt to add next entry to the next available gap between fixed blocks
            next_entry = entries.pop(0)
            new_entries.append(next_entry)
            new_entries.schedule_tail(hard_end)
            new_entries.extend(fixed_clusters.pop(0))

    schedule.schedule = new_entries

    return schedule, entries


# rewrite
def add_to_block_by_index(self, entry: Entry, block_ind: int) -> None:
    """
    Add the input entry 'on top of' the entry corresponding to the given index.
    """
    block_entry = self.schedule[block_ind]
    assert id(block_entry) == id(self.schedule[block_ind])
    assert block_entry.blocks.intersection(entry.categories)

    block_entry.add_subentry(entry)
