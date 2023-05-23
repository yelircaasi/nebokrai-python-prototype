from typing import List 

from planager.entities.entry import Entry
from planager.utils.datetime_extensions import PlTime


def compress(entries: List[Entry], start: PlTime, end: PlTime) -> List[Entry]:
    newentries = []
    total = end - start 
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


def entries_fit(entries: List[Entry], start: PlTime, stop: PlTime) -> bool:
    total_min = sum(map(Entry.mintime, filter(Entry.hasmass, entries)))
    return (start.timeto(stop) >= total_min)


def entries_fit_spare(entries: List[Entry], start: PlTime, stop: PlTime) -> bool:
    total_max = sum(map(Entry.maxtime, filter(Entry.hasmass, entries)))
    return (start.timeto(stop) >= total_max)


def adjust_forward(entries: List[Entry], start: PlTime, stop: PlTime) -> bool:
    newentries = []
    tracker = start.copy()
    for entry in entries:
        dur = entry.duration
        entry.start = tracker.copy()
        tracker += dur
        entry.end = tracker.copy()
        newentries.append(entry)
    return newentries


def adjust_backward(entries: List[Entry], start: PlTime, stop: PlTime) -> bool:
    newentries = []
    tracker = start.copy()
    for entry in entries[::-1]:
        dur = entry.duration
        entry.end = tracker.copy()
        tracker -= dur
        entry.start = tracker.copy()
        newentries.insert(0, entry)
    return newentries


def push_aside(newentry: Entry, before: List[Entry], after: List[Entry], overlaps: List[Entry]) -> List[Entry]:
    movable_before = []
    movable = before[-1].ismovable
    ind = -1
    while movable:
        movable_before.insert(0, before[ind])
        movable = before[-1].ismovable
        ind -= 1
    limit_before = before[-1].end
    movable_after = []
    movable = after[0].ismovable
    ind = 0
    while movable:
        movable_after.append(after[ind])
        movable = after[0].ismovable
        ind += 1
    limit_after = after[0].start
    
    fit_before = entries_fit(movable_before, limit_before, newentry.start)
    fit_after = entries_fit(movable_after, newentry.end, limit_after)
    if not (fit_before and fit_after):
        print("Not enough room to add task.")
        return 

    spare_before = entries_fit_spare(movable_before, limit_before, newentry.start)
    if spare_before:
        movable_before = adjust_backward(movable_before, limit_before, newentry.start)
    else:
        movable_before = compress(movable_before, limit_before, newentry.start)
    spare_after = entries_fit_spare(movable_after, newentry.end, limit_after)
    if movable_after:
        movable_after = adjust_forward(movable_after, newentry.end, limit_after)
    else:
        movable_after = compress(movable_after, newentry.end, limit_after)
    
    
    # NEED TO CONSOLIDATE HERE
    
    



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

    schedule = []
    overlap = overlaps[0]
    if overlap.priority <= 0:
        pre = overlap.copy(end=entry.start)
        post = overlap.copy(start=entry.end)
        return [pre, entry, post]
    elif entry.precedes(overlap) and (entry.mintime + overlap.mintime < entry.spansize(overlap)):
        entry, overlap = share_time(entry, overlap)

    return schedule


def resolve_2_collisions(entry, before, overlaps, after) -> List[Entry]:
    schedule = []
    return schedule


def resolve_n_collisions(entry, before, overlaps, after) -> List[Entry]:
    schedule = []
    return schedule
