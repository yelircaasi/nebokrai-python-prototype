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
from planager.entities.entry import Empty, Entry
from planager.utils.datetime_extensions import PTime


class TestEntryAdding(unittest.testcase):
    def __init__(self):
        self.day1 = Day(
            schedule=[
                Entry(
                    name="Sleep", 
                    start=PTime(), 
                    end=PTime(5), 
                    priority=0, 
                    ismovable=True, 
                    time=None, 
                    mintime=240
                ),
                Entry(
                    name="Morning Routine", 
                    start=PTime(5),      
                    end=PTime(7),      
                    priority=0, 
                    ismovable=True,  
                    time=None, 
                    mintime=30
                ),
                Entry(
                    name="Appointment",     
                    start=PTime(7),      
                    end=PTime(9),      
                    priority=0, 
                    ismovable=False, 
                    time=None, 
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
                    priority=0, 
                    ismovable=True,  
                    time=None, 
                    mintime=20
                ),
                Entry(
                    name="Programming",     
                    start=PTime(10, 15), 
                    end=PTime(11),     
                    priority=0, 
                    ismovable=True,  
                    time=None, 
                    mintime=40
                ),
                Entry(name="Empty",           
                    start=PTime(11),     
                    end=PTime(21),     
                    priority=0, 
                    ismovable=True,  
                    time=None, 
                    mintime=0
                ),
                Entry(name="Sleep",           
                    start=PTime(21),     
                    end=PTime(24), 
                    priority=0, 
                    ismovable=True,  
                    time=None, 
                    mintime=150
                ),
            ]
        )
        self.day2 = Day(
            schedule = []
        )
        self.day3 = Day(
            schedule = []
        )

    def test_add_to_empty(self): # TODO
        day = self.day1.copy()
        entry = Entry(name="", start=PTime(), end=PTime(), priority=0, ismovable=True)
        day.add(entry)
        assert ...

    def test_add_room_to_spare(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(11), end=PTime(13), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )
        
    def test_add_bump_down(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(10, 30), end=PTime(11), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Walk", 
            start=PTime(10, 15), 
            end=PTime(10, 45), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[6] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[7] == Entry(name="Empty",       
            start=PTime(11),     
            end=PTime(21),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=0
        )
        assert day.schedule[8] == Entry(name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )

    def test_add_adjacent(self):
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )

    def test_add_minimal_uncompressed(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 15), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )

    def test_add_compression(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
        assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)

    def test_add_no_room_before(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )

    def test_add_no_room_before(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )


    def test_add_no_room_after(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )


    def test_add_over_immovable(self): #TODO
        day =self.day1.copy()
        entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, ismovable=True)
        day.add(entry)

        assert day.schedule[0] == Entry(
            name="Sleep", 
            start=PTime(), 
            end=PTime(5), 
            priority=0, 
            ismovable=True, 
            time=None, 
            mintime=240
        )
        assert day.schedule[1] == Entry(
            name="Morning Routine", 
            start=PTime(5),      
            end=PTime(7),      
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=30
        )
        assert day.schedule[2] == Entry(
            name="Appointment",     
            start=PTime(7),      
            end=PTime(9),      
            priority=0, 
            ismovable=False, 
            time=None, 
            mintime=120
        )
        assert day.schedule[3] == Empty(
            start=PTime(9),
            end=PTime(9, 45),
        )
        assert day.schedule[4] == Entry(
            name="Shopping",    
            start=PTime(9, 45),  
            end=PTime(10, 15), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=20
        )
        assert day.schedule[5] == Entry(
            name="Programming",     
            start=PTime(10, 45), 
            end=PTime(11, 30),     
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=40
        )
        assert day.schedule[6] == Entry(
            name="Walk", 
            start=PTime(11), 
            end=PTime(13), 
            priority=50.0, 
            ismovable=True
        )
        assert day.schedule[7] == Empty(
            start=PTime(13),     
            end=PTime(21), 
        )
        assert day.schedule[8] == Entry(
            name="Sleep",       
            start=PTime(21),     
            end=PTime(24), 
            priority=0, 
            ismovable=True,  
            time=None, 
            mintime=150
        )
