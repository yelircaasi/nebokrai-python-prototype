from typing import Iterator

from ...config import Config
from ...util import PDate, TaskID
from ..container.tasks import Tasks
from .calendar import Calendar
from .task import Task


class Plan:
    """
    Contains allocation of tasks to days, along with methods for creating such an allocation.
    """

    def __init__(
        self,
        config: Config,
        calendar: Calendar,
    ) -> None:
        self.config = config
        self._calendar = calendar
        self._tasks: dict[TaskID, Task] = {}
        self._plan: dict[PDate, list[TaskID]] = {}

    def add_tasks(self, date: PDate, task_ids_: list[TaskID]) -> list[TaskID]:
        """
        Add tasks to a specified date in the plan. If the tasks exceed the date's available time,
          the lowest-priority excess task ids are returned.
        """
        task_ids = task_ids_[:]

        task_ids = sorted(
            list(set(task_ids + self._plan.get(date, []))),
            key=lambda x: (self._tasks[x].status == "done", self._tasks[x].priority),
            reverse=True,
        )
        excess: list[TaskID] = []
        avail_dict = self._calendar[date].available_dict

        # blocking logic
        category_names = set()
        for task_id in task_ids:
            category_names.update(self._tasks[task_id].categories)

        blocked_task_ids = []
        blocks = self._calendar[date].blocks

        # TODO: make `blocks` property correctly detect blocks inside of routine entries
        relevant_blocks = list(blocks.intersection(category_names))
        to_remove = []
        for block in relevant_blocks:
            for task_id in task_ids:
                if block in self._tasks[task_id].categories:
                    dur = self._tasks[task_id].remaining_duration
                    if dur <= avail_dict[block]:
                        self._tasks[task_id].block_assigned = block
                        blocked_task_ids.append(task_id)
                        to_remove.append(task_id)
                        avail_dict[block] -= dur
        for t_id in to_remove:
            task_ids.remove(t_id)

        available = avail_dict["empty"]
        total = sum(map(lambda _id: self._tasks[_id].remaining_duration, task_ids))
        while total > available:
            task_to_move = task_ids.pop()
            excess.append(task_to_move)
            total -= self._tasks[task_to_move].remaining_duration

        self._plan.update({date: blocked_task_ids + task_ids})
        for task_id in blocked_task_ids + task_ids:
            self._tasks[task_id].tmpdate = date
        return excess

    def add_subplan(
        self,
        subplan: dict[PDate, list[TaskID]],
        tasks: Tasks,
    ) -> None:
        """
        Adds subplan (like plan, but corresponding to single project) to the plan,
          rolling tasks over when the daily maximum is exceeded, according to priority.
        """
        if not subplan:
            return
        # id_ = list(subplan.values())[0][0]

        for date, task_id_list in subplan.items():
            for task_id in task_id_list:
                tasks[task_id].original_date = date

        for task in tasks:
            self._tasks.update({task.task_id: task})

        # excess_tasks: list[TaskID] = []

        for date, task_id_list in subplan.items():
            self.ensure_date(date)
            rollover: list[TaskID] = self.add_tasks(date, task_id_list)
            next_date = date.copy()
            while rollover:
                rollover = self.add_tasks(next_date, rollover)
                next_date += 1

    def ensure_date(self, date: PDate):
        if not date in self._plan:
            self._plan.update({date: []})

    @property
    def end_date(self) -> PDate:
        return max(self._plan)

    @property
    def start_date(self) -> PDate:
        return min(self._plan)

    @property
    def tasks(self) -> Tasks:
        return Tasks(self.config, self._tasks.values())

    @staticmethod
    def adjust_tmpdate_to_neighbors(t: Task, pre: Task, post: Task) -> Task:
        """
        Adjusts the .tmpdate attribute to be between the .tmpdate of two other tasks.
        """
        new_t = t.copy()
        if pre <= new_t <= post:
            return new_t
        limit_before = int(pre.tmpdate) + int(new_t.isafter(pre))
        limit_after: int = int(post.tmpdate) + int(post.isafter(new_t))
        if not limit_before <= limit_after:
            raise ValueError("Impossible task precedence resolution requested.")
        new_t.tmpdate = PDate.fromordinal(int((limit_before + limit_after) / 2))
        return new_t

    def items(self) -> Iterator[tuple[PDate, list[TaskID]]]:
        return iter(self._plan.items())

    def __iter__(self) -> Iterator[tuple[PDate, list[TaskID]]]:
        return iter(sorted(list(self._plan.items()), key=lambda x: x[0]))

    def __contains__(self, __date: PDate) -> bool:
        return __date in self._plan

    def __getitem__(self, __date: PDate) -> list[TaskID]:
        return self._plan.get(__date, [])

    def __setitem__(self, __date: PDate, __tasks: list[TaskID]) -> None:
        self._plan.update({__date: __tasks})

    def __str__(self) -> str:
        def task_repr(task_id: TaskID, date: PDate) -> str:
            task = self._tasks[task_id]
            name = str(task.name) or str(task.task_id)
            orig = ("orig: " + str(task.original_date)) if task.original_date != date else ""
            return (
                f"{task.status_symbol} {task.project_name[:30]: <30}   {name[:30]: <30}   "
                f"pr {task.priority}     {task.duration}m   {orig}   {task.block_assigned}"
            )

        def time_repr(date: PDate) -> str:
            entry_names = ", ".join([e.name for e in self._calendar[date].entries])
            blocks = "\n".join(
                (f"  {b}: {t}" for b, t in self._calendar[date].available_dict.items())
            )
            total_before = self._calendar[date].total_available
            total_after = total_before - sum(
                (self._tasks[task_id].remaining_duration for task_id in self._plan[date])
            )
            empty_before = self._calendar[date].empty_time
            empty_after = empty_before - sum(
                (
                    self._tasks[task_id].remaining_duration
                    for task_id in self._plan[date]
                    if not self._tasks[task_id].block_assigned
                )
            )
            return (
                f"Calendar entries: {entry_names}\n"
                f"Blocks:\n{blocks}\n"
                "Total available on calendar:\n"
                f"  Before planning: {empty_before}m empty; {total_before}m including blocks\n"
                f"  After planning:  {empty_after}m empty; {total_after}m including blocks"
            )

        line = 120 * "─" + "\n"

        newl = "\n"
        return "\n".join(
            [
                f"{line}{str(d)}\n\n{time_repr(d)}\n\n{newl.join([task_repr(t, d) for t in ids])}\n"
                for d, ids in self
            ]
        )

    def __repr__(self) -> str:
        return self.__str__()
