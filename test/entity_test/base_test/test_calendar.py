from pathlib import Path
import pytest

from planager.entity.base.calendar import Calendar, Day
from planager.util.pdatetime.pdate import PDate


class DayTest:
    day1 = Day()
    day2 = Day()
    day3 = Day()

    def test_init(self) -> None:
        assert self.day1
        assert self.day2
        assert self.day3

class CalendarTest:
    calendar1 = Calendar()
    calendar2 = Calendar()
    calendar3 = Calendar()

    exp_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )

    def test_init(self) -> None:
        assert self.calendar1
        assert self.calendar2
        assert self.calendar3

    def test_copy(self) -> None:
        assert self.calendar1.copy() ==  self.calendar1
        assert self.calendar2.copy() ==  self.calendar2
        assert self.calendar3.copy() ==  self.calendar3

        assert id(self.calendar1.copy()) !=  id(self.calendar1)
        assert id(self.calendar2.copy()) !=  id(self.calendar2)
        assert id(self.calendar3.copy()) !=  id(self.calendar3)

    def test_add(self) -> None:
        cal1 = self.calendar1.copy()
        cal2 = self.calendar1.copy()
        cal3 = self.calendar1.copy()

        day1 = Day()
        day2 = Day()
        day3 = Day()

        cal1.add(day1)
        cal2.add(day1)
        cal3.add(day1)

        assert day1 in cal1.days
        assert day2 in cal2.days
        assert day3 in cal3.days
        
        
    def test_from_norg_workspace(self) -> None:
        assert Calendar.from_norg_workspace(Path()) == self.calendar1
        assert Calendar.from_norg_workspace(Path()) == self.calendar2
        assert Calendar.from_norg_workspace(Path()) == self.calendar3

    def test_start_date(self) -> None:
        assert self.calendar1.start_date == PDate()
        assert self.calendar2.start_date == PDate()
        assert self.calendar3.start_date == PDate()

    def test_end_date(self) -> None:
        assert self.calendar1.end_date == PDate()
        assert self.calendar2.end_date == PDate()
        assert self.calendar3.end_date == PDate()

    def test_getitem(self) -> None:
        assert self.calendar1[2] == Day()
        assert self.calendar2[4] == Day()
        assert self.calendar3[-1] == Day()

    def test_setitem(self) -> None:
        cal1 = self.calendar1.copy()
        cal2 = self.calendar2.copy()
        cal3 = self.calendar3.copy()

        date1 = PDate()
        date2 = PDate()
        date3 = PDate()

        day1 = Day()
        day2 = Day()
        day3 = Day()

        cal1[date1] = day1
        cal2[date2] = day1
        cal3[date3] = day1

        assert cal1[date1] == day1
        assert cal2[date2] == day2
        assert cal3[date3] == day3

    def test_str(self):
        assert str(self.calendar1) == self.exp_string1
        assert str(self.calendar2) == self.exp_string2
        assert str(self.calendar3) == self.exp_string3

    def test_repr(self):
        assert repr(self.calendar1) == self.exp_string1
        assert repr(self.calendar2) == self.exp_string2
        assert repr(self.calendar3) == self.exp_string3