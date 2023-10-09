from typing import Callable, Iterable, Optional, Union

from ...config import Config
from ...util import PDate, PTime, tabularize
from ..container.entries import Entries
from ..container.tasks import Tasks
from .calendar import Calendar
from .entry import Empty, Entry
from .plan import Plan


class Schedule:
    """
    Contains entries assigned to times.
    """

    def __init__(
        self,
        config: Config,
        date: PDate,
        schedule: Iterable[Entry],
        weight_interval_min: Optional[float] = None,
        weight_interval_max: Optional[float] = None,
        prio_transform: Callable = lambda x: (x / 100) ** 1.5,
    ) -> None:
        self.schedule = Entries(config, schedule)
        self.config = config
        self.date: PDate = date or PDate.today() + 1  # TODO: remove default
        self.width: int = config.repr_width
        self.overflow: Entries = Entries(config)
        self.weight_interval_min = (
            weight_interval_min or config.default_schedule_weight_interval_min
        )
        self.weight_interval_max = (
            weight_interval_max or config.default_schedule_weight_interval_max
        )
        self.prio_transform: Callable = prio_transform

    def copy(self):
        newschedule = Schedule(self.config, self.date, [])
        newschedule.__dict__.update(self.__dict__)
        return newschedule

    @classmethod
    def from_calendar(cls, calendar: Calendar, date: PDate) -> "Schedule":
        return cls(calendar.config, date, calendar[date].entries)

    def add(self, entry: Entry) -> None:
        """
        Top-level abstraction for adding an entry to the schedule.

        First checks for a block to add on top of, otherwise follows the default logic.
        """
        # print(entry.start)
        # print(bool(entry.start))
        assert self.can_be_added(entry), f"--------------------------\n\n{entry}\n\n{self}"
        # TODO ^
        rel_block_inds = self.schedule.get_inds_of_relevant_blocks(entry)
        block_ind: Optional[int] = min(rel_block_inds) if rel_block_inds else None
        if block_ind:
            self.schedule.add_to_block_by_index(entry, block_ind)
        else:
            self.schedule = self.allocate_in_time(
                self.schedule + [entry], self.prio_weighting_function
            )

    @staticmethod
    def allocate_in_time(
        entries: "Entries",
        prio_weighting_function: Callable,
    ) -> "Entries":  # MOVE TO ENTRIES? NAH -> need to refactor this, make purely functional
        """
        Creates a schedule (i.e. entry list) from a list of entries. Steps:
          1) check whether the entries fit in a day
          2) get the compression factor, i.e. how much, on average, the entries need to be compacted
             in order to fit
          3) separate entries into fixed (immovable) and flex (movable)
          4) add the fixed entries to the schedule
          5) identify the gaps
          6) fill in the gaps with the flex items TODO
          7) resize between fixed points to remove small empty patches (where possible)
          TODO: add alignend functionality (but first get it working without)
        """
        # entries.extend(self.schedule)
        assert Entries.entry_list_fits(entries)
        compression_factor = round((24 * 60) / sum(map(lambda x: x.normaltime, entries)) - 0.01, 3)

        entries_fixed, entries_flex = entries.get_fixed_and_flex()
        schedule = Entries(
            entries.config,
            [Entry.first_entry(entries.config), *entries_fixed, Entry.last_entry(entries.config)],
        )
        # schedule = Entries(entries.config, [*entries_fixed])

        schedule.fill_gaps(entries_flex, prio_weighting_function, compression_factor)
        schedule.smooth_between_fixed(prio_weighting_function)

        return schedule

    def remove(self, entry: Entry) -> None:
        self.schedule.remove(entry)

    def names(self) -> list[str]:
        return [x.name for x in self.schedule]

    def starts(self) -> list[PTime]:
        return [x.start for x in self.schedule]

    def starts_strings(self) -> list[str]:
        return [str(x.start) for x in self.schedule]

    # def add_routines(
    #     self, routines_dict: dict[str, dict], routines: Routines
    # ) -> None:  #  -> KEEP
    #     for routine_name in routines_dict:
    #         routine = routines[routine_name]
    #         if routine.valid_on(self.date):
    #             self.add(routine.as_entry())
    #             print(self)
    #         else:
    #             print(f"Not valid on {self.date}.")
    #     raise ValueError  # ---

    def add_from_plan(self, plan: Plan, tasks: Tasks) -> None:  #  -> KEEP
        for task_id in plan[self.date]:
            self.add(tasks[task_id].as_entry(PTime.nonetime()))

    def can_be_added(self, entry: Entry) -> bool:
        """
        Checks whether the given entry can be added.
        """
        # MOVE TO ENTRIES? NAH, GOOD TO HAVE ACCESSIBLE
        # assert self.schedule.overlaps_are_movable(entry)
        if not entry.start:
            return True
        if not self.schedule.overlaps_are_movable(entry):
            print("A")
            return False
        if not entry.ismovable:
            print("B")
            overlaps = self.schedule.get_overlaps(entry)
            if not all(map(lambda x: x.ismovable, overlaps)):
                print("C")
                return False
        print("D")
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
            return self.weight_interval_min + interval * self.prio_transform(prio)

        return time_weight_from_prio

    @property
    def entries(self) -> Entries:
        return Entries(self.config, filter(lambda x: isinstance(x, Entry), self.schedule))

    def is_valid(self) -> bool:  # MAKE SIMILAR IN ENTRIES?
        """
        Checks whether all entries partition the time in the day.
        """
        return self.schedule.ispartitioned()

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
