from typing import Optional

from planager import entities, operators
from planager.config import ConfigType


class PlanPatcher:
    def __init__(self, config: Optional[ConfigType] = None) -> None:
        self._config = config

    def __call__(
        self, plan: entities.Plan, plan_patch: Optional[entities.PlanPatch]
    ) -> entities.Plan:
        if not plan_patch:
            return plan
        return plan  # TODO
