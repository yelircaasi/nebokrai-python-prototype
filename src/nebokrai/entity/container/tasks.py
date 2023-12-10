from collections import OrderedDict
from itertools import chain
from typing import Any, Callable, Iterable, Iterator, Optional, Union

from ...configuration import config
from ...util import NKDate, ProjectID, TaskID, tabularize
from ...util.serde.custom_dict_types import TaskDictRaw, TaskFullDictRaw
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
            self._tasks = OrderedDict(
                sorted(
                    map(lambda task: (task.task_id, task), tasks), key=lambda t: t[1].project_order
                )
            )

    @classmethod
    def deserialize(
        cls,
        tasks_dict_list: list[TaskDictRaw] | list[TaskFullDictRaw],
        project_id: Optional[ProjectID] = None,
        project_name: Optional[str] = None,
        project_priority: Optional[int] = None,
        project_duration: Optional[int] = None,
        project_categories: Optional[set[str]] = None,
    ) -> "Tasks":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        tasks_list: list[Task] = []
        for task_dict in tasks_dict_list:
            task = Task.deserialize(
                task_dict,
                project_id,
                project_name,
                project_priority,
                project_duration,
                project_categories or set(),
            )
            tasks_list.append(task)

        ret = cls(tasks_list)
        return ret

    def serialize(self) -> list[TaskFullDictRaw]:
        return list(map(Task.serialize, self._tasks.values()))

    def pop_tasks_from_blocks(self, available_dict: dict[str, int]) -> "Tasks":
        """
        Get tasks that can be added to the blocks specified in 'available_dict' and remove them
          from self.
        """
        relevant_block_names = sorted(
            self.get_relevant_block_names(available_dict), key=lambda bl: available_dict[bl]
        )
        blocked_tasks: Tasks = self.get_blocked_tasks(relevant_block_names, available_dict)
        self.remove_tasks(blocked_tasks)

        return blocked_tasks

    def get_blocked_tasks(
        self, relevant_block_names: Iterable[str], available_dict: dict[str, int]
    ) -> "Tasks":
        """
        Get member tasks that can be added to blocks according to the block time availablity
          dictionary.
        """
        blocked_tasks = Tasks()

        def block_filter(categories: set[str]) -> Callable[[str], bool]:
            def inner(block_name: str) -> bool:
                return (block_name in categories) and (dur <= available_dict[block_name])

            return inner

        for task in self._tasks.values():
            dur = task.remaining_duration
            block_names = list(filter(block_filter(task.categories), relevant_block_names))

            if block_names and not task.block_assigned:
                task.block_assigned = (block_name := block_names[0])
                blocked_tasks.add(task)
                available_dict[block_name] -= dur

        return blocked_tasks

    def remove_tasks(self, to_remove: Iterable[Task]) -> None:
        for task in to_remove:
            del self._tasks[task.task_id]

    def get_relevant_block_names(self, names: Iterable[str]) -> set[str]:
        """
        Returns a list of block names that correspond to the categories of this instance's member
          tasks.
        """
        category_sets: list[set[str]] = list(map(lambda t: t.categories, self.values()))
        category_names = set(chain.from_iterable(category_sets))
        relevant_block_names = set(names).intersection(category_names)
        return relevant_block_names

    def pop_excess_tasks(self, available_empty: int) -> "Tasks":
        """
        To be rewritten!
        """
        excess_tasks = Tasks()
        total = self.total_remaining_duration
        while total > available_empty:
            task_to_move = self.pop()
            excess_tasks.add(task_to_move)
            total -= task_to_move.remaining_duration
        return excess_tasks

    def update_original_date(self, date: NKDate) -> None:
        for task in self._tasks.values():
            task.original_date = date

    def update_tmnkdate(self, date: NKDate) -> None:
        for task in self._tasks.values():
            task.tmnkdate = date

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

    def __len__(self) -> int:
        return len(self._tasks)

    def __getitem__(self, __key: TaskID) -> Task:
        return self._tasks[__key]

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
