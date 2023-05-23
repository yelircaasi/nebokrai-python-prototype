from calendar import Calendar
from datetime import date, datetime, time
from enum import Enum

from planager.entities.entry import FIRST_ENTRY, LAST_ENTRY, Entry
from planager.entities.task import Task, RecurringTask, emptytask
from planager.utils.datetime_extensions import PlDate, PlDateTime, PlTime
from planager.utils.scheduling_helpers import resolve_1_collision, resolve_2_collisions, resolve_n_collisions


class AdjustmentType(Enum):
    AUTO = 0         # methods figure it out, based on priority and properties
    CLIP = 1         # higher-priority entry takes precedence and lower-priority activity makes way
    SHIFT = 2        # 
    COMPRESS = 3     # 
    COMPROMISE = 4   # 


class DefaultDay:
    def __init__(self, year, month, day):
        self.schedule = [
            Entry(
                name="Empty",
                start=PlDateTime(year, month, day, 0, 0),
                end=PlDateTime(year, month, day, 23, 59),
                priority=-1.0
            )
        ]

    def add_entry(self, entry: Entry, adjustment: AdjustmentType = AdjustmentType.AUTO):
        self.schedule.sort()
        before = [FIRST_ENTRY] + list(filter(entry.after, self.schedule))
        after = list(filter(entry.before, self.schedule)) + [LAST_ENTRY]
        overlaps = list(filter(entry.overlaps, filter(lambda ent: ent.priority >= 0, self.schedule)))
        collisions = len(overlaps)

        match adjustment:
            case AdjustmentType.AUTO:
                match collisions:
                    case 1:
                        self.schedule = resolve_1_collision(entry, before, overlaps, after)
                    case 2:
                        self.schedule = resolve_2_collisions(entry, before, overlaps, after)
                    case _:
                        self.schedule = resolve_n_collisions(entry, before, overlaps, after)

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

    def remove_entry(self, entry: Entry, adjustment: AdjustmentType = AdjustmentType.AUTO):
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
