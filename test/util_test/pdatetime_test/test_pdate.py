from datetime import date

import pytest

from planager.util.pdatetime import PDate
from planager.util.pdatetime.pdate import NoneDate


class PDateTest:
    date1 = PDate(2023, 5, 23)
    date2 = PDate(2011, 6, 15)
    date3 = PDate(2024, 8, 10)
    stdlib_date1 = date(2023, 5, 23)
    stdlib_date2 = date(2011, 6, 15)
    stdlib_date3 = date(2024, 8, 10)

    def test_init(self) -> None:
        assert isinstance(self.date1, PDate)
        assert isinstance(self.date2, PDate)
        assert isinstance(self.date3, PDate)

    def test_ensure_is_pdate(self) -> None:
        cand1 = PDate(2023, 5, 9)
        cand2 = "2023-05-09"
        cand3 = "2023-5-9"
        cand4 = 17
        cand5 = (2023, 5, 9)
        cand6 = ("2023", "5", "9")
        cand7 = ("2023", "05", "09")

        exp1 = cand1
        exp2 = cand1
        exp3 = cand1
        exp4 = PDate.today() + 17
        exp5 = cand1
        exp6 = cand1
        exp7 = cand1

        default = cand1

        imp1 = {}
        imp2 = "65"
        imp3 = "other string"
        imp4 = "65, 234, 34"
        imp5 = (-3, 456)
        imp6 = (3, 30, 56)
        imp7 = None

        assert PDate.ensure_is_pdate(cand1) == exp1
        assert PDate.ensure_is_pdate(cand2) == exp2
        assert PDate.ensure_is_pdate(cand3) == exp3
        assert PDate.ensure_is_pdate(cand4) == exp4
        assert PDate.ensure_is_pdate(cand5) == exp5
        assert PDate.ensure_is_pdate(cand6) == exp6
        assert PDate.ensure_is_pdate(cand7) == exp7

        assert PDate.ensure_is_pdate(imp1, default=default) == default
        assert PDate.ensure_is_pdate(imp2, default=default) == default
        assert PDate.ensure_is_pdate(imp3, default=default) == default
        assert PDate.ensure_is_pdate(imp4, default=default) == default
        assert PDate.ensure_is_pdate(imp5, default=default) == default
        assert PDate.ensure_is_pdate(imp6, default=default) == default
        assert PDate.ensure_is_pdate(imp7, default=default) == default

    def test_year(self) -> None:
        assert self.date1.year == 2023
        assert self.date2.year == 2011
        assert self.date3.year == 2024

    def test_year_setter(self) -> None:
        newdate = PDate(2023, 3, 5)
        newdate.year = 2025
        assert newdate.year == 2025

    def test_month(self) -> None:
        assert self.date1.month == 5
        assert self.date2.month == 6
        assert self.date3.month == 8

    def test_month_setter(self) -> None:
        newdate = PDate(2023, 3, 5)
        newdate.month = 12
        assert newdate.month == 12

    def test_day(self) -> None:
        assert self.date1.day == 23
        assert self.date2.day == 15
        assert self.date3.day == 10

    def test_day_setter(self) -> None:
        newdate = PDate(2023, 3, 5)
        newdate.day = 20
        assert newdate.day == 20

    def test_copy(self) -> None:
        newdate = self.date1.copy()
        assert id(newdate) != id(self.date1)
        assert self.date1.__dict__ == newdate.__dict__
        newdate2 = newdate.copy()
        assert id(newdate) != id(newdate2)
        assert newdate.__dict__ == newdate2.__dict__

    def test_from_string(self) -> None:
        assert PDate.from_string("2023-05-23") == self.date1
        assert PDate.from_string("2023.05.23") == self.date1
        assert PDate.from_string("2023-5-23") == self.date1
        assert PDate.from_string("2023 05 23") == self.date1
        assert PDate.from_string("2023 5 23") == self.date1

        assert PDate.from_string("2011-06-15") == self.date2
        assert PDate.from_string("2011-6-15") == self.date2
        assert PDate.from_string("2011.06.15") == self.date2
        assert PDate.from_string("2011 6 15") == self.date2

        assert PDate.from_string("2024-08-10") == self.date3
        assert PDate.from_string("2024.8.10") == self.date3
        assert PDate.from_string("2024-8-10") == self.date3
        assert PDate.from_string("2024 08 10") == self.date3

    def test_toordinal(self) -> None:
        assert self.date1.toordinal() == 738663 == self.stdlib_date1.toordinal()
        assert self.date2.toordinal() == 734303 == self.stdlib_date2.toordinal()
        assert self.date3.toordinal() == 739108 == self.stdlib_date3.toordinal()

    def test_fromordinal(self) -> None:
        d1 = PDate.fromordinal(738663)
        d2 = PDate.fromordinal(734303)
        d3 = PDate.fromordinal(739108)
        sd1 = date.fromordinal(738663)
        sd2 = date.fromordinal(734303)
        sd3 = date.fromordinal(739108)

        assert self.date1 == d1
        assert self.date2 == d2
        assert self.date3 == d3
        assert d1 == sd1
        assert d2 == sd2
        assert d3 == sd3

    def test_int(self) -> None:
        assert int(self.date1) == 738663
        assert int(self.date2) == 734303
        assert int(self.date3) == 739108

    def test_add(self) -> None:
        assert (self.date1 + 3) == PDate(2023, 5, 26)
        assert (self.date2 + 315) == PDate(2012, 4, 25)
        assert (self.date3 + 60) == PDate(2024, 10, 9)

    def test_sub(self) -> None:
        assert (self.date1 - 30) == PDate(2023, 4, 23)
        assert (self.date2 - 400) == PDate(2010, 5, 11)
        assert (self.date3 - 160) == PDate(2024, 3, 3)

    def test_pretty(self) -> None:
        assert self.date1.pretty() == "Tuesday, May 23rd, 2023"
        assert self.date2.pretty() == "Wednesday, June 15th, 2011"
        assert self.date3.pretty() == "Saturday, August 10th, 2024"

    def test_range(self) -> None:
        end_date = self.date1 + 3
        expected = [self.date1, self.date1 + 1, self.date1 + 2, self.date1 + 3]
        assert self.date1.range(end_date) == expected
        assert self.date1.range(3) == expected
        assert end_date.range(self.date1) == list(reversed(expected))
        assert end_date.range(-3) == list(reversed(expected))
        assert self.date1.range(end_date, inclusive=False) == expected[:-1]
        assert end_date.range(-3, inclusive=False) == list(reversed(expected))[1:]

    def test_tomorrow(self) -> None:
        tomorrow = PDate.tomorrow()
        stdlib_today = date.today()
        assert stdlib_today.toordinal() == (tomorrow.toordinal() - 1)

    def test_nonedate(self) -> None:
        assert PDate.nonedate() == NoneDate()

    def test_eq(self) -> None:
        assert self.date1 == PDate(2023, 5, 23)
        assert self.date2 == PDate(2011, 6, 15)
        assert self.date3 == PDate(2024, 8, 10)

    def test_lt(self) -> None:
        assert not (self.date1 < self.date1)
        assert self.date2 < self.date1 < self.date3
        assert not (self.date1 < self.date2)

    def test_gt(self) -> None:
        assert not (self.date1 > self.date1)
        assert self.date3 > self.date1 > self.date2
        assert not (self.date2 > self.date1)

    def test_le(self) -> None:
        assert self.date1 <= self.date1
        assert self.date2 <= self.date1 <= self.date3
        assert not (self.date1 <= self.date2)

    def test_ge(self) -> None:
        assert self.date1 >= self.date1
        assert self.date3 >= self.date1 >= self.date2
        assert not (self.date2 >= self.date1)

    def test_str(self) -> None:
        assert str(self.date1) == "2023-05-23"
        assert str(self.date2) == "2011-06-15"
        assert str(self.date3) == "2024-08-10"

    def test_repr(self) -> None:
        assert repr(self.date1) == "2023-05-23"
        assert repr(self.date2) == "2011-06-15"
        assert repr(self.date3) == "2024-08-10"


class NoneDateTest:
    nonedate = NoneDate()
    date1 = PDate(2023, 5, 23)
    date2 = PDate(2011, 6, 15)
    date3 = PDate(2024, 8, 10)

    def test_init(self) -> None:
        assert isinstance(self.nonedate, NoneDate)
        assert self.nonedate.year == 1970
        assert self.nonedate.month == 1
        assert self.nonedate.day == 1

    def test_eq(self) -> None:
        assert self.nonedate != self.date1
        assert self.nonedate != self.date2
        assert self.nonedate != self.date3

    def test_lt(self) -> None:
        assert not (self.nonedate < self.date1)
        assert not (self.nonedate < self.date2)
        assert not (self.nonedate < self.date3)

    def test_gt(self) -> None:
        assert not (self.nonedate > self.date1)
        assert not (self.nonedate > self.date2)
        assert not (self.nonedate > self.date3)

    def test_le(self) -> None:
        assert self.nonedate <= self.date1
        assert self.nonedate <= self.date2
        assert self.nonedate <= self.date3

    def test_ge(self) -> None:
        assert self.nonedate >= self.date1
        assert self.nonedate >= self.date2
        assert self.nonedate >= self.date3
