import pytest

from planager.entity.container.entries import Entries
from planager.entity.base.entry import Entry


class EntriesTest:
    entries1 = Entries()
    entries2 = Entries()
    entries3 = Entries()
    entries4 = Entries()

    def test_init(self) -> None:
        assert self.entries1
        assert self.entries2
        assert self.entries3
        assert self.entries4

    def test_iter(self) -> None:
        exp1 = []
        exp2 = {}
        exp3 = []
        exp4 = {}

        assert list(self.entries1)
        assert set(self.entries2)
        assert list(self.entries3)
        assert set(self.entries4)

    def test_slice(self) -> None:
        exp1 = []
        exp2 = []
        exp3 = []
        exp4 = []

        assert self.entries1.slice() == ...
        assert self.entries2.slice() == ...
        assert self.entries3.slice() == ...
        assert self.entries4.slice() == ...

    def test_getitem(self) -> None:
        exp1 = []
        exp2 = []
        exp3 = []
        exp4 = []

        assert self.entries1[...] == ...
        assert self.entries2[...] == ...
        assert self.entries3[...] == ...
        assert self.entries4[...] == ...

    def test_len(self) -> None:
        assert len(self.entries1) == ...
        assert len(self.entries2) == ...
        assert len(self.entries3) == ...
        assert len(self.entries4) == ...

    def test_add_entries(self) -> None:
        new1 = self.entries1 + self.entries2
        new2 = self.entries3 + self.entries4
        new3 = self.entries2 + self.entries4

        exp1 = []
        exp2 = []
        exp3 = []

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_add_entry(self) -> None:
        new1 = self.entries1 + Entry()
        new2 = self.entries2 + Entry()
        new3 = self.entries3 + Entry()

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_insert(self) -> None:
        new1 = Entries([e.copy() for e in self.entries1])
        new2 = Entries([e.copy() for e in self.entries2])
        new3 = Entries([e.copy() for e in self.entries3])

        new1.insert(Entry())
        new2.insert(Entry())
        new3.insert(Entry())

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_append(self) -> None:
        new1 = Entries([e.copy() for e in self.entries1])
        new2 = Entries([e.copy() for e in self.entries2])
        new3 = Entries([e.copy() for e in self.entries3])

        new1.append(Entry())
        new2.append(Entry())
        new3.append(Entry())

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_extend_with_entries(self) -> None:
        new1 = Entries([e.copy() for e in self.entries1])
        new2 = Entries([e.copy() for e in self.entries2])
        new3 = Entries([e.copy() for e in self.entries3])

        new1.insert(Entries())
        new2.insert(Entries())
        new3.insert(Entries())

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_extend_with_list(self) -> None:
        new1 = Entries([e.copy() for e in self.entries1])
        new2 = Entries([e.copy() for e in self.entries2])
        new3 = Entries([e.copy() for e in self.entries3])

        new1.insert([])
        new2.insert([])
        new3.insert([])

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_index(self) -> None:
        assert self.entries1.index(Entry()) == 0
        assert self.entries2.index(Entry()) == 3
        assert self.entries3.index(Entry()) == 1

    def test_pop(self) -> None:
        new1 = Entries([e.copy() for e in self.entries1])
        new2 = Entries([e.copy() for e in self.entries2])
        new3 = Entries([e.copy() for e in self.entries3])

        exp_entries1 = Entries()
        exp_entries2 = Entries()
        exp_entries3 = Entries()

        exp_entry1 = Entry()
        exp_entry2 = Entry()
        exp_entry3 = Entry()

        popped1 = new1.pop()
        popped2 = new2.pop(1)
        popped3 = new3.pop(-1)

        assert new1 == exp_entries1
        assert new2 == exp_entries2
        assert new3 == exp_entries3

        assert popped1 == exp_entry1
        assert popped2 == exp_entry2
        assert popped3 == exp_entry3
