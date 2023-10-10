from typing import Any, Iterable, Iterator, Optional, Union

from ...config import Config
from ...util import ProjectID, TaskID, tabularize
from ..base.task import Task

TaskInitType = Optional[Union[dict[TaskID, Task], Iterable[Task]]]


class Tasks:
    """
    Container class for multiple instances of the Task class.
    """

    def __init__(self, config: Config, tasks: TaskInitType = None) -> None:
        self.config = config
        self._tasks: dict[TaskID, Task] = {}
        if isinstance(tasks, dict):
            self._tasks = tasks
        else:
            tasks = tasks or []
            for i, task in enumerate(tasks):
                task.project_order = i + 1
            self._tasks = dict(map(lambda task: (task.task_id, task), tasks))

    @classmethod
    def from_dict(
        cls,
        config: Config,
        tasks_dict_list: list[dict[str, Any]],
        project_id: ProjectID,
        project_name: str,
        project_priority: Optional[int] = None,
        project_duration: Optional[int] = None,
        project_categories: Optional[set[str]] = None,
    ) -> "Tasks":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        tasks_list: list[Task] = []
        for task_dict in tasks_dict_list:
            task = Task.from_dict(
                config,
                task_dict,
                project_id,
                project_name,
                project_priority,
                project_duration,
                project_categories or set(),
            )
            tasks_list.append(task)

        return cls(config, tasks_list)

    def add(self, task: Task) -> None:
        self._tasks.update({task.task_id: task})

    @property
    def task_ids(self) -> list[TaskID]:
        return [t.task_id for t in self]

    def pretty(self, width: int = 80) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Tasks instance.
        """

        def format_number(s: Any) -> str:
            return (len(str(s)) == 1) * " " + f" {s} │ "

        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        top = tabularize("Tasks", width)
        empty = tabularize("", width)
        names = "\n".join(
            map(
                lambda x: tabularize(
                    f"{format_number(x[0])}{x[1].name} (ID {x[1].task_id})", width
                ),
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

    def update(self, __tasks: Union["Tasks", dict[TaskID, Task]]) -> None:
        for task_id, task in __tasks.items():
            self._tasks.update({task_id: task})

    def items(self) -> Iterator[tuple[TaskID, Task]]:
        return iter(self._tasks.items())

    def __iter__(self) -> Iterator[Task]:
        return iter(sorted(self._tasks.values(), key=lambda t: t.project_order))

    def __getitem__(self, __key: TaskID) -> Task:
        return self._tasks[__key]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
