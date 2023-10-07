from pathlib import Path
from typing import Any, Iterable, Iterator, Optional, Union

from ...util import ConfigType, Norg, PDate, PTime, tabularize
from ..base.task import Task


class Tasks:
    def __init__(
        self, tasks: Union[dict[tuple[str, str, str], Task], Iterable[Task]] = {}
    ) -> None:
        self._tasks: dict[tuple[str, str, str], Task] = {}
        if isinstance(tasks, dict):
            self._tasks = tasks
        else:
            for i, task in enumerate(tasks):
                task.project_order = i + 1
            self._tasks = dict(map(lambda task: (task.task_id, task), tasks))

    @classmethod
    def from_dict(
        cls,
        tasks_dict_list: list[dict[str, Any]],
        roadmap_code: str,
        project_code: str,
        project_name: str,
        project_priority: Optional[int] = None,
        project_duration: Optional[int] = None,
        project_categories: set[str] = set(),
    ) -> "Tasks":
        tasks_list: list[Task] = []
        for task_dict in tasks_dict_list:
            # task_id = (roadmap, project, task_dict["id"])
            task = Task.from_dict(
                task_dict,
                roadmap_code,
                project_code,
                project_name,
                project_priority,
                project_duration,
                project_categories,
            )
            tasks_list.append(task)

        return cls(tasks_list)

    @classmethod
    def from_string_iterable(
        cls,
        task_list: list[str],
        project_id: tuple[str, str],
        project_name: str,
        priority: Optional[int] = None,
        after: set[tuple[str, ...]] = set(),
    ) -> "Tasks":
        tasks = cls()
        for task_id_, name in enumerate(task_list, start=1):
            # name = name if isinstance(name, str) else name.name
            task_id = (*project_id, str(task_id_))
            task = (
                Task(name, project_name, task_id, priority)
                if priority is not None
                else Task(name, project_name, task_id)
            )
            tasks.add(task)
        return tasks

    # @classmethod
    # def from_norg_path(
    #     cls,
    #     norg_path: Path,
    #     project_id: tuple[str, str],
    #     project_name: str,  # **kwargs
    # ) -> "Tasks":
    #     assert project_name != "/"
    #     tasks = cls()
    #     norg_obj = Norg.from_path(norg_path)
    #     for item in norg_obj.items:
    #         item_id = item.name
    #         assert item_id, f"Item must have a name: {str(item)}"
    #         priority = int(str(item.priority)) if str(item.priority).isdigit() else 10
    #         tasks.add(
    #             Task(
    #                 name=item.name,
    #                 project_name=
    #                 task_id=(*project_id, item_id),
    #                 priority=priority,
    #             )
    #         )
    #     return tasks

    # @classmethod
    # def from_roadmaps(cls, roadmaps: Iterable[Iterable[Iterable["Task"]]]) -> "Tasks":
    #     new_tasks = Tasks()
    #     for roadmap in roadmaps:
    #         for project in roadmap:
    #             for task in project:
    #                 new_tasks._tasks.update({task.task_id: task})
    #     return new_tasks

    def add(self, task: Task) -> None:
        self._tasks.update({task.task_id: task})

    @property
    def task_ids(self) -> list[tuple[str, str, str]]:
        return [t.task_id for t in self]

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
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

    def update(self, __tasks: Union["Tasks", dict[tuple[str, str, str], Task]]) -> None:
        for task_id, task in __tasks.items():
            self._tasks.update({task_id: task})

    def items(self) -> Iterator[tuple[tuple[str, str, str], Task]]:
        return iter(self._tasks.items())

    def __iter__(self) -> Iterator[Task]:
        return iter(sorted(self._tasks.values(), key=lambda t: t.project_order))

    def __getitem__(self, __key: tuple[str, str, str]) -> Task:
        return self._tasks[__key]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
