from collections import OrderedDict
from typing import Any, Callable, Iterable, Iterator, Optional, Union

from ...configuration import config
from ...util import PDate, ProjectID, TaskID, tabularize
from ..base.task import Task

TaskInitType = Optional[Union[Iterable[Task], dict[TaskID, Task]]]


class Tasks:
    """
    Container class for multiple instances of the Task class.
    """

    def __init__(self, tasks: TaskInitType = None) -> None:
        self._tasks: OrderedDict[TaskID, Task] = OrderedDict()
        if isinstance(tasks, dict):
            self._tasks = OrderedDict(tasks)
        else:
            tasks = tasks or []
            # for i, task in enumerate(tasks):
            #     task.project_order = i + 1
            self._tasks = OrderedDict(
                sorted(
                    map(lambda task: (task.task_id, task), tasks), key=lambda t: t[1].project_order
                )
            )
        # if isinstance(tasks, list) and tasks:
        #     if tasks[0].project_name == "Notion - F.B. ML & DS":
        #         print(200 * "!")
        #         print(self._tasks)
        #         print(200 * "@")
        #         exit()

    @classmethod
    def from_dict(
        cls,
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
                task_dict,
                project_id,
                project_name,
                project_priority,
                project_duration,
                project_categories or set(),
            )
            tasks_list.append(task)
        # if project_name == "Notion - F.B. ML & DS":
        #     print(tasks_list)

        ret = cls(tasks_list)
        # if project_name == "Notion - F.B. ML & DS":
        #     print(ret)
        #     import pdb; pdb.set_trace()
        return ret

    def pop_tasks_from_blocks(self, available_dict: dict[str, int]) -> "Tasks":
        """
        To be rewritten!
        """
        print(available_dict)
        # ----------------------------------------------------------------------
        # # blocking logic
        # category_names = set()
        # for task in tasks:
        #     category_names.update(task.categories)
        # blocked_tasks = Tasks()
        # blocks = self._calendar[date].blocks
        # relevant_blocks = list(blocks.intersection(category_names))
        # to_remove: Tasks = Tasks()
        # for block in relevant_blocks:
        #     for task in tasks:
        #         if block in task.categories:
        #             dur = task.remaining_duration
        #             if dur <= avail_dict[block]:
        #                 task.block_assigned = block
        #                 blocked_tasks.add(task)
        #                 to_remove.add(task)
        #                 avail_dict[block] -= dur
        # for task_ in to_remove:
        #     tasks.remove(task_)
        # ----------------------------------------------------------------------

        return Tasks()

    def pop_excess_tasks(self, available_empty: int) -> "Tasks":
        """
        To be rewritten!
        """
        print(available_empty)
        # ----------------------------------------------------------------------
        # available = avail_dict["empty"]
        # total = tasks.total_remaining_duration
        # while total > available:
        #     task_to_move = tasks.pop()
        #     excess.add(task_to_move)
        #     total -= task_to_move.remaining_duration
        # ----------------------------------------------------------------------
        return Tasks()

    def update_original_date(self, date: PDate) -> None:
        for task in self._tasks.values():
            task.original_date = date

    def update_tmpdate(self, date: PDate) -> None:
        for task in self._tasks.values():
            task.tmpdate = date

    def extend(self, __tasks: "Tasks") -> None:
        for task in __tasks:
            self._tasks.update({task.task_id: task})

    def add(self, __task: Task) -> None:
        self._tasks.update({__task.task_id: __task})

    def remove(self, task: Task) -> None:
        del self._tasks[task.task_id]

    def pop(self, last: bool = True) -> Task:
        return self._tasks.popitem(last=last)[1]

    @property
    def task_ids(self) -> list[TaskID]:
        return [t.task_id for t in self]

    @property
    def total_remaining_duration(self) -> int:
        return sum(map(lambda t: t.remaining_duration, self))

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Tasks instance.
        """
        width = config.repr_width

        def format_number(s: Any) -> str:
            return (len(str(s)) == 1) * " " + f" {s} │ "

        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        top = tabularize("Tasks", width, thick=True)
        empty = tabularize("", width)
        names = "\n".join(
            map(
                lambda x: tabularize(
                    f"{format_number(x[0])}{str(x[1].task_id): <14} │ {x[1].name}", width
                ),
                enumerate(sorted(self._tasks.values(), key=lambda t: t.project_order), start=1),
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

    def keys(self) -> Iterator[TaskID]:
        return iter(self._tasks.keys())

    def values(self) -> Iterator[Task]:
        return iter(self._tasks.values())

    def sort(self, key: Optional[Callable[[Task], Any]] = None, reverse: bool = False) -> None:
        """
        Signature identical to list.sort(). Should always be used with a key; otherwise results
          will likely not be very meaningful.
        """
        if key:

            def new_key(k: TaskID) -> Any:
                return key(self._tasks[k])

            for task_id in sorted(self._tasks, key=new_key, reverse=reverse):
                self._tasks.move_to_end(task_id)

        for task_id in sorted(self._tasks, reverse=reverse):
            self._tasks.move_to_end(task_id)

    def __add__(self, __task_or_tasks: Union[Task, Iterable[Task]]) -> "Tasks":
        if isinstance(__task_or_tasks, Task):
            self._tasks.update({__task_or_tasks.task_id: __task_or_tasks})
        else:
            for __task in __task_or_tasks:
                self._tasks.update({__task.task_id: __task})
        return self

    def __bool__(self) -> bool:
        return bool(self._tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(sorted(self._tasks.values(), key=lambda t: t.project_order))

    def __getitem__(self, __key: TaskID) -> Task:
        return self._tasks[__key]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
