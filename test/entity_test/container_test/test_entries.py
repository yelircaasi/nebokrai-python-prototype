from typing import Set
import pytest
from planager.entity.base.schedule import Schedule

from planager.entity.container.entries import Entries
from planager.entity.base.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from planager.util.pdatetime.ptime import PTime


class EntriesTest:
    # entries1 = Entries(
    #     [
    #         Entry("1a", PTime(7), end=PTime()),
    #         Entry("1b", PTime(8), end=PTime()),
    #         Entry("1c", PTime(9), end=PTime()),
    #     ]
    # )
    # entries2 = Entries(
    #     [
    #         Entry("2a", PTime(14)),
    #     ]
    # )
    # entries3 = Entries(
    #     [
    #         Entry("3a", PTime(10)),
    #         Entry("3b", PTime(10, 30)),
    #         Entry("3c", PTime(14)),
    #         Entry("3d", PTime(15)),
    #         Entry("3e", PTime(17)),
    #         Entry("3f", PTime(20)),
    #     ]
    # )
    # entries4 = Entries()

    # schedule = Schedule()

    # def test_init(self) -> None:
    #     """

    #     """
    #     entries1 = Entries(
    #         [
    #             Entry("1a", PTime(7), end=PTime()),
    #             Entry("1b", PTime(8), end=PTime()),
    #             Entry("1c", PTime(9), end=PTime()),
    #         ]
    #     )
    #     assert entries1.start == PTime()
    #     assert entries1.end == PTime()

    # def test_copy(self) -> None:
    #     """

    #     """
    #     entries = Entries(
    #         [
    #             Entry("1a", PTime(7), end=PTime()),
    #             Entry("1b", PTime(8), end=PTime()),
    #             Entry("1c", PTime(9), end=PTime()),
    #         ]
    #     )
    #     copy = entries.copy()
    #     assert self.entries == copy
    #     assert entries.__dict__ == copy.__dict__
    #     assert id(entries) != id(copy)

    # def test_slice(self) -> None:
    #     """

    #     """
    #     entries1 = Entries()
    #     entries2 = Entries()
    #     entries3 = Entries()
    #     entries4 = Entries()
    #     exp1: list[Entry] = []
    #     exp2: list[Entry] = []
    #     exp3: list[Entry] = []
    #     exp4: list[Entry] = []

    #     assert self.entries1.slice(0, 2) == ...
    #     assert self.entries3.slice(2, 4) == ...
    #     assert self.entries3.slice(-3, None) == ...
    #     assert self.entries4.slice(None, 4) == ...
    #     assert self.entries2.slice(None, 4) == ...

    # def test_insert(self) -> None:
    #     """

    #     """
    #     new1a = self.entries1.copy()
    #     new1b = self.entries1.copy()
    #     new3 = self.entries3.copy()

    #     new1a.insert(0, Entry("", PTime()))
    #     new1b.insert(2, Entry("", PTime()))
    #     new3.insert(-3, Entry("", PTime()))

    #     exp1a = Entries()
    #     exp1b = Entries()
    #     exp3 = Entries()

    #     assert new1a == exp1a
    #     assert new1b == exp1b
    #     assert new3 == exp3

    # def test_append(self) -> None:
    #     """

    #     """
    #     new1 = self.entries1.copy()
    #     new2 = self.entries2.copy()
    #     new3 = self.entries3.copy()

    #     new1.append(Entry("", PTime()))
    #     new2.append(Entry("", PTime()))
    #     new3.append(Entry("", PTime()))

    #     exp1 = Entries()
    #     exp2 = Entries()
    #     exp3 = Entries()

    #     assert new1 == exp1
    #     assert new2 == exp2
    #     assert new3 == exp3

    # def test_extend_with_entries(self) -> None:
    #     """

    #     """
    #     new1 = self.entries1.copy()
    #     new2 = self.entries2.copy()
    #     new3 = self.entries3.copy()

    #     new1.insert(0, Entry("", PTime(0, 0)))
    #     new2.insert(1, Entry("", PTime(0, 0)))
    #     new3.insert(-2, Entry("", PTime(0, 0)))

    #     exp1 = Entries()
    #     exp2 = Entries()
    #     exp3 = Entries()

    #     assert new1 == exp1
    #     assert new2 == exp2
    #     assert new3 == exp3

    # def test_extend_with_list(self) -> None:
    #     """

    #     """
    #     new1 = self.entries1.copy()
    #     new2 = self.entries2.copy()
    #     new3 = self.entries3.copy()

    #     new1.insert(0, Entry("", PTime(0, 0)))
    #     new2.insert(3, Entry("", PTime(0, 0)))
    #     new3.insert(-4, Entry("", PTime(0, 0)))

    #     exp1 = Entries()
    #     exp2 = Entries()
    #     exp3 = Entries()

    #     assert new1 == exp1
    #     assert new2 == exp2
    #     assert new3 == exp3

    # def test_index(self) -> None:
    #     """

    #     """
    #     assert self.entries1.index(Entry("", PTime())) == 0
    #     assert self.entries2.index(Entry("", PTime())) == 3
    #     assert self.entries3.index(Entry("", PTime())) == 1

    # def test_pop(self) -> None:
    #     """

    #     """
    #     new1 = self.entries1.copy()
    #     new2 = self.entries2.copy()
    #     new3 = self.entries3.copy()

    #     exp_entries1 = Entries()
    #     exp_entries2 = Entries()
    #     exp_entries3 = Entries()

    #     exp_entry1 = Entry("", PTime())
    #     exp_entry2 = Entry("", PTime())
    #     exp_entry3 = Entry("", PTime())

    #     popped1 = new1.pop()
    #     popped2 = new2.pop(1)
    #     popped3 = new3.pop(-1)

    #     assert new1 == exp_entries1
    #     assert new2 == exp_entries2
    #     assert new3 == exp_entries3

    #     assert popped1 == exp_entry1
    #     assert popped2 == exp_entry2
    #     assert popped3 == exp_entry3

    # # [ ]
    # def test_start(self) -> None:
    #     assert self.entries1.start == PTime()
    #     assert self.entries2.start == PTime()
    #     assert self.entries3.start == PTime()
    #     assert self.entries4.start == PTime()

    # # [ ]
    # def test_end(self) -> None:
    #     assert self.entries1.start == PTime()
    #     assert self.entries2.start == PTime()
    #     assert self.entries3.start == PTime()
    #     assert self.entries4.start == PTime()

    # [ ]
    def test_ispartitioned(self) -> None:
        """
        Cases to test:
        1) partitioned
        2) unfilled gaps between
        3) overlaps between entries
        4) gaps and overlaps
        """
        empty = Entries()
        singleton = Entries()
        partitioned = Entries()
        gaps = Entries()
        overlaps = Entries()
        gaps_overlaps = Entries()

        assert empty.ispartitioned
        assert singleton.ispartitioned
        assert partitioned.ispartitioned
        assert not gaps.ispartitioned
        assert not overlaps.ispartitioned
        assert not gaps_overlaps.ispartitioned

    # [ ]
    def test_ensure_bookends(self) -> None:
        """
        Cases to test:
        1) no bookends already
        2) both bookends already
        3) only start bookend already
        4) only end bookend already
        """
        no_bookends = Entries()
        both = Entries()
        start_only = Entries()
        end_only = Entries()

        no_bookends_exp = Entries()
        both_exp = Entries()
        start_exp = Entries()
        end_exp = Entries()

        no_bookends.ensure_bookends()
        both.ensure_bookends()
        start_only.ensure_bookends()
        end_only.ensure_bookends()

        assert no_bookends == no_bookends_exp
        assert both == both_exp
        assert start_only == start_exp
        assert end_only == end_exp

        no_bookends.ensure_bookends()
        both.ensure_bookends()
        start_only.ensure_bookends()
        end_only.ensure_bookends()

        assert no_bookends == no_bookends_exp
        assert both == both_exp
        assert start_only == start_exp
        assert end_only == end_exp

    # [ ]
    def test_get_overlaps(self) -> None:
        """
        Cases to test:
        1) overlaps none
        2) overlaps tail end of one
        3) overlaps start of one
        4) overlaps on both sides
        5) overlaps 3
        6) overlaps 4
        7) coterminous
        8) adjacent to start but not overlapping
        9) adjacent to end but not overlapping
        """

        entries = Entries()

        no_overlaps = Entry("", start=PTime(), end=PTime())
        overlaps_end = Entry("", start=PTime(), end=PTime())
        overlaps_start = Entry("", start=PTime(), end=PTime())
        overlaps_both_ends = Entry("", start=PTime(), end=PTime())
        overlaps_3 = Entry("", start=PTime(), end=PTime())
        overlaps_4 = Entry("", start=PTime(), end=PTime())
        coterminous = Entry("", start=PTime(), end=PTime())
        adjacent_start = Entry("", start=PTime(), end=PTime())
        adjacent_end = Entry("", start=PTime(), end=PTime())

        exp_no_overlaps = Entries()
        exp_overlaps_end = Entries()
        exp_overlaps_start = Entries()
        exp_overlaps_both_ends = Entries()
        exp_overlaps_3 = Entries()
        exp_overlaps_4 = Entries()
        exp_coterminous = Entries()
        exp_adjacent_start = Entries()
        exp_adjacent_end = Entries()

        assert entries.get_overlaps(no_overlaps) == exp_no_overlaps
        assert entries.get_overlaps(overlaps_end) == exp_overlaps_end
        assert entries.get_overlaps(overlaps_start) == exp_overlaps_start
        assert entries.get_overlaps(overlaps_both_ends) == exp_overlaps_both_ends
        assert entries.get_overlaps(overlaps_3) == exp_overlaps_3
        assert entries.get_overlaps(overlaps_4) == exp_overlaps_4
        assert entries.get_overlaps(coterminous) == exp_coterminous
        assert entries.get_overlaps(adjacent_start) == exp_adjacent_start
        assert entries.get_overlaps(adjacent_end) == exp_adjacent_end

    # [ ]
    def test_overlaps_are_movable(self) -> None:
        """ """
        entries = Entries()

        entry_movable = Entry("", PTime())
        entry_immovable = Entry("", PTime())

        assert entries.overlaps_are_movable(entry_movable)
        assert entries.overlaps_are_movable(entry_immovable)

    # [ ]
    def test_get_fixed_groups(self) -> None:
        """
        Cases to test:
        1) no fixed
        2) fixed groups of size 1
        3) fixed groups of size 2 and 3
        """
        no_fixed = Entries()
        fixed_1 = Entries()
        fixed_2 = Entries()
        fixed_3 = Entries()

        assert no_fixed.get_fixed_groups() == []
        assert fixed_1.get_fixed_groups() == [
            Entries(),
            Entries(),
        ]
        assert fixed_2.get_fixed_groups() == [
            Entries(),
            Entries(),
        ]
        assert fixed_3.get_fixed_groups() == [
            Entries(),
            Entries(),
        ]

    # [ ]
    def test_get_fixed_and_flex(self) -> None:
        """
        Cases to test:
        1) all fixed
        2) all flex
        3) mixed
        4) empty
        """
        all_fixed = Entries()
        all_flex = Entries()
        mixed = Entries()
        empty = Entries()

        exp_all_fixed = (Entries(), Entries())
        exp_all_flex = (Entries(), Entries())
        exp_mixed = (Entries(), Entries())
        exp_empty = (Entries(), Entries())

        assert all_fixed.get_fixed_and_flex() == exp_all_fixed
        assert all_flex.get_fixed_and_flex() == exp_all_flex
        assert mixed.get_fixed_and_flex() == exp_mixed
        assert empty.get_fixed_and_flex() == exp_empty

    # [ ]
    def test_get_inds_of_relevant_blocks(self) -> None:
        """
        Cases to test:
        1) no relevant
        2) 1 relevant, 1 category-block match
        2) 1 relevant, 2 category-block matches
        3) 2 or more relevant, 1 category-block match
        3) 2 or more relevant, 2 or more category-block matches
        """
        entries = Entries()

        no_relevant = Entry("", PTime())
        relevant_1 = Entry("", PTime())
        relevant_2 = Entry("", PTime())
        two_relevant_1 = Entry("", PTime())
        two_relevant_2 = Entry("", PTime())

        exp_no_relevant: list[int] = []
        exp_relevant_1: list[int] = []
        exp_relevant_2: list[int] = []
        exp_two_relevant_1: list[int] = []
        exp_two_relevant_2: list[int] = []

        assert entries.get_inds_of_relevant_blocks(no_relevant) == exp_no_relevant
        assert entries.get_inds_of_relevant_blocks(relevant_1) == exp_relevant_1
        assert entries.get_inds_of_relevant_blocks(relevant_2) == exp_relevant_2
        assert entries.get_inds_of_relevant_blocks(two_relevant_1) == exp_two_relevant_1
        assert entries.get_inds_of_relevant_blocks(two_relevant_2) == exp_two_relevant_2

    # [ ]
    def test_add_to_block_by_index(self) -> None:
        """
        Cases to test:
        1) block is filled
        2) new entry smaller than block
        3) new entry snaps to block
        4) new entry compressed to fit in block
        5) new entry does not fit
        """
        entries = Entries()

        entries_filled = entries.copy()
        entries_smaller = entries.copy()
        entries_snaps = entries.copy()
        entries_compressed = entries.copy()
        entries_no_fit = entries.copy()

        filled = Entry("", PTime())
        smaller = Entry("", PTime())
        snaps = Entry("", PTime())
        compressed = Entry("", PTime())
        no_fit = Entry("", PTime())

        exp_filled = Entries()
        exp_smaller = Entries()
        exp_snaps = Entries()
        exp_compressed = Entries()
        exp_no_fit = Entries()

        entries.copy().add_to_block_by_index(filled, 99)
        entries.copy().add_to_block_by_index(smaller, 99)
        entries.copy().add_to_block_by_index(snaps, 99)
        entries.copy().add_to_block_by_index(compressed, 99)
        entries.copy().add_to_block_by_index(no_fit, 99)

        assert entries_filled == exp_filled
        assert entries_smaller == exp_smaller
        assert entries_snaps == exp_snaps
        assert entries_compressed == exp_compressed
        assert entries_no_fit == exp_no_fit

    # [ ]
    def test_entry_list_fits(self) -> None:
        """
        Cases to test:
        1) fits exactly
        2) fits with room to spare
        3) doesn't fit
        4) trivial fit: no entries
        5) single entry fit
        """
        exact = Entries()
        spare = Entries()
        no_fit = Entries()
        trivial = Entries()
        single = Entries()

        assert exact.entry_list_fits()
        assert spare.entry_list_fits()
        assert not no_fit.entry_list_fits()
        assert trivial.entry_list_fits()
        assert single.entry_list_fits()

    # [ ]
    def test_get_gaps(self) -> None:
        """
        Cases to test:
        1) no gaps
        2) all gaps (trivial)
        3) 1 gaps
        4) 2 gaps
        5) 3 gaps
        """
        dense = Entries()
        sparse = Entries()
        one = Entries()
        two = Entries()
        three = Entries()

        exp_dense = Entries()
        exp_sparse = Entries()
        exp_one = Entries()
        exp_two = Entries()
        exp_three = Entries()

        assert dense.get_gaps() == exp_dense
        assert sparse.get_gaps() == exp_sparse
        assert one.get_gaps() == exp_one
        assert two.get_gaps() == exp_two
        assert three.get_gaps() == exp_three

    # [ ]
    def test_fill_gaps(self) -> None:
        """
        Cases to test:
        1) too many entries (error)
        2) entries fit perfectly
        3) entries fit with snapping behavior
        4) entries fit with compression
        5) entries fit with both stretching (snapping) and compression
        6) some shuffling required (wrt priority) to achieve fit
        7) some shuffling required (wrt order) to achieve fit
        8) some shuffling required (wrt priority and order) to achieve fit
        """
        incumb_too_many = Entries()
        incumb_perfect = incumb_too_many.copy()
        incumb_snapping = incumb_too_many.copy()
        incumb_compression = incumb_too_many.copy()
        incumb_stretch_compress = incumb_too_many.copy()
        incumb_shuffle_prio = incumb_too_many.copy()
        incumb_shuffle_order = incumb_too_many.copy()
        incumb_shuffle_prio_order = incumb_too_many.copy()

        exp_too_many = Entries()
        exp_perfect = Entries()
        exp_snapping = Entries()
        exp_compression = Entries()
        exp_stretch_compress = Entries()
        exp_shuffle_prio = Entries()
        exp_shuffle_order = Entries()
        exp_shuffle_prio_order = Entries()

        new_too_many = Entries()
        new_perfect = Entries()
        new_snapping = Entries()
        new_compression = Entries()
        new_stretch_compress = Entries()
        new_shuffle_prio = Entries()
        new_shuffle_order = Entries()
        new_shuffle_prio_order = Entries()

        prio_weighter = Schedule().prio_weighting_function

        incumb_too_many.fill_gaps(new_too_many, prio_weighter)
        incumb_perfect.fill_gaps(new_perfect, prio_weighter)
        incumb_snapping.fill_gaps(new_snapping, prio_weighter)
        incumb_compression.fill_gaps(new_compression, prio_weighter)
        incumb_stretch_compress.fill_gaps(new_stretch_compress, prio_weighter)
        incumb_shuffle_prio.fill_gaps(new_shuffle_prio, prio_weighter)
        incumb_shuffle_order.fill_gaps(new_shuffle_order, prio_weighter)
        incumb_shuffle_prio_order.fill_gaps(new_shuffle_prio_order, prio_weighter)

        assert incumb_too_many == exp_too_many
        assert incumb_perfect == exp_perfect
        assert incumb_snapping == exp_snapping
        assert incumb_compression == exp_compression
        assert incumb_stretch_compress == exp_stretch_compress
        assert incumb_shuffle_prio == exp_shuffle_prio
        assert incumb_shuffle_order == exp_shuffle_order
        assert incumb_shuffle_prio_order == exp_shuffle_prio_order

    # [ ]
    def test_smooth_between_fixed(self) -> None:
        """
        Cases to test:
        1) doesn't fit
        2) underfilled
        3) compression required
        4) snapping required
        5) priority weighting required
        """
        entries_no_fit = Entries()
        entries_underfilled = Entries()
        entries_compression = Entries()
        entries_snapping = Entries()
        entries_weighting = Entries()

        prio_weighter = Schedule().prio_weighting_function

        exp_no_fit = Entries()
        exp_underfilled = Entries()
        exp_compression = Entries()
        exp_snapping = Entries()
        exp_weighting = Entries()

        entries_no_fit.smooth_between_fixed(prio_weighter)
        entries_underfilled.smooth_between_fixed(prio_weighter)
        entries_compression.smooth_between_fixed(prio_weighter)
        entries_snapping.smooth_between_fixed(prio_weighter)
        entries_weighting.smooth_between_fixed(prio_weighter)

        assert entries_no_fit == exp_no_fit
        assert entries_underfilled == exp_underfilled
        assert entries_compression == exp_compression
        assert entries_snapping == exp_snapping
        assert entries_weighting == exp_weighting

    # [ ]
    def test_add_over_block(self) -> None:
        """
        Cases to test:
        1) block is filled
        2) new entry smaller than block
        3) new entry snaps to block
        4) new entry compressed to fit in block
        5) new entry does not fit
        """
        block = Entry("", PTime())

        filled = Entry("", PTime())
        smaller = Entry("", PTime())
        snaps = Entry("", PTime())
        compressed = Entry("", PTime())
        no_fit = Entry("", PTime())

        exp_filled = Entries()
        exp_smaller = Entries()
        exp_snaps = Entries()
        exp_compressed = Entries()
        exp_no_fit = Entries()

        assert Entries.add_over_block(filled, block) == exp_filled
        assert Entries.add_over_block(smaller, block) == exp_smaller
        assert Entries.add_over_block(snaps, block) == exp_snaps
        assert Entries.add_over_block(compressed, block) == exp_compressed
        assert Entries.add_over_block(no_fit, block) == exp_no_fit

    # [ ]
    def test_smooth_entries(self) -> None:
        """
        Cases to test:
        1) underfilled
        2) compression required
        3) compression required and priority reweighting required
        4) snapping required
        5) impossible
        """

    # [ ]
    def test_allocate_in_time(self) -> None:
        """
        Cases:
        1) underfull
        2) perfect fit
        3) compression required, all flex
        4) overfull with fixed, so gap-filling required
        5) loose fit with snapping
        6) impossible
        """
        pwf = Schedule.prio_weighting_function

        entries_underfull = Entries()
        entries_perfect = Entries()
        entries_compression = Entries()
        entries_gapfilling = Entries()
        entries_snapping = Entries()
        entries_impossible = Entries()

        exp_underfull = Entries()
        exp_perfect = Entries()
        exp_compression = Entries()
        exp_gapfilling = Entries()
        exp_snapping = Entries()
        exp_impossible = Entries()

        assert Entries.allocate_in_time(entries_underfull, pwf) == exp_underfull
        assert Entries.allocate_in_time(entries_perfect, pwf) == exp_perfect
        assert Entries.allocate_in_time(entries_compression, pwf) == exp_compression
        assert Entries.allocate_in_time(entries_gapfilling, pwf) == exp_gapfilling
        assert Entries.allocate_in_time(entries_snapping, pwf) == exp_snapping
        assert Entries.allocate_in_time(entries_impossible, pwf) == exp_impossible

    # # [ ]
    # def test_iter(self) -> None:
    #     """
    #     Cases to test:
    #     1) empty
    #     2) nonempty
    #     3)
    #     """
    #     exp1: list[Entry] = [Entry("", PTime(0, 0))]
    #     exp2: set[Entry] = {Entry("", PTime(0, 0))}
    #     exp3: list[Entry] = [Entry("", PTime(0, 0))]
    #     exp4: set[Entry] = {Entry("", PTime(0, 0))}

    #     assert list(self.entries1)
    #     assert set(self.entries2)
    #     assert list(self.entries3)
    #     assert set(self.entries4)

    # # [ ]
    # def test_getitem(self) -> None:
    #     """
    #     Cases to test:
    #     1) possible
    #     2) impossible
    #     """
    #     exp1: list[Entry] = []
    #     exp2: list[Entry] = []
    #     exp3: list[Entry] = []
    #     exp4: list[Entry] = []

    #     assert self.entries1[0] == exp1
    #     assert self.entries2[2] == exp2
    #     assert self.entries3[-1] == exp3
    #     assert self.entries4[-2] == exp4

    # # [ ]
    # def test_len(self) -> None:
    #     """
    #     Cases to test:
    #     1) empty
    #     2) nonempty
    #     """
    #     assert len(self.entries1) == ...
    #     assert len(self.entries2) == ...
    #     assert len(self.entries3) == ...
    #     assert len(self.entries4) == ...

    # # [ ]
    # def test_add_entries(self) -> None:
    #     """
    #     Cases to test:
    #     1) empty, from left
    #     2) nonempty, from left
    #     3) empty, from right
    #     4) nonempty, from right
    #     """
    #     new1 = self.entries1 + self.entries2
    #     new2 = self.entries3 + self.entries4
    #     new3 = self.entries2 + self.entries4

    #     exp1: list[Entry] = []
    #     exp2: list[Entry] = []
    #     exp3: list[Entry] = []

    #     assert new1 == exp1
    #     assert new2 == exp2
    #     assert new3 == exp3

    # def test_add_entry(self) -> None:
    #     """
    #     Cases to test:
    #     1) empty, from left
    #     2) nonempty, from left
    #     3) empty, from right
    #     4) nonempty, from right
    #     """
    #     new1 = self.entries1 + Entry("", PTime())
    #     new2 = self.entries2 + Entry("", PTime())
    #     new3 = self.entries3 + Entry("", PTime())

    #     exp1 = Entries()
    #     exp2 = Entries()
    #     exp3 = Entries()

    #     assert new1 == exp1
    #     assert new2 == exp2
    #     assert new3 == exp3
