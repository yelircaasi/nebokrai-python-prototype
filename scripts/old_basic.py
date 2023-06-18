from planager import (
    Schedule,
    Empty,
    Entry,
    FIRST_ENTRY,
    LAST_ENTRY,
    PDate,
    PTime,
)


sleep1 = Entry(...)
sleep2 = Entry(...)
morning_routine = Entry(...)
evening_routine = Entry(...)

DEFAULT_DAY = Schedule()
DEFAULT_DAY.add(sleep1)
DEFAULT_DAY.add(sleep2)
DEFAULT_DAY.add(morning_routine)
DEFAULT_DAY.add(evening_routine)

day = DEFAULT_DAY.copy()
open_slots = day.open_slots()

taskentry1 = Entry(...)
taskentry2 = Entry(...)
taskentry3 = Entry(...)

added: bool = day.add_to_first_opening(taskentry1)
added = day.add_to_last_opening(taskentry2) if added else False
added = day.add_to_closest_opening(taskentry2) if added else False
