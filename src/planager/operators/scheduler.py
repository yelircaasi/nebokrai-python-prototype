from planager import entities
from planager.operators.schedule_patcher import SchedulePatcher
from planager.config import config


class Scheduler:
    def __init__(self, config):
        ...
        self.patch_schedule = SchedulePatcher(config)

    def __call__(
            
            self, 
            agenda: entities.Agenda,
            routines: entities.Routines,
            adhoc: entities.Adhoc,
            schedule_patch: entities.SchedulePatch
        
        ) -> entities.Schedule:

        #schedule = make_schedule(agenda, routines, adhoc)
        schedule = self.patch_schedule(self.config, schedule, schedule_patch)
        return schedule

