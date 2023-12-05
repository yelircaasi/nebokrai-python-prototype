import json
import os
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
from .tracking import Logs, Tracker
from .util import PDate, ProjectID, RoadmapID, TaskID, color, shift_declaration_ndays


class Planager:
    """
    One class to rule them all.
    """

    calendar: Calendar
    roadmaps: Roadmaps
    routines: Routines
    tracker: Tracker
    plan: Optional[Plan] = None
    schedules: Optional[Schedules] = None
    logs: Optional[Logs] = None
    declaration_edit_time: datetime
    plan_edit_time: datetime
    schedule_edit_time: datetime
    # derivation:

    def __init__(
        self, calendar: Calendar, roadmaps: Roadmaps, routines: Routines, tracker: Tracker
    ) -> None:
        self.calendar = calendar
        self.roadmaps = roadmaps
        self.routines = routines
        self.tracker = tracker

        with open(path_manager.edit_times, encoding="utf-8") as f:
            edit_times = json.load(f)

        def from_key(k: str) -> datetime:
            return datetime.fromisoformat(edit_times[k])

        self.declaration_edit_time = from_key("declaration_edit_time")
        self.plan_edit_time = from_key("plan_edit_time")
        self.schedule_edit_time = from_key("schedule_edit_time")

    @classmethod
    def from_json(cls) -> "Planager":  # TODO: move this to init; currently JSON is the One True Way
        """
        Instantiates from declaration.json.
        """

        with open(path_manager.declaration, encoding="utf-8") as f:
            dec = json.load(f)

        routines = Routines.deserialize(dec["routines"])
        calendar = Calendar.deserialize(routines, dec["calendar"])
        roadmaps = Roadmaps.deserialize(dec["roadmaps"])
        tracker = Tracker(dec["tracking"], dec["routines"])

        return cls(calendar, roadmaps, routines, tracker)

    def declare_interactive(self) -> None:
        print("Not yet implemented.")

    def derive(self) -> None:
        """
        Derives plan and schedules from declarations.
        """

        self.derive_plan()
        self.derive_schedules()

    def derive_plan(
        self,
    ) -> None:
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

        # if self.plan_edit_time > self.declaration_edit_time:
        plan = Plan(
            calendar=self.calendar,
        )
        # else:
        #     plan = Plan.from_derivation(path_manager.declaration, path_manager.derivation)

        projects = self.roadmaps.projects

        for project in projects.iter_by_priority:
            plan = update_plan(plan, project.subplan)
            print(f"Planning {color.magenta(project.name)}.")

        self.enforce_precedence_constraints(plan, projects)
        plan.fill_empty()

        self.plan = plan

    def derive_schedules(self) -> None:
        """
        Use information obtained from the declaration and the derived plan to derive,
          in turn, the schedules.
        """
        start_date_new, end_date_new = self.start_and_end_dates
        schedules, excess_entries = Schedules(), Entries()
        # ----
        end_date_new = PDate.from_string("2023-12-31")  # FIXME
        # ----
        for date in start_date_new.range(end_date_new):
            print(f"Scheduling {color.cyan(str(date))}.")
            schedule = Schedule.from_calendar(self.calendar, date)
            # TODO: add .earliest and .latest to entries

            schedules[date], excess_entries = add_from_plan_and_excess(
                schedule, self.plan, excess_entries
            )
        self.schedules = schedules

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

    def save_derivation(self) -> None:
        self.save_plan()
        self.save_schedules()

    def save_plan(self) -> None:
        """
        Writes plan to $PLANAGER_ROOT/derivation/plan.json and backs up the last plan file.
        """
        assert self.plan is not None
        os.rename(path_manager.plan, path_manager.plan_backup)
        with open(path_manager.plan, "w", encoding="utf-8") as f:
            json.dump(self.plan.serialize(), f, ensure_ascii=False, indent=4)
        with open(path_manager.txt_plan, "w", encoding="utf-8") as f:
            f.write(str(self.plan))
        with open(path_manager.txt_gantt, "w", encoding="utf-8") as f:
            f.write(self.plan.gantt_view)

    def save_schedules(self) -> None:
        """
        Writes schedules to $PLANAGER_ROOT/derivation/schedules.json and backs up the last schedules file.
        """
        assert self.schedules is not None
        os.rename(path_manager.schedules, path_manager.schedules_backup)
        with open(path_manager.schedules, "w", encoding="utf-8") as f:
            json.dump(self.schedules.serializes(), f, ensure_ascii=False, indent=4)
        with open(path_manager.txt_schedules, "w", encoding="utf-8") as f:
            f.write(str(self.schedules))

    def open_plan(self) -> None:
        ...

    def open_schedules(self) -> None:
        ...

    def track(self) -> None:
        print("Not yet finished!")
        self.tracker.record()

    @staticmethod
    def shift_declaration(ndays: int) -> None:
        shift_declaration_ndays(path_manager, ndays)

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
