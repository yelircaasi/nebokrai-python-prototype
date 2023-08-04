from typing import Callable, Iterable, Iterator, List, Optional, Tuple, Union

from planager.util.misc import round5
from planager.util.pdatetime.ptime import PTime

from ..base.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry


class Entries:
    def __init__(self, entries: Union["Entries", Iterable[Entry]] = []) -> None:
        self._entries: List[Entry] = list(entries)

    def copy(self) -> "Entries":
        return Entries((entry.copy() for entry in self._entries))

    def slice(  # -> KEEP
        self, __start: Optional[int], __stop: Optional[int]
    ) -> "Entries":  # type-idempotent; use indexing to get a single entry
        return Entries(entries=self._entries[__start:__stop])

    def insert(self, __index: int, __other: Entry) -> None:
        self._entries.insert(__index, __other)

    def append(self, __other: Entry) -> None:
        self._entries.append(__other)

    def extend(self, __other: Union["Entries", List[Entry]]) -> None:
        self._entries.extend(list(__other))

    def index(self, __entry: Entry) -> int:
        return self._entries.index(__entry)

    def pop(self, __index: int) -> Entry:
        entry = self._entries.pop(__index)
        return entry

    @property
    def ispartitioned(self):
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
        Verifies that the first and last entries in the schedule are the corresponding placeholder
          entries.
        """
        if not self._entries[0] == FIRST_ENTRY:
            self._entries.insert(0, FIRST_ENTRY)
        if not self._entries[-1] == LAST_ENTRY:
            self.append(LAST_ENTRY)

    def get_overlaps(self, entry: Entry) -> "Entries":
        return Entries(filter(lambda x: entry.overlaps(x), self._entries))

    def overlaps_are_movable(self, entry: Entry) -> bool:
        overlaps = self.get_overlaps(entry)
        return all(map(lambda x: x.ismovable, overlaps))

    def get_fixed_groups(self) -> List[Tuple["Entries", PTime, PTime]]:
        ret: List = []
        entries_fixed, _ = self.get_fixed_and_flex()
        fixed_indices = list(map(lambda entry: self.index(entry), entries_fixed))
        if not fixed_indices[0] == 0:
            fixed_indices.insert(0, 0)
        fixed_indices.append(len(self._entries))
        for a, b in zip(fixed_indices[:-1], fixed_indices[1:]):
            group: Entries = self.slice(a, b).copy()
            if group:
                start: PTime = group[0].start
                ret.append([group, start, PTime()])
        for i in range(len(ret) - 1):
            ret[i][2] = ret[i + 1][1]
        if ret:
            ret[0][1], ret[-1][2] = PTime(0), PTime(24)
        return [(a, b, c) for a, b, c in ret]

    def get_fixed_and_flex(self) -> Tuple["Entries", "Entries"]:
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

    def get_inds_of_relevant_blocks(
        self, entry: Entry
    ) -> List[int]:
        categories: set = entry.categories

        def check(entry_: Entry) -> bool:
            return bool(categories.intersection(entry_.blocks))

        relevant = filter(check, self._entries)
        return list(map(lambda x: self.index(x), relevant))

    def add_to_block_by_index(
        self, entry: Entry, block_ind: int
    ) -> None:  # REWRITE WITH .insert()
        new_entries = Entries.add_over_block(entry, self[block_ind])
        self._entries = list(
            self.slice(None, block_ind)
            + new_entries
            + self.slice(block_ind + 1, None)
        )

    def entry_list_fits(self) -> bool:
        return sum(map(lambda x: x.mintime, self._entries)) < (24 * 60)

    def get_gaps(self) -> List[Empty]:
        pairs = zip(self._entries[None: -1], self._entries[1: None])
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
        Adjusts each sequence of entries (type Entries) between two fixed points to fit consecutively between them.
        """
        ret: Entries = Entries()
        groups = self.get_fixed_groups()
        for group, start, end in groups:
            smoothed: Entries = self.smooth_entries(group, start, end, priority_weighter)
            ret.extend(smoothed)
        self._entries = list(ret)

    @staticmethod
    def add_over_block(
        entry: Entry, block: Entry
    ) -> "Entries":
        entry_dur = entry.duration
        entry.start = block.start
        entry.end = min(block.end, block.start + entry_dur)
        block.start = entry.end
        return Entries([entry, block])

    @staticmethod
    def smooth_entries(
        entries: "Entries",
        start: PTime,
        end: PTime,
        priority_weighter: Callable[[Union[int, float]], float],
    ) -> "Entries":

        total = start.timeto(end)
        underfilled = sum(map(lambda x: x.maxtime, entries)) < total
        
        if underfilled:
            entries.smooth_underfilled(start, end)
            return entries

        entries.adjust_weighted(start, end, priority_weighter)
        entries.ensure_fits(start, end)

                                                                                # TODO: add safeguard to respect mintime and maxtime
        return entries
    
    def smooth_underfilled(                                                     # move to Entries as method
        _entries: "Entries", _start: PTime, _end: PTime
    ) -> None:
        ret: Entries = Entries()
        time_tmp = _entries[0].start.copy()
        for entry in _entries:
            entry.start = time_tmp.copy()
            time_tmp += entry.duration
            entry.end = time_tmp.copy()
            ret.append(entry)
        empty = Empty(start=ret[-1].end, end=_end)
        ret.append(empty)

    def adjust_weighted(                                                        # move to Entries as method
        _entries: "Entries",
        _start: PTime,
        _end: PTime,
        priority_weighter: Callable[[Union[int, float]], float],
    ) -> None:
        ret: Entries = Entries()
        time_tmp = _entries[0].start.copy()
        total_duration = sum(map(Entry.duration, _entries))
        total = _start.timeto(_end)
        ratio = total / total_duration
        for entry in _entries:
            duration: int = entry.duration
            weight = priority_weighter(entry.priority)
            duration = max(
                min(round5(weight * ratio * duration), entry.maxtime), entry.mintime
            )
            entry.start = time_tmp.copy()
            time_tmp += duration
            entry.end = time_tmp.copy()
            ret.append(entry)

    def ensure_fits(                                                            # move to Entries as method
        self, _start: PTime, _end: PTime
    ) -> None:
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
        ind_to_adjust = self._entries.index(extremum(self._entries, key=lambda x: x.priority))
        self._entries[ind_to_adjust].end += diff
        for ind in range(ind_to_adjust + 1, len(self._entries)):
            self._entries[ind].start += diff
            self._entries[ind].end += diff

    def __iter__(self) -> Iterator[Entry]:
        return iter(self._entries)

    def __getitem__(self, __index: int) -> Entry:
        return self._entries[__index]

    def __len__(self) -> int:
        return len(self._entries)

    def __add__(self, __other: Union["Entries", Entry, List[Entry]]) -> "Entries":
        if isinstance(__other, Entries) or isinstance(__other, list):
            return Entries(self._entries + list(__other))
        elif isinstance(__other, Entry):
            return Entries(self._entries + [__other])
        else:
            raise ValueError(
                f"Invalid type for method '__add__' of class 'Entries': {type(__other)}"
            )
