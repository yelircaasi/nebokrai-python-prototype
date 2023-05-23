from planager.entities.day import DefaultDay
from planager.utils.datetime_extensions import PlTime


def check_day_validity(day: DefaultDay) -> bool:
    if len(day.schedule) == 1:
        adjacency = True
    else:
        adjacency = all(map(lambda x: x[0].end == x[1].start, zip(day.schedule[:-1], day.schedule[1:])))
    return adjacency and (day.schedule[0].start == PlTime()) and (day.schedule[-1].end == PlTime(23, 59))
