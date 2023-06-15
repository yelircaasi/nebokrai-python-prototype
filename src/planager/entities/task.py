from pathlib import Path
from typing import Dict, List, Optional

from planager.config import _Config as ConfigType
from planager.entities import Calendar, Project, Tasks
from planager.utils.datetime_extensions import PDate
from planager.utils.data.norg.norg_utils import Norg, norg_utils as norg



class Task:
    def __init__(self) -> None:
        self.x = ...


class Tasks:
    def __init__(self) -> None:
        ...

    def __getitem__(self, __name: str) -> Any:
        task = ...
        return task
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...


class TaskPatch:
    def __init__(self) -> None:
        self.x = ...


class TaskPatches:
    def __init__(self) -> None:
        ...

    def __getitem__(self, __name: str) -> Any:
        task = ...
        return task
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
    
    @classmethod
    def from_norg_workspace(workspace_root: Path) -> "TaskPatches":
        patches = ...
        return patches