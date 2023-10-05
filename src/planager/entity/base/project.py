import re
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional, Union

from ...util import (
    ClusterType,
    Norg,
    PDate,
    Regexes,
    SubplanType,
    expand_task_segments,
    tabularize,
)
from ..container.tasks import Tasks
from .task import Task


class Project:
    def __init__(
        self,
        name: str,
        project_id: tuple[str, str],
        tasks: Union[list[str], str, Tasks] = [],
        priority: int = 10,
        start: Optional[PDate] = None,
        end: Optional[PDate] = None,
        interval: int = 7,
        cluster_size: int = 1,
        duration: int = 30,
        description: str = "",
        notes: str = "",
        dependencies: set[
            tuple[str, ...]
        ] = set(),  # not maximally strong, but avoids a mypy headache
        categories: set[str] = set(),
    ) -> None:
        self.name = Norg.norg_item_head(name).name
        self.project_id = project_id
        self._tasks: Tasks = (
            Tasks.from_string_iterable(
                expand_task_segments(tasks) if isinstance(tasks, str) else tasks,
                project_id=project_id,
                project_name=name,
            )
            if not isinstance(tasks, Tasks)
            else tasks
        )
        self.priority = priority
        self.start = start or PDate.tomorrow() + 730 + (hash(self.name) % 60)
        self.end = (
            PDate.ensure_is_pdate(end) if end else None
        )  # (PDate.tomorrow() + (hash(self.name) % 60) + 180)
        self.interval = interval
        self.cluster_size = cluster_size
        self.duration = duration
        self.description = description
        self.notes = notes
        self.dependencies = dependencies
        self.categories = categories

        if self.end:
            assert (
                self.end > self.start
            ), f"{self.name}: End date ({self.end}) must be greater than start date ({self.start})."

    @classmethod
    def from_dict(
        cls, roadmap_code: str, project_code: str, project_dict: dict[str, Any]
    ) -> "Project":
        project_id = (roadmap_code, project_code)
        start_str = project_dict["start"] if "start" in project_dict else ""
        end_str = project_dict["end"] if "end" in project_dict else ""

        return cls(
            project_dict["name"],
            project_id,
            tasks=Tasks.from_dict(
                roadmap_code, project_code, project_dict["name"], project_dict["tasks"]
            ),
            priority=int(project_dict.get("priority") or 10),
            start=PDate.ensure_is_pdate(start_str) if start_str else None,
            end=PDate.ensure_is_pdate(end_str) if end_str else None,
            interval=int(project_dict.get("interval") or 7),
            cluster_size=int(project_dict.get("cluster_size") or 1),
            duration=int(project_dict.get("duration") or 30),
            description=project_dict.get("description", ""),
            notes=project_dict.get("notes", ""),
            categories=set(re.split(", ?", project_dict.get("categories", ""))),
        )

    # @classmethod
    # def from_norg_path(
    #     cls,
    #     norg_path: Path,
    #     project_name: str,
    #     priority: int = 10,
    #     start: Optional[PDate] = None,
    #     end: Optional[PDate] = None,
    #     interval: int = 7,
    #     cluster_size: int = 1,
    #     duration: int = 30,
    #     tags: set = set(),
    #     description: str = "",
    #     notes: str = "",
    #     dependencies: set[tuple[str, ...]] = set(),
    #     # **kwargs,
    # ) -> "Project":
    #     norg_obj = Norg.from_path(norg_path)
    #     project_id = (norg_obj.parent, norg_obj.doc_id)
    #     tasks = Tasks.from_norg_path(norg_path, project_id, project_name)
    #     c = cls(
    #         name=norg_obj.title,
    #         project_id=project_id,
    #         tasks=tasks,
    #         priority=priority,
    #         start=start,
    #         end=end,
    #         interval=interval,
    #         cluster_size=cluster_size,
    #         duration=duration,
    #         tags=tags,
    #         description=description,
    #         notes=notes,
    #         path=norg_path,
    #         dependencies=dependencies,
    #     )
    #     return c

    # @classmethod
    # def from_roadmap_item(
    #     cls, norg_item_string: str, roadmap_id: str, roadmap_path: Path
    # ) -> "Project":
    #     item = Norg.norg_item_from_string(norg_item_string)
    #     item_id = item.item_id[-1] if item.item_id else None
    #     return cls(
    #         name=item.name or "<Placeholder Project Name>",
    #         project_id=(roadmap_id, item_id or "<Roadmap Placeholder ID>"),
    #         tasks=[],  # TODO
    #         priority=item.priority or 10,
    #         start=item.start_date or PDate.today() + 7,
    #         end=item.end_date or PDate.today() + 107,
    #         interval=item.interval or 7,
    #         cluster_size=item.cluster_size or 1,
    #         duration=item.duration or 30,
    #         tags=item.tags or set(),
    #         description=item.description or "",
    #         notes=item.notes or "",
    #         path=item.path,
    #         dependencies=item.dependencies or set(),
    #     )

    def copy(self) -> "Project":
        copy = Project(self.name, self.project_id)
        copy.__dict__.update(self.__dict__)
        return copy

    # def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
    #     ...

    @property
    def clusters(self) -> ClusterType:
        """
        Divides a list of tasks into k clusters of size `cluster_size`.
        """
        task_ids = self._tasks.task_ids
        length = len(task_ids)
        quotient, remainder = divmod(length, self.cluster_size)
        num_clusters = quotient + int(bool(remainder))
        ret: ClusterType = [
            task_ids[self.cluster_size * i : self.cluster_size * (i + 1)]
            for i in range(num_clusters)
        ]
        return ret

    @property
    def subplan(self) -> SubplanType:
        """
        Spaces out a list of clusters between a start and end date, given some interval.
        """
        clusters = self.clusters
        if not clusters:
            return {}
        nclusters = len(clusters)

        if self.end:
            while nclusters > self.start.daysto(self.end):
                print(
                    f"Not enough time allocated to '{self.name}': {self.start} - {self.end}, {nclusters} clusters, cluster size {self.cluster_size}."
                )
                self.cluster_size += 1
                clusters = self.clusters
                nclusters = len(clusters)

        if len(clusters) == 1:
            return {self.start: clusters[0]}
        elif self.end:
            ndays = int(self.get_end()) - int(self.start)
            factor = ndays / nclusters
            ints = [int(round(i * factor)) for i in range(nclusters)]
            # print(nclusters, ndays, ints)
        elif self.interval:
            gap = self.interval
            ints = [i * gap for i in range(nclusters)]
        else:
            print(self.name)
            raise ValueError(
                "Invalid parameter configuration. "
                "For `Project` class, two of `start`, `end`, and `interval` must be defined."
            )

        # start: PDate = self.start or PDate.tomorrow() + (hash(self.name) % 7)

        subplan: SubplanType = {
            self.start + ints[i]: cluster for i, cluster in enumerate(clusters)
        }

        return subplan

    def get_end(self) -> PDate:
        return self.end or (self.start + 365)

    @property
    def tasks(self) -> Tasks:
        return self._tasks

    @property
    def task_ids(self) -> list[tuple[str, str, str]]:
        return self._tasks.task_ids

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        # format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(
            f"Project: {self.name} (ID {'-'.join(self.project_id)})", width, thick=True
        )
        empty = tabularize("", width, thick=True)
        tasks = map(
            lambda x: tabularize(
                f"{x.status_symbol} {'-'.join(x.task_id): <14} │ {x.name: <48}{x.duration:>3}m {x.priority:>3}",
                width,
                thick=True,
            ),
            self._tasks,
        )
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + "\n".join(tasks)
            + "\n"
            + empty
            + bottombeam
        )

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def __getitem__(self, __key: Union[str, tuple[str, str, str]]) -> Task:
        if isinstance(__key, str):
            return self._tasks[(*self.project_id, __key)]
        elif isinstance(__key, tuple):
            # raise ValueError("Accessing a task from Project via a tuple ID is deprecated.")
            print("Accessing a task from Project via a tuple ID is deprecated.")
            return self._tasks[__key]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
