from typing import List, Tuple 

from planager.entities.entry import Empty, Entry, FIRST_ENTRY, LAST_ENTRY
from planager.utils.datetime_extensions import PTime
from planager.utils.misc import round5


def compress(entries: List[Entry], start: PTime, end: PTime) -> List[Entry]:
    newentries = []
    total = start.timeto(end)
    scale = sum(map(Entry.duration, entries)) / total 
    newlengths = [round5(scale * x.duration) for x in entries]
    newlengths[-1] += (total - sum(newlengths))
    tracker = start.copy()
    for entry, duration in zip(entries, newlengths):
        entry.start = tracker.copy()
        tracker += duration 
        entry.end = tracker.copy()
        newentries.append(entry)
    return newentries


def entries_fit(entries: List[Entry], start: PTime, stop: PTime) -> bool:
    total_min = sum(map(lambda x: x.mintime, filter(Entry.hasmass, entries)))
    return (start.timeto(stop) >= total_min)


def entries_fit_spare(entries: List[Entry], start: PTime, stop: PTime) -> bool:
    total_max = sum(map(lambda x: x.maxtime, filter(Entry.hasmass, entries)))
    return (start.timeto(stop) >= total_max)


def adjust_forward(entries: List[Entry], start: PTime, stop: PTime) -> List[Entry]:
    newentries = []
    tracker = start.copy()
    for entry in entries:
        dur = entry.duration()
        entry.start = tracker.copy()
        tracker += dur
        entry.end = tracker.copy()
        newentries.append(entry)
    return newentries


def adjust_backward(entries: List[Entry], start: PTime, stop: PTime) -> List[Entry]:
    newentries = []
    tracker = start.copy()
    for entry in entries[::-1]:
        dur = entry.duration()
        entry.end = tracker.copy()
        tracker -= dur
        entry.start = tracker.copy()
        newentries.insert(0, entry)
    return newentries


def split_before(before: List[Entry]) -> Tuple[List[Entry], List[Entry], PTime]:
    print(before)
    movable_before = []
    # if not before[0] == FIRST_ENTRY:
    #     before.insert(0, FIRST_ENTRY)
    ismovable = before[-1].ismovable
    ind = -1
    while ismovable:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(ind)
        print(before[ind])
        movable_before.insert(0, before[ind])
        ismovable = before[ind - 1].ismovable
        ind -= 1
    before = before[:ind + 1]
    print("============ before")
    print(before)
    limit_before = PTime() if not before else before[-1].end

    return (before, movable_before, limit_before)


def split_after(after: List[Entry]) -> Tuple[List[Entry], List[Entry], PTime]:
    movable_after = []
    # if not after[-1] == LAST_ENTRY:
    #     after.append(LAST_ENTRY)
    ismovable = after[0].ismovable
    ind = 0
    while ismovable:
        movable_after.append(after[ind])
        ismovable = after[ind + 1].ismovable
        ind += 1
    after = after[ind:]
    print("============ after")
    print(after)
    limit_after = PTime(24) if not after else after[0].start

    return (movable_after, after, limit_after)


def add_entry_default(newentry: Entry, before: List[Entry], after: List[Entry], overlaps: List[Entry]) -> List[Entry]:
    # formerly push_aside
    before, movable_before, limit_before = split_before(before)
    movable_after, after, limit_after = split_after(after)
    
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
    return before + movable_before + [newentry] + movable_after + after
    

def share_time(entry1: Entry, entry2: Entry):
    start, end = entry1.spansize(entry2)
    if entry1.overlaps_first(entry2):
        ...
    elif entry1.overlaps_second(entry2):
        ...
    
    return entry1, entry2


# def resolve_1_collision(
#     entry: Entry, 
#     before: List[Entry], 
#     overlaps: List[Entry], 
#     after: List[Entry]
#     ) -> List[Entry]:

#     schedule = []
#     overlap = overlaps[0]
#     if overlap.priority <= 0:
#         pre = overlap.copy(end=entry.start)
#         post = overlap.copy(start=entry.end)
#         return [pre, entry, post]
#     elif entry.precedes(overlap) and (entry.mintime + overlap.mintime < entry.spansize(overlap)):
#         entry, overlap = share_time(entry, overlap)

#     return schedule


# def resolve_2_collisions(entry, before, overlaps, after) -> List[Entry]:
#     schedule = []
#     return schedule


# def resolve_n_collisions(entry, before, overlaps, after) -> List[Entry]:
#     schedule = []
#     return schedule
