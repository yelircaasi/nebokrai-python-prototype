from calendar import Calendar
#from datetime import date, time
from enum import Enum

from planager.entities.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from planager.utils.datetime_extensions import PDate, PTime
# from planager.utils.scheduling_helpers import resolve_1_collision, resolve_2_collisions, resolve_n_collisions
from planager.utils.misc import tabularize


class AdjustmentType(Enum):
    AUTO = 0         # methods figure it out, based on priority and properties
    CLIP = 1         # higher-priority entry takes precedence and lower-priority activity makes way
    SHIFT = 2        # 
    COMPRESS = 3     # 
    COMPROMISE = 4   # 


class Day:
    def __init__(self, 
            year=PDate.today().year, 
            month=PDate.today().month, 
            day=PDate.today().day, 
            schedule=None, 
            width: int = 80
        ) -> None:
        self.schedule = schedule or [Empty(start=PTime(), end=PTime(24))]
        self.date = PDate(year, month, day)
        self.width = width

    def copy(self):
        newday = Day()
        newday.__dict__.update(self.__dict__)
        return newday

    def add(self, entry: Entry, adjustment: AdjustmentType = AdjustmentType.AUTO):
        self.schedule.sort()
        before = [FIRST_ENTRY] + list(filter(entry.after, self.schedule))
        after = list(filter(entry.before, self.schedule)) + [LAST_ENTRY]
        overlaps = list(filter(entry.overlaps, filter(lambda ent: ent.priority >= 0, self.schedule)))
        collisions = len(overlaps)

        match adjustment:
            case AdjustmentType.AUTO:
                ...
                # match collisions:
                #     case 1:
                #         self.schedule = resolve_1_collision(entry, before, overlaps, after)
                #     case 2:
                #         self.schedule = resolve_2_collisions(entry, before, overlaps, after)
                #     case _:
                #         self.schedule = resolve_n_collisions(entry, before, overlaps, after)

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

        self.schedule = ...

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


# d = Day(2023, 5, 23)
# d.schedule = [
#     Entry(name="Entry 1", start=PTime(4,30), end=PTime(5,45)), 
#     Entry(name="Entry 2", start=PTime(7,10), end=PTime(7,30), priority=56), 
#     Entry(name="R & R", start=PTime(9,15), end=PTime(9,50)), 
#     Entry(name="Last Entry for the day: reading at my own discretion", start=PTime(17,30), end=PTime(19,15), priority=10)
# ]
