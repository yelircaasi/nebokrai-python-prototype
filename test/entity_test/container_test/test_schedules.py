from pathlib import Path
import pytest

from planager.entity.container.schedules import Schedules
from planager.entity.base.schedule import Schedule
from planager.util.pdatetime.pdate import PDate


class SchedulesTest:
    def test_init_and_from_norg_workspace(self) -> None:
        schedules = Schedules.from_norg_workspace(Path(""))
        exp = Schedules()
        schedule_dict: dict[PDate, Schedule] = {}

        assert schedules == exp
        assert schedules._schedules == exp._schedules == schedule_dict

    def test_len(self) -> None:
        schedules = Schedules()
        schedules_empty = Schedules()

        assert len(schedules) == 4
        assert len(schedules_empty) == 0

    def test_getitem(self) -> None:
        schedules = Schedules()
        schedule = Schedule()
        day = PDate(2100, 1, 1)

        assert schedules[day] == schedule

    def test_setitem(self) -> None:
        schedules = Schedules()
        schedule = Schedule()
        day = PDate(2100, 1, 1)

        schedules[day] = schedule

        assert schedules[day] == schedule

    def test_str(self) -> None:
        schedules = Schedule()
        exp = ()
        assert str(schedules) == exp

    def test_repr(self) -> None:
        schedules = Schedule()
        exp = ()
        assert repr(schedules) == exp
