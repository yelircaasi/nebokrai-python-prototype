import re
from typing import Iterator, Optional, Union

from nebokrai.util import color
from nebokrai.util.serde.custom_dict_types import ProjectDictRaw

from ...configuration import config
from ...util import NKDate, ProjectID, RoadmapID, TaskID, tabularize
from ..container.tasks import Tasks
from .task import Task


class Project:
    """
    Container for tasks, in addition to project info.
    """

    def __init__(
        self,
        name: str,
        project_id: ProjectID,
        tasks: Tasks,
        priority: Optional[float],
        start: Optional[NKDate],
        end: Optional[NKDate],
        interval: Optional[int],
        cluster_size: Optional[int],
        duration: Optional[int],
        description: str = "",
        notes: str = "",
        dependencies: Optional[set[Union[RoadmapID, ProjectID, TaskID]]] = None,
        categories: Optional[set[str]] = None,
    ) -> None:
        self.name = name
        self.project_id = project_id
        self._tasks = tasks
        self.priority = priority or config.default_priority
        self.start = start or NKDate.tomorrow() + config.default_project_dates_missing_offset + (
            hash(self.name) % config.default_project_dates_missing_hashmod
        )
        self.end = end if end else None
        self.interval = interval or config.default_interval
        self.cluster_size = cluster_size or config.default_cluster_size
        self.duration = duration or config.default_duration
        self.description = description
        self.notes = notes
        self.dependencies = dependencies or set()
        self.categories = (categories or set()).union(config.default_categories)

        if self.end:
            assert (
                self.end > self.start
            ), f"{self.name}: End date ({self.end}) must be greater than start date ({self.start})."

    @classmethod
    def deserialize(cls, project_id: ProjectID, project_dict: ProjectDictRaw) -> "Project":
        """
        Instantiates from config, json-derived dic, and project information.
        """
        start_str = project_dict["start"] if "start" in project_dict else ""
        end_str = project_dict["end"] if "end" in project_dict else ""

        priority = int(project_dict.get("priority") or config.default_priority)
        duration = int(project_dict.get("duration") or config.default_duration)
        categories = set(filter(bool, re.split(", ?", project_dict.get("categories", "")))).union(
            config.default_categories
        )
        tasks = Tasks.deserialize(
            project_dict["tasks"],
            project_id,
            project_dict["name"],
            project_priority=priority,
            project_duration=duration,
            project_categories=categories,
        )

        return cls(
            project_dict["name"],
            project_id,
            tasks=tasks,
            priority=priority,
            start=NKDate.from_string(start_str) if start_str else None,
            end=NKDate.from_string(end_str) if end_str else None,
            interval=int(project_dict.get("interval") or config.default_interval),
            cluster_size=int(project_dict.get("cluster_size") or config.default_cluster_size),
            duration=duration,
            description=project_dict.get("description", ""),
            notes=project_dict.get("notes", ""),
            categories=categories,
        )

    def copy(self) -> "Project":
        copy = Project(
            self.name,
            self.project_id,
            self.tasks,
            self.priority,
            self.start,
            self.end,
            self.interval,
            self.cluster_size,
            self.duration,
        )
        copy.__dict__.update(self.__dict__)
        return copy

    @property
    def clusters(self) -> list[list[Task]]:
        """
        Divides a list of tasks into k clusters of size `cluster_size`.
        """
        # def split_for_date_constraints(cluster: Iterable[Task]) -> list[list[Task]]:
        #     tasks = sorted(cluster, key=lambda t: (t.earliest_date, t.latest_date))
        #     first = [tasks.pop(0)]
        #     _earliest = tasks[0].earliest_date
        #     _latest = tasks[0].latest_date
        #     while tasks and tasks[0]
        # tasks = sorted(sorted(list(self._tasks), key=lambda t: t.latest_date), key=lambda t: t.latest_date
        tasks = list(self._tasks)
        length = len(tasks)
        quotient, remainder = divmod(length, self.cluster_size)
        num_clusters = quotient + int(bool(remainder))
        prelim: list[list[Task]] = [
            tasks[self.cluster_size * i : self.cluster_size * (i + 1)] for i in range(num_clusters)
        ]
        # ret = []
        # for pre_cluster in prelim:
        #     earliest, latest = pre_cluster.earliest_data, pre_cluster.latest_date
        #     if earliest > latest:
        #         for sub_cluster in split_for_date_constraints(pre_cluster):
        #             ret.append(sub_cluster)
        #     else:
        #         ret.append(pre_cluster)
        return prelim

    def plan_tasks_old(self, tasks: Tasks) -> dict[NKDate, Tasks]:
        """ """
        clusters = self.clusters
        if not clusters:
            return {}
        nclusters = len(clusters)

        if len(clusters) == 1:
            return {self.start: Tasks(clusters[0])}
        # if self.end:
        #     while nclusters > self.start.daysto(self.end):
        #         time_info = f"{self.start} - {self.end}"
        #         cluster_info = "{nclusters} clusters, cluster size {self.cluster_size}"
        #         print(f"Not enough time allocated to '{self.name}': {time_info}, {cluster_info}.")
        #         self.cluster_size += 1
        #         clusters = self.clusters
        #         nclusters = len(clusters)
        #
        #     ndays = int(self.get_end()) - int(self.start)
        #     factor = ndays / nclusters
        #     offsets = [int(round(i * factor)) for i in range(nclusters)]
        # elif self.interval:
        #     gap = self.interval
        #     offsets = [i * gap for i in range(nclusters)]
        else:
            raise ValueError(
                f"Invalid parameter configuration for {self.name}. "
                "For `Project` class, two of `start`, `end`, and `interval` must be defined."
            )
        protoplan: dict[NKDate, Tasks] = {
            self.start + offset: Tasks(cluster) for cluster, offset in zip(clusters, offsets)
        }

        protoplan: dict[NKDate, Tasks] = {}
        for cluster in clusters:
            earliest = cluster.earliest_date
            latest = cluster.latest_date
            if earliest:
                if self.end and not (earliest <= self.end):
                    raise ValueError(
                        f"Project {str(self.project_id)} contains a task whose earliest permissible"
                        f"date ({str(earliest)}) is after the end of the project ("
                        f"{str(self.end)})."
                    )
            if latest:
                if not (latest >= self.start):
                    raise ValueError(
                        f"Project {str(self.project_id)} contains a task whose latest permissible"
                        f"date ({str(latest)}) is before the start of the project ("
                        f"{str(self.start)})."
                    )

        return protoplan

    def make_protoplan_end_fixed(
        self, clusters: list[list[Task]], start: NKDate, end: NKDate
    ) -> list[tuple[NKDate, Tasks]]:
        nclusters = len(clusters)
        while nclusters > start.daysto(end):
            time_info = f"{self.start} - {self.end}"
            cluster_info = f"{nclusters} clusters, cluster size {self.cluster_size}"
            print(
                f"Not enough time allocated to '{str(self.project_id)}': "
                f"{time_info}, {cluster_info}. Incrementing cluster size."
            )
            self.cluster_size += 1
            # clusters = self.clusters
            nclusters = len(clusters)

        ndays = int(end) - int(start)
        factor = ndays / nclusters
        offsets = [int(round(i * factor)) for i in range(nclusters)]
        protoplan: list[tuple[NKDate, Tasks]] = [
            (start + offset, Tasks(cluster)) for cluster, offset in zip(clusters, offsets)
        ]
        return protoplan

    def plan_tasks_end_fixed(
        self, clusters: list[list[Task]], start: NKDate, end: NKDate
    ) -> dict[NKDate, Tasks]:
        """ """
        protoplan = self.make_protoplan_end_fixed(clusters, start, end)
        final_plan: dict[NKDate, Tasks] = {}
        protoplan_list = list(protoplan.items())
        while protoplan_list:
            protodate, cluster = protoplan_list.pop(0)
            earliest = cluster.earliest_date
            latest = cluster.latest_date
            if latest and latest < protodate:
                if (not final_plan) or (max(final_plan) < latest):
                    return final_plan | self.plan_tasks_end_fixed(
                        [clust for d, clust in protoplan_list], latest, end
                    )
                self.check_latest(latest, protodate)
                # raise ValueError(
                #     f"Impossible to create subplan from project {str(self.project_id)}"
                #     " due to latest date of at least one task (interval-based planning)."
                # )
            if earliest and earliest > protodate:
                return final_plan | self.plan_tasks_end_fixed(
                    [clust for d, clust in protoplan_list], earliest, end
                )
            final_plan.update({protodate: cluster})
        return final_plan

    def make_protoplan_end_flex(
        self,
        clusters: list[list[Task]],
        start: NKDate,
        interval: int,
    ) -> list[tuple[NKDate, Tasks]]:
        nclusters = len(clusters)
        if self.interval:
            offsets = [i * interval for i in range(nclusters)]
        else:
            raise ValueError(f"Project {str(self.project_id)} has no end and no interval defined.")
        protoplan: list[tuple[NKDate, Tasks]] = [
            (start + offset, Tasks(cluster)) for cluster, offset in zip(clusters, offsets)
        ]
        return protoplan

    def plan_tasks_end_flex(
        self, clusters: list[list[Task]], start: NKDate, interval: int
    ) -> dict[NKDate, Tasks]:
        """ """
        protoplan_list = self.make_protoplan_end_flex(clusters, start, interval)
        final_plan: dict[NKDate, Tasks] = {}
        while protoplan_list:
            protodate, cluster = protoplan_list.pop(0)
            earliest = cluster.earliest_date
            latest = cluster.latest_date
            self.check_latest(latest, protodate)
            if earliest and earliest > protodate:
                return final_plan | self.plan_tasks_end_flex(
                    [clust for d, clust in protoplan_list], earliest, interval
                )
        return final_plan

    def check_earliest(self, earliest: NKDate, other: NKDate) -> None:
        if earliest and earliest > other:
            raise ValueError(
                f"Impossible to create subplan from project {str(self.project_id)}"
                " due to earliest date of at least one task (interval-based planning)."
            )

    def check_latest(self, latest: NKDate, other: NKDate) -> None:
        if latest and latest < other:
            raise ValueError(
                f"Impossible to create subplan from project {str(self.project_id)}"
                " due to latest date of at least one task (interval-based planning)."
            )

    @property
    def subplan(self) -> dict[NKDate, Tasks]:
        """
        Spaces out a list of clusters between a start and end date, given some interval.
        """
        # subplan = self.plan_tasks(self._tasks)
        clusters, start = self.clusters, self.start
        match (len(clusters)):
            case 0:
                return {}
            case 1:
                cluster = clusters[0]
                earliest, latest = cluster.earliest_date, cluster.latest_date

                return {start: Tasks(cluster)}
            case _:
                return (
                    self.plan_tasks_end_fixed(clusters, start, self.end)
                    if self.end
                    else self.plan_tasks_end_flex(clusters, start, self.interval)
                )

    def get_end(self) -> NKDate:
        return self.end or (self.start + 365)

    @property
    def tasks(self) -> Tasks:
        return self._tasks

    @property
    def task_ids(self) -> list[TaskID]:
        return self._tasks.task_ids

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Task instance.
        """
        width = config.repr_width
        top = (
            "\n"
            + tabularize(
                f"Project: {self.name} (ID {'-'.join(self.project_id)})", width, thick=True
            )
            + "\n"
        )
        empty = tabularize("", width, thick=True)
        tasks = map(
            lambda x: tabularize(
                (
                    f"{x.status_symbol} {'-'.join(x.task_id): <14} │ "
                    f"{x.name: <48}{x.duration:>3}m {x.priority:>3}"
                ),
                width,
                thick=True,
            ),
            self._tasks,
        )
        return (
            "\n"
            + "┏"
            + (width - 2) * "━"
            + "┓\n"
            + empty
            + top
            + empty
            + "\n┠"
            + (width - 2) * "─"
            + "┨\n"
            + empty
            + "\n".join(tasks)
            + "\n"
            + empty
            + "\n┗"
            + (width - 2) * "━"
            + "┛"
        )

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def __getitem__(self, __key: TaskID) -> Task:
        if isinstance(__key, TaskID):
            return self._tasks[__key]
        raise KeyError(f"Invalid key for Project object: {__key}")

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def repr1(self) -> str:
        def stringify(task: Task) -> str:
            return f"{color.magenta(task.name[:20])} ({color.cyan(str(task.task_id))})"

        tasks_string = " | ".join(map(stringify, self._tasks))
        return f"{color.magenta(self.name)}: start {color.green(self.start)}: {tasks_string}"
