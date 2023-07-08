import pytest

from planager.entities.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from planager.entities.schedule import Schedule
from planager.utils.algorithms.scheduling import (
    add_entry_default,
    add_immovable,
    add_movable,
    add_over_empty,
    adjust_backward,
    adjust_forward,
    compress,
    compress_weighted,
    entries_fit,
    entries_fit_normal,
    get_overlaps,
    slot_is_empty,
    split_after,
    split_before,
    get_before_and_after,
)
from planager.utils.datetime_extensions import PTime

# define entries as building blocks


# empty day
def get_empty_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Empty(start=PTime(0), end=PTime(24)),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


# default day (with sleep, work, meals)
def get_default_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Entry(name="Sleep", start=PTime(0), end=PTime(5), priority=75),
            Entry(name="Morning Routine", start=PTime(5), end=PTime(7)),
            Entry(name="Work", start=PTime(7), end=PTime(12)),
            Entry(name="Lunch", start=PTime(12), end=PTime(13)),
            Entry(name="Work", start=PTime(13), end=PTime(16)),
            Entry(name="Workout", start=PTime(16), end=PTime(17)),
            Entry(name="Piano", start=PTime(17), end=PTime(18)),
            Entry(name="Dinner", start=PTime(18), end=PTime(19)),
            Entry(name="Study", start=PTime(19), end=PTime(20)),
            Entry(name="Evening Routine", start=PTime(20), end=PTime(22)),
            Entry(name="Sleep", start=PTime(22), end=PTime(24), priority=75),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


# day with few activities
def get_sparse_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
            ),
            Empty(start=PTime(5), end=PTime(10)),
            Entry(
                name="Activity 1",
                start=PTime(10),
                end=PTime(11, 30),
            ),
            Empty(start=PTime(11, 30), end=PTime(13, 30)),
            Entry(
                name="Activity 2",
                start=PTime(13, 30),
                end=PTime(14, 15),
            ),
            Empty(start=PTime(14, 15), end=PTime(15, 45)),
            Entry(
                name="Activity 3",
                start=PTime(15, 45),
                end=PTime(18, 30),
            ),
            Empty(start=PTime(18, 30), end=PTime(22)),
            Entry(
                name="Sleep",
                start=PTime(22),
                end=PTime(24),
                priority=75,
            ),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


# packed full day (error expected)
def get_saturated_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
                mintime=300,
            ),
            Entry(
                name="Activity 1",
                start=PTime(5),
                end=PTime(7),
                mintime=120,
            ),
            Entry(
                name="Activity 2",
                start=PTime(7),
                end=PTime(8),
                mintime=60,
            ),
            Entry(
                name="Activity 3",
                start=PTime(8),
                end=PTime(10),
                mintime=120,
            ),
            Entry(
                name="Activity 4",
                start=PTime(10),
                end=PTime(12, 30),
                mintime=150,
            ),
            Entry(
                name="Activity 5",
                start=PTime(12, 30),
                end=PTime(15),
                ismovable=False,
                mintime=150,
            ),
            Entry(
                name="Activity 6",
                start=PTime(15),
                end=PTime(16, 15),
                mintime=75,
            ),
            Entry(
                name="Activity 7",
                start=PTime(16, 15),
                end=PTime(19),
                mintime=165,
            ),
            Entry(
                name="Activity 8",
                start=PTime(19),
                end=PTime(21),
                mintime=120,
            ),
            Entry(
                name="Activity 9",
                start=PTime(21),
                end=PTime(22),
                mintime=60,
            ),
            Entry(
                name="Sleep",
                start=PTime(22),
                end=PTime(24),
                priority=75,
                mintime=120,
            ),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


