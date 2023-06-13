from planager import entities
from planager.operators.plan_patcher import PlanPatcher
from planager.config import config


class Planner:
    def __init__(self, config):
        self.config = config
        self.patch_plan = PlanPatcher(config)

    def __call__(
            
            self, 
            projects: entities.Projects,
            calendar: entities.Calendar,
            plan_patches: entities.PlanPatches
        
        ) -> entities.Plan:
        
        plan = entities.Plan(
            config=self.config, 
            calendar=calendar,
        )
        for project in projects:
            plan.add_tasks_from_project(project)
        
        plan = self.patch_plan(self.config, plan, plan_patches)

        return plan