from typing import Any, Literal, Optional

from nebokrai.util import color

from ...configuration import config
from ...util import NKDate, NKTime, ProjectID, TaskID, tabularize
from ...util.serde.custom_dict_types import TaskDictParsed, TaskDictRaw, TaskFullDictRaw
from ...util.serde.deserialization import parse_task_dict
from .entry import Entry


class Task:
    """
    Represents a single atomic unit of a project, used for planning and
      used as a template for an entry.
    """

    tmpdate: NKDate = NKDate.nonedate()

    def __init__(
        self,
        name: str,
        project_name: str,
        task_id: TaskID,
        priority: Optional[float],
        duration: Optional[int],
        dependencies: Optional[set[TaskID]] = None,
        date_earliest: Optional[NKDate] = None,
        date_latest: Optional[NKDate] = None,
        tmpdate: Optional[NKDate] = None,
        notes: str = "",
        status: Literal["todo", "done"] = "todo",
        blocks: Optional[set[str]] = None,
        categories: Optional[set[str]] = None,
    ) -> None:
        # meta / info
        self.name = name
        self.project_name = project_name  # unnecessary
        self.task_id = task_id
        self.notes = notes

        # algo
        self.priority = config.default_priority if priority is None else priority
        self.duration = config.default_duration if duration is None else duration
        self.dependencies = dependencies or set()
        self.date_earliest = date_earliest
        self.date_latest = date_latest
        self.project_order = -1
        self.status = status
        self.blocks = blocks or set()
        self.categories = (categories or set()).union(config.default_categories)

        # record
        self.tmpdate = tmpdate if tmpdate else self.tmpdate
        self.original_date: NKDate = NKDate.nonedate()
        self.block_assigned = ""

    @classmethod
    def deserialize(
        cls,
        task_dict_raw: TaskDictRaw | TaskFullDictRaw,
        project_id: Optional[ProjectID],
        project_name: Optional[str],
        project_priority: Optional[float] = None,
        project_duration: Optional[int] = None,
        project_categories: Optional[set[str]] = None,
    ) -> "Task":
        """
        Instantiates from config, json-derived dic, and project information.
        """
        task_dict: TaskDictParsed = parse_task_dict(task_dict_raw)
        project_name_str: str = task_dict.get("project_name") or project_name or "?"
        project_id = project_id or task_dict["project_id"]
        task_code = task_dict["id"].split('-')[-1] or "?"
        task_id = project_id.task_id(task_code) if project_id else TaskID("?", "?", task_code) #TaskID(roadmap_id, project_id_str, task_dict["id"])
        priority: float = task_dict.get("priority") or project_priority or config.default_priority
        duration: int = task_dict.get("duration") or project_duration or config.default_duration

        return cls(
            task_dict["name"],
            project_name_str,
            task_id,
            priority=priority,
            duration=duration,
            notes=task_dict["notes"],
            status=task_dict.get("status") or "todo",
            dependencies=task_dict["dependencies"],
            categories=task_dict.get("categories")
            or set(),  # config.comma_split(task_dict.get("categories") or '').union(project_categories or set()),
        )

    @classmethod
    def deserialize_from_full(cls, full_dict: TaskFullDictRaw) -> "Task":
        """
        Instantiate Task object from dictio-ry corresponding to JSON format.
        """
        project_id_str: Optional[str] = full_dict["project_id"]
        project_id: Optional[ProjectID] = (
            ProjectID.from_string(project_id_str) if project_id_str else None
        )
        return cls.deserialize(full_dict, project_id, full_dict["project_name"])

    def serialize(self) -> TaskFullDictRaw:
        return {
            "name": self.name,
            "project_name": self.project_name,
            "project_id": str(self.task_id.project_id),
            "id": str(self.task_id),
            "priority": self.priority,
            "duration": self.duration,
            "dependencies": ",".join(sorted(map(str, self.dependencies))),
            "notes": self.notes,
            "status": self.status,
            "categories": ",".join(self.categories),
        }

    def copy(self) -> "Task":
        t = Task(self.name, self.project_name, self.task_id, self.priority, self.duration)
        t.__dict__.update(self.__dict__)
        return t

    @property
    def fullname(self) -> str:
        return f"{self.name} ({self.project_name})"

    def isafter(self, __other: "Task") -> bool:
        return self.task_id in __other.dependencies

    def as_entry(
        self,
        start: Optional[NKTime] = None,
        end: Optional[NKTime] = None,
    ) -> Entry:
        """
        Create an instance of Entry from a task.
        """
        if not start:
            start = NKTime.nonetime()
        return Entry(
            f"{self.name} ({self.project_name})",
            start,
            end,
            priority=self.priority,
            blocks=self.blocks,
            categories=self.categories,
            notes=self.notes,
            normaltime=self.duration,
        )

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
        width = config.repr_width
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
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

    def __hash__(self) -> int:
        return hash(self.task_id)

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

    @property
    def repr1(self) -> str:
        taskid = color.red(str(self.task_id) + 17 * ' ')[:27]
        name = color.green(self.name + 20 * ' ')[:30]
        prio = color.magenta('prio ' + str(self.priority))
        dur = color.cyan(str(self.duration) + 'min')
        order = color.yellow('order ' + str(self.project_order))
        return f"  {taskid: <27} {name: <30} {prio:<8} {dur:<7} {order:<9}"
        # self.name = name
        # self.project_name = project_name  # unnecessary
        # self.task_id = task_id
        # self.notes = notes

        # # algo
        # self.priority = config.default_priority if priority is None else priority
        # self.duration = config.default_duration if duration is None else duration
        # self.dependencies = dependencies or set()
        # self.date_earliest = date_earliest
        # self.date_latest = date_latest
        # self.project_order = -1
        # self.status = status
        # self.blocks = blocks or set()
        # self.categories = (categories or set()).union(config.default_categories)

        # # record
        # self.tmpdate = tmpdate if tmpdate else self.tmpdate
        # self.original_date: NKDate = NKDate.nonedate()
        # self.block_assigned = ""