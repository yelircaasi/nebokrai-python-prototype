from typing import List, Set
import pytest
from planager.entity.base.schedule import Schedule

from planager.entity.container.entries import Entries
from planager.entity.base.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from planager.util.pdatetime.ptime import PTime


class EntriesTest:
    entries1 = Entries()
    entries2 = Entries()
    entries3 = Entries()
    entries4 = Entries()

    schedule = Schedule()

    def test_init(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1
        assert self.entries2
        assert self.entries3
        assert self.entries4

    def test_copy(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        copy1 = self.entries1.copy()
        assert self.entries1 == copy1
        assert self.entries1.__dict__ == copy1.__dict__
        assert id(self.entries1) != id(copy1)

    def test_slice(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        exp1: List[Entry] = []
        exp2: List[Entry] = []
        exp3: List[Entry] = []
        exp4: List[Entry] = []

        assert self.entries1.slice(0, 2) == ...
        assert self.entries2.slice(2, 4) == ...
        assert self.entries3.slice(-3, None) == ...
        assert self.entries4.slice(None, 4) == ...

    def test_insert(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        new1.insert(0, Entry("", PTime()))
        new2.insert(2, Entry("", PTime()))
        new3.insert(-3, Entry("", PTime()))

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_append(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        new1.append(Entry("", PTime()))
        new2.append(Entry("", PTime()))
        new3.append(Entry("", PTime()))

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_extend_with_entries(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        new1.insert(0, Entry("", PTime(0, 0)))
        new2.insert(1, Entry("", PTime(0, 0)))
        new3.insert(-2, Entry("", PTime(0, 0)))

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_extend_with_list(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        new1.insert(0, Entry("", PTime(0, 0)))
        new2.insert(3, Entry("", PTime(0, 0)))
        new3.insert(-4, Entry("", PTime(0, 0)))

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_index(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.index(Entry("", PTime())) == 0
        assert self.entries2.index(Entry("", PTime())) == 3
        assert self.entries3.index(Entry("", PTime())) == 1

    def test_pop(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        exp_entries1 = Entries()
        exp_entries2 = Entries()
        exp_entries3 = Entries()

        exp_entry1 = Entry("", PTime())
        exp_entry2 = Entry("", PTime())
        exp_entry3 = Entry("", PTime())

        popped1 = new1.pop()
        popped2 = new2.pop(1)
        popped3 = new3.pop(-1)

        assert new1 == exp_entries1
        assert new2 == exp_entries2
        assert new3 == exp_entries3

        assert popped1 == exp_entry1
        assert popped2 == exp_entry2
        assert popped3 == exp_entry3

    # [ ]
    def test_start(self) -> None:
        assert self.entries1.start == PTime()
        assert self.entries2.start == PTime()
        assert self.entries3.start == PTime()
        assert self.entries4.start == PTime()

    # [ ]
    def test_end(self) -> None:
        assert self.entries1.start == PTime()
        assert self.entries2.start == PTime()
        assert self.entries3.start == PTime()
        assert self.entries4.start == PTime()
    
    # [ ]
    def test_ispartitioned(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.ispartitioned
        assert self.entries2.ispartitioned
        assert self.entries3.ispartitioned

        faulty1 = Entries()
        faulty2 = Entries()
        faulty3 = Entries()

        assert not faulty1.ispartitioned
        assert not faulty2.ispartitioned
        assert not faulty3.ispartitioned

    # [ ]
    def test_ensure_bookends(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        entries4 = Entries()
        entries5 = Entries()
        entries6 = Entries()

        assert entries4 != self.entries1
        assert entries5 != self.entries2
        assert entries6 != self.entries3

        new1.ensure_bookends()
        new2.ensure_bookends()
        new3.ensure_bookends()

        assert new1 == self.entries1
        assert new2 == self.entries2
        assert new3 == self.entries3

        entries4.ensure_bookends()
        entries5.ensure_bookends()
        entries6.ensure_bookends()

        assert entries4 == self.entries1
        assert entries5 == self.entries2
        assert entries6 == self.entries3

    # [ ]
    def test_get_overlaps(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.get_overlaps(Entry("", PTime())) == Entries(
            [Entry("", PTime()), Entry("", PTime())]
        )
        assert self.entries2.get_overlaps(Entry("", PTime())) == Entries(
            [Entry("", PTime()), Entry("", PTime())]
        )
        assert self.entries3.get_overlaps(Entry("", PTime())) == Entries(
            [Entry("", PTime()), Entry("", PTime())]
        )

    # [ ]
    def test_overlaps_are_movable(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.overlaps_are_movable(Entry("", PTime()))
        assert self.entries2.overlaps_are_movable(Entry("", PTime()))
        assert self.entries3.overlaps_are_movable(Entry("", PTime()))

        assert not self.entries1.overlaps_are_movable(Entry("", PTime()))
        assert not self.entries2.overlaps_are_movable(Entry("", PTime()))
        assert not self.entries3.overlaps_are_movable(Entry("", PTime()))

    # [ ]
    def test_get_fixed_groups(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.get_fixed_groups() == [
            (Entries(), PTime(), PTime()),
            (Entries(), PTime(), PTime()),
        ]
        assert self.entries2.get_fixed_groups() == [
            (Entries(), PTime(), PTime()),
            (Entries(), PTime(), PTime()),
        ]
        assert self.entries3.get_fixed_groups() == [
            (Entries(), PTime(), PTime()),
            (Entries(), PTime(), PTime()),
        ]

    # [ ]
    def test_get_fixed_and_flex(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.get_fixed_and_flex() == (Entries(), Entries())
        assert self.entries2.get_fixed_and_flex() == (Entries(), Entries())
        assert self.entries3.get_fixed_and_flex() == (Entries(), Entries())

    # [ ]
    def test_get_inds_of_relevant_blocks(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.get_inds_of_relevant_blocks(Entry("", PTime())) == []
        assert self.entries1.get_inds_of_relevant_blocks(Entry("", PTime())) == []
        assert self.entries1.get_inds_of_relevant_blocks(Entry("", PTime())) == []

        assert self.entries2.get_inds_of_relevant_blocks(Entry("", PTime())) == []
        assert self.entries2.get_inds_of_relevant_blocks(Entry("", PTime())) == []
        assert self.entries2.get_inds_of_relevant_blocks(Entry("", PTime())) == []

        assert self.entries3.get_inds_of_relevant_blocks(Entry("", PTime())) == []
        assert self.entries3.get_inds_of_relevant_blocks(Entry("", PTime())) == []
        assert self.entries3.get_inds_of_relevant_blocks(Entry("", PTime())) == []

    # [ ]
    def test_add_to_block_by_index(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1.copy()
        new2 = self.entries2.copy()
        new3 = self.entries3.copy()

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        new1.add_to_block_by_index(Entry("", PTime(0, 0)), 3)
        new2.add_to_block_by_index(Entry("", PTime(0, 0)), 1)
        new3.add_to_block_by_index(Entry("", PTime(0, 0)), -2)

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    # [ ]
    def test_entry_list_fits(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.entry_list_fits() == ...
        assert self.entries2.entry_list_fits() == ...
        assert self.entries3.entry_list_fits() == ...

    # [ ]
    def test_get_gaps(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.entries1.get_gaps() == [
            Empty(PTime(0, 0), PTime(0, 0)),
            Empty(PTime(0, 0), PTime(0, 0)),
            Empty(PTime(0, 0), PTime(0, 0)),
        ]
        assert self.entries2.get_gaps() == [
            Empty(PTime(0, 0), PTime(0, 0)),
            Empty(PTime(0, 0), PTime(0, 0)),
            Empty(PTime(0, 0), PTime(0, 0)),
        ]
        assert self.entries3.get_gaps() == [
            Empty(PTime(0, 0), PTime(0, 0)),
            Empty(PTime(0, 0), PTime(0, 0)),
            Empty(PTime(0, 0), PTime(0, 0)),
        ]

    # [ ]
    def test_fill_gaps(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        entries1 = self.entries1.copy()
        entries2 = self.entries2.copy()
        entries3 = self.entries3.copy()

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        entries1.fill_gaps(
            Entries([Entry("", PTime(0, 0))]), self.schedule.prio_weighting_function
        )
        entries2.fill_gaps(
            Entries([Entry("", PTime(0, 0))]), self.schedule.prio_weighting_function
        )
        entries3.fill_gaps(
            Entries([Entry("", PTime(0, 0))]), self.schedule.prio_weighting_function
        )

        assert entries1 == exp1
        assert entries2 == exp2
        assert entries3 == exp3

    # [ ]
    def test_smooth_between_fixed(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        entries1 = Entries()
        entries2 = Entries()
        entries3 = Entries()

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        entries1.smooth_between_fixed(self.schedule.prio_weighting_function)
        entries2.smooth_between_fixed(self.schedule.prio_weighting_function)
        entries3.smooth_between_fixed(self.schedule.prio_weighting_function)

        assert entries1 == exp1
        assert entries2 == exp2
        assert entries3 == exp3

    # [ ]
    def test_add_over_block(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert Entries.add_over_block(
            Entry("", PTime(0, 0)), Entry("", PTime(0, 0))
        ) == Entries(entries=[Entry("", PTime()), Entry("", PTime())])
        assert Entries.add_over_block(
            Entry("", PTime(0, 0)), Entry("", PTime(0, 0))
        ) == Entries(entries=[Entry("", PTime()), Entry("", PTime())])
        assert Entries.add_over_block(
            Entry("", PTime(0, 0)), Entry("", PTime(0, 0))
        ) == Entries(entries=[Entry("", PTime()), Entry("", PTime())])

    # [ ]
    def test_smooth_entries(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        entries1 = self.entries1.copy()
        entries2 = self.entries2.copy()
        entries3 = self.entries3.copy()

        assert (
            self.entries1.smooth_entries(
                entries1,
                PTime(0, 0),
                PTime(0, 0),
                self.schedule.prio_weighting_function,
            )
            == entries1
        )
        assert (
            Entries.smooth_entries(
                entries1,
                PTime(0, 0),
                PTime(0, 0),
                self.schedule.prio_weighting_function,
            )
            == entries2
        )
        assert (
            Entries.smooth_entries(
                entries1,
                PTime(0, 0),
                PTime(0, 0),
                self.schedule.prio_weighting_function,
            )
            == entries3
        )

    def test_iter(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        exp1: List[Entry] = [Entry("", PTime(0, 0))]
        exp2: Set[Entry] = {Entry("", PTime(0, 0))}
        exp3: List[Entry] = [Entry("", PTime(0, 0))]
        exp4: Set[Entry] = {Entry("", PTime(0, 0))}

        assert list(self.entries1)
        assert set(self.entries2)
        assert list(self.entries3)
        assert set(self.entries4)

    def test_getitem(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        exp1: List[Entry] = []
        exp2: List[Entry] = []
        exp3: List[Entry] = []
        exp4: List[Entry] = []

        assert self.entries1[0] == exp1
        assert self.entries2[2] == exp2
        assert self.entries3[-1] == exp3
        assert self.entries4[-2] == exp4

    def test_len(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert len(self.entries1) == ...
        assert len(self.entries2) == ...
        assert len(self.entries3) == ...
        assert len(self.entries4) == ...

    def test_add_entries(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1 + self.entries2
        new2 = self.entries3 + self.entries4
        new3 = self.entries2 + self.entries4

        exp1: List[Entry] = []
        exp2: List[Entry] = []
        exp3: List[Entry] = []

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3

    def test_add_entry(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        new1 = self.entries1 + Entry("", PTime())
        new2 = self.entries2 + Entry("", PTime())
        new3 = self.entries3 + Entry("", PTime())

        exp1 = Entries()
        exp2 = Entries()
        exp3 = Entries()

        assert new1 == exp1
        assert new2 == exp2
        assert new3 == exp3
