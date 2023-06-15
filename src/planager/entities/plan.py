from pathlib import Path
from typing import Dict, List, Optional

from planager.config import config
from planager.config import _Config as ConfigType
from planager.entities import Calendar, Project, Tasks
from planager.utils.datetime_extensions import PDate
from planager.utils.data.norg.norg_utils import Norg, norg_utils as norg


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
    def __init__(self) -> None:
        ...

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "PlanPatches":
        file = workspace_dir / "roadmaps.norg"
        parsed: Dict = Norg.from_path(file)
        ...
        return cls()