from typing import Optional

from ..entity import (
    Calendar,
    Plan,
    Roadmaps,
    Routines,
    Schedule,
    SchedulePatches,
    Schedules,
    Tasks,
)
from ..util import ConfigType, PDate
from .patcher import SchedulePatcher


class Scheduler:
    def __init__(self, config: Optional[ConfigType] = None):
        ...
        self.patch_schedule = SchedulePatcher(config)

    def __call__(
        self,
        calendar: Calendar,
        plan: Plan,
        roadmaps: Roadmaps,
        routines: Routines,
    ) -> Schedules:
        start_date_new = roadmaps.start_date or (PDate.tomorrow())
        end_date_new: PDate = roadmaps.end_date or max(
            plan.end_date,
            calendar.end_date,
        )
        schedules = Schedules()
        for date in start_date_new.range(end_date_new):
            schedule = Schedule.from_calendar(calendar, date)
            # schedule.add_routines(calendar[date].routine_dict, routines)
            schedule.add_from_plan(plan, roadmaps.tasks)
            # schedule = self.patch_schedule(schedule, schedule_patches[date])
            schedules[date] = schedule
            # print(len(schedules))
        return schedules
