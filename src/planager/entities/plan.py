from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

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

    # def add_tasks_from_project(self, project: Project) -> None:
    #     ...

    def add_tasks(tasks: Tasks) -> None:
        ...

    def add_subplan(
        self,
        subplan: Dict[PDate, Union[List[int], List[Tuple[int, int, int]]]],
        tasks: Tasks,
        plan_id: Optional[Tuple[int, int]] = None,
    ) -> None:
        id_ = list(subplan.values())[0][0]
        if not (
            (plan_id and isinstance(id_, int))
            or ((not plan_id) and (isinstance(id_, tuple)))
        ):
            raise ValueError("plan_id and task id must be of compatible types.")

        for task in tasks:
            print(task)
            self._tasks.update({(*plan_id, task.id) if plan_id else task.id: task})
        for date, task_list in subplan:
            print(date)
            for task_id in task_list:
                if isinstance(task_id, int):
                    new_task_id: Tuple[int, int, int] = (*plan_id, task_id)
                else:
                    new_task_id: Tuple[int, int, int] = (*task_id,)
                self._plan[date].append(new_task_id)

    @property
    def end_date(self) -> PDate:
        return max(self._plan)

    @property
    def start_date(self) -> PDate:
        return min(self._plan)


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
