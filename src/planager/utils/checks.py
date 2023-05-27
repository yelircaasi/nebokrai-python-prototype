from planager.entities.day import DayAgenda
from planager.utils.datetime_extensions import PTime


def check_day_validity(day: DayAgenda) -> bool:
    if len(day.schedule) == 1:
        adjacency = True
    else:
        adjacency = all(map(lambda x: x[0].end == x[1].start, zip(day.schedule[:-1], day.schedule[1:])))
    return adjacency and (day.schedule[0].start == PTime()) and (day.schedule[-1].end == PTime(24))
