from planager.entities.schedule import Schedule
from planager.utils.datetime_extensions import PTime


def check_day_validity(schedule: Schedule) -> bool:
    if len(schedule.schedule) == 1:
        adjacency = True
    else:
        adjacency = all(
            map(
                lambda x: x[0].end == x[1].start,
                zip(schedule.schedule[:-1], schedule.schedule[1:]),
            )
        )
    return (
        adjacency
        and (schedule.schedule[0].start == PTime())
        and (schedule.schedule[-1].end == PTime(24))
    )
