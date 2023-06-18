from typing import Optional

from planager import entities, operators
from planager.config import ConfigType


class PlanPatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        pass

    def __call__(
        self, plan: entities.Plan, plan_patches: entities.PlanPatch
    ) -> entities.Plan:
        ...
        return plan
