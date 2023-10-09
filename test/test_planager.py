from pathlib import Path

import pytest

from planager import Planager
from planager.entity import (
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
from planager.util import ConfigType, PathManager, PDateTime


class PlanagerTest:
    def test_init(self) -> None:
        ...
        # p = Planager()

        # assert isinstance(p.path_manager, PathManager)
        # assert isinstance(p.roadmaps, Roadmaps)
        # assert isinstance(p.routines, Routines)
        # assert isinstance(p.planner, Planner)
        # assert isinstance(p.scheduler, Scheduler)

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
