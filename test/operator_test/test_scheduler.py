from typing import Tuple
import pytest
from planager.config import _Config

from planager.entity.base.calendar import Calendar
from planager.entity.base.plan import Plan
from planager.entity.base.project import Project
from planager.entity.container.roadmaps import Roadmaps
from planager.entity.container.routines import Routines
from planager.entity.container.schedules import Schedules
from planager.entity.container.tasks import Tasks
from planager.entity.patch.schedule_patch import SchedulePatches
from planager.operator.planner import Planner
from planager.operator.scheduler import Scheduler
from planager.util import PDate


class SchedulerTest:
    # def test_init(self) -> None:

    def test_call(self) -> None:
        plan = Plan()
        calendar = Calendar()
        tasks = Tasks()
        routines = Routines()
        schedule_patches = SchedulePatches()
        start_date = PDate()
        end_date = PDate()

        exp_default = Schedules()
        scheduler_default = Scheduler()
        schedules_default = scheduler_default(
            plan,
            calendar,
            tasks,
            routines,
            schedule_patches,
            start_date,
            end_date,
        )
        assert schedules_default == exp_default

        exp_custom = Schedules()
        cfg = _Config()
        scheduler_custom = Scheduler(cfg)
        schedules_custom = scheduler_custom(
            plan,
            calendar,
            tasks,
            routines,
            schedule_patches,
            start_date,
            end_date,
        )
        assert schedules_custom == exp_custom

    # def test_call_2(self) -> None:

    # def test_call_3(self) -> None:
