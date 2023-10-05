from itertools import islice
from typing import Any, Optional, Union

from ..entity import (
    Calendar,
    Plan,
    PlanPatch,
    PlanPatches,
    Project,
    Projects,
    Roadmaps,
    TaskPatches,
    Task,
    Tasks,
)
from ..util import ClusterType, ConfigType, PDate, expand_task_segments
from .patcher import PlanPatcher, TaskPatcher

SubplanType = dict[PDate, list[tuple[str, str, str]]]


class Planner:
    """
    Class that handles creation of the one instance of `Plan`.

    Not yet implemented:
    * functionality for breaking up and reallocating clusters. -> Happens automatically?
    """

    def __init__(self, config: Optional[ConfigType] = None):
        self.config = config
        self.patch_plan = PlanPatcher(config)
        self.patch_tasks = TaskPatcher(config)

    def __call__(
        self,
        roadmaps: Roadmaps,
        calendar: Calendar,
        task_patches: Optional[TaskPatches] = None,
        plan_patches: Optional[PlanPatches] = None,
    ) -> Plan:
        """
        Create the plan (the one instance of the `Plan` class) from the roadmaps and calendar, as well as task_patches
          and plan_patches. Designed to be:
          * declarative (user says what rather than how)
          * pure (no side effects)
          * deterministic (same input -> same output)
          This makes the automated planning process predictable and transparent.
        """
        plan = Plan(
            config=self.config,
            calendar=calendar,
        )
        projects = roadmaps.projects
        projects.patch_tasks(task_patches)
        # projects.order_by_dependency()

        for project in projects:
            plan.add_subplan(project.subplan, project._tasks)
        # plan.reorder_by_precedence()

        # plan = self.patch_plan(plan, plan_patches)

        # ----------------------------------------------------------------------------------------------------------------------------------
        # enforce temporal precedence constraints

        self.enforce_precedence_constraints(plan, projects)
        # ----------------------------------------------------------------------------------------------------------------------------------

        return plan

    @staticmethod
    def enforce_precedence_constraints(plan: Plan, projects: Projects) -> None:
        inverse_plan = {}
        for date, ids in plan._plan.items():
            for task_id in ids:
                inverse_plan.update({task_id: date})

        def get_date(_id: Union[tuple[str, str, str], tuple[str, str]]) -> PDate:
            if len(_id) == 2:
                return max(map(lambda t: inverse_plan[t], (projects[_id])))
            elif len(_id) == 3:
                return inverse_plan[projects[_id]]
            else:
                raise ValueError("ID must have 2 or 3 elements.")

        for task in projects._tasks:
            if task.dependencies:
                plan_date = inverse_plan[task_id]
                limiting_dependency = max(task.dependencies, key=get_date)
                earliest_date = inverse_plan[limiting_dependency] + 1
                if plan_date < earliest_date:
                    raise ValueError(
                        f"Task {'<>'.join(task_id)} assigned to {plan_date}, but earliest permissible date is {earliest_date}. Please adjust the declaration and run the derivation again. \n  Limiting dependency: {'<>'.join(limiting_dependency)}."
                    )
