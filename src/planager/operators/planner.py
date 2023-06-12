from planager import entities
from planager.operators.plan_patcher import PlanPatcher
from planager.config import config


class Adjuster:
    def __init__(self, config):
        ...
        self.patch_plan = PlanPatcher(config)

    def __call__(
            
            self, 
            plan: entities.Schedule, 
            plan_patch: entities.PlanPatch
        
        ) -> entities.Plan:
        
        plan = self.patch_plan(self.config, plan, plan_patch)
        return plan