from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from planager.config import _Config as ConfigType
from planager.utils.misc import tabularize
from .calendar import Calendar
from planager.utils.datetime_extensions import PDate
from planager.utils.data.norg.norg_utils import Norg
from planager.utils.data.norg import norg_utils as norg


class Task:
    def __init__(self, name: str, id: int, priority: int = 10, **kwargs) -> None:
        self.name = name
        self.id = id
        self.priority = priority
        self.__dict__.update(**kwargs)

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
        top = tabularize(f"Task: {self.name} (ID {self.id})", width, pad=1)
        empty = tabularize("", width)
        priority = tabularize(f"  Priority: {self.priority}", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + priority
            + "\n"
            + empty
            + bottombeam
        )


class Tasks:
    def __init__(self) -> None:
        self._tasks = {}

    def add(self, task: Task) -> None:
        self._tasks.update({task.id: task})

    def __iter__(self) -> Iterable[Task]:
        return iter(self._tasks.values())

    def __getitem__(self, __key: int) -> Task:
        return self._tasks[__key]

    @classmethod
    def from_norg_path(cls, norg_path: Path, **kwargs) -> "Tasks":
        tasks = cls()
        norg = Norg.from_path(norg_path)
        for id, item in enumerate(norg.items, start=1):
            parse = Norg.parse_item_with_attributes(item)
            tasks.add(Task(parse["title"], id, **parse["attributes"]))
        return tasks

    @classmethod
    def from_string_iterable(
        cls, task_list: List[str], priority: Optional[int] = None
    ) -> "Tasks":
        tasks = cls()
        for id, name in enumerate(task_list, start=1):
            name = name if isinstance(name, str) else name.name
            task = Task(name, id, priority) if priority is not None else Task(name, id)
            tasks.add(task)
        return tasks

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
        top = tabularize("Tasks", width, pad=1)
        empty = tabularize("", width)
        names = "\n".join(
            map(
                lambda x: tabularize(f"{format_number(x[0])}{x[1].name}", width),
                self._tasks.items(),
            )
        )
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + names
            + "\n"
            + empty
            + bottombeam
        )

    # def __getitem__(self, __name: str) -> Any:
    #     task = ...
    #     return task

    # def __setitem__(self, __name: str, __value: Any) -> None:
    #     ...


class TaskPatch:
    def __init__(self) -> None:
        self.x = ...


class TaskPatches:
    def __init__(self) -> None:
        ...

    def __getitem__(self, __name: str) -> Any:
        task = ...
        return task

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "TaskPatches":
        # file = workspace_dir / "roadmaps.norg"
        # parsed = Norg.from_path(file)
        # ...
        # return cls()
        return cls()
