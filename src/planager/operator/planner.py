from itertools import islice
from typing import Any, Dict, List, Optional, Tuple, Union

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

SubplanType = Dict[PDate, List[Tuple[str, str, str]]]


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
            subplan: SubplanType = self.get_subplan_from_project(
                project
            )  # TODO: make subplan respect precedence
            plan.add_subplan(subplan, project._tasks)
        # plan.reorder_by_precedence()

        plan = self.patch_plan(plan, plan_patches)

        # ----------------------------------------------------------------------------------------------------------------------------------
        # enforce temporal precedence constraints

        self.enforce_precedence_constraints(plan, projects)
        # ----------------------------------------------------------------------------------------------------------------------------------

        return plan

    def get_subplan_from_project(  # move to Plan?
        self,
        project: Project,
    ) -> SubplanType:
        """
        A subplan is a dictionary assigning tasks to days. It is an intermediate step created to be merged into the
          instance of `Plan`.
        """
        # ----------------------------------------------------------------------------------------------------------------------------------
        # make subplan respect temporal precedence constraints
        # for task in self._tasks:
        #     for dep_id in task.dependencies:
        #         if len(dep_id) == 2:
        #             if task.tmpdate <
        #         elif len(dep_id) == 3:

        # for dep_id in project.dependencies:
        #     newdate = (self.get_end_from_id(dep_id, projects) or PDate.today()) + 1
        #     project.rigid_shift_start(newdate)
        # ----------------------------------------------------------------------------------------------------------------------------------

        clusters: ClusterType = self.cluster_task_ids(
            project.task_ids, project.cluster_size
        )
        subplan: SubplanType = self.allocate_in_time(clusters, project)

        return subplan

    @staticmethod
    def cluster_task_ids(  # move to Plan?
        task_ids: List[Tuple[str, str, str]], cluster_size: int
    ) -> ClusterType:
        """
        Divides a list of tasks into k clusters of size `cluster_size`.
        """
        n = cluster_size
        length = len(task_ids)
        quotient, remainder = divmod(length, n)
        num_clusters = quotient + int(bool(remainder))
        ret: ClusterType = [task_ids[n * i : n * (i + 1)] for i in range(num_clusters)]
        return ret

    @staticmethod
    def allocate_in_time(  # move to Plan?
        clusters: ClusterType,
        project: Project,
        # earliest_dates: Dict[Tuple[str, str, str], PDate]
    ) -> SubplanType:
        """
        Spaces out a list of clusters between a start and end date, given some interval.
        """
        nclusters = len(clusters)
        if len(clusters) == 1:
            return {project.get_start(): clusters[0]}
        elif project.end:
            ndays = int(project.get_end()) - int(project.get_start())
            gap = int((ndays - nclusters) / (nclusters - 1))
        elif project.interval:
            gap = project.interval - 1
        else:
            print(project.name)
            raise ValueError(
                "Invalid parameter configuration. "
                "For `Project` class, two of `start`, `end`, and `interval` must be defined."
            )

        start: PDate = project.start or PDate.tomorrow() + (hash(project.name) % 7)
        subplan: SubplanType = {
            start + (i + i * gap): cluster for i, cluster in enumerate(clusters)
        }

        return subplan

    # def get_end_from_id(entity_id: Union[Tuple[str, str], Tuple[str, str, str]], projects: Projects) -> Optional[PDate]:
    #     if len(entity_id) == 2:
    #         return projects[entity_id].end
    #     elif len(entity_id) == 3:
    #         return projects[entity_id].tmpdate
    #     else:
    #         return None

    @staticmethod
    def enforce_precedence_constraints(plan: Plan, projects: Projects) -> None:
        inverse_plan = {}
        for date, ids in plan._plan.items():
            for task_id in ids:
                inverse_plan.update({task_id: date})

        def get_date(_id: Union[Tuple[str, str, str], Tuple[str, str]]) -> PDate:
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
