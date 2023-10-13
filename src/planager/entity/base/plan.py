from typing import Iterable, Iterator

from ...config import Config
from ...util import PDate
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
        self._tasks: Tasks = Tasks(config)
        self._plan: dict[PDate, Tasks] = {date: Tasks(config) for date in calendar}

    def add_tasks(self, date: PDate, tasks: Iterable[Task]) -> Tasks:
        """
        Add tasks to a specified date in the plan. If the tasks exceed the date's available time,
          the lowest-priority excess task ids are returned.
        """
        # if date > PDate(2026, 6, 15):
        #     print(date)
        #     date = PDate(2026, 6, 15)

        tasks = Tasks(self.config, tasks) + self._plan.get(date, [])
        tasks.sort(key=lambda t: (t.status == "done", t.priority), reverse=True)
        excess: Tasks = Tasks(self.config)
        avail_dict = self._calendar[date].available_dict
        # print(tasks)

        # blocking logic
        category_names = set()
        for task in tasks:
            category_names.update(task.categories)

        blocked_tasks = Tasks(self.config)
        blocks = self._calendar[date].blocks

        # TODO: make `blocks` property correctly detect blocks inside of routine entries
        relevant_blocks = list(blocks.intersection(category_names))
        to_remove: Tasks = Tasks(self.config)
        for block in relevant_blocks:
            for task in tasks:
                if block in task.categories:
                    dur = task.remaining_duration
                    if dur <= avail_dict[block]:
                        task.block_assigned = block
                        blocked_tasks.add(task)
                        to_remove.add(task)
                        avail_dict[block] -= dur
        for task_ in to_remove:
            tasks.remove(task_)

        available = avail_dict["empty"]
        total = tasks.total_remaining_duration
        while total > available:
            task_to_move = tasks.pop()
            excess.add(task_to_move)
            total -= task_to_move.remaining_duration

        self._plan.update({date: blocked_tasks + tasks})
        for task in blocked_tasks + tasks:
            task.tmpdate = date

        return excess

    def add_subplan(
        self,
        subplan: dict[PDate, Tasks],
    ) -> None:
        """
        Adds subplan (like plan, but corresponding to single project) to the plan,
          rolling tasks over when the daily maximum is exceeded, according to priority.
        """
        if not subplan:
            return
        # id_ = list(subplan.values())[0][0]

        for date, task_list in subplan.items():
            for task in task_list:
                task.original_date = date

        for tasks_ in subplan.values():
            for task_ in tasks_:
                self._tasks.add(task_)

        # excess_tasks: list[TaskID] = []

        for date, task_list in subplan.items():
            self.ensure_date(date)
            rollover: Tasks = self.add_tasks(date, task_list)
            # print(task_list)
            # print("%%%%%%%%%%")
            next_date = date.copy()
            while rollover:
                rollover = self.add_tasks(next_date, rollover)
                next_date += 1

    def ensure_date(self, date: PDate):
        if not date in self._plan:
            self._plan.update({date: Tasks(self.config)})

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

    def items(self) -> Iterator[tuple[PDate, Tasks]]:
        return iter(self._plan.items())

    def __iter__(self) -> Iterator[PDate]:
        return iter(self._plan.keys())

    def __contains__(self, __date: PDate) -> bool:
        return __date in self._plan

    def __getitem__(self, __date: PDate) -> Tasks:
        return self._plan.get(__date, Tasks(self.config))

    def __setitem__(self, __date: PDate, __tasks: Tasks) -> None:
        self._plan.update({__date: __tasks})

    def __str__(self) -> str:
        def task_repr(task: Task, date: PDate) -> str:
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
            total_after = total_before - sum((task.remaining_duration for task in self._plan[date]))
            empty_before = self._calendar[date].empty_time
            empty_after = empty_before - sum(
                (task.remaining_duration for task in self._plan[date] if not task.block_assigned)
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
                for d, ids in self.items()
            ]
        )

    def __repr__(self) -> str:
        return self.__str__()
