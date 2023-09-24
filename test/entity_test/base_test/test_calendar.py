from pathlib import Path
import pytest

from planager.entity.base.calendar import Calendar, Day
from planager.util.pdatetime.pdate import PDate


class DayTest:
    def test_init(self) -> None:
        day_default = Day()
        day_custom = Day()

        assert day_default.date == ...
        assert day_default.entries == ...
        assert day_default.available == ...
        assert day_default.routines == ...

        assert day_custom.date == ...
        assert day_custom.entries == ...
        assert day_custom.available == ...
        assert day_custom.routines == ...

    def test_copy(self) -> None:
        day = Day()
        copy = day.copy()

        assert day.__dict__ == copy.__dict__


class CalendarTest:
    def test_init(self) -> None:
        calendar = Calendar()

    def test_copy(self) -> None:
        calendar = Calendar()

    def test_add(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        cal1 = self.calendar1.copy()
        cal2 = self.calendar1.copy()
        cal3 = self.calendar1.copy()

        day1 = Day(PDate(0, 0, 0))
        day2 = Day(PDate(0, 0, 0))
        day3 = Day(PDate(0, 0, 0))

        cal1.add(day1)
        cal2.add(day1)
        cal3.add(day1)

        assert day1 in cal1.days
        assert day2 in cal2.days
        assert day3 in cal3.days

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

    def test_start_date(self) -> None:
        calendar = Calendar()
        start = PDate()

        assert calendar.start_date == start

    def test_end_date(self) -> None:
        calendar = Calendar()
        end = PDate()

        assert calendar.end_date == end

    def test_getitem(self) -> None:
        calendar = Calendar()
        day = Day()
        date = PDate()

        assert calendar[date] == day

    def test_setitem(self) -> None:
        calendar = Calendar()
        day = Day()
        date = PDate()

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
