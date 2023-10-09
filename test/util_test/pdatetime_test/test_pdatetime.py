import re
from datetime import date, datetime, time

import pytest

from planager.util.pdatetime import PDateTime


class PDateTimeTest:
    datetime1 = PDateTime(2022, 10, 13, 8, 15, 33)
    datetime2 = PDateTime(2023, 3, 7, 9, 0, 0)

    def test_init(self) -> None:
        assert True

    def test_now_str(self) -> None:
        rx = re.compile(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d")
        assert re.match(rx, self.datetime1.now_string())
        assert re.match(rx, self.datetime2.now_string())

    def test_now(self) -> None:
        def now_works() -> bool:
            dt = PDateTime.now()
            sdt = datetime.now()
            return (dt.year, dt.month, dt.day, dt.hour, dt.minute) == (
                sdt.year,
                sdt.month,
                sdt.day,
                sdt.hour,
                sdt.minute,
            ) and (abs(dt.second - sdt.second) < 2)

        times_match = now_works()
        if not times_match:
            times_match = now_works()

        assert times_match

    def test_from_string(self) -> None:
        assert True

    def test_bool(self) -> None:
        dt = PDateTime(2023, 3, 7, 9, 0, 0, isblank=True)

        assert self.datetime1
        assert self.datetime2
        assert not dt

    def test_copy(self) -> None:
        dt1 = PDateTime(2022, 10, 13, 8, 15, 33)
        dt2 = PDateTime(2023, 3, 7, 9, 0, 0)

        assert self.datetime1 == dt1
        assert self.datetime2 == dt2

        assert id(self.datetime1) != id(dt1)
        assert id(self.datetime2) != id(dt2)

    def test_str(self) -> None:
        assert str(self.datetime1) == "2022-10-13 08:15:33"
        assert str(self.datetime2) == "2023-03-07 09:00:00"

    def test_repr(self) -> None:
        assert repr(self.datetime1) == "2022-10-13 08:15:33"
        assert repr(self.datetime2) == "2023-03-07 09:00:00"

    def test_eq(self) -> None:
        assert self.datetime1 == PDateTime(2022, 10, 13, 8, 15, 33)
        assert self.datetime2 == PDateTime(2023, 3, 7, 9, 0, 0)
        assert self.datetime1 != self.datetime2

    def test_lt(self) -> None:
        assert self.datetime1 < self.datetime2
        assert not (self.datetime2 < self.datetime1)

    def test_gt(self) -> None:
        assert self.datetime2 > self.datetime1
        assert not (self.datetime1 > self.datetime2)

    def test_le(self) -> None:
        assert self.datetime1 <= self.datetime1
        assert self.datetime1 <= self.datetime2
        assert not (self.datetime2 <= self.datetime1)

    def test_ge(self) -> None:
        assert self.datetime2 >= self.datetime2
        assert self.datetime2 >= self.datetime1
        assert not (self.datetime1 >= self.datetime2)
