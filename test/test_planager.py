from pathlib import Path
import pytest

from planager import Planager
from planager.entity import (
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
from planager.operator import Planner, Scheduler
from planager.util import ConfigType, PDateTime, PathManager


class PlanagerTest:
    def test_init(self) -> None:
        p = Planager()

        assert not p.path_manager
        assert not p.roadmaps
        assert not p.adhoc
        assert not p.projects
        assert not p.tasks
        assert not p.routines
        assert not p.plan
        assert not p.schedules
        assert not p.planner
        assert not p.scheduler
        assert not p.plan_patches
        assert not p.schedule_patches
        assert not p.task_patches
        assert not p._last_update

        assert isinstance(p.path_manager, PathManager)
        assert isinstance(p.roadmaps, Roadmaps)
        assert isinstance(p.adhoc, AdHoc)
        assert isinstance(p.projects, Projects)
        assert isinstance(p.tasks, Tasks)
        assert isinstance(p.routines, Routines)
        assert isinstance(p.plan, Plan)
        assert isinstance(p.schedules, Schedules)
        assert isinstance(p.planner, Planner)
        assert isinstance(p.scheduler, Scheduler)
        assert isinstance(p.plan_patches, PlanPatches)
        assert isinstance(p.schedule_patches, SchedulePatches)
        assert isinstance(p.task_patches, TaskPatches)
        assert p._last_update is None

    def test_from_norg_workspace(self) -> None:
        workspace = Path(__file__).parent / "data" / "norg_workspace1"
        p = Planager.from_norg_workspace(workspace)

        assert p.path_manager
        assert p.roadmaps
        assert p.adhoc
        assert p.projects
        assert p.tasks
        assert p.routines
        assert p.plan
        assert p.schedules
        assert p.planner
        assert p.scheduler
        assert p.plan_patches
        assert p.schedule_patches
        assert p.task_patches
        assert p._last_update

        assert isinstance(p.path_manager, PathManager)
        assert isinstance(p.roadmaps, Roadmaps)
        assert isinstance(p.adhoc, AdHoc)
        assert isinstance(p.projects, Projects)
        assert isinstance(p.tasks, Tasks)
        assert isinstance(p.routines, Routines)
        assert isinstance(p.plan, Plan)
        assert isinstance(p.schedules, Schedules)
        assert isinstance(p.planner, Planner)
        assert isinstance(p.scheduler, Scheduler)
        assert isinstance(p.plan_patches, PlanPatches)
        assert isinstance(p.schedule_patches, SchedulePatches)
        assert isinstance(p.task_patches, TaskPatches)
        assert p._last_update is None

    def test_from_json(self) -> None:
        assert True

    def test_from_html(self) -> None:
        assert True

    def test_derive(self) -> None:
        assert True

    def test_reconfigure(self) -> None:
        assert True

    def test_setup_from_norg_workspace(self) -> None:
        assert True

    def test_write_norg(self) -> None:
        assert True

    def test_write_json(self) -> None:
        assert True

    def test_write_html(self) -> None:
        assert True

    def test_roadmap_tree(self) -> None:
        assert True

    def test_getitem(self) -> None:
        assert True

    def test_setitem(self) -> None:
        assert True

    def test_str(self) -> None:
        assert True

    def test_repr(self) -> None:
        assert True
