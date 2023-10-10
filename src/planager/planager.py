import json
from pathlib import Path
from typing import Any, Optional, Union

from .config import Config
from .entity import (
    Calendar,
    Day,
    Plan,
    Project,
    Projects,
    Roadmap,
    Roadmaps,
    Routines,
    Schedule,
    Schedules,
    Task,
)
from .util import PathManager, PDate, ProjectID, RoadmapID, TaskID


class Planager:
    """
    One class to rule them all.
    """

    path_manager: PathManager
    calendar: Calendar
    roadmaps: Roadmaps
    routines: Routines
    plan: Optional[Plan] = None
    schedules: Optional[Schedules] = None

    def __init__(self, config, calendar, roadmaps, routines, pathmanager) -> None:
        self.config = config
        self.calendar: Calendar = calendar
        self.roadmaps: Roadmaps = roadmaps
        self.routines: Routines = routines
        self.pathmanager: PathManager = pathmanager

    @classmethod
    def from_json(cls, json_root: Path) -> "Planager":
        """
        Instantiates from declaration.json.
        """

        pathmanager = PathManager(json_root)
        with open(pathmanager.declaration, encoding="utf-8") as f:
            dec = json.load(f)

        config = Config.from_dict(dec["config"])
        routines = Routines.from_dict(config, dec["routines"])
        calendar = Calendar.from_dict(config, routines, dec["calendar"])
        roadmaps = Roadmaps.from_dict(config, dec["roadmaps"])

        return cls(config, calendar, roadmaps, routines, pathmanager)

    def derive(self) -> None:
        """
        Derives plan and schedules from declarations.
        """

        self.plan = self.derive_plan(self.calendar, self.roadmaps)
        self.schedules = self.derive_schedules(
            self.calendar,
            self.plan,
            self.roadmaps,
        )

    def derive_plan(
        self,
        calendar: Calendar,
        roadmaps: Roadmaps,
    ) -> Plan:
        """
        Create the plan (the one instance of the `Plan` class) from the roadmaps and calendar,
          as well as task_patches and plan_patches. Designed to be:
          * declarative (user says what rather than how)
          * pure (no side effects)
          * deterministic (same input -> same output)
          This makes the automated planning process predictable and transparent.

        Not yet implemented:
          functionality for breaking up and reallocating clusters. -> Happens automatically?
        """
        plan = Plan(
            config=self.config,
            calendar=calendar,
        )

        projects = roadmaps.projects

        for project in projects.iter_by_priority:
            plan.add_subplan(project.subplan, project.tasks)

        self.enforce_precedence_constraints(plan, projects)

        return plan

    def derive_schedules(
        self,
        calendar: Calendar,
        plan: Plan,
        roadmaps: Roadmaps,
    ) -> Schedules:
        """
        Use information obtained from the declaration and the derived plan to derive,
          in turn, the schedules.
        """
        start_date_new = roadmaps.start_date or (PDate.tomorrow())
        end_date_new: PDate = roadmaps.end_date or max(
            plan.end_date,
            calendar.end_date,
        )
        schedules = Schedules(self.config, {})
        for date in start_date_new.range(end_date_new):
            schedule = Schedule.from_calendar(calendar, date)
            schedule.add_from_plan(plan, roadmaps.tasks)
            schedules[date] = schedule
        return schedules

    @staticmethod
    def enforce_precedence_constraints(plan: Plan, projects: Projects) -> None:
        """
        Checks that all temporal dependencies are respected and raises an informative
          error if that is not the case.
        """
        inverse_plan: dict[TaskID, PDate] = {}
        for date, ids in plan.items():
            for task_id in ids:
                inverse_plan.update({task_id: date})

        def get_date(_id: Union[TaskID, ProjectID]) -> PDate:
            if isinstance(_id, ProjectID):
                return max(map(lambda t: inverse_plan[t], (projects[_id])))
            if isinstance(_id, TaskID):
                return inverse_plan[projects.get_task(_id).task_id]
            raise ValueError("ID must have 2 or 3 elements.")

        for task in projects.tasks:
            if task.dependencies:
                plan_date = inverse_plan[task.task_id]
                limiting_dependency = max(task.dependencies, key=get_date)
                earliest_date = inverse_plan[limiting_dependency] + 1
                if plan_date < earliest_date:
                    raise ValueError(
                        (
                            f"Task {'<>'.join(task.task_id)} assigned to {plan_date}, "
                            f"but earliest permissible date is {earliest_date}."
                            "Please adjust the declaration and run the derivation again. \n  "
                            f"Limiting dependency: {'<>'.join(limiting_dependency)}."
                        )
                    )

    def write_json(self) -> None:
        """
        Writes derivation to json folder.
        """

    def roadmap_tree(self) -> str:
        """
        Prints the roadmap in a hierarchical tree representation.
        """
        lines = []
        for roadmap in self.roadmaps:
            lines.append(f"{roadmap.name} (ID {roadmap.roadmap_id})")
            for project in roadmap:
                lines.append(f"    {project.name} (ID {project.project_id})")
                for task in project:
                    lines.append(f"        {task.name} (ID {task.task_id})")
        return "\n".join(lines)

    def make_gantt_string(self, raw: bool = False) -> str:
        """
        Creates a Gantt-style representation of the declaration and resulting plan.
        """
        project_name_length = 30

        today = PDate.today()
        end_date = PDate.today() + 400

        def make_project_line(project: Project) -> str:
            def get_dates(project: Project, raw: bool) -> dict[PDate, str]:
                if raw:
                    return {
                        _date: project[_tasks[-1]].status
                        for _date, _tasks in project.subplan.items()
                    }

                assert self.plan, "Plan must be defined in order to be shown as a gantt."

                ret: dict[PDate, str] = {}
                for date, task_ids in self.plan.items():
                    relevant_ids = [
                        _task_id for _task_id in task_ids if _task_id in project.project_id
                    ]
                    if relevant_ids:
                        task_id = relevant_ids[0]
                        ret.update({date: self.roadmaps.get_task(task_id).status})

                return ret

            def format_name(proj_name: str) -> str:
                if len(proj_name) <= project_name_length:
                    return f"{proj_name: <{project_name_length}} ║ "
                return proj_name[: (project_name_length - 6)] + "…" + proj_name[-5:] + " ║ "

            status2char = {"todo": "○", "done": "●"}
            line = format_name(project.name)

            dates = get_dates(project, raw)
            middle = ""

            if not dates:
                return ""
            if len(dates) == 1:
                middle += status2char[dates[min(dates)]]
            else:
                middle += status2char[dates[min(dates)]]
                for d1, d2 in zip(sorted(list(dates))[:-1], sorted(list(dates))[1:]):
                    if d1 >= today:
                        middle += (d1.daysto(d2) - 1) * "―" + status2char[dates[d2]]

            line += (today.daysto(min(dates)) * " ") + middle + (max(dates).daysto(end_date) * " ")
            return line

        roadmap_dict = {r.roadmap_id: i for i, r in enumerate(self.roadmaps)}
        lines = [
            (roadmap_dict[project.project_id.roadmap_id], make_project_line(project))
            for project in self.roadmaps.projects
        ]
        lines = list(filter(lambda x: x[1] != "", lines))

        def myfind(s: str, sub: str) -> int:
            return s.find(sub) + 999 * (s.find(sub) < 0)

        def myrfind(s: str, sub: str) -> int:
            return s.rfind(sub) + 999 * (s.rfind(sub) < 0)

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
                chars.append(("║" * (d.month == 1 and d.day == 1) + "│" * (d.day == 1) + " ")[0])

            return project_name_length * " " + " ║ " + "".join(chars)

        line1 = make_header()
        gantt = "\n".join([line1, line1, ""]) + "\n".join(map(lambda x: x[1], lines))
        return gantt

    def __getitem__(
        self, __key: Union[RoadmapID, ProjectID, TaskID]
    ) -> Union[Roadmap, Project, Task, Day]:
        if isinstance(__key, RoadmapID):
            return self.roadmaps[__key]
        if isinstance(__key, ProjectID):
            return self.roadmaps[__key.roadmap_id][__key]
        if isinstance(__key, TaskID):
            return self.roadmaps[__key.roadmap_id][__key.project_id][__key]
        if isinstance(__key, PDate):
            return self.schedules[__key]
        raise KeyError(f"Invalid key for Planager object: {__key}")

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