# non-empty day, compression required
def get_compressible_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
                mintime=270,
            ),
            Entry(
                name="Activity 1",
                start=PTime(5),
                end=PTime(7),
                priority=60,
                mintime=60,
            ),
            Entry(
                name="Activity 2",
                start=PTime(7),
                end=PTime(8),
                priority=80,
                mintime=40,
            ),
            Entry(
                name="Activity 3",
                start=PTime(8),
                end=PTime(10),
                priority=50,
                mintime=90,
            ),
            Entry(
                name="Activity 4",
                start=PTime(10),
                end=PTime(12, 30),
                priority=30,
                mintime=90,
            ),
            Entry(
                name="Activity 5",
                start=PTime(12, 30),
                end=PTime(15),
                ismovable=False,
                priority=65,
                mintime=60,
            ),
            Entry(
                name="Activity 6",
                start=PTime(15),
                end=PTime(16, 15),
                priority=70,
                mintime=45,
            ),
            Entry(
                name="Activity 7",
                start=PTime(16, 15),
                end=PTime(19),
                priority=75,
                mintime=120,
            ),
            Entry(
                name="Activity 8",
                start=PTime(19),
                end=PTime(21),
                priority=20,
                mintime=60,
            ),
            Entry(
                name="Activity 9",
                start=PTime(21),
                end=PTime(22),
                priority=90,
                mintime=45,
            ),
            Entry(
                name="Sleep",
                start=PTime(22),
                end=PTime(24),
                priority=75,
                mintime=90,
            ),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


# non-empty day, shifting but no compression
def get_loose_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
                mintime=240,
            ),
            Entry(
                name="Activity 1",
                start=PTime(5),
                end=PTime(7),
                priority=60,
                mintime=90,
            ),
            Entry(
                name="Activity 2",
                start=PTime(7),
                end=PTime(8),
                priority=45,
                mintime=40,
            ),
            Entry(
                name="Activity 3",
                start=PTime(8),
                end=PTime(10),
                priority=35,
                mintime=90,
            ),
            Empty(
                start=PTime(10),
                end=PTime(12, 30),
            ),
            Entry(
                name="Activity 4",
                start=PTime(12, 30),
                end=PTime(15),
                priority=50,
                mintime=120,
            ),
            Entry(
                name="Activity 5",
                start=PTime(15),
                end=PTime(16, 15),
                priority=95,
                mintime=75,
            ),
            Empty(
                start=PTime(16, 15),
                end=PTime(19),
            ),
            Entry(
                name="Activity 6",
                start=PTime(19),
                end=PTime(21),
                priority=75,
                mintime=75,
            ),
            Entry(
                name="Activity 7",
                start=PTime(21),
                end=PTime(22),
                priority=65,
                mintime=60,
            ),
            Entry(
                name="Sleep",
                start=PTime(22),
                end=PTime(24),
                priority=75,
                mintime=100,
            ),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


# non-empty day, overflow around immovable
def get_shiftaround_day() -> Schedule:
    sched = Schedule(
        schedule=[
            FIRST_ENTRY,
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
                mintime=240,
            ),
            Entry(
                name="Activity 1",
                start=PTime(5),
                end=PTime(7),
                priority=60,
                mintime=90,
            ),
            Entry(
                name="Activity 2",
                start=PTime(7),
                end=PTime(8),
                priority=45,
                mintime=40,
            ),
            Entry(
                name="Activity 3",
                start=PTime(8),
                end=PTime(10),
                priority=35,
                mintime=90,
            ),
            Empty(
                start=PTime(10),
                end=PTime(12, 30),
            ),
            Entry(
                name="Activity 4",
                start=PTime(12, 30),
                end=PTime(15),
                ismovable=False,
                priority=50,
                mintime=120,
            ),
            Entry(
                name="Activity 5",
                start=PTime(15),
                end=PTime(16, 15),
                ismovable=False,
                priority=95,
                mintime=75,
            ),
            Empty(
                start=PTime(16, 15),
                end=PTime(19),
            ),
            Entry(
                name="Activity 6",
                start=PTime(19),
                end=PTime(21),
                priority=75,
                mintime=75,
            ),
            Entry(
                name="Activity 7",
                start=PTime(21),
                end=PTime(22),
                ismovable=False,
                priority=65,
                mintime=60,
            ),
            Entry(
                name="Sleep",
                start=PTime(22),
                end=PTime(24),
                priority=75,
                mintime=100,
            ),
            LAST_ENTRY,
        ]
    )
    sched.ensure_bookends()
    assert sched.ispartitioned()
    return sched


