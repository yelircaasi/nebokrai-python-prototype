import re
from typing import Iterator, Optional, Union

from planager.util.serde.custom_dict_types import ProjectDictRaw

from ...configuration import config
from ...util import PDate, ProjectID, RoadmapID, TaskID, tabularize
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
        start: Optional[PDate],
        end: Optional[PDate],
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
        self.start = start or PDate.tomorrow() + config.default_project_dates_missing_offset + (
            hash(self.name) % config.default_project_dates_missing_hashmod
        )
        self.end = PDate.ensure_is_pdate(end) if end else None
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

        return cls(
            project_dict["name"],
            project_id,
            tasks=Tasks.deserialize(
                project_dict["tasks"],
                project_id,
                project_dict["name"],
                project_priority=priority,
                project_duration=duration,
                project_categories=categories,
            ),
            priority=priority,
            start=PDate.ensure_is_pdate(start_str) if start_str else None,
            end=PDate.ensure_is_pdate(end_str) if end_str else None,
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
        tasks = list(self._tasks)
        length = len(tasks)
        quotient, remainder = divmod(length, self.cluster_size)
        num_clusters = quotient + int(bool(remainder))
        ret: list[list[Task]] = [
            tasks[self.cluster_size * i : self.cluster_size * (i + 1)] for i in range(num_clusters)
        ]
        return ret

    @property
    def subplan(self) -> dict[PDate, Tasks]:
        """
        Spaces out a list of clusters between a start and end date, given some interval.
        """
        clusters = self.clusters
        if not clusters:
            return {}
        nclusters = len(clusters)

        if self.end:
            while nclusters > self.start.daysto(self.end):
                time_info = f"{self.start} - {self.end}"
                cluster_info = "{nclusters} clusters, cluster size {self.cluster_size}"
                print(f"Not enough time allocated to '{self.name}': {time_info}, {cluster_info}.")
                self.cluster_size += 1
                clusters = self.clusters
                nclusters = len(clusters)

        if len(clusters) == 1:
            return {self.start: Tasks(clusters[0])}
        if self.end:
            ndays = int(self.get_end()) - int(self.start)
            factor = ndays / nclusters
            ints = [int(round(i * factor)) for i in range(nclusters)]
        elif self.interval:
            gap = self.interval
            ints = [i * gap for i in range(nclusters)]
        else:
            raise ValueError(
                f"Invalid parameter configuration for {self.name}. "
                "For `Project` class, two of `start`, `end`, and `interval` must be defined."
            )

        subplan: dict[PDate, Tasks] = {
            self.start + ints[i]: Tasks(cluster) for i, cluster in enumerate(clusters)
        }

        return subplan

    def get_end(self) -> PDate:
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
