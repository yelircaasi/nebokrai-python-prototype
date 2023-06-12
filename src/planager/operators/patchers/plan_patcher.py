from planager import entities


class PlanPatcher:
    def __init__(self, config) -> None:
        self.config = config

    def __call__(
            self, 
            plan: entities.Plan, 
            plan_patches: entities.patches.PlanPatch
        ) -> entities.Plan:
        ...
        return plan
