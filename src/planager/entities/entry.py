#from datetime import time

from planager.utils.datetime_extensions import PTime
from planager.utils.misc import tabularize


class Entry:
    def __init__(self, obj, start: PTime, end: PTime, priority=0, ismovable=True, notes=""):
        self.__dict__.update(locals())
        
    def duration(self) -> int:
        return self.end - self.start
    
    def hasmass(self) -> bool:
        return self.priority > 0

    def before(self, entry2: "Entry") -> bool:
        return self.end <= entry2.start

    def after(self, entry2: "Entry") -> bool:
        return self.start >= entry2.end

    def overlaps(self, entry2: "Entry") -> bool:
        return (self.start < entry2.start < self.end) or (entry2.start < self.start < entry2.end)

    def overlaps_first(self, entry2: "Entry") -> bool:
        return (self.start <= entry2.start < self.end <= entry2.end)

    def overlaps_second(self, entry2: "Entry") -> bool:
        return (entry2.start <= self.start < entry2.end <= self.end)

    def surrounds(self, entry2: "Entry") -> bool:
        return (self.start < entry2.start < entry2.end < self.end)

    def surrounded(self, entry2: "Entry") -> bool:
        return (entry2.start < self.start < self.end < entry2.end)

    def precedes(self, entry2: "Entry") -> bool:
        return self.priority > entry2.priority

    def temporal_relationship(self, entry2: "Entry") -> str:
        if self.before(entry2):
            return "before"
        elif self.after(entry2):
            return "after"
        elif self.overlaps_first(entry2):
            return "overlaps_first"
        elif self.overlaps_second(entry2):
            return "overlaps_second"
        elif self.surrounds(entry2):
            return "surrounds"
        elif self.surrounded(entry2):
            return "surrounded"
        
    def pretty(self, width: int = 80) -> str:
        
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = thickbeam + tabularize(self.start, width) + thinbeam
        return header + "\n".join((tabularize(s, width) for s in (self.obj, f"Priority: {self.priority}", self.notes)))

# ent = Entry(PTime(5,30), PTime(6,20), "Workout", priority=30, notes="Running, pullups, pushups, medecine ball")
# print(ent.pretty())

FIRST_ENTRY = Entry(start=PTime(0), end=PTime(0), movable=False)
LAST_ENTRY = Entry(start=PTime(23, 59), end=PTime(23, 59), movable=False)
