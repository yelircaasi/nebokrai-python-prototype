from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

from planager.config import _Config as ConfigType
from planager.config import config
from planager.utils.algorithms.planning import SubplanType
from planager.utils.data.norg import norg_utils as norg
from planager.utils.data.norg.norg_utils import Norg
from planager.utils.datetime_extensions import PDate

from .calendar import Calendar
from .project import Project
from .task import Task, Tasks


class Plan:
    def __init__(
        self,
        config: Optional[ConfigType] = None,
        calendar: Optional[Calendar] = None,
    ) -> None:
        self._config = config
        self._calendar = calendar
        self._tasks: Dict[Tuple[int, int, int], Task] = {}
        self._plan: Dict[PDate, List[Tuple[int, int, int]]] = {}

    def __getitem__(self, __date: PDate) -> List[Tuple[int, int, int]]:
        return self._plan[__date]

    def __setitem__(self, __date: PDate, __tasks: List[Tuple[int, int, int]]) -> None:
        self._plan.update({__date: __tasks})

    # def add_tasks_from_project(self, project: Project) -> None:
    #     TODO

    def add_tasks(self, date: PDate, tasks: Union[Tasks, Iterable[Task]]) -> None:
        task_ids = [task.id for task in tasks]
        if date in self._plan:
            task_ids = list(set(task_ids + self._plan[date]))
        self._plan.update({date: task_ids})

    def add_subplan(
        self,
        subplan: Dict[PDate, List[Tuple[int, int, int]]],
        tasks: Tasks,
        # plan_id: Optional[Tuple[int, int]] = None,
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
            #print(task)
            self._tasks.update({task.id: task})
        for date, task_list in subplan.items():
            #print(date)
            for task_id in task_list:
                # if isinstance(task_id, int):
                #     new_task_id: Tuple[int, int, int] = (*plan_id, task_id)
                # else:
                #     new_task_id: Tuple[int, int, int] = (*task_id,)
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
        nl = '\n'
        box = lambda s: f"┏━{len(str(s)) * '━'}━┓\n┃ {s} ┃\n┗━{len(str(s)) * '━'}━┛"
        task_repr = lambda t: f"[{t.project_name[:40]}] :: {t.name}"
        return '\n'.join((f"{box(a)}\n{nl.join(map(task_repr, [self._tasks[id] for id in b]))}" for a, b in sorted(self._plan.items())))
    
    def __repr__(self) -> str:
        #print("plan")
        return self.__str__()
        

class PlanPatch:
    def __init__(self) -> None:
        ...


class PlanPatches:
    def __init__(self, patches: List[PlanPatch] = []) -> None:
        self.patches = patches

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "PlanPatches":
        # file = workspace_dir / "roadmaps.norg"
        # parsed = Norg.from_path(file)
        # ...
        # return cls()
        return cls()
