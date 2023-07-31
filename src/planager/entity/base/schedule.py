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

    def make_default_day(self) -> Entries:
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
        # dict = read_norg_day(path)
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
        assert self.can_be_added(entry)  # TODO
        block_ind = min(self.get_inds_of_relevant_blocks(entry))
        if block_ind:
            self.add_to_block_by_index(entry, block_ind)
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

    def add_routines(self, routines: Routines) -> None: #  -> KEEP
        for routine in routines:
            if routine.valid_on(self.date):
                print("===========", routine.name)
                self.add(routine.as_entry(None))
                print(self)
            else:
                print(f"Not valid on {self.date}.")
        raise ValueError  # ---

    def add_from_plan(self, plan: Plan, tasks: Tasks) -> None: #  -> KEEP
        for task_id in plan[self.date]:
            self.add(tasks[task_id].as_entry(None))

    def add_adhoc(self, adhoc: AdHoc) -> None: #  -> KEEP
        for entry in adhoc[self.date]:
            self.add(entry)

    def ensure_bookends(self) -> None: # MOVE TO ENTRIES?
        """
        Verifies that the first and last entries in the schedule are the corresponding placeholder
          entries.
        """
        if not self.schedule[0] == FIRST_ENTRY:
            self.schedule.insert(0, FIRST_ENTRY)
        if not self.schedule[-1] == LAST_ENTRY:
            self.schedule.append(LAST_ENTRY)

    def ispartitioned(self): # MOVE TO ENTRIES?
        if len(self.schedule) == 1:
            adjacency = True
        else:
            adjacency = all(
                map(
                    lambda x: x[0].end == x[1].start,
                    zip(self.schedule[:-1], self.schedule[1:]),
                )
            )
        return (
            adjacency
            and (self.schedule[0].start == PTime())
            and (self.schedule[-1].end == PTime(24))
        )

    def get_inds_of_relevant_blocks(self, entry: Entry) -> List[int]:  # MOVE TO ENTRIES?
        categories: set = entry.categories

        def check(entry_: Entry) -> bool:
            return bool(categories.intersection(entry_.blocks))

        relevant = filter(check, self.schedule)
        return list(map(lambda x: self.schedule.index(x), relevant))

    def add_to_block_by_index(self, entry: Entry, block_ind: int) -> None: # MOVE TO ENTRIES?
        new_entries = self.add_over_block(entry, self.schedule[block_ind])
        self.schedule = (
            self.schedule.slice(None, block_ind)
            + new_entries
            + self.schedule.slice(block_ind + 1, None)
        )

    def can_be_added(self, entry: Entry) -> bool: # MOVE TO ENTRIES?
        assert self.overlaps_are_movable(entry)
        if not entry.ismovable:
            overlaps = self.get_overlaps(entry)
            if not all(map(lambda x: x.ismovable, overlaps)):
                return False
        return sum(map(lambda x: x.mintime, self.schedule)) + entry.mintime < (24 * 60)

    def get_overlaps(self, entry: Entry) -> Entries: # MOVE TO ENTRIES?
        return Entries(filter(lambda x: entry.overlaps(x), self.schedule))

    def overlaps_are_movable(self, entry: Entry) -> bool: # MOVE TO ENTRIES?
        overlaps = self.get_overlaps(entry)
        return all(map(lambda x: x.ismovable, overlaps))

    def allocate_in_time(self, entries: Entries) -> Entries: # MOVE TO ENTRIES?
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
        assert self.entry_list_fits(entries)
        compression_factor = round(
            (24 * 60) / sum(map(lambda x: x.normaltime, entries)) - 0.01, 3
        )

        entries_fixed, entries_flex = self.get_fixed_and_flex(entries)
        schedule = Entries([FIRST_ENTRY, *entries_fixed, LAST_ENTRY])

        schedule = self.fill_gaps(schedule, entries_flex, compression_factor)
        schedule = self.smooth_between_fixed(schedule)

        return schedule

    @staticmethod
    def add_over_block(entry: Entry, block: Entry) -> Entries: # MOVE TO ENTRIES? -> KEEP
        entry_dur = entry.duration()
        entry.start = block.start
        entry.end = min(block.end, block.start + entry_dur)
        block.start = entry.end
        return Entries([entry, block])

    @staticmethod
    def get_fixed_and_flex(entries: Entries) -> Tuple[Entries, Entries]: # MOVE TO ENTRIES?
        entries_fixed = Entries(
            sorted(
                list(filter(lambda x: not x.ismovable, entries)),
                key=lambda x: (x.order, x.priority),
            )
        )
        entries_flex = Entries(
            sorted(
                list(filter(lambda x: x.ismovable, entries)),
                key=lambda x: (x.order, x.priority),
            )
        )
        return entries_fixed, entries_flex

    @staticmethod
    def entry_list_fits(entries: Entries) -> bool: # MOVE TO ENTRIES?
        return sum(map(lambda x: x.mintime, entries)) < (24 * 60)

    @staticmethod
    def get_gaps(sched: Entries) -> List[Empty]:
        pairs = zip(sched.slice(None, -1), sched.slice(1, None))
        return [Empty(start=a.end, end=b.start) for a, b in pairs]

    def get_fixed_groups(self, sched: Entries) -> List[Tuple[Entries, PTime, PTime]]: # MOVE TO ENTRIES?
        ret: List = []
        entries_fixed, _ = self.get_fixed_and_flex(sched)
        fixed_indices = list(map(lambda entry: sched.index(entry), entries_fixed))
        if not fixed_indices[0] == 0:
            fixed_indices.insert(0, 0)
        fixed_indices.append(len(sched))
        for a, b in zip(fixed_indices[:-1], fixed_indices[1:]):
            group: Entries = sched.slice(a, b)
            if group:
                start: PTime = group[0].start
                ret.append([group, start, PTime()])
        for i in range(len(ret) - 1):
            ret[i][2] = ret[i + 1][1]
        if ret:
            ret[0][1], ret[-1][2] = PTime(0), PTime(24)
        return [(a, b, c) for a, b, c in ret]

    def fill_gaps(
        self,
        sched: Entries,
        flex_entries: Entries,
        compression_factor: float = 1.0,
    ) -> Entries: # MOVE TO ENTRIES?
        while flex_entries:
            flex = flex_entries.pop(0)
            gaps = self.get_gaps(sched)

            i = 0
            while i < len(gaps):
                gap = gaps[i]
                if gap.fits(flex, ratio=compression_factor):
                    flex.start = gap.start
                    duration = round5(compression_factor * flex.normaltime)
                    duration = round5(
                        max(
                            flex.mintime,
                            self.time_weight_from_prio(flex.priority) * duration,
                        )
                    )
                    flex.end = flex.start + duration
                    sched.insert(i + 1, flex)
                i += 1
        return sched

    def smooth_between_fixed(self, sched: Entries) -> Entries: # MOVE TO ENTRIES?
        ret: Entries = Entries()
        groups = self.get_fixed_groups(sched)
        for group, start, end in groups:
            smoothed: Entries = self.smooth_entries(group, start, end)
            ret.extend(smoothed)
        return ret

    def smooth_entries(self, entries: Entries, start: PTime, end: PTime) -> Entries: # MOVE TO ENTRIES?
        ret: Entries = Entries()
        total = start.timeto(end)

        underfilled = sum(map(lambda x: x.maxtime, entries)) < total
        time_tmp = entries[0].start.copy()

        if underfilled:
            time_tmp = entries[0].start.copy()
            for entry in entries:
                entry.start = time_tmp.copy()
                time_tmp += duration
                entry.end = time_tmp.copy()
                ret.append(entry)
            empty = Empty(start=ret[-1].end, end=end)
            ret.append(empty)
            return ret

        # weighted adjustment
        total_duration = sum(map(Entry.duration, entries))
        ratio = total / total_duration
        for entry in entries:
            duration: int = entry.duration()
            weight = self.time_weight_from_prio(entry.priority)
            duration = max(
                min(round5(weight * ratio * duration), entry.maxtime), entry.mintime
            )
            entry.start = time_tmp.copy()
            time_tmp += duration
            entry.end = time_tmp.copy()
            ret.append(entry)

        # make sure it fits exactly
        total_duration = sum(map(Entry.duration, ret))
        ratio = total / total_duration
        lengths = list(
            map(
                lambda x: max(min(round5(ratio * x), entry.maxtime), entry.mintime),
                map(Entry.duration, ret),
            )
        )
        total_duration = sum(lengths)
        diff = total - total_duration
        extremum = min if (diff > 0) else max
        ind_to_adjust = ret.index(extremum(ret, key=lambda x: x.priority))
        ret[ind_to_adjust].end += diff
        # TODO: add safeguard to respect mintime and mintime
        for ind in range(ind_to_adjust + 1, len(ret)):
            ret[ind].start += diff
            ret[ind].end += diff

        return ret

    def time_weight_from_prio(self, prio: Union[int, float]) -> float: # MOVE TO ENTRIES?
        interval = self.weight_interval_max - self.weight_interval_min
        return self.weight_interval_min + interval * self.prio_transform(prio)

    def is_valid(self) -> bool: # MAKE SIMILAR IN ENTRIES?
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
        topbeam = "┏" + (self.width - 2) * "━" + "┓"
        date = tabularize(self.date.pretty(), self.width)
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
  