class TestScheduling:
    def test_get_overlaps(self):
        empty_day = get_empty_day().schedule
        default_day = get_default_day().schedule
        sparse_day = get_sparse_day().schedule
        saturated_day = get_saturated_day().schedule
        compressible_day = get_compressible_day().schedule
        loose_day = get_loose_day().schedule
        shiftaround_day = get_shiftaround_day().schedule

        entry_for_empty = Entry(name="", start=PTime(9), end=PTime(10))
        entry_for_default = Entry(name="", start=PTime(6), end=PTime(13, 30))
        entry_for_sparse = Entry(name="", start=PTime(10, 30), end=PTime(14, 30))
        entry_for_saturated = Entry(name="", start=PTime(0), end=PTime(9))
        entry_for_compressible = Entry(name="", start=PTime(2), end=PTime(3))
        entry_for_loose = Entry(name="", start=PTime(12, 30), end=PTime(15))
        entry_for_shiftaround = Entry(name="", start=PTime(20), end=PTime(24))

        empty_expected = [Empty(start=PTime(0), end=PTime(24))]
        default_expected = [
            Entry(name="Morning Routine", start=PTime(5), end=PTime(7)),
            Entry(name="Work", start=PTime(7), end=PTime(12)),
            Entry(name="Lunch", start=PTime(12), end=PTime(13)),
            Entry(name="Work", start=PTime(13), end=PTime(16)),
        ]
        sparse_expected = [
            Entry(
                name="Activity 1",
                start=PTime(10),
                end=PTime(11, 30),
            ),
            Empty(start=PTime(11, 30), end=PTime(13, 30)),
            Entry(
                name="Activity 2",
                start=PTime(13, 30),
                end=PTime(14, 15),
            ),
            Empty(start=PTime(14, 15), end=PTime(15, 45)),
        ]
        saturated_expected = [
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
                mintime=300,
            ),
            Entry(
                name="Activity 1",
                start=PTime(5),
                end=PTime(7),
                mintime=120,
            ),
            Entry(
                name="Activity 2",
                start=PTime(7),
                end=PTime(8),
                mintime=60,
            ),
            Entry(
                name="Activity 3",
                start=PTime(8),
                end=PTime(10),
                mintime=120,
            ),
        ]
        compressible_expected = [
            Entry(
                name="Sleep",
                start=PTime(0),
                end=PTime(5),
                priority=75,
                mintime=270,
            ),
        ]
        loose_expected = [
            Entry(
                name="Activity 4",
                start=PTime(12, 30),
                end=PTime(15),
                priority=50,
                mintime=120,
            ),
        ]
        shiftaround_expected = [
            Entry(
                name="Activity 6",
                start=PTime(19),
                end=PTime(21),
                priority=75,
                mintime=75,
            ),
            Entry(
                name="Activity 7",
                start=PTime(21),
                end=PTime(22),
                ismovable=False,
                priority=65,
                mintime=60,
            ),
            Entry(
                name="Sleep",
                start=PTime(22),
                end=PTime(24),
                priority=75,
                mintime=100,
            ),
        ]

        assert get_overlaps(entry_for_empty, empty_day) == empty_expected
        assert get_overlaps(entry_for_default, default_day) == default_expected
        assert get_overlaps(entry_for_sparse, sparse_day) == sparse_expected
        assert get_overlaps(entry_for_saturated, saturated_day) == saturated_expected
        assert (
            get_overlaps(entry_for_compressible, compressible_day)
            == compressible_expected
        )
        result = get_overlaps(entry_for_loose, loose_day)
        # print('\n'.join(map(str, result)))
        # print('\n'.join(map(str, loose_expected)))
        assert result == loose_expected
        assert (
            get_overlaps(entry_for_shiftaround, shiftaround_day) == shiftaround_expected
        )

        assert True

    def test_slot_is_empty(self):
        empty_day = get_empty_day().schedule
        default_day = get_default_day().schedule
        sparse_day = get_sparse_day().schedule
        saturated_day = get_saturated_day().schedule
        compressible_day = get_compressible_day().schedule
        loose_day = get_loose_day().schedule
        shiftaround_day = get_shiftaround_day().schedule

        assert slot_is_empty(empty_day[1:2]) == True
        assert slot_is_empty(default_day[2:4]) == False
        assert slot_is_empty(sparse_day[:]) == False
        assert slot_is_empty(saturated_day[3:]) == False
        assert slot_is_empty(compressible_day[:4]) == False
        assert slot_is_empty(loose_day[5:6]) == True
        assert slot_is_empty(shiftaround_day[3:4]) == False

        assert True

    def test_get_before_and_after(self):
        empty_day = get_empty_day().schedule
        schedule = [
            Entry(name="Morning Routine", start=PTime(5), end=PTime(7)),
            Entry(name="Work", start=PTime(7), end=PTime(12)),
            Entry(name="Lunch", start=PTime(12), end=PTime(13)),
            Entry(name="Work", start=PTime(13), end=PTime(16)),
            Entry(name="Workout", start=PTime(16), end=PTime(17)),
            Entry(name="Piano", start=PTime(17), end=PTime(18)),
            Entry(name="Dinner", start=PTime(18), end=PTime(19)),
        ]

        entry1 = Entry(name="", start=PTime(13, 30))
        entry2 = Entry(name="", start=PTime(4))
        entry3 = Entry(name="", start=PTime(20))
        entry4 = Entry(name="", start=PTime(13))

        expected_empty = ([], [])
        expected1 = (schedule[:4], schedule[4:])
        expected2 = ([], schedule)
        expected3 = (schedule, [])
        expected4 = expected1

        print(get_before_and_after(entry1, empty_day))
        assert get_before_and_after(entry1, empty_day) == expected_empty
        assert get_before_and_after(entry1, schedule) == expected1
        assert get_before_and_after(entry2, schedule) == expected2
        assert get_before_and_after(entry3, schedule) == expected3
        assert get_before_and_after(entry4, schedule) == expected4

        assert True

    def test_compress(self):
        # empty_expected = []
        input_ = [
            Entry(name="Work", start=PTime(7), end=PTime(12)),
            Entry(name="Lunch", start=PTime(12), end=PTime(13)),
            Entry(name="Work", start=PTime(13), end=PTime(16)),
            Entry(name="Workout", start=PTime(16), end=PTime(17)),
            Entry(name="Piano", start=PTime(17), end=PTime(18)),
            Entry(name="Dinner", start=PTime(18), end=PTime(19)),
        ]
        expected = [
            Entry(name="Work", start=PTime(9), end=PTime(12, 20)),
            Entry(name="Lunch", start=PTime(12, 20), end=PTime(13)),
            Entry(name="Work", start=PTime(13), end=PTime(15)),
            Entry(name="Workout", start=PTime(15), end=PTime(15, 40)),
            Entry(name="Piano", start=PTime(15, 40), end=PTime(16, 20)),
            Entry(name="Dinner", start=PTime(16, 20), end=PTime(17)),
        ]
        # sparse_expected = []
        # saturated_expected = []
        # compressible_expected = []
        # loose_expected = []
        # shiftaround_expected = []

        # assert compress(empty_day, PTime(), PTime()) == empty_expected
        assert compress(input_, PTime(9), PTime(17)) == expected

        # assert compress(sparse_day, PTime(), PTime()) == sparse_expected
        # assert compress(saturated_day, PTime(), PTime()) == saturated_expected
        # assert compress(compressible_day, PTime(), PTime()) == compressible_expected
        # assert compress(loose_day, PTime(), PTime()) == loose_expected
        # assert compress(shiftaround_day, PTime(), PTime()) == shiftaround_expected

        assert True

    # def test_compress_weighted(self):
    # empty_day = get_empty_day().schedule
    # default_day = get_default_day().schedule
    # sparse_day = get_sparse_day().schedule
    # saturated_day = get_saturated_day().schedule
    # compressible_day = get_compressible_day().schedule
    # loose_day = get_loose_day().schedule
    # shiftaround_day = get_shiftaround_day().schedule

    # empty_expected = []
    # default_expected = []
    # sparse_expected = []
    # saturated_expected = []
    # compressible_expected = []
    # loose_expected = []
    # shiftaround_expected = []

    # assert compress(empty_day, PTime(), PTime()) == empty_expected
    # assert compress(default_day, PTime(), PTime()) == default_expected
    # assert compress(sparse_day, PTime(), PTime()) == sparse_expected
    # assert compress(saturated_day, PTime(), PTime()) == saturated_expected
    # assert compress(compressible_day, PTime(), PTime()) == compressible_expected
    # assert compress(loose_day, PTime(), PTime()) == loose_expected
    # assert compress(shiftaround_day, PTime(), PTime()) == shiftaround_expected

    # assert True

    def test_entries_fit(self):
        empty_day = get_empty_day().schedule
        default_day = get_default_day().schedule

        assert entries_fit(empty_day, PTime(2), PTime(3)) == True
        assert entries_fit(empty_day, PTime(2), PTime(2)) == True
        assert entries_fit(default_day[2:7], PTime(5), PTime(11)) == True
        assert entries_fit(default_day[2:7], PTime(5), PTime(10)) == False

        explicit = [
            Entry(
                name="Activity 1",
                start=PTime(7),
                mintime=40,
            ),
            Entry(
                name="Activity 2",
                start=PTime(9),
                mintime=35,
            ),
            Entry(
                name="Activity 3",
                start=PTime(11),
                mintime=20,
            ),
        ]
        assert entries_fit(explicit, PTime(11), PTime(12, 30)) == False
        assert entries_fit(explicit, PTime(11), PTime(12, 35)) == True
        assert entries_fit(explicit, PTime(11), PTime(12, 40)) == True

        assert True

    def test_entries_fit_normal(self):
        empty_day = get_empty_day().schedule
        default_day = get_default_day().schedule

        assert entries_fit_normal(empty_day, PTime(2), PTime(3)) == True
        assert entries_fit_normal(empty_day, PTime(2), PTime(2)) == True
        assert entries_fit_normal(default_day[2:7], PTime(5), PTime(17)) == True
        assert entries_fit_normal(default_day[2:7], PTime(5), PTime(16)) == False

        explicit = [
            Entry(
                name="Activity 1",
                start=PTime(7),
                normaltime=40,
            ),
            Entry(
                name="Activity 2",
                start=PTime(9),
                normaltime=35,
            ),
            Entry(
                name="Activity 3",
                start=PTime(11),
                normaltime=20,
            ),
        ]
        assert entries_fit_normal(explicit, PTime(11), PTime(12, 30)) == False
        assert entries_fit_normal(explicit, PTime(11), PTime(12, 35)) == True
        assert entries_fit_normal(explicit, PTime(11), PTime(12, 40)) == True

        assert True

    def test_split_before(self):
        # empty_day = get_empty_day().schedule
        # default_day = get_default_day().schedule
        # sparse_day = get_sparse_day().schedule
        # saturated_day = get_saturated_day().schedule
        # compressible_day = get_compressible_day().schedule
        # loose_day = get_loose_day().schedule
        # shiftaround_day = get_shiftaround_day().schedule

        # empty_expected = []
        # default_expected = []
        # sparse_expected = []
        # saturated_expected = []
        # compressible_expected = []
        # loose_expected = []
        # shiftaround_expected = []

        # assert split_before(empty_day[...]) == empty_expected
        # assert split_before(default_day[...]) == default_expected
        # assert split_before(sparse_day[...]) == sparse_expected
        # assert split_before(saturated_day[...]) == saturated_expected
        # assert split_before(compressible_day[...]) == compressible_expected
        # assert split_before(loose_day[...]) == loose_expected
        # assert split_before(shiftaround_day[...]) == shiftaround_expected

        assert True

    def test_split_after(self):
        # empty_day = get_empty_day().schedule
        # default_day = get_default_day().schedule
        # sparse_day = get_sparse_day().schedule
        # saturated_day = get_saturated_day().schedule
        # compressible_day = get_compressible_day().schedule
        # loose_day = get_loose_day().schedule
        # shiftaround_day = get_shiftaround_day().schedule

        # empty_expected = []
        # default_expected = []
        # sparse_expected = []
        # saturated_expected = []
        # compressible_expected = []
        # loose_expected = []
        # shiftaround_expected = []

        # assert split_after(empty_day[...]) == empty_expected
        # assert split_after(default_day[...]) == default_expected
        # assert split_after(sparse_day[...]) == sparse_expected
        # assert split_after(saturated_day[...]) == saturated_expected
        # assert split_after(compressible_day[...]) == compressible_expected
        # assert split_after(loose_day[...]) == loose_expected
        # assert split_after(shiftaround_day[...]) == shiftaround_expected

        assert True

    def test_add_over_empty(self):
        # assert add_over_empty(Entry(...), Empty(...)) == [...]
        # assert add_over_empty(Entry(...), Empty(...)) == [...]
        # assert add_over_empty(Entry(...), Empty(...)) == [...]
        # assert add_over_empty(Entry(...), Empty(...)) == [...]
        # assert add_over_empty(Entry(...), Empty(...)) == [...]
        # assert add_over_empty(Entry(...), Empty(...)) == [...]

        assert True

    def test_add_movable(self):
        # empty_day = get_empty_day().schedule
        # default_day = get_default_day().schedule
        # sparse_day = get_sparse_day().schedule
        # saturated_day = get_saturated_day().schedule
        # compressible_day = get_compressible_day().schedule
        # loose_day = get_loose_day().schedule
        # shiftaround_day = get_shiftaround_day().schedule

        # empty_expected = []
        # default_expected = []
        # sparse_expected = []
        # saturated_expected = []
        # compressible_expected = []
        # loose_expected = []
        # shiftaround_expected = []

        # assert add_movable(Entry(...), empty_day) == empty_expected
        # assert add_movable(Entry(...), default_day) == default_expected
        # assert add_movable(Entry(...), sparse_day) == sparse_expected
        # assert add_movable(Entry(...), saturated_day) == saturated_expected
        # assert add_movable(Entry(...), compressible_day) == compressible_expected
        # assert add_movable(Entry(...), loose_day) == loose_expected
        # assert add_movable(Entry(...), shiftaround_day) == shiftaround_expected

        assert True

    def test_add_immovable(self):
        # empty_day = get_empty_day().schedule
        # default_day = get_default_day().schedule
        # sparse_day = get_sparse_day().schedule
        # saturated_day = get_saturated_day().schedule
        # compressible_day = get_compressible_day().schedule
        # loose_day = get_loose_day().schedule
        # shiftaround_day = get_shiftaround_day().schedule

        # empty_expected = []
        # default_expected = []
        # sparse_expected = []
        # saturated_expected = []
        # compressible_expected = []
        # loose_expected = []
        # shiftaround_expected = []

        # assert add_immovable(Entry(...), empty_day) == empty_expected
        # assert add_immovable(Entry(...), default_day) == default_expected
        # assert add_immovable(Entry(...), sparse_day) == sparse_expected
        # assert add_immovable(Entry(...), saturated_day) == saturated_expected
        # assert add_immovable(Entry(...), compressible_day) == compressible_expected
        # assert add_immovable(Entry(...), loose_day) == loose_expected
        # assert add_immovable(Entry(...), shiftaround_day) == shiftaround_expected

        assert True

    def test_add_entry_default(self):

        # ----------------------------------------------------------------------------
        # movable to empty day

        # immovable to empty day

        # movable over empty slot

        # immovable over empty slot

        # movable over empty, near other task, forcing snap: task is movable and before

        # movable over empty, near other task, forcing snap: task is movable and after

        # movable over empty, near other task, forcing snap: task is immovable and before

        # movable over empty, near other task, forcing snap: task is immovable and after

        # immovable over empty, near other task, forcing snap: task is movable and before

        # immovable over empty, near other task, forcing snap: task is movable and after

        # immovable over empty, near other task, forcing snap: task is immovable and before

        # immovable over empty, near other task, forcing snap: task is immovable and after

        # add movable over movable-before

        # add movable over movable-after
        
        # add movable over immovable-before

        # add movable over immovable-after

        # add immovable over movable-before

        # add immovable over movable-after
        
        # (impossible) add immovable over immovable-before

        # (impossible) add immovable over immovable-after

        # (impossible) entry over saturated day

        # (impossible) entry over near-saturated day

        # add movable in a way that will require reordering based on order attribute

        # add immovable in a way that will require flowaround

        # add immovable in a way that will require flowaround, trumping order
        
        
        # ----------------------------------------------------------------------------
        # empty_day = get_empty_day().schedule
        # default_day = get_default_day().schedule
        # sparse_day = get_sparse_day().schedule
        # saturated_day = get_saturated_day().schedule
        # compressible_day = get_compressible_day().schedule
        # loose_day = get_loose_day().schedule
        # shiftaround_day = get_shiftaround_day().schedule

        # empty_expected = []
        # default_expected = []
        # sparse_expected = []
        # saturated_expected = []
        # compressible_expected = []
        # loose_expected = []
        # shiftaround_expected = []

        # assert add_entry_default(Entry(...), empty_day) == empty_expected
        # assert add_entry_default(Entry(...), default_day) == default_expected
        # assert add_entry_default(Entry(...), sparse_day) == sparse_expected
        # assert add_entry_default(Entry(...), saturated_day) == saturated_expected
        # assert add_entry_default(Entry(...), compressible_day) == compressible_expected
        # assert add_entry_default(Entry(...), loose_day) == loose_expected
        # assert add_entry_default(Entry(...), shiftaround_day) == shiftaround_expected

        assert True
