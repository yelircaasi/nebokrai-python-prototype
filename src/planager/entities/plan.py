from pathlib import Path
from typing import Optional

from planager.config import config
from planager.config import _Config as ConfigType
from planager.entities import Calendar, Project


class Plan:
    def __init__(
            self,
            config: Optional[ConfigType] = None,
            calendar: Optional[Calendar] = None,
        ) -> None:
        ...

    def add_tasks_from_project(self, project: Project) -> None:
        ...


class PlanPatch:
    def __init__(self) -> None:
        ...


class PlanPatches:
    def __init__(self) -> None:
        ...

    @classmethod
    def from_norg_workspace(workspace_root: Path) -> "PlanPatches":
        patches = ...
        return patches
