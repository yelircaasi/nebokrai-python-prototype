from typing import Iterable, Iterator, List, Optional, Union

from ..base.entry import Entry


class Entries:
    def __init__(self, entries: Union["Entries", Iterable[Entry]] = []) -> None:
        self._entries: List[Entry] = list(entries)

    def slice( # -> KEEP
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
