from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from .entity import (
    AdHoc,
    Calendar,
    Plan,
    PlanPatches,
    Project,
    Projects,
    Roadmap,
    Roadmaps,
    Routines,
    SchedulePatches,
    Schedules,
    Task,
    TaskPatches,
    Tasks,
)
from .operator import Planner, Scheduler
from .util import ConfigType, PDateTime


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
        self.plan = Plan()
        self.schedules = Schedules()

        self.planner = Planner()
        self.scheduler = Scheduler()

        self.plan_patches = PlanPatches()
        self.schedule_patches = SchedulePatches()
        self.task_patches = TaskPatches()

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
        plgr.schedule_patches = SchedulePatches.from_norg_workspace(workspace)
        plgr.calendar = Calendar.from_norg_workspace(workspace)
        plgr.tasks = Tasks.from_roadmaps(plgr.roadmaps)

        # operators
        plgr.planner = Planner(config)
        plgr.scheduler = Scheduler(config)

        # derivation
        plgr.plan = plgr.planner(
            plgr.roadmaps,
            plgr.tasks,
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

    def __getitem__(self, __key: Union[str, tuple]) -> Union[Roadmap, Project, Task]:
        if isinstance(__key, str):
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

    @staticmethod
    def setup_from_norg_workspace(
        workspace: Path,
    ) -> Tuple[
        Calendar,
        Roadmaps,
        Routines,
        AdHoc,
        PlanPatches,
        SchedulePatches,
        TaskPatches,
    ]:
        """
        Obtains all declaration information needed to perform a derivation.
        """
        calendar = Calendar.from_norg_workspace(workspace)
        roadmaps = Roadmaps.from_norg_workspace(workspace)
        routines = Routines.from_norg_workspace(workspace)
        adhoc = AdHoc.from_norg_workspace(workspace)
        plan_patches = PlanPatches.from_norg_workspace(workspace)
        schedule_patches = SchedulePatches.from_norg_workspace(workspace)
        task_patches = TaskPatches.from_norg_workspace(workspace)
        return (
            calendar,
            roadmaps,
            routines,
            adhoc,
            plan_patches,
            schedule_patches,
            task_patches,
        )

    @staticmethod
    def derive(
        planner: Planner,
        scheduler: Scheduler,
        calendar: Calendar,
        roadmaps: Roadmaps,
        routines: Routines,
        adhoc: AdHoc,
        plan_patches: PlanPatches,
        schedule_patches: SchedulePatches,
        task_patches: TaskPatches,
    ) -> Tuple[Plan, Schedules]:
        """
        Derives plan and schedules from declarations.
        """

        tasks = Tasks.from_roadmaps(roadmaps)
        plan = planner(roadmaps, tasks, calendar, task_patches, plan_patches)
        schedules = scheduler(
            plan,
            tasks,
            routines,
            adhoc,
            schedule_patches,
            calendar.start_date,
            calendar.end_date,
        )
        return (plan, schedules)

    def write_norg(self) -> None:
        """
        Writes derivation to norg workspace.
        """
