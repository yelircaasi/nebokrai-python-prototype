import re
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from ...util import Norg, PDate, Regexes, expand_task_segments, tabularize
from ..container.tasks import Tasks
from .task import Task


class Project:
    def __init__(
        self,
        name: str,
        id: Tuple[int, int],
        tasks: Union[List[str], str, Tasks] = [],
        priority: int = 10,
        start: Optional[PDate] = None,
        end: Optional[PDate] = None,
        interval: int = 7,
        cluster_size: int = 1,
        duration: int = 30,
        tags: set = set(),
        description: str = "",
        notes: str = "",
        path: Union[str, Path] = "",
        before: List[Tuple[int, int]] = [],
        after: List[Tuple[int, int]] = [],
    ) -> None:
        self.name = name
        self.id = id
        self._tasks: Tasks = (
            Tasks.from_string_iterable(
                expand_task_segments(tasks) if isinstance(tasks, str) else tasks,
                project_id=id,
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
        self.before = before
        self.after = after

    def copy(self) -> "Project":
        copy = Project(self.name, self.id)
        copy.__dict__.update(self.__dict__)
        return copy

    # def get_tasks(self, task_patches: Optional[TaskPatches] = None) -> Tasks:
    #     ...

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def __getitem__(self, __key: Tuple[int, int, int]) -> Task:
        return self._tasks[__key]

    @classmethod
    def from_norg_path(
        cls,
        norg_path: Path,
        project_name: str,
        **kwargs,
    ) -> "Project":
        norg_obj = Norg.from_path(norg_path)
        project_id = (norg_obj.parent, norg_obj.id)
        tasks = Tasks.from_norg_path(norg_path, project_id, project_name)
        c = cls(
            name=norg_obj.title,
            id=project_id,
            tasks=tasks,
            # path=norg_path,
            **kwargs,
            # notes=norg.notes,
        )
        return c

    @classmethod
    def from_roadmap_item(
        cls, item: str, id: Tuple[int, int], roadmap_path: Path
    ) -> "Project":
        # norg = Norg.from_path(norg_path)
        regx = Regexes.first_line
        result = re.search(regx, item)
        title = result.groups()[0] if result else ""
        attributes = Norg.get_attributes(item)
        priority = attributes.get("priority", 10)
        if "||" in title:
            name, tasks = re.split("\s*\|\|\s*", title)

            return cls(
                name,
                id,
                tasks,
                priority=attributes.get("priority", 10),
                start=PDate.ensure_is_pdate(attributes.get("start")),
                end=attributes.get("end"),
                interval=attributes.get("interval", 7),
                cluster_size=int(attributes.get("cluster_size", 1)),
                duration=int(attributes.get("duration", 30)),
                tags=set(attributes.get("tags", [])),
                description=attributes.get("description", ""),
                notes=attributes.get("notes", ""),
                path=attributes.get("path", ""),
                before=attributes.get("before", []),
                after=attributes.get("after", []),
            )

        else:
            project_name, link = Norg.parse_link(item)
            if link:
                path = roadmap_path.parent.parent / link.replace("$/", "")
                try:
                    assert path.exists()
                except:
                    raise IOError(f"Path does not exist: {path}.")
                return cls.from_norg_path(
                    path,
                    project_name,
                    priority=attributes.get("priority", 10),
                    start=PDate.ensure_is_pdate(attributes.get("start")),
                    end=attributes.get("end"),
                    interval=attributes.get("interval", 7),
                    cluster_size=int(attributes.get("cluster_size", 1)),
                    duration=int(attributes.get("duration", 30)),
                    tags=set(attributes.get("tags", [])),
                    description=attributes.get("description", ""),
                    notes=attributes.get("notes", ""),
                    path=attributes.get("path", ""),
                    before=attributes.get("before", []),
                    after=attributes.get("after", []),
                )
            else:
                raise ValueError(f"No path found in roadmap item: {item}.")

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(f"Project: {self.name} (ID {self.id})", width, pad=1)
        empty = tabularize("", width)
        tasks = map(
            lambda x: tabularize(
                f"{format_number(x.id)}{x.name} (priority {x.priority})", width
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

    def get_start(self) -> PDate:
        ret = self.start or PDate.tomorrow() + (hash(self.name) % 60)
        return ret

    def get_end(self) -> PDate:
        return self.end or PDate.tomorrow() + 365
