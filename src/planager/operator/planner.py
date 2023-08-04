from itertools import islice
from typing import Any, Dict, List, Optional, Tuple, Union

from ..entity import (
    Calendar,
    Plan,
    PlanPatch,
    PlanPatches,
    Project,
    Roadmaps,
    TaskPatches,
    Tasks,
)
from ..util import ClusterType, ConfigType, PDate, expand_task_segments
from .patcher import PlanPatcher, TaskPatcher

SubplanType = Dict[PDate, List[Tuple[str, str, str]]]


class Planner:
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
        plan = Plan(
            config=self.config,
            calendar=calendar,
        )
        projects = roadmaps.get_projects()
        projects.patch_tasks(task_patches)
        projects.order_by_dependency()

        for project in projects:
            subplan: SubplanType = self.get_subplan_from_project(project, calendar)
            plan.add_subplan(subplan, project._tasks)
        plan.reorder_by_precedence()

        plan = self.patch_plan(plan, plan_patches)

        return plan

    def get_subplan_from_project( # move to Plan?
        self,
        project: Project,
        calendar: Calendar,
    ) -> SubplanType:
        """
        A subplan is a dictionary assigning tasks to days. It is an intermediate step created to be merged with
        """

        clusters: ClusterType = self.cluster_task_ids(
            project.task_ids, project.cluster_size
        )
        subplan: SubplanType = self.allocate_in_time(clusters, project)

        return subplan

    @staticmethod
    def cluster_task_ids( # move to Plan?
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
    def allocate_in_time( # move to Plan?
        clusters: ClusterType,
        project: Project,
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
