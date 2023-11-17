import json
import re
from datetime import datetime
from typing import Any, Optional, Union

from .configuration import path_manager
from .entity import (
    Calendar,
    Day,
    Entries,
    Plan,
    Project,
    Projects,
    Roadmap,
    Roadmaps,
    Routines,
    Schedule,
    Schedules,
    Task,
    add_from_plan_and_excess,
    update_plan,
)
from .tracking.logs import Logs
from .util import PDate, ProjectID, RoadmapID, TaskID


class Planager:
    """
    One class to rule them all.
    """

    calendar: Calendar
    roadmaps: Roadmaps
    routines: Routines
    plan: Optional[Plan] = None
    schedules: Optional[Schedules] = None
    logs: Optional[Logs] = None
    declaration_edit_time: datetime
    plan_edit_time: datetime
    schedule_edit_time: datetime
    derivation: dict[str, Any]

    def __init__(self, calendar, roadmaps, routines) -> None:
        self.calendar: Calendar = calendar
        self.roadmaps: Roadmaps = roadmaps
        self.routines: Routines = routines

        with open(path_manager.edit_times, encoding="utf-8") as f:
            edit_times = json.load(f)

        def from_key(k: str) -> datetime:
            return datetime.fromisoformat(edit_times[k])

        self.declaration_edit_time = from_key("declaration_edit_time")
        self.plan_edit_time = from_key("plan_edit_time")
        self.schedule_edit_time = from_key("schedule_edit_time")

    @classmethod
    def from_json(cls) -> "Planager":
        """
        Instantiates from declaration.json.
        """

        with open(path_manager.declaration, encoding="utf-8") as f:
            dec = json.load(f)

        routines = Routines.from_dict(dec["routines"])
        calendar = Calendar.from_dict(routines, dec["calendar"])
        roadmaps = Roadmaps.from_dict(dec["roadmaps"])

        return cls(calendar, roadmaps, routines)

    def derive(self) -> None:
        """
        Derives plan and schedules from declarations.
        """

        self.plan = self.derive_plan()
        self.schedules = self.derive_schedules()

    def derive_plan(
        self,
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

        if self.plan_edit_time > self.declaration_edit_time:
            plan = Plan(
                calendar=self.calendar,
            )
        else:
            plan = Plan.from_path(path_manager.declaration)

        projects = self.roadmaps.projects

        for project in projects.iter_by_priority:
            plan = update_plan(plan, project.subplan)
            print(project.name)

        self.enforce_precedence_constraints(plan, projects)

        return plan

    def derive_schedules(self) -> Schedules:
        """
        Use information obtained from the declaration and the derived plan to derive,
          in turn, the schedules.
        """
        start_date_new, end_date_new = self.start_and_end_dates
        schedules, excess_entries = Schedules(), Entries()
        for date in start_date_new.range(end_date_new):
            schedule = Schedule.from_calendar(
                self.calendar, date
            )  # TODO: add .earliest and .latest to entries
            schedules[date], excess_entries = add_from_plan_and_excess(
                schedule, self.plan, excess_entries
            )
        return schedules

    @property
    def start_and_end_dates(self) -> tuple[PDate, PDate]:
        """
        Returns start and end date recovered from information in the  roadmaps.
        """
        assert self.plan
        start_date = self.roadmaps.start_date or (PDate.tomorrow())
        end_date: PDate = self.roadmaps.end_date or max(
            self.plan.end_date,
            self.calendar.end_date,
        )
        return start_date, end_date

    @staticmethod
    def enforce_precedence_constraints(plan: Plan, projects: Projects) -> None:
        """
        Checks that all temporal dependencies are respected and raises an informative
          error if that is not the case.
        """
        inverse_plan = plan.inverse

        def get_last_date(_id: Union[TaskID, ProjectID]) -> PDate:
            if isinstance(_id, ProjectID):
                return max(map(lambda t: inverse_plan[t], (projects[_id])))
            if isinstance(_id, TaskID):
                return inverse_plan[projects.get_task(_id)]
            raise ValueError(f"Invalid key for inverse plan [dict]: {_id} [{type(_id)}]")

        for task in filter(lambda t: bool(t.dependencies), projects.tasks):
            limiting_dep = projects.get_task(max(task.dependencies, key=get_last_date))
            if (plan_date := inverse_plan[task]) >= (earliest := inverse_plan[limiting_dep] + 1):
                continue
            raise ValueError(
                (
                    f"Task {'<>'.join(task.task_id)} assigned to {plan_date}, "
                    f"but earliest permissible date is {earliest}."
                    "  Please adjust the declaration and run the derivation again. \n  "
                    f"  Limiting dependency: {limiting_dep}."
                )
            )

    def track(self) -> None:
        print("Not yet implemented!")

    @staticmethod
    def shift_declaration(ndays: int) -> None:
        if not ndays:
            return None
        with open(path_manager.declaration, encoding="utf-8") as f:
            declaration_dict = json.load(f)
        with open(path_manager.tmp_declaration, "w", encoding="utf-8") as f:
            json.dump(declaration_dict, f, ensure_ascii=False, indent=4)
        roadmaps_dict = declaration_dict["roadmaps"]
        roadmaps_string = json.dumps(roadmaps_dict, ensure_ascii=False)

        all_dates = list(
            map(PDate.from_string, re.findall(r"(?<=\")\d{4}-\d\d-\d\d(?=\")", roadmaps_string))
        )
        min_date, max_date = min(all_dates), max(all_dates)
        print(min_date, max_date)
        date_range = max_date.range(min_date) if ndays > 0 else min_date.range(max_date)
        for date in date_range:
            roadmaps_string = roadmaps_string.replace(str(date), str(date + ndays))
        declaration_dict["roadmaps"] = json.loads(roadmaps_string)

        with open(path_manager.declaration, "w", encoding="utf-8") as f:
            json.dump(declaration_dict, f, indent=4, ensure_ascii=False)

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

    @property
    def summary(self) -> str:
        return "\n\n".join(
            (
                "",
                self.roadmaps.summary,
                self.calendar.summary,
                self.plan.summary if self.plan else "No plan defined.",
                self.schedules.summary if self.schedules else "No schedule defined.",
                self.logs.summary if self.logs else "No logs defined.",
            )
        )

    def make_gantt_string(self, raw: bool = False) -> str:
        """
        Creates a Gantt-style representation of the declaration and resulting plan.
        """
        project_name_max_length = 30

        today = PDate.today()
        end_date = PDate.today() + 400

        def make_project_line(project: Project) -> str:
            def get_dates(project: Project, raw: bool) -> dict[PDate, str]:
                if raw:
                    return {
                        _date: project[list(_tasks.values())[-1].task_id].status
                        for _date, _tasks in project.subplan.items()
                    }

                assert self.plan, "Plan must be defined in order to be shown as a gantt."

                ret: dict[PDate, str] = {}
                for date, tasks in self.plan.items():
                    relevant_tasks = [
                        _task for _task in tasks if _task.task_id in project.project_id
                    ]
                    if relevant_tasks:
                        task = relevant_tasks[-1]
                        ret.update({date: task.status})

                return ret

            def format_name(proj_name: str) -> str:
                if len(proj_name) <= project_name_max_length:
                    return f"{proj_name: <{project_name_max_length}} ║ "
                return proj_name[: (project_name_max_length - 6)] + "…" + proj_name[-5:] + " ║ "

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
        assert lines
        if not list(filter(lambda x: x[1] != "", lines)):
            print(lines)
        lines = list(filter(lambda x: x[1] != "", lines))
        assert lines

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
        assert lines

        def make_header(lines_: list[tuple[int, str]]) -> str:
            chars = []
            t = PDate.today()
            maxlen: int = max(map(len, map(lambda x: x[1], lines_)))
            for d in t.range(maxlen):
                chars.append(("║" * (d.month == 1 and d.day == 1) + "│" * (d.day == 1) + " ")[0])

            return project_name_max_length * " " + " ║ " + "".join(chars)

        line1 = make_header(lines)
        gantt = "\n".join([line1, line1, ""]) + "\n".join(map(lambda x: x[1], lines))
        return gantt

    def show_dashboard(self) -> None:
        print("Not yet implemented!")

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
