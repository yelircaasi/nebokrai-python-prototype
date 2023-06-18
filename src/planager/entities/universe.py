from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from planager.config import ConfigType
from planager.entities import (AdHoc, Calendar, Entry, Plan, PlanPatch,
                               PlanPatches, Project, Projects, Roadmap,
                               Roadmaps, Routine, Routines, Schedule,
                               SchedulePatch, SchedulePatches, Schedules, Task,
                               TaskPatch, TaskPatches, Tasks)
from planager.operators import Planner, Scheduler
from planager.utils.datetime_extensions import PDateTime  # util:      1


class Universe:
    files = []
    roadmaps: Roadmaps
    adhoc: AdHoc
    projects: Projects
    tasks: Tasks
    routines: Routines
    plan: Plan
    schedules: Schedules
    calendar: Calendar

    planner: Planner
    scheduler: Scheduler

    plan_patches: List[PlanPatch]
    schedule_patches: List[SchedulePatch]
    task_patches: List[TaskPatch]
    last_update: Optional[PDateTime]
    deps_highlevel: Dict
    deps_lowlevel: Dict
    norg_workspace: Optional[Path]
    json_dir: Optional[Path]
    html_dir: Optional[Path]

    def __init__(self) -> None:
        self.files = []
        self.roadmaps = Roadmaps()
        self.adhoc = AdHoc()
        self.projects = Projects()
        self.tasks = Tasks()
        self.routines = Routines()
        self.plan: Plan = Plan()
        self.schedules = Schedules()

        self.planner = Planner()
        self.scheduler = Scheduler()

        self.plan_patches: List[PlanPatch] = []
        self.schedule_patches: List[SchedulePatch] = []
        self.task_patches: List[TaskPatch] = []

        self._last_update: Optional[PDateTime] = None
        self.deps_highlevel = {}
        self.deps_lowlevel = {}
        self.norg_workspace: Optional[Path] = None
        self.json_dir: Optional[Path] = None
        self.html_dir: Optional[Path] = None

    @classmethod
    def from_norg_workspace(
        cls,
        workspace: Path,
        config: Optional[ConfigType] = None,
    ) -> "Universe":
        univ = cls()

        # direct reading
        univ.roadmaps = Roadmaps.from_norg_workspace(workspace)
        univ.routines = Routines.from_norg_workspace(workspace)
        univ.adhoc = AdHoc.from_norg_workspace(workspace)
        univ.plan_patches = PlanPatches.from_norg_workspace(workspace)  # STILL EMPTY
        univ.task_patches = TaskPatches.from_norg_workspace(workspace)  # STILL EMPTY
        univ.schedule_patches = SchedulePatches.from_norg_workspace(
            workspace
        )  # STILL EMPTY
        univ.calendar = Calendar.from_norg_workspace(workspace)

        # operators
        univ.planner = Planner(config)
        univ.scheduler = Scheduler(config)

        # derivation
        univ.plan: Plan = univ.planner(
            univ.projects,
            univ.calendar,
            univ.task_patches,
            univ.plan_patches,
        )
        """
        univ.schedules: Schedules = univ.scheduler(
            univ.plan, 
            univ.routines, 
            univ.adhoc, 
            univ.schedule_patches,
        )
        """
        return univ

    @classmethod
    def from_json_dir(cls, workspace: Path) -> "Universe":
        return cls()

    @classmethod
    def from_html_dir(cls, workspace: Path) -> "Universe":
        return cls()

    def recalculate_norg(self) -> None:
        ...

    def recalculate_json(self) -> None:
        ...

    def recalculate_html(self) -> None:
        ...

    def reconfigure(self, config: ConfigType) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __getitem__(self, __key: Union[int, tuple]) -> Routine:
        if isinstance(__key, int):
            return self.roadmaps[__key]
        match len(__key):
            case 2:
                r, p = __key
                return self.roadmaps[r].projects[p]
            case 3:
                r, p, t = __key
                return self.roadmaps[r].projects[p].tasks[t]
            case _:
                raise KeyError(f"Key '{__key}' invalid for 'Universe' object.")

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
