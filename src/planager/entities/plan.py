from pathlib import Path
from typing import Dict, List, Optional

from planager.config import config
from planager.config import _Config as ConfigType
from .calendar import Calendar
from .project import Project
from .task import Tasks
from planager.utils.datetime_extensions import PDate
from planager.utils.data.norg.norg_utils import Norg
from planager.utils.data.norg import norg_utils as norg


class Plan:
    def __init__(
            self,
            config: Optional[ConfigType] = None,
            calendar: Optional[Calendar] = None,
        ) -> None:
        self.config = config
        self.calendar = calendar
        self.tasks = Tasks()

    # def add_tasks_from_project(self, project: Project) -> None:
    #     ...

    def add_tasks(tasks: Tasks) -> None:
        ...

    def add_subplan(
            self,
        subplan: Dict[PDate, List[int]],
        tasks: Tasks,
    ) -> None:
        
        self.tasks.merge(tasks)
        #self.



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