from pathlib import Path
from typing import Optional


class PathManager:
    adhoc: Path
    calendar: Path
    config: Path
    default_day: Path
    habits: Path
    routines: Path
    plan_patches: Path
    roadmaps: Path
    schedule_patches: Path
    task_patches: Path

    calendar_folder: Path
    completed_folder: Path
    plan_folder: Path
    projects_folder: Path
    roadmaps_folder: Path
    schedules_folder: Path
    tasks_folder: Path

    def __init__(self, folder: Optional[Path] = None) -> None:
        self.folder = folder
        self.filetype = ...

    def __bool__(self) -> bool:
        return self.folder is not None
