from typing import List, Tuple 

from planager.entities.entry import Empty, Entry, FIRST_ENTRY, LAST_ENTRY
from planager.utils.datetime_extensions import PTime
from planager.utils.misc import round5


def get_overlaps(entry: Entry, schedule: List[Entry], include_empty: bool = True) -> List[Entry]:
    if include_empty:
        return list(filter(entry.overlaps, schedule))
    return list(filter(entry.overlaps, filter(lambda ent: ent.priority >= 0, schedule)))


def slot_is_empty(overlaps: List[Entry]) -> bool:
    if len(overlaps) > 1:
        return False
    incumbent = overlaps[0]
    is_empty = isinstance(incumbent, Empty)
    return is_empty


def split_schedule_old(entry: Entry, schedule: List[Entry]) -> Tuple[List[Entry], List[Entry], List[Entry]]:
    before = list(filter(entry.after, schedule))
    after = list(filter(entry.before, schedule))
    overlaps = list(filter(entry.overlaps, filter(lambda ent: ent.priority >= 0, schedule)))
    return before, after, overlaps


def split_schedule(entry: Entry, schedule: List[Entry]) -> Tuple[List[Entry], List[Entry]]:
    _schedule = [x.copy() for x in schedule]
    before = list(filter(entry.after, _schedule))
    after = list(filter(entry.before, _schedule))
    return before, after


def compress(entries: List[Entry], start: PTime, end: PTime) -> List[Entry]:
    for e in entries:
        print(e)
    print(f"start: {start}")
    print(f"end:   {end}")
    entries = list(filter(lambda x: x.priority >= 0, entries))
    total = start.timeto(end)
    scale = total / sum(map(Entry.duration, entries))

    def getnewlength(ent: Entry) -> int:
        newlength = round5(scale * ent.duration())
        newlength = min(ent.maxtime, newlength)
        newlength = max(ent.mintime, newlength)
        return newlength
    
    newentries = []
    newlengths = [getnewlength(x) for x in entries]
    #newlengths[0] += (total - sum(newlengths))
    
    entries_tail = []
    newentries_tail = []
    newlengths_tail = []
    align_end = entries[-1].align_end
    while align_end:
        entries_tail.insert(0, entries.pop())
        newlengths_tail.insert(0, newlengths.pop())
        align_end = entries[-1].align_end

    tracker = start.copy()
    for entry, duration in zip(entries, newlengths):
        print(tracker)
        entry.start = tracker.copy()
        tracker += duration 
        entry.end = tracker.copy()
        newentries.append(entry)

    if newlengths_tail:
        tracker = end.copy()
        for entry, duration in zip(entries_tail[::-1], newlengths_tail[::-1]):
            entry.end = tracker.copy()
            tracker -= duration 
            entry.start = tracker.copy()
            newentries_tail.insert(0, entry)

        if newentries[-1].end != newentries_tail[0].start:
            empty_start = newentries[-1].end
            empty_end = newentries_tail[0].start
            newentries.append(Empty(start=empty_start, end=empty_end))
    else:
        empty_start = newentries[-1].end
        newentries.append(Empty(start=empty_start, end=end))

    return newentries + newentries_tail


def compress_weighted(entries: List[Entry], start: PTime, end: PTime, weights) -> List[Entry]:
    ...


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
    #print(before)
    movable_before = []
    # if not before[0] == FIRST_ENTRY:
    #     before.insert(0, FIRST_ENTRY)
    ismovable = before[-1].ismovable
    ind = -1
    while ismovable:
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #print(ind)
        #print(before[ind])
        movable_before.insert(0, before[ind])
        ismovable = before[ind - 1].ismovable
        ind -= 1
    before = before[:ind + 1]
    #print("============ before")
    #print(before)
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
    #print("============ after")
    #print(after)
    limit_after = PTime(24) if not after else after[0].start

    return (movable_after, after, limit_after)


def add_over_empty(entry: Entry, empty: Empty) -> List[Entry]:
    if entry.surrounded(empty):
        return [
            Empty(start=empty.start, end=entry.start),
            entry,
            Empty(start=entry.end, end=empty.end)
        ]
    elif entry.shares_start_shorter():
        return [
            entry,
            Empty(start=entry.end, end=empty.end)
        ]
    elif entry.shares_end_shorter():
        return [
            Empty(start=empty.start, end=entry.start),
            entry
        ]
    else:
        raise ValueError("Cannot add over empty entry which is shorter!")
        return [empty]


def add_movable(entry: Entry, schedule: List[Entry]):
    before, after = split_schedule(entry, schedule)
    
    before, movable_before, limit_before = split_before(before)
    movable_after, after, limit_after = split_after(after)
    inbetween = movable_before + [entry] + movable_after
    compressed = compress(inbetween, limit_before, limit_after)
    if compressed:
        print("Entry successfully added.")
        return before + compressed + after
    else:
        print("Entry could not be added!")
        return schedule





def add_immovable(entry: Entry, schedule: List[Entry]):
    before, after = split_schedule(entry, schedule)
    
    before, movable_before, limit_before = split_before(before)
    movable_after, after, limit_after = split_after(after)

    fit_before = entries_fit(movable_before, limit_before, entry.start)
    fit_after = entries_fit(movable_after, entry.end, limit_after)
    if not (fit_before and fit_after):
        print("Not enough room to add task.")
        return 

    spare_before = entries_fit_spare(movable_before, limit_before, entry.start)
    if spare_before:
        movable_before = adjust_backward(movable_before, limit_before, entry.start)
    else:
        movable_before = compress(movable_before, limit_before, entry.start)
    spare_after = entries_fit_spare(movable_after, entry.end, limit_after)
    if movable_after:
        movable_after = adjust_forward(movable_after, entry.end, limit_after)
    else:
        movable_after = compress(movable_after, entry.end, limit_after)
    
    # NEED TO CONSOLIDATE HERE
    return before + movable_before + [entry] + movable_after + after


def add_entry_default(entry: Entry, schedule: List[Entry]) -> List[Entry]:
    # formerly push_aside
    overlaps = get_overlaps(entry, schedule)
    if slot_is_empty(overlaps):
        ind = schedule.index(overlaps[0])
        del schedule[ind]
        new_entries = add_over_empty(entry, overlaps[0])
        while new_entries:
            schedule.insert(ind, new_entries.pop())
        return schedule

    func = add_movable if entry.ismovable else add_immovable
    return func(entry, schedule)
    
    #WITH OVERLAPS
    # if all(map(lambda x: x.ismovable, overlaps)):
    #     limit_overlap_before = entry.end
    #     limit_overlap_after = entry.start
    # else:
    #     limit_overlap_before = min(map(lambda x: x.ismovable, overlaps)).start
    #     limit_overlap_after = min(map(lambda x: x.ismovable, overlaps)).end
    

