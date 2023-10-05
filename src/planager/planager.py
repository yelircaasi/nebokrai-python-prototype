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
    Schedule,
    Schedules,
    Task,
    TaskPatches,
    Tasks,
)
from .operator import Planner, Scheduler
from .util import ConfigType, PDate, PathManager


class Planager:
    path_manager: PathManager
    calendar: Calendar
    roadmaps: Roadmaps
    routines: Routines
    plan: Optional[Plan] = None
    schedules: Optional[Schedules] = None

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
        # routines = Routines.from_dict(dec["routines"])
        routines = Routines()

        return cls(calendar, roadmaps, routines, pathmanager)

    # @classmethod
    # def from_html(cls, html_dir: Path) -> "Planager":

    #     return cls()

    def derive(self) -> None:
        """
        Derives plan and schedules from declarations.
        """

        # tasks = roadmaps.tasks  # Tasks.from_roadmaps(roadmaps)
        self.plan = self.planner(self.calendar, self.roadmaps)
        # schedules = self.scheduler(
        #     self.calendar,
        #     self.plan,
        #     self.roadmaps,
        #     self.routines,
        # )

    # def reconfigure(self, config: ConfigType) -> None:
    #     ...

    # def write_norg(self) -> None:
    #     """
    #     Writes derivation to norg workspace.
    #     """

    def write_json(self) -> None:
        """
        Writes derivation to json folder.
        """

    # def write_html(self) -> None:
    #     """
    #     Writes derivation to html folder.
    #     """

    def roadmap_tree(self) -> str:
        lines = []
        for roadmap in self.roadmaps:
            lines.append(f"{roadmap.name} (ID {roadmap.roadmap_id})")
            for project in roadmap:
                lines.append(f"    {project.name} (ID {project.project_id})")
                for task in project:
                    lines.append(f"        {task.name} (ID {task.task_id})")
        return "\n".join(lines)

    def make_gantt_string(self, raw: bool = False) -> str:
        LENGTH = 30

        today = PDate.today()
        # end_date = self.plan.end_date
        end_date = PDate.today() + 400

        def make_project_line(project: Project) -> str:
            def get_dates(project: Project, raw: bool) -> dict[PDate, str]:
                if raw:
                    return {
                        d: project[l[-1][-1]].status for d, l in project.subplan.items()
                    }
                else:
                    assert (
                        self.plan
                    ), "Plan must be defined in order to be shown as a gantt."
                    rcode, pcode = project.project_id
                    ret: dict[PDate, str] = {}
                    for date, task_ids in self.plan.items():
                        rel_ids = [
                            (r, p, _)
                            for (r, p, _) in task_ids
                            if (r == rcode and p == pcode)
                        ]
                        if rel_ids:
                            task_id = rel_ids[0]
                            ret.update({date: self.roadmaps.get_task(task_id).status})

                    return ret

            def format_name(proj_name: str) -> str:
                if len(proj_name) <= LENGTH:
                    return f"{proj_name: <{LENGTH}} ║ "
                else:
                    return proj_name[: (LENGTH - 6)] + "…" + proj_name[-5:] + " ║ "

            status2char = {"todo": "○", "done": "●"}
            line = format_name(project.name)

            dates = get_dates(project, raw)
            middle = ""

            if not dates:
                return ""
            elif len(dates) == 1:
                middle += status2char[dates[min(dates)]]
            else:
                middle += status2char[dates[min(dates)]]
                for d1, d2 in zip(sorted(list(dates))[:-1], sorted(list(dates))[1:]):
                    if d1 >= today:
                        middle += (d1.daysto(d2) - 1) * "―" + status2char[dates[d2]]

            line += (
                (today.daysto(min(dates)) * " ")
                + middle
                + (max(dates).daysto(end_date) * " ")
            )
            # print(len(line))
            # print(line)
            return line

        roadmap_dict = {r.roadmap_id: i for i, r in enumerate(self.roadmaps)}
        lines = [
            (roadmap_dict[project.project_id[0]], make_project_line(project))
            for project in self.roadmaps.projects
        ]
        lines = list(filter(lambda x: x[1] != "", lines))
        myfind = lambda s, sub: s.find(sub) + 999 * (s.find(sub) < 0)
        myrfind = lambda s, sub: s.rfind(sub) + 999 * (s.rfind(sub) < 0)
        # lines.sort(key=lambda line: (line[0], min(myfind(line[1], '○'), myfind(line[1], '●')), min(myrfind(line[1], '○'), myrfind(line[1], '●'))))
        lines.sort(
            key=lambda line: (
                min(myfind(line[1], "○"), myfind(line[1], "●")),
                min(myrfind(line[1], "○"), myrfind(line[1], "●")),
                line[0],
            )
        )

        def make_header() -> str:
            chars = []
            t = PDate.today()
            maxlen = max(map(len, map(lambda x: x[1], lines)))
            for d in t.range(maxlen):
                chars.append(
                    ("║" * (d.month == 1 and d.day == 1) + "│" * (d.day == 1) + " ")[0]
                )

            return LENGTH * " " + " ║ " + "".join(chars)

        line1 = make_header()
        gantt = "\n".join([line1, line1, ""]) + "\n".join(map(lambda x: x[1], lines))
        # print(gantt)
        return gantt

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
