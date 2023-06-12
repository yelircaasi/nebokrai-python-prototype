from planager import entities
from planager.operators.schedule_patcher import SchedulePatcher
from planager.config import config


class Adjuster:
    def __init__(self, config):
        ...
        self.patch_schedule = SchedulePatcher(config)

    def __call__(
        
            self, 
            schedule: entities.Schedule, 
            schedule_patch: entities.SchedulePatch
        
        ) -> entities.Schedule:
        
        schedule = self.patch_schedule(self.config, schedule, schedule_patch)
        return schedule

