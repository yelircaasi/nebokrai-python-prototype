import json
from pathlib import Path
from typing import Any, Iterable, Iterator

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

    @classmethod
    def from_declaration_path(cls, declaration_path: Path) -> "Plan":
        with open(declaration_path) as f:
            declaration = json.load(f)

    @property
    def dictionary(self) -> dict[str, Any]:
        return {}

    def ensure_date(self, date: PDate):
        if date not in self._plan:
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


def add_tasks(plan: Plan, date: PDate, tasks: Iterable[Task]) -> Tasks:
    """
    Add tasks to a specified date in the plan. If the tasks exceed the date's available time,
      the lowest-priority excess task ids are returned.
    """
    plan.ensure_date(date)
    tasks = Tasks(plan.config, tasks) + plan._plan.get(date, [])
    avail_dict = plan._calendar[date].available_dict

    blocked_tasks: Tasks = tasks.pop_tasks_from_blocks(avail_dict)
    # filter out "wildcard" and "total" -> blocks = set(avail_dict).difference(
    # ...{"wildcard", "total"})
    excess = tasks.pop_excess_tasks(avail_dict["wildcard"])

    tasks.extend(blocked_tasks)
    tasks.sort(key=lambda t: t.priority)
    tasks.update_tmpdate(date)

    plan._plan.update({date: tasks})
    return plan, excess

    # tasks = Tasks(plan.config, tasks) + plan._plan.get(date, [])
    # tasks.sort(key=lambda t: (t.status == "done", t.priority), reverse=True)
    # excess: Tasks = Tasks(self.config)

    # blocked_tasks = tasks.pop_from_blocks(blocks, avail_dict)
    # ----------------------------------------------------------------------
    # # blocking logic
    # category_names = set()
    # for task in tasks:
    #     category_names.update(task.categories)
    # blocked_tasks = Tasks(self.config)
    # blocks = self._calendar[date].blocks
    # relevant_blocks = list(blocks.intersection(category_names))
    # to_remove: Tasks = Tasks(self.config)
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

    # excess = tasks.pop_excess(avail_dict["wildcard"])
    # ----------------------------------------------------------------------
    # available = avail_dict["empty"]
    # total = tasks.total_remaining_duration
    # while total > available:
    #     task_to_move = tasks.pop()
    #     excess.add(task_to_move)
    #     total -= task_to_move.remaining_duration
    # ----------------------------------------------------------------------

    # tasks.extend(blocked_tasks)
    # tasks.sort(key=lambda t: t.priority)
    # self._plan.update({date: tasks})
    # tasks.update_tmpdate(date)

    # return excess


def add_subplan(
    plan_dict: dict[PDate, Tasks],
    subplan: dict[PDate, Tasks],
) -> Plan:
    """
    Adds subplan (like plan, but corresponding to single project) to the plan,
      rolling tasks over when the daily maximum is exceeded, according to priority.
    """
    # for date, tasks_ in subplan.items():
    # for task in task_list:
    #     task.original_date = date
    # self.ensure_date(date)
    # tasks_.update_original_date(date)
    # self._tasks.extend(tasks_)

    # for tasks_ in subplan.values():
    # # for task_ in tasks_:
    # #     self._tasks.add(task_)
    # self._tasks.extend(tasks_)

    for date, tasks_ in subplan.items():
        tasks_.update_original_date(date)
        plan_dict, rollover = add_tasks(plan_dict, date, tasks_)
        next_date = date.copy()
        while rollover:
            plan_dict, rollover = add_tasks(plan_dict, next_date, rollover)
            next_date += 1
