from typing import List, Optional

from planager.config import ConfigType, config
from planager.entities.adhoc import AdHoc
from planager.entities.plan import Plan
from planager.entities.routine import Routines
from planager.entities.schedule import Schedule, SchedulePatches, Schedules
from planager.entities.task import Tasks
from planager.operators.patchers import SchedulePatcher
from planager.utils.datetime_extensions import PDate


class Scheduler:
    def __init__(self, config: Optional[ConfigType] = None):
        ...
        self.patch_schedule = SchedulePatcher(config)

    def __call__(
        self,
        plan: Plan,
        tasks: Tasks,
        routines: Routines,
        adhoc: AdHoc,
        schedule_patches: SchedulePatches,
        start_date: Optional[PDate] = PDate.today() + 1,
        end_date: Optional[PDate] = None,
    ) -> Schedules:
        # schedule = make_schedule(agenda, routines, adhoc)
        start_date_new = start_date or (PDate.tomorrow())
        end_date_new: PDate = end_date or max(
            plan.end_date,
            adhoc.end_date,
            schedule_patches.end_date,
        )
        schedules = Schedules()
        for date in start_date_new.range(end_date_new):
            schedule = Schedule(date.year, date.month, date.day)
            schedule.add_routines(routines)
            # schedule.add_from_plan(plan, tasks)
            # schedule.add_adhoc(adhoc)
            # schedule = self.patch_schedule(schedule, schedule_patches[date])
            schedules[date] = schedule
            print(len(schedules))
        return schedules
