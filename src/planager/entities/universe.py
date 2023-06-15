from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING

from planager.entities import (
    AdHoc,
    Calendar,
    Entry,
    Plan,
    PlanPatch,
    PlanPatches,
    Project,
    Projects,
    Roadmap,
    Roadmaps,
    Routine,
    Routines,
    Schedule,
    Schedules,
    SchedulePatch,
    SchedulePatches,
    Task,
    Tasks,
    TaskPatch,
    TaskPatches,
)
from planager.operators import (
    Planner,
    Scheduler,
)
from planager.utils.datetime_extensions import PDateTime                                          # util:      1
if TYPE_CHECKING:
    from planager.config import _Config as ConfigType                                             # config: 


class Universe:
    files = []
    roadmaps: Roadmaps
    adhoc: AdHoc
    projects: Projects
    tasks: Tasks
    routines: Routines
    plan: Plan
    schedules: Schedules

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
        self.roadmaps   = Roadmaps()
        self.adhoc      = AdHoc()
        self.projects   = Projects()
        self.tasks      = Tasks()
        self.routines   = Routines()
        self.plan: Plan = Plan()
        self.schedules  = Schedules()

        self.planner   = Planner()
        self.scheduler = Scheduler()
        
        self.plan_patches     = List[PlanPatch] = []
        self.schedule_patches = List[SchedulePatch] = []
        self.task_patches     = List[TaskPatch] = []

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
        config: "ConfigType"
        ) -> "Universe":
        
        univ = cls()

        # direct reading
        univ.roadmaps         = Roadmaps.from_norg_workspace(workspace)
        univ.routines         = Routines.from_norg_workspace(workspace)
        univ.adhoc            = AdHoc.from_norg_workspace(workspace)
        univ.plan_patches     = PlanPatches.from_norg_workspace(workspace)
        univ.task_patches     = TaskPatches.from_norg_workspace(workspace)
        univ.schedule_patches = SchedulePatches.from_norg_workspace(workspace)
        
        # operators
        univ.planner     = Planner(config)
        univ.scheduler   = Scheduler(config)
        
        # derivation
        univ.plan: Plan = univ.planner(
            univ.projects,
            univ.calendar,
            univ.task_patches,
            univ.plan_patches,
        )
        univ.schedules: Schedules = univ.scheduler(
            univ.plan, 
            univ.routines, 
            univ.adhoc, 
            univ.schedule_patches,
        )

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

    def reconfigure(self, conig: ConfigType) -> None:

        ...
