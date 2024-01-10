from typing import Callable, Iterable, Optional, Union

from ...configuration import config
from ...util import NKDate, NKTime, color, tabularize
from ...util.serde.custom_dict_types import ScheduleDictRaw
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
        date: NKDate,
        schedule: Iterable[Entry],
        weight_interval_min: Optional[float] = None,
        weight_interval_max: Optional[float] = None,
        schedule_weight_transform_exponent: Optional[float] = None,
    ) -> None:
        self.width: int = config.repr_width

        self.schedule = Entries(schedule)

        # meta / info
        self.date: NKDate = date

        # algo
        self.weight_interval_min = (
            weight_interval_min or config.default_schedule_weight_interval_min
        )
        self.weight_interval_max = (
            weight_interval_max or config.default_schedule_weight_interval_max
        )
        self.schedule_weight_transform_exponent = (
            schedule_weight_transform_exponent or config.default_sched_weight_transform_exp
        )

        # record
        self.overflow: Entries = Entries()

    def copy(self):
        newschedule = Schedule(config, self.date, [])
        newschedule.__dict__.update(self.__dict__)
        return newschedule

    def serialize(self) -> ScheduleDictRaw:
        """
        Serialize contents of the current instance as a JSON-writable dictionary.
        """
        serialized: ScheduleDictRaw = {
            "date": str(self.date),
            "entries": list(map(Entry.serialize, self.entries)),
        }
        return serialized

    @classmethod
    def from_calendar(cls, calendar: Calendar, date: NKDate) -> "Schedule":
        return cls(date, calendar[date].entries)

    @classmethod
    def from_derivation(cls, schedule_derivation_dict: ScheduleDictRaw) -> "Schedule":
        """
        Create an instance from the dictionary from derivation/plan.json.
        """
        print(schedule_derivation_dict)  # TODO
        date = NKDate(2025, 1, 1)
        schedule_list: list[Entry] = []
        return Schedule(date, schedule_list)  # TODO

    def remove(self, entry: Entry) -> None:
        self.schedule.remove(entry)

    def names(self) -> list[str]:
        return [x.name for x in self.schedule]

    def starts(self) -> list[NKTime]:
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

    def get_flex_entries_and_fixed_clusters(
        self, entries: Entries = Entries()
    ) -> tuple[list[Entry], list[Entry]]:
        """
        Gets a list of movable entries and a list of lists (clusters) of adjacent fixed entries.
        """
        temp_entries = self.schedule + entries
        flex = sorted([e for e in temp_entries if e.ismovable], key=lambda e: e.start)
        fixed = sorted([e for e in temp_entries if not e.ismovable], key=lambda e: e.start)

        return flex, fixed

    @property
    def entries(self) -> Entries:
        return Entries(filter(lambda x: isinstance(x, Entry), self.schedule))

    @property
    def is_valid(self) -> bool:
        """
        Checks whether all entries partition the time in the day.
        """
        return self.schedule.ispartitioned

    @property
    def summary(self) -> str:
        return "'Schedule.summary' not yet implemented."

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

    @property
    def repr1(self) -> str:
        def stringify(entry: Entry) -> str:
            return f"{color.green(entry.start)} {color.magenta(entry.name)}"

        return f"Schedule {self.date}: {' | '.join(map(stringify, self.schedule))}"


def entries_from_plan_and_excess(plan: Plan, excess: Entries, date: NKDate) -> Entries:
    """
    Combine entries from plan with excess
    """
    entries = Entries(map(lambda t: t.as_entry(), plan[date]))
    entries.extend(excess)
    return entries


def add_to_blocks(schedule: Schedule, entries: Entries) -> tuple[Schedule, Entries]:
    """
    Add entries to blocks in schedule where possible.
    """
    to_remove = []
    for entry in entries:
        for block in schedule.schedule:
            if entry.categories.intersection(block.blocks) and entry not in to_remove:
                block.add_subentry(entry)
                print(f"Added {color.yellow(entry.fullname)} to {color.green(str(schedule.date))}.")

                to_remove.append(entry)
    for entry in to_remove:
        entries.remove(entry)
        print(f"Removed {color.yellow(entry.fullname)} from list.")
    return schedule, entries


def zip_flex_and_fixed(
    flex_entries: list[Entry],
    fixed_entries: list[Entry],
) -> Entries:
    """
    Adds two lists, consisting of movable and immovable entries, according to which one fits next
      without violating immovability constraints.
    """
    flex_entries.sort(key=lambda e: (e.order, -e.priority))
    new_entries = Entries()

    while flex_entries or fixed_entries:
        # color.pgreen("Zipping fixed and flex entries:")
        # color.pgreen(new_entries.summary)
        flex_entries, fixed_entries = new_entries.append_flex_or_fixed(flex_entries, fixed_entries)

    return new_entries


def assert_plan_and_date(plan: Optional[Plan], date: NKDate) -> Plan:
    """
    Ensures that the plan is not None and contains the specified day.
    """
    if plan is None:
        raise ValueError("'plan' must already be defined when scheduling.")
    if plan.get(date) is None:
        raise ValueError(f"Date '{date}' missing from plan.")
    return plan


def add_from_plan_and_excess(
    schedule: Schedule, plan: Optional[Plan], excess: Entries
) -> tuple[Schedule, "Entries"]:
    """
    Adds all tasks planned for this day, converting tasks to entries.
    """
    color.pblack("Entering add_from_plan_and_excess()")
    plan = assert_plan_and_date(plan, schedule.date)
    entries: Entries = entries_from_plan_and_excess(plan, excess, schedule.date)
    schedule, entries = add_to_blocks(schedule, entries)
    flex_entries, fixed_clusters = schedule.get_flex_entries_and_fixed_clusters(entries)

    schedule.schedule = zip_flex_and_fixed(flex_entries, fixed_clusters)

    color.pblack("Exiting add_from_plan_and_excess()")

    return schedule, entries
