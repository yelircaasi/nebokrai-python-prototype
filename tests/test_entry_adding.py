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
from planager.entities.day import Day
from planager.entities.entry import Empty, Entry
from planager.utils.datetime_extensions import PTime


def test_add_to_empty():
    day = Day(2023, 5, 23)
    entry = Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True)
    day.add(entry)
    assert ...


def test_add_room_to_spare():
    day = Day(2023, 5, 23)
    day.schedule = [
        Entry(name="Sleep",           start=PTime(),       end=PTime(5),      priority=0, movable=True,  time=None, mintime=240),
        Entry(name="Morning Routine", start=PTime(5),      end=PTime(7),      priority=0, movable=True,  time=None, mintime=30),
        Entry(name="Appointment",     start=PTime(7),      end=PTime(9),      priority=0, movable=False, time=None, mintime=120),
        Empty(                        start=PTime(9),      end=PTime(9, 45),  ),
        Entry(name="Shopping",        start=PTime(9, 45),  end=PTime(10, 15), priority=0, movable=True,  time=None, mintime=20),
        Entry(name="Programming",     start=PTime(10, 15), end=PTime(11),     priority=0, movable=True,  time=None, mintime=40),
        Entry(name="Empty",           start=PTime(11),     end=PTime(21),     priority=0, movable=True,  time=None, mintime=0),
        Entry(name="Sleep",           start=PTime(21),     end=PTime(24), priority=0, movable=True,  time=None, mintime=149),
    ]
    entry = Entry(name="Walk", start=PTime(10, 30), end=PTime(11), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0),   end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk",  start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)


def test_add_minimal_room(): #TODO
    day = Day(2023, 5, 23)
    day.schedule = [
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
    ]
    entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)


def test_add_compression(): #TODO
    day = Day(2023, 5, 23)
    day.schedule = [
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
        Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),
    ]
    entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)


def test_add_no_room_before(): #TODO
    day = Day(2023, 5, 23)
    day.schedule = [Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),]
    entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)


def test_add_no_room_before(): #TODO
    day = Day(2023, 5, 23)
    day.schedule = [Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),]
    entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)


def test_add_no_room_after(): #TODO
    day = Day(2023, 5, 23)
    day.schedule = [Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),]
    entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)


def test_add_over_immovable(): #TODO
    day = Day(2023, 5, 23)
    day.schedule = [Entry(name="", start=PTime(), end=PTime(), priority=0, movable=True),]
    entry = Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    day.add(entry)

    assert day.schedule[0] == Entry(name="Empty", start=PTime(0, 0), end=PTime(14, 30), priority=-1.0)
    assert day.schedule[1] == Entry(name="Walk", start=PTime(14, 30), end=PTime(15, 15), priority=50.0, movable=True)
    assert day.schedule[2] == Entry(name="Empty", start=PTime(15, 15), end=PTime(24), priority=-1.0)
