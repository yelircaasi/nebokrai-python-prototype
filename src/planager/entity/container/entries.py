import itertools
import operator
from typing import Any, Callable, Iterable, Iterator, Optional, Union

from ...util import PTime
from ..base.entry import Empty, Entry

EntriesInitType = Optional[Union["Entries", Iterable[Entry]]]


class Entries:
    """
    Container class for multiple instances of the Entry class.
    """

    def __init__(self, entries: EntriesInitType = None) -> None:
        self._entries: list[Entry] = list(entries or [])

    def copy(self) -> "Entries":
        return Entries((entry.copy() for entry in self._entries))

    def slice(self, __start: Optional[int], __stop: Optional[int]) -> "Entries":
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

    def remove(self, __entry: Entry) -> None:
        self._entries.remove(__entry)

    def sort(self, key: Callable[[Entry], Any] = lambda e: e.start) -> None:
        self._entries.sort(key=key)

    @property
    def start(self) -> PTime:
        return min(self._entries, key=lambda x: x.start).start if self._entries else PTime()

    @property
    def end(self) -> PTime:
        return max(self._entries, key=lambda x: x.end).end if self._entries else PTime(24)

    @property
    def total_duration(self) -> int:
        return sum(map(lambda e: e.duration, self._entries))

    @property
    def total_normaltime(self) -> int:
        return sum(map(lambda e: e.normaltime, self._entries))

    @property
    def last_fixed(self) -> Entry:
        """
        Return the last fixed (ismovable==False) Entry object.
        """
        fixed = [e for e in self if not e.ismovable]
        if not fixed:
            return Entry.first_entry()
        return fixed[-1]

    @property
    def fixed_to_end(self) -> "Entries":
        """
        Return from the last fixed (ismovable==False) Entry object to the last object.
        """
        fixed = [e for e in self if not e.ismovable]
        if not fixed:
            return self
        return Entries(self._entries[self.index(fixed[-1]) :])

    @property
    def blocks(self) -> set[str]:
        """
        Returns the set of blocks contained in the day.
        """
        block_set = set()
        for entry in self:
            block_set.update(entry.blocks)
        return block_set

    def available_for_block(self, block: str) -> int:
        return sum(
            map(
                lambda ent: ent.available,
                filter(lambda e: block in e.blocks, self._entries),
            )
        )

    @property
    def ispartitioned(self):
        """
        Check whether a list of entries partitions a day, i.e. are sequential and adjacent,
          begin at 00:00, and end at 24:00.
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

    def get_overlaps(self, entry: Entry) -> "Entries":
        """
        Return an instance of Entries containing all entries that overlap with the query entry.
        """
        return Entries(filter(entry.overlaps, self._entries))

    def overlaps_are_movable(self, entry: Entry) -> bool:
        """
        Check whether the entries that overlap with the query entry are all movable.
        """
        overlaps = self.get_overlaps(entry)
        if not overlaps:
            return True
        return all(map(lambda x: x.ismovable, overlaps))

    def get_flex_sandwiches(self) -> list[tuple[list[Entry], list[Entry], list[Entry]]]:
        """
        Returns two instances of Entries containing, respectively, the fixed (immovable) and
          flex (movable) entries contained in the current instance.
        """

        def get_indices(my_iter: Iterable[Any]) -> list[list[int]]:
            return [
                [e[0] for e in d[1]]
                for d in itertools.groupby(enumerate(my_iter), key=operator.itemgetter(1))
            ]

        full_list = self.with_gaps
        indices = get_indices(map(lambda e: e.ismovable, full_list))
        entries_list = [[full_list[i] for i in cluster] for cluster in indices]
        return list(zip(entries_list[::2], entries_list[1::2], entries_list[2::2]))

    def append_flex_or_fixed(
        self, flex: list[Entry], fixed: list[Entry]
    ) -> tuple[list[Entry], list[Entry]]:
        """
        Receives two lists, consisting of flex and fixed (movable and immovable) entries.
          Adds whichever entry comes next, subject to the constraint that if a flex entry is too
          long to fit before the next fixed entry, the fixed entry will be added.
        """
        self._entries = self.entries_sorted
        if not (flex or fixed):
            pass
        if not flex:
            self._entries.append(fixed.pop(0))
        elif not fixed:
            self._entries.append(flex.pop(0))
        else:
            hard_boundary = fixed[0].start if fixed else PTime(24)
            available = self.earliest_end.timeto(hard_boundary)
            next_entry = flex.pop(0) if available >= flex[0].mintime else fixed.pop(0)
            self._entries.append(next_entry)

        return flex, fixed

    @property
    def earliest_end(self) -> PTime:
        return PTime(0) if not self._entries else self.entries_sorted[-1].end

    @property
    def entries_sorted(self) -> list[Entry]:
        return sorted(self._entries, key=lambda e: e.start)

    def get_inds_of_relevant_blocks(self, entry: Entry) -> list[int]:
        """
        For the given query entry, return the indices of the entries with blocks matching the
          query entry's categories, i.e. the indices of the entries over which the query entry
          can be added.
        """
        categories: set = entry.categories

        def check(entry_: Entry) -> bool:
            return bool(categories.intersection(entry_.blocks))

        relevant = filter(check, self._entries)
        return list(map(self.index, relevant))

    def entry_list_fits(self) -> bool:
        """
        Check whether the sum of minimum durations of all entries fits in a single day.
        """
        return sum(map(lambda x: x.mintime, self._entries)) < (24 * 60)

    @property
    def with_gaps(self) -> list[Union[Entry, Empty]]:
        """
        Version of the instance with all empty space accounted for, via `Empty` objects.
        """
        gaps = self.gaps
        return sorted([*self._entries, *gaps], key=lambda e: e.start)

    @property
    def gaps(self) -> list[Empty]:
        """
        Return a list of empty entries corresponding to the times which are not yet occupied.
        """
        pairs = zip(self._entries[None:-1], self._entries[1:None])
        gaps = [Empty(start=a.end, end=b.start) for a, b in pairs]
        return [gap for gap in gaps if gap.duration > 0]

    @property
    def summary(self) -> str:
        return "Not yet implemented."

    def __bool__(self) -> bool:
        return bool(self._entries)

    def __iter__(self) -> Iterator[Entry]:
        return iter(self._entries)

    def __getitem__(self, __index: int) -> Entry:
        return self._entries[__index]

    def __len__(self) -> int:
        return len(self._entries)

    def __add__(self, __other: Union["Entries", Entry, list[Entry]]) -> "Entries":
        """
        An instance of Entries can be added (left or right) to another instance of Entries or to
          an instance of Entry.
        """
        if isinstance(__other, (Entries, list)):
            return Entries(self._entries + list(__other))
        if isinstance(__other, Entry):
            return Entries(self._entries + [__other])
        raise ValueError(f"Invalid type for method '__add__' of class 'Entries': {type(__other)}")

    def __str__(self) -> str:
        return "\n".join(map(str, self._entries))

    def __repr__(self) -> str:
        return self.__str__()
