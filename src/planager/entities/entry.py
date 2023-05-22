from datetime import time


class Entry:
    def __init__(self, start: PlTime, end: PlTime, obj, priority):
        self.__dict__.update(locals())

    def length(self) -> int:
        return self.end - self.start

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

    