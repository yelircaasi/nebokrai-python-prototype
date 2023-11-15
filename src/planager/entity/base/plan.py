import json
from pathlib import Path
from typing import Any, Iterable, Iterator

from ...util import PDate
from ..container.routines import Routines
from ..container.tasks import Tasks
from .calendar import Calendar
from .task import Task


class Plan:
    """
    Contains allocation of tasks to days, along with methods for displaying
      this allocation.
    """

    def __init__(
        self,
        calendar: Calendar,
    ) -> None:
        self.calendar = calendar
        self.tasks: Tasks = Tasks()
        self.plan_dict: dict[PDate, Tasks] = {date: Tasks() for date in calendar}

    @classmethod
    def from_path(cls, declaration_path: Path) -> "Plan":
        """
        Reads a saved plan in .json format.
        """
        with open(declaration_path, encoding="utf-8") as f:
            declaration = json.load(f)
        return cls(
            calendar=Calendar.from_dict(
                Routines.from_dict(declaration["routines"]), declaration["calendar"]
            ),
        )

    @property
    def dictionary(self) -> dict[str, Any]:
        return {}

    def ensure_date(self, date: PDate):
        if date not in self.plan_dict:
            self.plan_dict.update({date: Tasks()})

    @property
    def end_date(self) -> PDate:
        return max(self.plan_dict)

    @property
    def start_date(self) -> PDate:
        return min(self.plan_dict)

    def items(self) -> Iterator[tuple[PDate, Tasks]]:
        return iter(self.plan_dict.items())

    def __iter__(self) -> Iterator[PDate]:
        return iter(self.plan_dict.keys())

    def __contains__(self, __date: PDate) -> bool:
        return __date in self.plan_dict

    def __getitem__(self, __date: PDate) -> Tasks:
        return self.plan_dict.get(__date, Tasks())

    def __setitem__(self, __date: PDate, __tasks: Tasks) -> None:
        self.plan_dict.update({__date: __tasks})

    @property
    def summary(self) -> str:
        return "Plan.summary property is not yet implemented."

    def __str__(self) -> str:
        def task_repr(task: Task, date: PDate) -> str:
            name = str(task.name) or str(task.task_id)
            orig = ("orig: " + str(task.original_date)) if task.original_date != date else ""
            return (
                f"{task.status_symbol} {task.project_name[:30]: <30}   {name[:30]: <30}   "
                f"pr {task.priority}     {task.duration}m   {orig}   {task.block_assigned}"
            )

        def time_repr(date: PDate) -> str:
            entry_names = ", ".join([e.name for e in self.calendar[date].entries])
            blocks = "\n".join(
                (f"  {b}: {t}" for b, t in self.calendar[date].available_dict.items())
            )
            total_before = self.calendar[date].total_available
            total_after = total_before - sum(
                (task.remaining_duration for task in self.plan_dict[date])
            )
            empty_before = self.calendar[date].empty_time
            empty_after = empty_before - sum(
                (
                    task.remaining_duration
                    for task in self.plan_dict[date]
                    if not task.block_assigned
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
                for d, ids in self.items()
            ]
        )

    def __repr__(self) -> str:
        return self.__str__()


# pure
def add_tasks(plan: Plan, date: PDate, tasks: Iterable[Task]) -> tuple[Plan, Tasks]:
    """
    Add tasks to a specified date in the plan. If the tasks exceed the date's available time,
      the lowest-priority excess task ids are returned.
    """
    plan.ensure_date(date)
    tasks = Tasks(tasks) + plan.plan_dict.get(date, [])
    avail_dict = plan.calendar[date].available_dict

    blocked_tasks: Tasks = tasks.pop_tasks_from_blocks(avail_dict)
    excess = tasks.pop_excess_tasks(avail_dict["wildcard"])

    tasks.extend(blocked_tasks)
    tasks.sort(key=lambda t: t.priority)
    tasks.update_tmpdate(date)
    tasks.update_original_date(date)

    plan.plan_dict.update({date: tasks})
    return plan, excess


# pure
def update_plan(  # add_subplan(
    plan: Plan,
    subplan: dict[PDate, Tasks],
) -> Plan:
    """
    Adds subplan (like plan, but corresponding to single project) to the plan,
      rolling tasks over when the daily maximum is exceeded, according to priority.
    """
    for date, tasks_ in subplan.items():
        plan, rollover = add_tasks(plan, date, tasks_)

        while rollover:
            next_date = date.copy()
            plan, rollover = add_tasks(plan, next_date, rollover)
            next_date += 1

    return plan
