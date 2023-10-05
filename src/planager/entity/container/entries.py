from typing import Any, Callable, Iterable, Iterator, Optional, Union

from planager.util.misc import round5
from planager.util.pdatetime.ptime import PTime

from ..base.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry



class Entries:
    def __init__(self, entries: Union["Entries", Iterable[Entry]] = []) -> None:
        self._entries: list[Entry] = list(entries)

    def copy(self) -> "Entries":
        return Entries((entry.copy() for entry in self._entries))

    def __bool__(self) -> bool:
        return bool(self._entries)

    def slice(self, __start: Optional[int], __stop: Optional[int]) -> "Entries":
        # type-idempotent; use indexing to get a single entry
        return Entries(entries=self._entries[__start:__stop])

    def insert(self, __index: int, __other: Entry) -> None:
        self._entries.insert(__index, __other)

    def append(self, __other: Entry) -> None:
        self._entries.append(__other)

    def extend(self, __other: Union["Entries", list[Entry]]) -> None:
        self._entries.extend(list(__other))

    def index(self, __entry: Entry) -> int:
        return self._entries.index(__entry)

    def pop(self, __index: int = -1) -> Entry:
        entry = self._entries.pop(__index)
        return entry

    @property
    def start(self) -> PTime:
        if not self._entries:
            return PTime()
        return min(self._entries, key=lambda x: x.start).start

    @property
    def end(self) -> PTime:
        if not self._entries:
            return PTime(24)
        return max(self._entries, key=lambda x: x.start).start

    @property
    def total_duration(self) -> int:
        return sum(map(lambda e: e.duration, self._entries))
    
    @property
    def blocks(self) -> set[str]:
        block_set = set()
        for entry in self:
            block_set.update(entry.blocks)
        return block_set
    
    def available_for_block(self, block: str) -> int:
        return sum(map(lambda ent: ent.available, filter(lambda e: block in e.blocks, self._entries)))

    @property
    def ispartitioned(self):
        """
        Check whether a list of entries partitions a day, i.e. are sequential and adjacent, begin at 00:00, and end
          at 24:00.
        """
        if len(self._entries) == 1:
            adjacency = True
        else:
            adjacency = all(
                map(
                    lambda x: x[0].end == x[1].start,
                    zip(self._entries[:-1], self._entries[1:]),
                )
            )
        return (
            adjacency
            and (self._entries[0].start == PTime())
            and (self._entries[-1].end == PTime(24))
        )

    def ensure_bookends(self) -> None:
        """
        Verifies that the first and last entries in the schedule are the corresponding placeholder entries.
        """
        if not self._entries[0] == FIRST_ENTRY:
            self._entries.insert(0, FIRST_ENTRY)
        if not self._entries[-1] == LAST_ENTRY:
            self.append(LAST_ENTRY)

    def get_overlaps(self, entry: Entry) -> "Entries":
        """
        Return an instance of Entries containing all entries that overlap with the query entry.
        """
        return Entries(filter(lambda x: entry.overlaps(x), self._entries))

    def overlaps_are_movable(self, entry: Entry) -> bool:
        """
        Check whether the entries that overlap with the query entry are all movable.
        """
        overlaps = self.get_overlaps(entry)
        return all(map(lambda x: x.ismovable, overlaps))

    def get_fixed_groups(self) -> list["Entries"]:
        """
        Return a list of Entries instances, each of which constitutes an immovable block.
        """
        ret: list = []
        entries_fixed, _ = self.get_fixed_and_flex()
        fixed_indices = list(map(lambda entry: self.index(entry), entries_fixed))
        if not fixed_indices[0] == 0:
            fixed_indices.insert(0, 0)
        fixed_indices.append(len(self._entries))
        for a, b in zip(fixed_indices[:-1], fixed_indices[1:]):
            group: Entries = self.slice(a, b).copy()
            if group:
                ret.append(group)
        return ret

    def get_fixed_and_flex(self) -> tuple["Entries", "Entries"]:
        """
        Returns two instances of Entries containing, respectively, the fixed (immovable) and flex (movable) entries
          contained in the current instance.
        """
        entries_fixed = Entries(
            sorted(
                list(filter(lambda x: not x.ismovable, self._entries)),
                key=lambda x: (x.order, x.priority),
            )
        )
        entries_flex = Entries(
            sorted(
                list(filter(lambda x: x.ismovable, self._entries)),
                key=lambda x: (x.order, x.priority),
            )
        )
        return entries_fixed, entries_flex

    def get_inds_of_relevant_blocks(self, entry: Entry) -> list[int]:
        """
        For the given query entry, return the indices of the entries with blocks matching the query entry's categories,
          i.e. the indices of the entries over which the query entry can be added.
        """
        categories: set = entry.categories

        def check(entry_: Entry) -> bool:
            return bool(categories.intersection(entry_.blocks))

        relevant = filter(check, self._entries)
        return list(map(lambda x: self.index(x), relevant))

    def add_to_block_by_index(
        self, entry: Entry, block_ind: int
    ) -> None:  # REWRITE WITH .insert() (?)
        """
        Add the input entry 'on top of' the entry corresponding to the given index.
        """
        new_entries = Entries.add_over_block(entry, self._entries[block_ind])
        self._entries = list(
            self.slice(None, block_ind) + new_entries + self.slice(block_ind + 1, None)
        )

    def entry_list_fits(self) -> bool:
        """
        Check whether the sum of minimum durations of all entries fits in a single day.
        """
        return sum(map(lambda x: x.mintime, self._entries)) < (24 * 60)

    def get_gaps(self) -> list[Empty]:
        """
        Return a list of empty entries corresponding to the times which are not yet occupied.
        """
        pairs = zip(self._entries[None:-1], self._entries[1:None])
        return list(
            filter(
                lambda x: x.duration > 0,
                (Empty(start=a.end, end=b.start) for a, b in pairs),
            )
        )

    def fill_gaps(
        self,
        flex_entries: "Entries",
        priority_weighter: Callable[[Union[int, float]], float],
        compression_factor: float = 1.0,
    ) -> None:
        """
        Takes a list of entries and adds them to the list of entries by filling in gaps according to priority and
          front-to-back (i.e. back-to-front for entries where entry.alignend is True).
        """
        while flex_entries:
            flex = flex_entries.pop(0)
            gaps = self.get_gaps()

            i = 0
            while i < len(gaps):
                gap: Empty = gaps[i]
                if gap.accommodates(flex, ratio=compression_factor):
                    flex.start = gap.start
                    duration = round5(compression_factor * flex.normaltime)
                    duration = round5(
                        max(
                            flex.mintime,
                            priority_weighter(flex.priority) * duration,
                        )
                    )
                    flex.end = flex.start + duration
                    self.insert(i + 1, flex)
                i += 1

    def smooth_between_fixed(
        self,
        priority_weighter: Callable[[Union[int, float]], float],
    ) -> None:
        """
        Adjusts each sequence of entries (type Entries) between two fixed points to fit consecutively between them,
          using priority weighting to determine time allocation.
        """
        result: Entries = Entries()
        fixed, flex = self.get_fixed_and_flex()

        before_after_dict = {
            flex_entry: (
                max(
                    filter(lambda x: x.end <= flex_entry.start, fixed),
                    key=lambda x: x.start,
                ),
                min(
                    filter(lambda x: x.start >= flex_entry.end, fixed),
                    key=lambda x: x.start,
                ),
            )
            for flex_entry in flex
        }  # could be simplified with more methods of Entries

        flex_groups: dict[tuple[Entry, Entry], Entries] = {
            before_after: Entries(
                sorted(
                    [k for k, v in before_after_dict.items() if v == before_after],
                    key=lambda x: x.start,
                )
            )
            for before_after in before_after_dict.values()
        }

        for (fixed_before, fixed_after), flex_group in flex_groups.items():
            result.append(fixed_before)
            result.extend(
                self.smooth_entries(
                    flex_group, fixed_before.end, fixed_after.start, priority_weighter
                )
            )
        result.append(fixed_after)
        self._entries = list(result)[1:-1]

    @staticmethod
    def add_over_block(entry: Entry, block: Entry) -> "Entries":
        """
        Adds an entry on top of another entry which acts as a block (i.e. which accepts other entries inside it),
          returning an instance of Entries containing
        """
        entry_dur = entry.duration
        entry.start = block.start
        entry.end = min(block.end, block.start + entry_dur)
        block.start = entry.end
        return Entries([entry, block])

    @staticmethod
    def smooth_entries(
        entries: "Entries",
        _start: PTime,
        _end: PTime,
        priority_weighter: Callable[[Union[int, float]], float],
    ) -> "Entries":
        """
        Takes an instance of Entries and ensures that it fits smoothly between _start and _end.
        """
        total = _start.timeto(_end)
        underfilled = sum(map(lambda x: x.maxtime, entries)) < total

        if underfilled:
            entries.smooth_underfilled(_start, _end)
            return entries

        entries.adjust_weighted(_start, _end, priority_weighter)
        entries.ensure_fits(_start, _end)

        # TODO: add safeguard to respect mintime and maxtime
        return entries

    def smooth_underfilled(self, _start: PTime, _end: PTime) -> None:
        """
        Allocate entries sequentially and without gaps, except at the end.
        """
        result: list[Entry] = []
        time_tmp = _start.copy()
        for entry in self._entries:
            entry.start = time_tmp.copy()
            time_tmp += entry.duration
            entry.end = time_tmp.copy()
            result.append(entry)
        empty = Empty(start=result[-1].end, end=_end)
        result.append(empty)
        self._entries = result

    def adjust_weighted(
        self,
        _start: PTime,
        _end: PTime,
        priority_weighter: Callable[[Union[int, float]], float],
    ) -> None:
        """
        Fit the current entries between _start and _end, using priority weighting.
        """
        result: list[Entry] = []
        time_tmp = self._entries[0].start.copy()
        total_duration = sum(map(Entry.duration, self._entries))
        total = _start.timeto(_end)
        ratio = total / total_duration
        for entry in self._entries:
            duration: int = entry.duration
            weight = priority_weighter(entry.priority)
            duration = max(
                min(round5(weight * ratio * duration), entry.maxtime), entry.mintime
            )
            entry.start = time_tmp.copy()
            time_tmp += duration
            entry.end = time_tmp.copy()
            result.append(entry)
        self._entries = result

    def ensure_fits(self, _start: PTime, _end: PTime) -> None:
        """
        Makes the current entries fit exactly between _start and _end.
        """
        total = _start.timeto(_end)
        total_duration = sum(map(Entry.duration, self._entries))
        ratio = total / total_duration
        lengths = list(
            map(
                lambda entry: max(
                    min(round5(ratio * entry.duration), entry.maxtime),
                    entry.mintime,
                ),
                self._entries,
            )
        )
        total_duration = sum(lengths)
        diff = total - total_duration
        extremum = min if (diff > 0) else max
        ind_to_adjust = self._entries.index(
            extremum(self._entries, key=lambda x: x.priority)
        )
        self._entries[ind_to_adjust].end += diff
        for ind in range(ind_to_adjust + 1, len(self._entries)):
            self._entries[ind].start += diff
            self._entries[ind].end += diff

    @staticmethod
    def allocate_in_time(
        entries: "Entries",
        prio_weighting_function: Callable,
    ) -> (
        "Entries"
    ):  # MOVE TO ENTRIES? NAH -> need to refactor this, make purely functional
        """
        Creates a schedule (i.e. entry list) from a list of entries. Steps:
          1) check whether the entries fit in a day
          2) get the compression factor, i.e. how much, on average, the entries need to be compacted in order to fit
          3) separate entries into fixed (immovable) and flex (movable)
          4) add the fixed entries to the schedule
          5) identify the gaps
          6) fill in the gaps with the flex items TODO
          7) resize between fixed points to remove small empty patches (where possible)
          TODO: add alignend functionality (but first get it working without)
        """
        # entries.extend(self.schedule)
        assert Entries.entry_list_fits(entries)
        compression_factor = round(
            (24 * 60) / sum(map(lambda x: x.normaltime, entries)) - 0.01, 3
        )

        entries_fixed, entries_flex = entries.get_fixed_and_flex()
        schedule = Entries([FIRST_ENTRY, *entries_fixed, LAST_ENTRY])

        schedule.fill_gaps(entries_flex, prio_weighting_function, compression_factor)
        schedule.smooth_between_fixed(prio_weighting_function)

        return schedule

    def __iter__(self) -> Iterator[Entry]:
        return iter(self._entries)

    def __getitem__(self, __index: int) -> Entry:
        return self._entries[__index]

    def __len__(self) -> int:
        return len(self._entries)

    def __add__(self, __other: Union["Entries", Entry, list[Entry]]) -> "Entries":
        """
        An instance of Entries can be added (left or right) to another instance of Entries or to an instance of Entry.
        """
        if isinstance(__other, Entries) or isinstance(__other, list):
            return Entries(self._entries + list(__other))
        elif isinstance(__other, Entry):
            return Entries(self._entries + [__other])
        else:
            raise ValueError(
                f"Invalid type for method '__add__' of class 'Entries': {type(__other)}"
            )

    def __str__(self) -> str:
        return "\n".join(map(str, self._entries))

    def __repr__(self) -> str:
        return self.__str__()
