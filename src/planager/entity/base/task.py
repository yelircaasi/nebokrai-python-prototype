import re
from typing import Any, Literal, Optional

from planager.config import Config
from planager.util import PDate, ProjectID, PTime, TaskID, tabularize

from .entry import Entry


class Task:
    """
    Represents a single atomic unit of a project, used for planning and
      used as a template for an entry.
    """

    tmpdate: PDate = PDate.nonedate()

    def __init__(
        self,
        config: Config,
        name: str,
        project_name: str,
        task_id: TaskID,
        priority: Optional[int],
        duration: Optional[int],
        dependencies: Optional[set[TaskID]] = None,
        tmpdate: Optional[PDate] = None,
        notes: str = "",
        status: Literal["todo", "done"] = "todo",
        blocks: Optional[set[str]] = None,
        categories: Optional[set[str]] = None,
    ) -> None:
        self.config = config

        # meta / info
        self.name = name
        self.project_name = project_name  # unnecessary
        self.task_id = task_id
        self.notes = notes

        # algo
        self.priority = config.default_priority if priority is None else priority
        self.duration = config.default_duration if duration is None else duration
        self.dependencies = dependencies or set()
        self.project_order = -1
        self.status = status
        self.blocks = blocks or set()
        self.categories = (categories or set()).union(config.default_categories)

        # record
        self.tmpdate = tmpdate if tmpdate else self.tmpdate
        self.original_date: PDate = PDate.nonedate()
        self.block_assigned = ""

    @classmethod
    def from_dict(
        cls,
        config: Config,
        task_dict: dict[str, Any],
        project_id: ProjectID,
        project_name: str,
        project_priority: Optional[int] = None,
        project_duration: Optional[int] = None,
        project_categories: Optional[set[str]] = None,
    ) -> "Task":
        """
        Instantiates from config, json-derived dic, and project information.
        """

        def parse_id(s: str) -> TaskID:
            res = re.split(r"\W", s)
            return TaskID(res[0], res[1], res[2])

        task_id = project_id.task_id(task_dict["id"])
        deps_raw = re.split(", ?", task_dict.get("dependencies", ""))
        cats_raw = re.split(", ?", task_dict.get("categories", ""))

        return cls(
            config,
            task_dict["name"],
            project_name,
            task_id,
            priority=int(task_dict.get("priority") or project_priority or config.default_priority),
            duration=int(task_dict.get("duration") or project_duration or config.default_duration),
            dependencies=set(map(parse_id, filter(bool, deps_raw))),  # if deps_raw else set(),
            notes=task_dict.get("notes") or "",
            status=task_dict.get("status") or "todo",
            categories=set(filter(bool, cats_raw)).union(project_categories or set()),
        )

    def copy(self) -> "Task":
        t = Task(
            self.config, self.name, self.project_name, self.task_id, self.priority, self.duration
        )
        t.__dict__.update(self.__dict__)
        return t

    def isafter(self, __other: "Task") -> bool:
        return self.task_id in __other.dependencies

    def as_entry(self, start: Optional[PTime]) -> Entry:
        """
        Create an instance of Entry from a task.
        """
        # TODO
        if not start:
            start = PTime.nonetime()
        return Entry(self.config, self.name, start)

    @property
    def status_symbol(self) -> str:
        return {"todo": "☐", "done": "✔"}[self.status]

    @property
    def remaining_duration(self) -> int:
        return self.duration * int(self.status == "todo")

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Task instance.
        """
        width = self.config.repr_width
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        # format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(
            f"Task: {self.task_id[1][:30]} <> {self.name} (ID {'<>'.join(self.task_id)})",
            width,
        )
        empty = tabularize("", width)
        priority = tabularize(f"  Priority: {self.priority}", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + priority
            + "\n"
            + empty
            + bottombeam
        )

    def __eq__(self, __other: Any) -> bool:
        return self.__dict__ == __other.__dict__

    def __lt__(self, __other: Any) -> bool:
        return (
            (self.task_id in __other.dependencies)
            and (__other.task_id not in self.dependencies)
            or (__other.tmpdate > self.tmpdate)
        )

    def __gt__(self, __other: Any) -> bool:
        return (
            (__other.task_id in self.dependencies)
            and (self.task_id not in __other.dependencies)
            or (self.tmpdate > __other.tmpdate)
        )

    def __le__(self, __other: Any) -> bool:
        return (
            (not self.task_id not in __other.dependencies)
            and (__other.task_id not in self.dependencies)
            and (__other.tmpdate >= self.tmpdate)
        )

    def __ge__(self, __other: Any) -> bool:
        return (
            (__other.task_id not in self.dependencies)
            and (self.task_id not in __other.dependencies)
            and (self.tmpdate >= __other.tmpdate)
        )

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
