from calendar import Calendar
#from datetime import date, time
from enum import Enum
from pathlib import Path
from typing import List

from planager.entities.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from planager.utils.datetime_extensions import PDate, PTime
# from planager.utils.scheduling_helpers import resolve_1_collision, resolve_2_collisions, resolve_n_collisions
from planager.utils.misc import tabularize
from planager.utils.data.norg import make_norg_header, make_norg_body, make_norg_notes
from planager.utils.scheduling_helpers import add_entry_default


class AdjustmentType(Enum):
    AUTO = 0         # methods figure it out, based on priority and properties
    CLIP = 1         # higher-priority entry takes precedence and lower-priority activity makes way
    SHIFT = 2        # 
    COMPRESS = 3     # 
    COMPROMISE = 4   # 


class Day:
    def __init__(
            self, 
            year=PDate.today().year, 
            month=PDate.today().month, 
            day=PDate.today().day, 
            schedule=None, 
            width: int = 80
        ) -> None:
        self.schedule = schedule or [FIRST_ENTRY, Empty(start=PTime(), end=PTime(24)), LAST_ENTRY]
        self.date = PDate(year, month, day)
        self.width = width

    def ensure_bookends(self) -> None:
        if not self.schedule[0] == FIRST_ENTRY:
            self.schedule.insert(0, FIRST_ENTRY)
        if not self.schedule[-1] == LAST_ENTRY:
            self.schedule.append(LAST_ENTRY)

    @classmethod
    def from_norg(cls, path: Path) -> "Day":
        #dict = read_norg_day(path)
        day = cls()
        return day

    @classmethod
    def from_json(cls, path: Path) -> "Day":
        day = cls()
        return day
    
    def to_norg(self, path: Path) -> None:
        header = make_norg_header()
        #body = "\n\n".join(map(Entry.to_norg, self.schedule[1:-1]))
        #notes = make_norg_notes()
        ...

    def to_json(self, path: Path) -> None:
        ...

    def copy(self):
        newday = Day()
        newday.__dict__.update(self.__dict__)
        return newday

    def add(self, entry: Entry, adjustment: AdjustmentType = AdjustmentType.AUTO):
        self.ensure_bookends()
        self.schedule.sort(key=lambda x: x.start)
        

        match adjustment:
            case AdjustmentType.AUTO:
                self.schedule = add_entry_default(entry, self.schedule)
                
                #TODO: integrate collision handling into before and after logic
                

            case AdjustmentType.CLIP:
                raise NotImplemented
            case AdjustmentType.SHIFT:
                raise NotImplemented
            case AdjustmentType.COMPRESS:
                raise NotImplemented
            case AdjustmentType.COMPROMISE:
                raise NotImplementedError
            case _:
                print("Invalid adjustment type.")

    def remove(self, entry: Entry, adjustment: AdjustmentType = AdjustmentType.AUTO):
        before = filter(entry.after, self.schedule)
        after = filter(entry.before, self.schedule)
        overlaps = filter(entry.overlaps, self.schedule)

        match adjustment:
            case AdjustmentType.AUTO:
                ...
            case AdjustmentType.CLIP:
                raise NotImplemented
            case AdjustmentType.SHIFT:
                raise NotImplemented
            case AdjustmentType.COMPRESS:
                raise NotImplemented
            case AdjustmentType.COMPROMISE:
                raise NotImplemented
            case _:
                print("Invalid adjustment type.")
        
        self.schedule = ...

    def __repr__(self) -> str:
        topbeam = "┏" + (self.width - 2) * "━" + "┓"
        date = tabularize(self.date.pretty(), self.width)
        bottombeam = "┗" + (self.width - 2) * "━" + "┛"
        
        lines = []
        lines.append(topbeam)
        lines.append(date)
        for entry in self.schedule:
            if entry.priority >= 0:
                lines.append(entry.pretty())
        lines.append(bottombeam)
        return "\n".join(lines)
    
    def __str__(self) -> str:

        return self.__repr__()
    
    def ispartitioned(self):
        if len(self.schedule) == 1:
            adjacency = True
        else:
            adjacency = all(map(lambda x: x[0].end == x[1].start, zip(self.schedule[:-1], self.schedule[1:])))
        return adjacency and (self.schedule[0].start == PTime()) and (self.schedule[-1].end == PTime(24))

    def names(self) -> List[str]:
        return [x.name for x in self.schedule]
    
    def starts(self) -> List[PTime]:
        return [x.start for x in self.schedule]
    
    def starts_str(self) -> List[PTime]:
        return [str(x.start) for x in self.schedule]


# d = Day(2023, 5, 23)
# d.schedule = [
#     Entry(name="Entry 1", start=PTime(4,30), end=PTime(5,45)), 
#     Entry(name="Entry 2", start=PTime(7,10), end=PTime(7,30), priority=56), 
#     Entry(name="R & R", start=PTime(9,15), end=PTime(9,50)), 
#     Entry(name="Last Entry for the day: reading at my own discretion", start=PTime(17,30), end=PTime(19,15), priority=10)
# ]
