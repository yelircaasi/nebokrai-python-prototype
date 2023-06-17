from typing import List, Optional
from planager import entities
from planager.operators.patchers import SchedulePatcher
from planager.config import ConfigType, config
from planager.utils.datetime_extensions import PDate


class Scheduler:
    def __init__(self, config: Optional[ConfigType] = None):
        ...
        self.patch_schedule = SchedulePatcher(config)

    def __call__(
            
            self, 
            plan: entities.Plan,
            routines: entities.Routines,
            adhoc: entities.AdHoc,
            schedule_patches: entities.SchedulePatches,
            start_date: Optional[PDate] = PDate.today() + 1,
            end_date: Optional[PDate] = None,
        
        ) -> entities.Schedules:

        #schedule = make_schedule(agenda, routines, adhoc)
        end_date = end_date or max(plan.end_date(), adhoc.end_date(), schedule_patches.end_date(),)
        schedules = entities.Schedules()
        for date in start_date.range(end_date):
            schedule = entities.Schedule()
            schedule.add_routines(routines)
            schedule.add_from_plan(plan)
            schedule.add_adhoc(adhoc)
            schedule = self.patch_schedule(self.config, schedule, schedule_patches)
            schedules.add_schedule(schedule)
        return schedules
