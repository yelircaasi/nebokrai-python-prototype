from pathlib import Path
from typing import Any

import pytest

from planager.entity.base.calendar import Calendar, Day
from planager.util.pdatetime.pdate import PDate


class DayTest:
    def test_init(self) -> None:
        day_default = Day(PDate(2100, 1, 1))
        day_custom = Day(PDate(2100, 1, 1))

        assert day_default.date == ...
        assert day_default.entries == ...
        assert day_default.available == ...
        assert day_default.routine_names == ...

        assert day_custom.date == ...
        assert day_custom.entries == ...
        assert day_custom.available == ...
        assert day_custom.routine_names == ...

    def test_copy(self) -> None:
        day = Day(PDate(2100, 1, 1))
        copy = day.copy()

        assert day.__dict__ == copy.__dict__

    def test_available(self) -> None:
        day = Day(PDate(2100, 1, 1))

        assert day.available == ...

    def test_from_dict(self) -> None:
        day_dict: dict[str, Any] = {}
        date = PDate(2100, 1, 1)
        day = Day.from_dict(date, day_dict)
        exp = Day(date)

        assert day == exp


class CalendarTest:
    def test_init(self) -> None:
        calendar = Calendar()

    def test_from_dict(self) -> None:
        calendar_dict: dict[str, Any] = {}
        calendar = Calendar.from_dict(calendar_dict)
        exp = Calendar()

        assert calendar == exp

    def test_from_norg_workspace(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        calendar1 = Calendar.from_norg_workspace(path1)
        calendar2 = Calendar.from_norg_workspace(path2)
        calendar3 = Calendar.from_norg_workspace(path3)

        assert Calendar.from_norg_workspace(path1) == calendar1
        assert Calendar.from_norg_workspace(path2) == calendar2
        assert Calendar.from_norg_workspace(path3) == calendar3

    def test_copy(self) -> None:
        calendar = Calendar()

    def test_add(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        calendar = Calendar()
        copy = calendar.copy()

        day1 = Day(PDate(0, 0, 0))
        day2 = Day(PDate(0, 0, 0))
        day3 = Day(PDate(0, 0, 0))

        copy.add(day1)
        copy.add(day1)
        copy.add(day1)

        assert day1 in copy.days
        assert day2 in copy.days
        assert day3 in copy.days

    def test_start_date(self) -> None:
        calendar = Calendar()
        start = PDate(2100, 1, 1)

        assert calendar.start_date == start

    def test_end_date(self) -> None:
        calendar = Calendar()
        end = PDate(2100, 1, 1)

        assert calendar.end_date == end

    def test_getitem(self) -> None:
        calendar = Calendar()
        date = PDate(2100, 1, 1)
        day = Day(date)

        assert calendar[date] == day

    def test_setitem(self) -> None:
        calendar = Calendar()
        date = PDate(2100, 1, 1)
        day = Day(date)

        calendar[date] = day

        assert calendar[date] == day

    def test_str(self):
        calendar = Calendar()
        exp = ()
        assert str(calendar) == exp

    def test_repr(self):
        calendar = Calendar()
        exp = ()
        assert repr(calendar) == exp
