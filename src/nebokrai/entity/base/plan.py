import json
from itertools import chain
from pathlib import Path
from typing import Iterable, Iterator

from ...util import NKDate
from ...util.serde.custom_dict_types import DeclarationDictRaw, PlanDictRaw
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
        self.plan_dict: dict[NKDate, Tasks] = {date: Tasks() for date in calendar}

    def serialize(self) -> PlanDictRaw:
        return {str(date): tasks.serialize() for date, tasks in self.plan_dict.items()}

    @classmethod
    def deserialize(
        cls, declaration_dict: DeclarationDictRaw, plan_derivation_dict: PlanDictRaw
    ) -> "Plan":
        """
        Instantiate Plan object from dictionary corresponding to JSON format.
        """

        routines = Routines.deserialize(declaration_dict["routines"])
        calendar_dict = declaration_dict["calendar"]
        plan = cls(calendar=Calendar.deserialize(routines, calendar_dict))
        plan.plan_dict = cls.deserialize_plan_dict(plan_derivation_dict)
        plan.tasks = Tasks(chain.from_iterable(plan.plan_dict.values()))

        return cls(calendar=Calendar.deserialize(routines, calendar_dict))

    @classmethod
    def from_derivation(cls, declaration_path: Path, plan_derivation_path: Path) -> "Plan":  # TODO
        """
        Reads a saved plan in .json format.
        """
        with open(declaration_path, encoding="utf-8") as f:
            declaration = json.load(f)
        with open(plan_derivation_path, encoding="utf-8") as f:
            plan_derivation = json.load(f)

        return cls.deserialize(declaration, plan_derivation)

    @staticmethod
    def deserialize_plan_dict(plan_derivation_dict: PlanDictRaw) -> dict[NKDate, Tasks]:
        return {
            NKDate.from_string(date): Tasks.deserialize(tasks)
            for date, tasks in plan_derivation_dict.items()
        }

    @property
    def inverse(self) -> dict[Task, NKDate]:
        """
        Returns a dictionary mapping tasks to dates.
        """
        inverse_plan: dict[Task, NKDate] = {}
        for date, tasks_ in self.items():
            for task_ in tasks_:
                inverse_plan.update({task_: date})
        return inverse_plan

    def ensure_date(self, date: NKDate):
        if date not in self.plan_dict:
            self.plan_dict.update({date: Tasks()})

    @property
    def end_date(self) -> NKDate:
        return max(self.plan_dict)

    @property
    def start_date(self) -> NKDate:
        return min(self.plan_dict)

    def fill_empty(self) -> None:
        """
        Add an empty Tasks instance to days missing.
        """
        for date in self.start_date.range(self.end_date):
            if date not in self.plan_dict:
                self.plan_dict.update({date: Tasks()})

    def items(self) -> Iterator[tuple[NKDate, Tasks]]:
        return iter(self.plan_dict.items())

    def __iter__(self) -> Iterator[NKDate]:
        return iter(self.plan_dict.keys())

    def __contains__(self, __date: NKDate) -> bool:
        return __date in self.plan_dict

    def __getitem__(self, __date: NKDate) -> Tasks:
        return self.plan_dict[__date]

    def get(self, __date: NKDate, __default: Tasks = Tasks()) -> Tasks:
        return self.plan_dict.get(__date, __default)

    def __setitem__(self, __date: NKDate, __tasks: Tasks) -> None:
        self.plan_dict.update({__date: __tasks})

    @property
    def summary(self) -> str:
        return "Plan.summary property is not yet implemented."

    @property
    def gantt_view(self) -> str:
        """
        Creates a Gantt-style representation of the declaration and resulting plan.
        """
        project_name_max_length = 30

        linechar = "―"
        circles = {"todo": "○", "done": "●"}

        date2idx = {d: i for i, d in enumerate(min(self.plan_dict).range(max(self.plan_dict)))}
        ndays = len(date2idx)

        def format_name(proj_name: str) -> str:
            if len(proj_name) <= project_name_max_length:
                return f"{proj_name: <{project_name_max_length}} ║ "
            return proj_name[: (project_name_max_length - 6)] + "…" + proj_name[-5:] + " ║ "

        project_names = list(
            set(map(lambda t: t.project_name, chain.from_iterable(self.plan_dict.values())))
        )
        pname2idx = {p: i for i, p in enumerate(project_names)}

        grid = []
        for i in range(len(project_names)):
            line = ndays * [linechar]
            grid.append(line)

        for _date, _tasks in self.plan_dict.items():
            for task in _tasks:
                pnum = pname2idx[task.project_name]
                dnum = date2idx[_date]
                symbol = circles[task.status]
                grid[pnum][dnum] = symbol

        lines = list(map("".join, grid))
        line_tuples = sorted(
            zip(map(format_name, project_names), lines), key=lambda x: x[1], reverse=True
        )

        return "\n".join(map("".join, line_tuples))

    def __str__(self) -> str:
        def task_repr(task: Task, date: NKDate) -> str:
            name = str(task.name) or str(task.task_id)
            orig = ("orig: " + str(task.original_date)) if task.original_date != date else ""
            return (
                f"{task.status_symbol} {task.project_name[:30]: <30}   {name[:30]: <30}   "
                f"pr {task.priority}     {task.duration}m   {orig}   {task.block_assigned}"
            )

        def time_repr(date: NKDate) -> str:
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
                f"Calendar entries: \n  {entry_names}\n"
                f"Blocks:\n{blocks}\n"
                "Total available on calendar:\n"
                f"  Before planning: {empty_before}m empty; {total_before}m including blocks\n"
                f"  After planning:  {empty_after}m empty; {total_after}m including blocks"
            )

        double_line = 120 * "═" + "\n"
        line = 120 * "─" + "\n"

        newl = "\n"
        return "\n".join(
            [
                (
                    f"{double_line}{str(d)}\n{line}{time_repr(d)}\n\n"
                    f"{newl.join([task_repr(t, d) for t in ids])}\n"
                )
                for d, ids in self.items()
            ]
        )

    def __repr__(self) -> str:
        return self.__str__()


def add_tasks(plan: Plan, date: NKDate, tasks: Iterable[Task]) -> tuple[Plan, Tasks]:
    """
    Add tasks to a specified date in the plan. If the tasks exceed the date's available time,
      the lowest-priority excess task ids are returned.
    """
    plan.ensure_date(date)
    tasks = Tasks(tasks) + plan.plan_dict.get(date, [])
    avail_dict = plan.calendar[date].available_dict

    blocked_tasks: Tasks = tasks.pop_tasks_from_blocks(avail_dict)
    excess = tasks.pop_excess_tasks(avail_dict["empty"])

    tasks.extend(blocked_tasks)
    tasks.sort(key=lambda t: t.priority)
    tasks.update_tmnkdate(date)
    tasks.update_original_date(date)

    plan.plan_dict.update({date: tasks})
    return plan, excess


def update_plan(
    plan: Plan,
    subplan: dict[NKDate, Tasks],
) -> Plan:
    """
    Adds subplan (like plan, but corresponding to single project) to the plan,
      rolling tasks over when the daily maximum is exceeded, according to priority.
    """
    for date, tasks_ in subplan.items():
        plan, rollover = add_tasks(plan, date, tasks_)

        next_date = date.copy()
        while rollover:
            plan, rollover = add_tasks(plan, next_date, rollover)
            next_date += 1

    return plan
