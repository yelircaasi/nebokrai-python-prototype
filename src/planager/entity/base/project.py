import re
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional, Union

from ...util import Norg, PDate, Regexes, expand_task_segments, tabularize
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
        tags: set = set(),
        description: str = "",
        notes: str = "",
        path: Optional[Path] = None,
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
        self.start = start or PDate.tomorrow() + (hash(self.name) % 60)
        self.end = PDate.ensure_is_pdate(end)
        self.interval = interval
        self.cluster_size = cluster_size
        self.duration = duration
        self.tags = tags
        self.description = description
        self.notes = notes
        self.path = Path(path) if path else path
        self.dependencies = dependencies
        self.categories = categories

    @classmethod
    def from_dict(cls, roadmap_id: str, project_dict: dict[str, Any]) -> "Project":
        project_id = (roadmap_id, project_dict["id"])

        return cls(
            project_dict["name"],
            project_id,
        )

    @classmethod
    def from_norg_path(
        cls,
        norg_path: Path,
        project_name: str,
        priority: int = 10,
        start: Optional[PDate] = None,
        end: Optional[PDate] = None,
        interval: int = 7,
        cluster_size: int = 1,
        duration: int = 30,
        tags: set = set(),
        description: str = "",
        notes: str = "",
        dependencies: set[tuple[str, ...]] = set(),
        # **kwargs,
    ) -> "Project":
        norg_obj = Norg.from_path(norg_path)
        project_id = (norg_obj.parent, norg_obj.doc_id)
        tasks = Tasks.from_norg_path(norg_path, project_id, project_name)
        c = cls(
            name=norg_obj.title,
            project_id=project_id,
            tasks=tasks,
            priority=priority,
            start=start,
            end=end,
            interval=interval,
            cluster_size=cluster_size,
            duration=duration,
            tags=tags,
            description=description,
            notes=notes,
            path=norg_path,
            dependencies=dependencies,
        )
        return c

    @classmethod
    def from_roadmap_item(
        cls, norg_item_string: str, roadmap_id: str, roadmap_path: Path
    ) -> "Project":
        item = Norg.norg_item_from_string(norg_item_string)
        item_id = item.item_id[-1] if item.item_id else None
        return cls(
            name=item.name or "<Placeholder Project Name>",
            project_id=(roadmap_id, item_id or "<Roadmap Placeholder ID>"),
            tasks=[],  # TODO
            priority=item.priority or 10,
            start=item.start_date or PDate.today() + 7,
            end=item.end_date or PDate.today() + 107,
            interval=item.interval or 7,
            cluster_size=item.cluster_size or 1,
            duration=item.duration or 30,
            tags=item.tags or set(),
            description=item.description or "",
            notes=item.notes or "",
            path=item.path,
            dependencies=item.dependencies or set(),
        )

    def copy(self) -> "Project":
        copy = Project(self.name, self.project_id)
        copy.__dict__.update(self.__dict__)
        return copy

    # def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
    #     ...

    def get_start(self) -> PDate:
        return self.start or PDate.tomorrow() + (hash(self.name) % 60)

    def get_end(self) -> PDate:
        return self.get_start() + 365

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
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"Project: {self.name} (ID {self.project_id})", width)
        empty = tabularize("", width)
        tasks = map(
            lambda x: tabularize(
                f"{format_number(x.task_id)}{x.name} (priority {x.priority})", width
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

    def __getitem__(self, __key: tuple[str, str, str]) -> Task:
        return self._tasks[__key]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
