from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union
from itertools import chain

from ...util import ConfigType, PDate
from ..container.tasks import Tasks
from .calendar import Calendar
from .task import Task


class Plan:
    def __init__(
        self,
        config: Optional[ConfigType] = None,
        calendar: Optional[Calendar] = None,
    ) -> None:
        self._config = config
        self._calendar = calendar
        self._tasks: dict[tuple[str, str, str], Task] = {}
        self._plan: dict[PDate, list[tuple[str, str, str]]] = {}

    def copy(self) -> "Plan":
        p = Plan(self._config, self._calendar)
        p._tasks = self._tasks
        p._plan = self._plan
        return p

    def add_tasks(
        self, date: PDate, task_ids: List[Tuple[str, str, str]]
    ) -> List[Tuple[str, str, str]]:
        """
        Add tasks to a specified date in the plan. If the tasks exceed the date's max_load, the lowest-priority excess
          task ids are returned.
        """
        # task_ids = [task.task_id for task in tasks]
        if date in self._plan:
            task_ids = sorted(
                list(set(task_ids + self._plan[date])),
                key=lambda x: self._tasks[x].priority,
                reverse=True,
            )
        excess: List[Tuple[str, str, str]] = []
        total = sum(map(lambda _id: self._tasks[_id].duration, task_ids))
        max_load = self._calendar[date].max_load if self._calendar else 240

        while total > max_load:
            task_to_move = task_ids.pop()
            excess.append(task_to_move)
            total -= self._tasks[task_to_move].duration

        self._plan.update({date: task_ids})
        for task_id in task_ids:
            self._tasks[task_id].tmpdate = date
        return excess

    def add_subplan(
        self,
        subplan: Dict[PDate, List[Tuple[str, str, str]]],
        tasks: Tasks,
    ) -> None:
        """
        Adds subplan (like plan, but corresponding to single project) to the plan, rolling tasks over when the daily
          maximum is exceeded, according to priority.
        """
        if not subplan:
            return
        id_ = list(subplan.values())[0][0]

        for task in tasks:
            self._tasks.update({task.task_id: task})

        for date, task_id_list in subplan.items():
            self.ensure_date(date)
            rollover: List[Tuple[str, str, str]] = self.add_tasks(date, task_id_list)
            next_date = date.copy()
            while rollover:
                rollover = self.add_tasks(next_date, rollover)
                next_date += 1

    def ensure_date(self, date: PDate):
        """ """
        if not date in self._plan.keys():
            self._plan.update({date: []})

    @property
    def end_date(self) -> PDate:
        return max(self._plan)

    @property
    def start_date(self) -> PDate:
        return min(self._plan)

    @property
    def tasks(self) -> List[Task]:
        return sorted(self._tasks.values())

    # def reorder_by_precedence(self) -> None:
    #     """

    #     """
    #     tasks = list(map(lambda t: self._tasks[t.task_id], self.tasks))
    #     newtasks = []
    #     self._plan = {}
    #     for t, pre, post in zip(tasks[:-2], tasks[1:-1], tasks[2:]):
    #         newtask = self.adjust_tmpdate_to_neighbors(t, pre, post)
    #         newtasks.append(newtask)
    #         if not newtask.tmpdate in self._plan:
    #             self._plan.update({newtask.tmpdate: []})
    #         self._plan[t.tmpdate].append(newtask.task_id)

    @staticmethod
    def adjust_tmpdate_to_neighbors(t: Task, pre: Task, post: Task) -> Task:
        """ """
        new_t = t.copy()
        if pre <= new_t <= post:
            return new_t
        else:
            limit_before = int(pre.tmpdate) + int(new_t.isafter(pre))
            limit_after: int = int(post.tmpdate) + int(post.isafter(new_t))
            if not limit_before <= limit_after:
                raise ValueError("Impossible task precedence resolution requested.")
            new_t.tmpdate = PDate.fromordinal(int((limit_before + limit_after) / 2))
            return new_t

    def __contains__(self, __date: PDate) -> bool:
        return __date in self._plan

    def __getitem__(self, __date: PDate) -> List[Tuple[str, str, str]]:
        return self._plan.get(__date, [])

    def __setitem__(self, __date: PDate, __tasks: List[Tuple[str, str, str]]) -> None:
        self._plan.update({__date: __tasks})

    def __str__(self) -> str:
        nl = "\n"
        box = lambda s: f"┏━{len(str(s)) * '━'}━┓\n┃ {s} ┃\n┗━{len(str(s)) * '━'}━┛"
        task_repr = lambda t: f"[{t.project_name[:40]}] <> {t.name}"
        return "\n".join(
            (
                f"{box(a)}\n{nl.join(map(task_repr, [self._tasks[task_id] for task_id in b]))}"
                for a, b in sorted(self._plan.items())
            )
        )

    def __repr__(self) -> str:
        return self.__str__()
