from pathlib import Path
import pytest

from planager.entity.base.calendar import Calendar, Day
from planager.util.pdatetime.pdate import PDate


class DayTest:
    day1 = Day(PDate(0, 0, 0))
    day2 = Day(PDate(0, 0, 0))
    day3 = Day(PDate(0, 0, 0))

    def test_init(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.day1
        assert self.day2
        assert self.day3


class CalendarTest:
    calendar1 = Calendar()
    calendar2 = Calendar()
    calendar3 = Calendar()

    exp_string1 = "\n" "\n" "\n" "\n"
    exp_string2 = "\n" "\n" "\n" "\n"
    exp_string3 = "\n" "\n" "\n" "\n"

    def test_init(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.calendar1
        assert self.calendar2
        assert self.calendar3

    def test_copy(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.calendar1.copy() == self.calendar1
        assert self.calendar2.copy() == self.calendar2
        assert self.calendar3.copy() == self.calendar3

        assert id(self.calendar1.copy()) != id(self.calendar1)
        assert id(self.calendar2.copy()) != id(self.calendar2)
        assert id(self.calendar3.copy()) != id(self.calendar3)

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
        """
        Cases:
        1)
        2)
        3)
        """
        assert Calendar.from_norg_workspace(Path()) == self.calendar1
        assert Calendar.from_norg_workspace(Path()) == self.calendar2
        assert Calendar.from_norg_workspace(Path()) == self.calendar3

    def test_start_date(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.calendar1.start_date == PDate(0, 0, 0)
        assert self.calendar2.start_date == PDate(0, 0, 0)
        assert self.calendar3.start_date == PDate(0, 0, 0)

    def test_end_date(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.calendar1.end_date == PDate(0, 0, 0)
        assert self.calendar2.end_date == PDate(0, 0, 0)
        assert self.calendar3.end_date == PDate(0, 0, 0)

    def test_getitem(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.calendar1[PDate(0, 0, 0)] == Day(PDate(0, 0, 0))
        assert self.calendar2[PDate(0, 0, 0)] == Day(PDate(0, 0, 0))
        assert self.calendar3[PDate(0, 0, 0)] == Day(PDate(0, 0, 0))

    def test_setitem(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        cal1 = self.calendar1.copy()
        cal2 = self.calendar2.copy()
        cal3 = self.calendar3.copy()

        date1 = PDate(0, 0, 0)
        date2 = PDate(0, 0, 0)
        date3 = PDate(0, 0, 0)

        day1 = Day(PDate(0, 0, 0))
        day2 = Day(PDate(0, 0, 0))
        day3 = Day(PDate(0, 0, 0))

        cal1[date1] = day1
        cal2[date2] = day1
        cal3[date3] = day1

        assert cal1[date1] == day1
        assert cal2[date2] == day2
        assert cal3[date3] == day3

    def test_str(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert str(self.calendar1) == self.exp_string1
        assert str(self.calendar2) == self.exp_string2
        assert str(self.calendar3) == self.exp_string3

    def test_repr(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert repr(self.calendar1) == self.exp_string1
        assert repr(self.calendar2) == self.exp_string2
        assert repr(self.calendar3) == self.exp_string3
