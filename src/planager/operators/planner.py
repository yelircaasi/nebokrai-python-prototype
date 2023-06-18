from itertools import islice
from typing import Any, Dict, List, Optional

from planager import entities
from planager.config import ConfigType
from planager.operators.patchers import PlanPatcher, TaskPatcher
from planager.utils.algorithms.planning import ClusterType, SubplanType
# from planager.config import config
from planager.utils.datetime_extensions import PDate
from planager.utils.misc import expand_task_segments


class Planner:
    def __init__(self, config: Optional[ConfigType] = None):
        self.config = config
        self.patch_plan = PlanPatcher(config)
        self.patch_tasks = TaskPatcher(config)

    def __call__(
        self,
        projects: entities.Projects,
        calendar: entities.Calendar,
        task_patches: Optional[entities.TaskPatches] = None,
        plan_patches: Optional[entities.PlanPatches] = None,
    ) -> entities.Plan:
        plan = entities.Plan(
            config=self.config,
            calendar=calendar,
        )

        projects.patch_tasks(self.patch_tasks)
        projects.order_by_dependency()

        for project in projects:
            project_id = (project.parent, project.id)
            subplan: SubplanType = self.get_subplan_from_tasks(
                project.tasks, project, calendar
            )
            plan.add_subplan(subplan, project.tasks, project_id)

        plan = self.patch_plan(plan, plan_patches)

        return plan

    def get_subplan_from_tasks(
        self,
        tasks: entities.Tasks,
        project: entities.Project,
        calendar: entities.Calendar,
    ) -> SubplanType:
        start: Optional[PDate] = project.start
        end: Optional[PDate] = project.end
        cluster_size: int = project.cluster_size
        interval: int = project.interval

        clusters: ClusterType = self.cluster_task_ids(tasks.ids(), cluster_size)
        subplan: SubplanType = self.allocate_in_time(clusters, tasks, project)

        return subplan

    @staticmethod
    def cluster_task_ids(task_ids: List[int], cluster_size: int) -> ClusterType:
        n = cluster_size
        length = len(task_ids)
        quotient, remainder = divmod(length, n)
        num_clusters = quotient + int(bool(remainder))
        return [task_ids[n * i : n * (i + 1)] for i in range(num_clusters)]

    @staticmethod
    def allocate_in_time(
        clusters: ClusterType,
        tasks: entities.Tasks,
        project: entities.Project,
    ) -> SubplanType:
        nclusters = len(clusters)
        if len(clusters) == 1:
            return {project.start: clusters[0]}
        elif project.end:
            ndays = int(project.end) - int(project.start)
            gap = int((ndays - nclusters) / (nclusters - 1))
        elif project.interval:
            gap = project.interval - 1
        else:
            raise ValueError(
                "Invalid parameter configuration. "
                "For `Project` class, two of `start`, `end`, and `interval` must be defined."
            )

        subplan = {
            project.start + (i + i * gap): cluster for i, cluster in enumerate(clusters)
        }
        return subplan
