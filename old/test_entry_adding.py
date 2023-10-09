"""
Case to test:
- adding to empty day
- adding to full day with room to spare
- adding to full day with minimal room
- adding to full day with some compression required
- adding to full day with no room before (should fail)
- adding to full day with no room after (should fail)
- adding to time already occupied by immovable entry

"""
import unittest

from planager.entity import FIRST_ENTRY, LAST_ENTRY, Empty, Entry, Schedule
from planager.util import PTime


class TestEntryAdding(unittest.TestCase):
    def __init__(self):
        self.day1 = Schedule(
            schedule=[
                FIRST_ENTRY,
                Entry(
                    name="Sleep",
                    start=PTime(),
                    end=PTime(5),
                    priority=60,
                    ismovable=True,
                    normaltime=None,
                    mintime=240,
                ),
                Entry(
                    name="Morning Routine",
                    start=PTime(5),
                    end=PTime(7),
                    priority=80,
                    ismovable=True,
                    normaltime=None,
                    mintime=30,
                ),
                Entry(
                    name="Appointment",
                    start=PTime(7),
                    end=PTime(9),
                    priority=99,
                    ismovable=False,
                    normaltime=None,
                    mintime=120,
                ),
                Empty(
                    start=PTime(9),
                    end=PTime(9, 45),
                ),
                Entry(
                    name="Shopping",
                    start=PTime(9, 45),
                    end=PTime(10, 15),
                    priority=40,
                    ismovable=True,
                    normaltime=None,
                    mintime=20,
                ),
                Entry(
                    name="Programming",
                    start=PTime(10, 15),
                    end=PTime(11),
                    priority=50,
                    ismovable=True,
                    normaltime=None,
                    mintime=40,
                ),
                Empty(start=PTime(11), end=PTime(21)),
                Entry(
                    name="Sleep",
                    start=PTime(21),
                    end=PTime(24),
                    priority=80,
                    ismovable=True,
                    normaltime=None,
                    mintime=150,
                    alignend=True,
                ),
                LAST_ENTRY,
            ]
        )
        self.day2 = Schedule(schedule=[])
        self.day3 = Schedule(schedule=[])

    def test_add_to_empty(self):
        schedule = Schedule()
        entry = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
        schedule.add(entry)
        print(schedule)
        print(schedule.schedule)

        assert schedule.schedule[1] == Empty(
            start=PTime(),
            end=PTime(11),
        )
        assert schedule.schedule[2] == Entry(
            name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True
        )
        assert schedule.schedule[3] == Empty(
            start=PTime(13),
            end=PTime(24),
        )

    def test_add_room_to_spare(self):
        schedule = self.day1.copy()
        entry = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
        schedule.add(entry)
        print("\n\n\n")
        print(schedule)
        print(schedule.schedule)

        self.d = schedule

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_bump_down(self):
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(10, 30),
            end=PTime(11),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_adjacent(self):
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(14, 30),
            end=PTime(15, 15),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_minimal_uncompressed(self):
        schedule = self.day1.copy()
        entry = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_with_compression(self):
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(10, 30),
            end=PTime(13),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_no_room_before(self):  # TODO
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(14, 30),
            end=PTime(15, 15),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_OTHER_THING(self):  # TODO
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(14, 30),
            end=PTime(15, 15),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_no_room_after(self):  # TODO
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(14, 30),
            end=PTime(15, 15),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times

    def test_add_over_immovable(self):  # TODO
        schedule = self.day1.copy()
        entry = Entry(
            name="Walk",
            start=PTime(14, 30),
            end=PTime(15, 15),
            priority=50.0,
            ismovable=True,
        )
        schedule.add(entry)

        assert schedule.ispartitioned()
        assert_names = [
            "First",
            "Sleep",
            "Morning Routine",
            "Appointment",
            "Shopping",
            "Programming",
            "Walk",
            "Empty",
            "Sleep",
            "Last",
        ]
        assert schedule.names() == assert_names
        assert_times = [
            "00:00",
            "00:00",
            "05:00",
            "07:00",
            "09:00",
            "10:00",
            "11:30",
            "15:30",
            "18:00",
            "24:00",
        ]
        assert schedule.starts_str() == assert_times


# t = TestEntryAdding()
# t.test_add_to_empty()
# t.test_add_room_to_spare()
# e = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
# s = t.day1.schedule
# d = t.day1
# entries = [x for x in s[4:] if x.priority >= 0]
# entries.insert(2, e)
# start = PTime(9)
# end = PTime(24)
