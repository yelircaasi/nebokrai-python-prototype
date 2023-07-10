from ..entity.base.schedule import Schedule
from ..util.pdatetime import PTime


def schedule_is_valid(schedule: Schedule) -> bool:
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
