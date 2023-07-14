from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

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
        self._tasks: Dict[Tuple[str, str, str], Task] = {}
        self._plan: Dict[PDate, List[Tuple[str, str, str]]] = {}

    def __getitem__(self, __date: PDate) -> List[Tuple[str, str, str]]:
        return self._plan.get(__date, [])

    def __setitem__(self, __date: PDate, __tasks: List[Tuple[str, str, str]]) -> None:
        self._plan.update({__date: __tasks})

    # def add_tasks_from_project(self, project: Project) -> None:
    #     TODO

    def add_tasks(self, date: PDate, tasks: Union[Tasks, Iterable[Task]]) -> None:
        task_ids = [task.task_id for task in tasks]
        if date in self._plan:
            task_ids = list(set(task_ids + self._plan[date]))
        self._plan.update({date: task_ids})

    def add_subplan(
        self,
        subplan: Dict[PDate, List[Tuple[str, str, str]]],
        tasks: Tasks,
        # plan_id: Optional[Tuple[str, str]] = None,
    ) -> None:
        if not subplan:
            return
        id_ = list(subplan.values())[0][0]
        # if not (
        #     (plan_id and isinstance(id_, int))
        #     or ((not plan_id) and (isinstance(id_, tuple)))
        # ):
        #     raise ValueError("plan_id and task id must be of compatible types.")

        for task in tasks:
            self._tasks.update({task.task_id: task})
        for date, task_list in subplan.items():
            for task_id in task_list:
                # if isinstance(task_id, int):
                #     new_task_id: Tuple[str, str, str] = (*plan_id, task_id)
                # else:
                #     new_task_id: Tuple[str, str, str] = (*task_id,)
                self.ensure_date(date)
                self._plan[date].append(task_id)

    def ensure_date(self, date: PDate):
        if not date in self._plan.keys():
            self._plan.update({date: []})

    @property
    def end_date(self) -> PDate:
        return max(self._plan)

    @property
    def start_date(self) -> PDate:
        return min(self._plan)

    def __str__(self) -> str:
        nl = "\n"
        box = lambda s: f"┏━{len(str(s)) * '━'}━┓\n┃ {s} ┃\n┗━{len(str(s)) * '━'}━┛"
        task_repr = lambda t: f"[{t.project_name[:40]}] :: {t.name}"
        return "\n".join(
            (
                f"{box(a)}\n{nl.join(map(task_repr, [self._tasks[task_id] for task_id in b]))}"
                for a, b in sorted(self._plan.items())
            )
        )

    def __repr__(self) -> str:
        return self.__str__()
