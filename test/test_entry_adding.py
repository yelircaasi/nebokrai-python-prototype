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

from planager.entities.day import Day
from planager.entities.entry import Empty, Entry, FIRST_ENTRY, LAST_ENTRY
from planager.utils.datetime_extensions import PTime


class TestEntryAdding(unittest.TestCase):
    def __init__(self):
        self.day1 = Day(
            schedule=[
                FIRST_ENTRY,
                Entry(
                    name="Sleep", 
                    start=PTime(), 
                    end=PTime(5), 
                    priority=60, 
                    ismovable=True, 
                    normaltime=None, 
                    mintime=240
                ),
                Entry(
                    name="Morning Routine", 
                    start=PTime(5),      
                    end=PTime(7),      
                    priority=80, 
                    ismovable=True,  
                    normaltime=None, 
                    mintime=30
                ),
                Entry(
                    name="Appointment",     
                    start=PTime(7),      
                    end=PTime(9),      
                    priority=99, 
                    ismovable=False, 
                    normaltime=None, 
                    mintime=120
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
                    mintime=20
                ),
                Entry(
                    name="Programming",     
                    start=PTime(10, 15), 
                    end=PTime(11),     
                    priority=50, 
                    ismovable=True,  
                    normaltime=None, 
                    mintime=40
                ),
                Empty(
                    start=PTime(11),
                    end=PTime(21)
                ),
                Entry(name="Sleep",           
                    start=PTime(21),     
                    end=PTime(24), 
                    priority=80, 
                    ismovable=True,  
                    normaltime=None, 
                    mintime=150,
                    alignend=True
                ),
                LAST_ENTRY,
            ]
        )
        self.day2 = Day(
            schedule = []
        )
        self.day3 = Day(
            schedule = []
        )

    def test_add_to_empty(self):
        day = Day()
        entry = Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        day.add(entry)
        print(day)
        print(day.schedule)

        assert day.schedule[1] == Empty(
            start=PTime(), 
            end=PTime(11), 
        )
        assert day.schedule[2] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[3] == Empty(
            start=PTime(13), 
            end=PTime(24), 
        )

    def test_add_room_to_spare(self):
        day = self.day1.copy()
        entry = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
        day.add(entry)
        print("\n\n\n")
        print(day)
        print(day.schedule)

        self.d = day
        
        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times
        
    def test_add_bump_down(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(10, 30), end=PTime(11), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times


    def test_add_adjacent(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times

    def test_add_minimal_uncompressed(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times

    def test_add_with_compression(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(10, 30), end=PTime(13), priority=50.0, ismovable=True)
        day.add(entry)
        
        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times

    def test_add_no_room_before(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times

    def test_add_no_room_before(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times
        
    def test_add_no_room_after(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times

    def test_add_over_immovable(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.ispartitioned()
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
            "Last"
        ]
        assert day.names() == assert_names
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
        assert day.starts_str() == assert_times


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