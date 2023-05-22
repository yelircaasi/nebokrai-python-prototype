from typing import List 

from planager.utils.entry import Entry


def compress(start: PlTime, end: PlTime, entries: List[Entry]) -> List[Entry]:
    newentries = []
    total = end - start 
    lengths = list(map(Entry.length, entries))
    scale = sum(map(Entry.length, entries)) / total 
    newlengths = [round(scale * x.length) for x in entries]
    newlengths[-1] += (total - sum(newlengths))
    tracker = start.copy()
    for entry, duration in zip(entries, newlengths):
        entry.start = tracker.copy()
        tracker += duration 
        entry.end = tracker.copy()
        newentries.append(entry)
    return newentries


def share_time(entry1: Entry, entry2: Entry):
    start, end = entry1.spansize(entry2)
    if entry1.overlaps_first(entry2):
        ...
    elif entry1.overlaps_second(entry2):
        ...
    
    return entry1, entry2

def resolve_1_collision(
    entry: Entry, 
    before: List[Entry], 
    overlaps: List[Entry], 
    after: List[Entry]
    ) -> List[Entry]:
    overlap = overlaps[0]
    if overlap.priority <= 0:
        pre = overlap.copy(end=entry.start)
        post = overlap.copy(start=entry.end)
        return [pre, entry, post]
    elif entry.precedes(overlap) and (entry.mintime + overlap.mintime < entry.spansize(overlap)):
        entry, overlap = share_time(entry, overlap)

    return schedule


def resolve_2_collisions(entry, before, overlaps, after) -> List[Entry]:
    
    return schedule


def resolve_n_collisions(entry, before, overlaps, after) -> List[Entry]:
    
    return schedule
