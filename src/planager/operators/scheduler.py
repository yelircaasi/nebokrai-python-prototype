from typing import List, Optional

from ..config import ConfigType
from ..entity.base.adhoc import AdHoc
from ..entity.base.plan import Plan
from ..entity.base.schedule import Schedule
from ..entity.container.routines import Routines
from ..entity.container.schedules import Schedules
from ..entity.container.tasks import Tasks
from ..entity.patch.schedule_patch import SchedulePatches
from ..operators.patcher import SchedulePatcher
from ..util.pdatetime import PDate


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
