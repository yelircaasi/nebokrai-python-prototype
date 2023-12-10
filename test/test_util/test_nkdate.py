from datetime import date

import pytest

from nebokrai.util import NKDate
from nebokrai.util.nkdatetime.nkdate import NoneDate


def test_basic_nkdate() -> None:
    date1 = NKDate(2023, 2, 20)
    assert date1 == date1 == NKDate(2023, 2, 20)
    assert str(date1) == "2023-02-20"
    assert date1 != NKDate(2023, 2, 21)
    assert date1 != NKDate(2023, 3, 20)
    assert date1 != NKDate(2022, 2, 20)


def test_from_string() -> None:
    assert NKDate(2020, 2, 2) == NKDate.from_string("2020-2-2") == NKDate.from_string("2020-02-02")


def test_from_string_errors() -> None:
    with pytest.raises(TypeError) as excinfo:
        d1 = NKDate.from_string(3)  # type: ignore
    assert str(excinfo.value) == (
        "Invalid type for NKDate.from_string: '<class 'int'>' (value: '3')."
    )

    with pytest.raises(ValueError) as excinfo:  # type: ignore
        d2 = NKDate.from_string("not a date")
    assert str(excinfo.value) == ("Invalid string for conversion to NKDate: 'not a date'.")


def test_date_arithmetic() -> None:
    date1 = NKDate(2030, 2, 1)
    date2 = NKDate(2031, 2, 3)
    date3 = NKDate(2031, 2, 3)

    assert date1 < date2
    assert date2 > date1
    assert date1 <= date2
    assert date2 <= date3
    assert date2 >= date1
    assert date2 >= date3
    assert date2 == date3

    assert not (date1 >= date2)
    assert not (date1 > date2)
    assert not (date2 <= date1)
    assert not (date2 < date1)

    assert not (date2 < date3)
    assert not (date2 > date3)


def test_properties() -> None:
    date1 = NKDate(2000, 10, 5)

    date1.year = 2010
    assert date1.year == 2010

    date1.month = 6
    assert date1.month == 6

    date1.day = 2
    assert date1.day == 2


def test_daysto() -> None:
    date1 = NKDate(2030, 2, 1)
    date2 = NKDate(2030, 2, 5)

    assert date1.daysto(date2) == 4
    assert date2.daysto(date1) == -4
    assert date1.daysto(date1) == date2.daysto(date2) == 0


def test_today_and_tomorrow() -> None:
    stdlib_today = date.today()
    today = NKDate.today()
    assert stdlib_today == today

    tomorrow = NKDate.tomorrow()
    assert tomorrow == (today + 1)


def test_hash() -> None:
    date1 = NKDate(2011, 11, 11)
    assert hash(date1) == hash((2011, 11, 11))


def test_pretty() -> None:
    assert NKDate(2023, 12, 1).pretty() == "Friday, December 1st, 2023"
    assert NKDate(2023, 12, 2).pretty() == "Saturday, December 2nd, 2023"
    assert NKDate(2023, 12, 3).pretty() == "Sunday, December 3rd, 2023"
    assert NKDate(2023, 12, 4).pretty() == "Monday, December 4th, 2023"
    assert NKDate(2023, 12, 5).pretty() == "Tuesday, December 5th, 2023"
    assert NKDate(2023, 12, 6).pretty() == "Wednesday, December 6th, 2023"
    assert NKDate(2023, 12, 7).pretty() == "Thursday, December 7th, 2023"
    assert NKDate(2023, 12, 21).pretty() == "Thursday, December 21st, 2023"
    assert NKDate(2023, 12, 22).pretty() == "Friday, December 22nd, 2023"
    assert NKDate(2023, 12, 23).pretty() == "Saturday, December 23rd, 2023"
    assert NKDate(2023, 12, 24).pretty() == "Sunday, December 24th, 2023"


def test_range() -> None:
    date1 = NKDate(2025, 2, 1)
    date2 = NKDate(2025, 2, 3)
    date3 = NKDate(2025, 2, 3)

    assert (
        date1.range(date2)
        == date1.range(2)
        == [NKDate(2025, 2, 1), NKDate(2025, 2, 2), NKDate(2025, 2, 3)]
    )
    assert date2.range(date1) == [NKDate(2025, 2, 3), NKDate(2025, 2, 2), NKDate(2025, 2, 1)]
    assert date2.range(date3) == date3.range(date2) == [date2] == [date3]

    assert date1.range(date2, inclusive=False) == [NKDate(2025, 2, 1), NKDate(2025, 2, 2)]
    assert date2.range(date1, inclusive=False) == [NKDate(2025, 2, 3), NKDate(2025, 2, 2)]

    assert date2.range(date2) == date2.range(date3, inclusive=False) == [date2]


def test_non3date() -> None:
    nd = NoneDate()
    assert nd == NKDate.nonedate()
    assert not nd
    assert bool(nd) == False
    assert nd == nd == NoneDate()
    assert str(nd) == "NoneDate"

    other = NKDate(2020, 2, 20)
    assert (nd < other) == False
    assert (nd > other) == False
    assert (nd >= other) == False
    assert (nd >= other) == False
    assert (nd == other) == False

    assert (nd.__lt__(other)) == False
    assert (nd.__gt__(other)) == False
    assert (nd.__le__(other)) == False
    assert (nd.__ge__(other)) == False
    assert (nd.__eq__(other)) == False


def test_nkdate_vs_nonedate_comparison() -> None:
    nd = NoneDate()
    other = NKDate(2020, 2, 20)

    assert (other < nd) == False
    assert (other > nd) == False
    assert (other >= nd) == False
    assert (other >= nd) == False
    assert (other == nd) == False

    assert (other.__lt__(nd)) == False
    assert (other.__gt__(nd)) == False
    assert (other.__le__(nd)) == False
    assert (other.__ge__(nd)) == False
    assert (other.__eq__(nd)) == False
