import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union

from .entity import (
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
from .util import ConfigType, PDateTime, PathManager


class Planager:
    path_manager: PathManager = PathManager()
    roadmaps: Roadmaps
    projects: Projects
    tasks: Tasks
    routines: Routines
    plan: Plan
    schedules: Schedules
    calendar: Calendar

    planner: Planner
    scheduler: Scheduler

    # plan_patches: PlanPatches
    # schedule_patches: SchedulePatches
    # task_patches: TaskPatches
    # _last_update: Optional[PDateTime]

    def __init__(self, calendar, roadmaps, routines, pathmanager) -> None:
        self.calendar: Calendar = calendar
        self.roadmaps: Roadmaps = roadmaps
        self.routines: Routines = routines
        self.pathmanager: PathManager = pathmanager

        # operators
        self.planner = Planner()  # config)
        self.scheduler = Scheduler()  # config)

    @classmethod
    def from_json(cls, json_root: Path) -> "Planager":
        pathmanager = PathManager(json_root)
        with open(pathmanager.declaration) as f:
            dec = json.load(f)

        # config = Config.from_dict(dec["config"])
        calendar = Calendar.from_dict(dec["calendar"])
        roadmaps = Roadmaps.from_dict(dec["roadmaps"])
        routines = Routines.from_dict(dec["routines"])

        return cls(calendar, roadmaps, routines, pathmanager)

    # @classmethod
    # def from_html(cls, html_dir: Path) -> "Planager":

    #     return cls()

    @staticmethod
    def derive(
        planner: Planner,
        scheduler: Scheduler,
        calendar: Calendar,
        roadmaps: Roadmaps,
        routines: Routines,
    ) -> tuple[Plan, Schedules]:
        """
        Derives plan and schedules from declarations.
        """

        tasks = roadmaps.tasks  # Tasks.from_roadmaps(roadmaps)
        plan = planner(roadmaps, calendar)
        schedules = scheduler(
            plan,
            calendar,
            tasks,
            routines,
            calendar.start_date,
            calendar.end_date,
        )
        return (plan, schedules)

    def reconfigure(self, config: ConfigType) -> None:
        ...

    def write_norg(self) -> None:
        """
        Writes derivation to norg workspace.
        """

    def write_json(self) -> None:
        """
        Writes derivation to json folder.
        """

    def write_html(self) -> None:
        """
        Writes derivation to html folder.
        """

    def roadmap_tree(self) -> str:
        lines = []
        for roadmap in self.roadmaps:
            lines.append(f"{roadmap.name} (ID {roadmap.roadmap_id})")
            for project in roadmap:
                lines.append(f"    {project.name} (ID {project.project_id})")
                for task in project:
                    lines.append(f"        {task.name} (ID {task.task_id})")
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

    def __str__(self) -> str:
        return "\n\n".join(
            (
                self.roadmap_tree(),
                str(self.routines),
                str(self.plan),
                # self.schedule,
            )
        )

    def __repr__(self) -> str:
        return self.__str__()
