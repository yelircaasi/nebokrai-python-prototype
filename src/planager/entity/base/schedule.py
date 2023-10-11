from typing import Callable, Iterable, Optional, Union

from ...config import Config
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
        config: Config,
        date: PDate,
        schedule: Iterable[Entry],
        weight_interval_min: Optional[float] = None,
        weight_interval_max: Optional[float] = None,
        prio_transform: Callable = lambda x: (x / 100) ** 1.5,
    ) -> None:
        self.config = config
        self.width: int = config.repr_width

        self.schedule = Entries(config, schedule)
        # meta / info
        self.date: PDate = date

        # algo
        self.weight_interval_min = (
            weight_interval_min or config.default_schedule_weight_interval_min
        )
        self.weight_interval_max = (
            weight_interval_max or config.default_schedule_weight_interval_max
        )
        self.prio_transform: Callable = prio_transform

        # record
        self.overflow: Entries = Entries(config)

    def copy(self):
        newschedule = Schedule(self.config, self.date, [])
        newschedule.__dict__.update(self.__dict__)
        return newschedule

    @classmethod
    def from_calendar(cls, calendar: Calendar, date: PDate) -> "Schedule":
        return cls(calendar.config, date, calendar[date].entries)

    def add_from_plan_and_excess(self, plan: Plan, excess: Entries) -> "Entries":
        """
        Adds all tasks planned for this day, converting tasks to entries.
        """
        # combine entries from plan with excess
        entries = Entries(self.config, map(lambda t: t.as_entry(), plan[self.date]))
        entries.extend(excess)

        # first, add to blocks where possible
        to_remove = []
        for entry in entries:
            for block in self.schedule:
                if entry.categories.intersection(block.blocks) and not entry in to_remove:
                    block.add_subentry(entry)
                    to_remove.append(entry)
        for entry in to_remove:
            entries.remove(entry)

            # rel_block_inds = self.schedule.get_inds_of_relevant_blocks(entry)
            # block_ind: Optional[int] = min(rel_block_inds) if rel_block_inds else None

            # if block_ind:
            #     self.add_to_block_by_index(entry, block_ind)

        # combine entries to add with the flex entries of the day
        flex_entries, fixed_clusters = self.get_flex_list_and_fixed_clusters()

        entries.extend(flex_entries)
        entries.sort(key=lambda e: (e.order, -e.priority))
        print("entries", ", ".join([f"{e.name} ({e.order}, -{e.priority})" for e in entries]))

        # order flex entries first by order, then by priority as a tiebreaker
        # flex_entries.sort(key=lambda e: (e.order, -e.priority))
        # print("flex_entries", ", ".join([f"{e.name} ({e.order}, -{e.priority})"
        # for e in flex_entries]))
        # print(f"flex_entries:\n{Entries(self.config, flex_entries)}")

        new_entries = Entries(self.config)
        next_entry = entries.pop(0)

        # heavy-lifting loop
        while fixed_clusters:
            new_entries.extend(fixed_clusters.pop(0))
            if fixed_clusters:
                hard_limit = fixed_clusters[0][0].start
                while entries and (
                    (new_entries.fixed_to_end.total_normaltime + next_entry.normaltime)
                    < new_entries.last_fixed.start.timeto(hard_limit)
                ):
                    # 1) attempt to add next entry to the next available gap between fixed blocks
                    next_entry = entries.pop(0)
                    # print(f"new_entries:\n{Entries(self.config, new_entries)}")
                    new_entries.append(next_entry)

        print(
            "new entries", ", ".join([f"{e.name} ({e.order}, -{e.priority})" for e in new_entries])
        )
        self.schedule = new_entries
        return entries

        # 2) if it does not fit (or is too tight), search for next entry that fits

        # go back to (1) and repeat the process

        # return excess entries (should be just entries that don't fit to to clumsy
        #   arrangement of fixed entries)

        # OLD:
        # for task in plan[self.date]:
        #     entry = task.as_entry()
        #     self.add(entry)

    def get_flex_list_and_fixed_clusters(self) -> tuple[list[Entry], list[list[Entry]]]:
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

    # def add(self, entry: Entry) -> None:
    #     """
    #     Top-level abstraction for adding an entry to the schedule.

    #     First checks for a block to add on top of, otherwise follows the default logic.
    #     """
    #     assert self.can_be_added(entry), (
    #         "-------------------------- CANNOT ADD\n\n" f"{entry}\n\nTO\n\n{self}\n\n"
    #     )

    #     rel_block_inds = self.schedule.get_inds_of_relevant_blocks(entry)
    #     block_ind: Optional[int] = min(rel_block_inds) if rel_block_inds else None
    #     # print("rel_block_inds", rel_block_inds)
    #     # print("block_ind", block_ind)
    #     # print(entry.categories)

    #     if block_ind:
    #         self.add_to_block_by_index(entry, block_ind)

    #     else:
    #         self.add_to_empty(entry)

    def add_to_block_by_index(self, entry: Entry, block_ind: int) -> None:
        """
        Add the input entry 'on top of' the entry corresponding to the given index.
        """

        block_entry = self.schedule[block_ind]
        assert id(block_entry) == id(self.schedule[block_ind])
        assert block_entry.blocks.intersection(entry.categories)

        block_entry.add_subentry(entry)

    # def add_to_empty(self, __entry: Entry) -> None:
    #     # self.schedule = self.allocate_in_time(
    #     #     self.schedule + [__entry], self.prio_weighting_function
    #     # )

    #     # flex_clusters = self.get_flex_clusters()
    #     self.schedule.get_fixed_and_flex()

    # @staticmethod
    # def allocate_in_time(
    #     entries: "Entries",
    #     prio_weighting_function: Callable,
    # ) -> "Entries":
    #     """
    #     Creates a schedule (i.e. entry list) from a list of entries. Steps:
    #       1) check whether the entries fit in a day
    #       2) get the compression factor, i.e. how much, on average,
    #          the entries need to be compacted in order to fit
    #       3) separate entries into fixed (immovable) and flex (movable)
    #       4) add the fixed entries to the schedule
    #       5) identify the gaps
    #       6) fill in the gaps with the flex items
    #       7) resize between fixed points to remove small empty patches (where possible)
    #       TODO: add alignend functionality (but first get it working without)
    #     """
    #     assert entries.entry_list_fits()
    #     compression_factor = round((24 * 60) / sum(
    #         map(lambda x: x.normaltime, entries)) - 0.01, 3
    #     )

    #     entries_fixed, entries_flex = entries.get_fixed_and_flex()
    #     schedule = Entries(
    #         entries.config,
    #         [Entry.first_entry(entries.config), *entries_fixed, Entry.last_entry(entries.config)],
    #     )

    #     schedule.fill_gaps(entries_flex, prio_weighting_function, compression_factor)
    #     schedule.smooth_between_fixed(prio_weighting_function)

    #     return schedule

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

    def is_valid(self) -> bool:
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
