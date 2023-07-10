from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .config import ConfigType
from .entity.base.adhoc import AdHoc
from .entity.base.calendar import Calendar
from .entity.base.plan import Plan
from .entity.base.project import Project
from .entity.base.roadmap import Roadmap
from .entity.base.task import Task
from .entity.container.projects import Projects
from .entity.container.roadmaps import Roadmaps
from .entity.container.routines import Routines
from .entity.container.schedules import Schedules
from .entity.container.tasks import Tasks
from .entity.patch.plan_patch import PlanPatches
from .entity.patch.schedule_patch import SchedulePatches
from .entity.patch.task_patch import TaskPatches
from .operators import Planner, Scheduler
from .util.pdatetime import PDateTime  # util:      1


class Planager:
    files: List[str] = []
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

    plan_patches: PlanPatches
    schedule_patches: SchedulePatches
    task_patches: TaskPatches
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

        self.plan_patches: PlanPatches = PlanPatches()
        self.schedule_patches: SchedulePatches = SchedulePatches()
        self.task_patches: TaskPatches = TaskPatches()

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
    ) -> "Planager":
        plgr = cls()

        # direct reading
        plgr.roadmaps = Roadmaps.from_norg_workspace(workspace)
        plgr.routines = Routines.from_norg_workspace(workspace)
        plgr.adhoc = AdHoc.from_norg_workspace(workspace)
        plgr.plan_patches = PlanPatches.from_norg_workspace(workspace)  # STILL EMPTY
        plgr.task_patches = TaskPatches.from_norg_workspace(workspace)  # STILL EMPTY
        plgr.schedule_patches = SchedulePatches.from_norg_workspace(
            workspace
        )  # STILL EMPTY
        plgr.calendar = Calendar.from_norg_workspace(workspace)
        plgr.tasks = Tasks.from_roadmaps(plgr.roadmaps)

        # operators
        plgr.planner = Planner(config)
        plgr.scheduler = Scheduler(config)

        # derivation
        plgr.plan = plgr.planner(
            plgr.roadmaps,
            plgr.calendar,
            plgr.task_patches,
            plgr.plan_patches,
        )
        print(plgr.schedules)
        plgr.schedules = plgr.scheduler(
            plgr.plan,
            plgr.tasks,
            plgr.routines,
            plgr.adhoc,
            plgr.schedule_patches,
        )
        return plgr

    @classmethod
    def from_json(cls, json_dir: Path) -> "Planager":
        return cls()

    @classmethod
    def from_html(cls, html_dir: Path) -> "Planager":
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
        return "\n\n".join(
            (
                self.roadmap_tree(),
                str(self.routines),
                str(self.adhoc),
                str(self.plan),
                # self.schedule,
            )
        )

    def __repr__(self) -> str:
        return self.__str__()

    def roadmap_tree(self) -> str:
        lines = []
        for roadmap in self.roadmaps:
            lines.append(f"{roadmap.name} (ID {roadmap.id})")
            for project in roadmap:
                lines.append(f"    {project.name} (ID {project.id})")
                for task in project:
                    lines.append(f"        {task.name} (ID {task.id})")
        return "\n".join(lines)

    def __getitem__(self, __key: Union[int, tuple]) -> Union[Roadmap, Project, Task]:
        if isinstance(__key, int):
            return self.roadmaps[__key]
        match len(__key):
            case 2:
                r, p = __key
                return self.roadmaps[r]._projects[p]
            case 3:
                r, p, t = __key
                return self.roadmaps[r]._projects[p].tasks[t]
            case _:
                raise KeyError(f"Key '{__key}' invalid for 'Planager' object.")

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
