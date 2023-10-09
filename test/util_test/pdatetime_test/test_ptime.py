from typing import Set

import pytest

from planager.util.pdatetime import PTime


class PTimeTest:
    time1 = PTime(7)
    time2 = PTime(14, 17)
    time3 = PTime()
    time4 = PTime(24)
    time5 = PTime(isblank=True)

    def test_init(self) -> None:
        assert (self.time1.hour, self.time1.minute) == (7, 0)
        assert (self.time2.hour, self.time2.minute) == (14, 17)
        assert (self.time3.hour, self.time3.minute) == (0, 0)
        assert (self.time4.hour, self.time4.minute) == (24, 0)
        assert (self.time5.hour, self.time5.minute) == (0, 0)

    def test_from_string(self) -> None:
        assert (
            self.time1
            == PTime.from_string("07:00")
            == PTime.from_string("7:00")
            == PTime.from_string("7")
        )
        assert self.time2 == PTime.from_string("14:17")
        assert (
            self.time3
            == PTime.from_string("00:00")
            == PTime.from_string("0:00")
            == PTime.from_string("0")
        )
        assert self.time4 == PTime.from_string("24:00") == PTime.from_string("24")

    def test_ensure_is_ptime(self) -> None:
        cand1 = PTime(5, 30)
        cand2 = "5:30"
        cand3 = "05:30"
        cand4 = 17
        cand5 = (14, 30)
        cand6 = ("14", "00")

        exp1 = cand1
        exp2 = cand1
        exp3 = cand1
        exp4 = PTime(17)
        exp5 = PTime(14, 30)
        exp6 = PTime(14)

        default = PTime(16, 57)

        imp1: Set = set()
        imp2 = "65"
        imp3 = "other string"
        imp4 = 25
        imp5 = (-3, 456)
        imp6 = (3, 30, 56)
        imp7 = None

        assert PTime.ensure_is_ptime(cand1) == exp1
        assert PTime.ensure_is_ptime(cand2) == exp2
        assert PTime.ensure_is_ptime(cand3) == exp3
        assert PTime.ensure_is_ptime(cand4) == exp4
        assert PTime.ensure_is_ptime(cand5) == exp5
        assert PTime.ensure_is_ptime(cand6) == exp6

        assert PTime.ensure_is_ptime(imp1, default=default) == default
        assert PTime.ensure_is_ptime(imp2, default=default) == default
        assert PTime.ensure_is_ptime(imp3, default=default) == default
        assert PTime.ensure_is_ptime(imp4, default=default) == default
        assert PTime.ensure_is_ptime(imp5, default=default) == default
        assert PTime.ensure_is_ptime(imp6, default=default) == default
        assert PTime.ensure_is_ptime(imp7, default=default) == default

    def test_bool(self) -> None:
        assert self.time1
        assert self.time2
        assert self.time3
        assert self.time4
        assert not self.time5

    def test_copy(self) -> None:
        t1 = self.time1.copy()
        t2 = self.time2.copy()
        t3 = self.time3.copy()
        t4 = self.time4.copy()
        t5 = self.time5.copy()

        assert self.time1 == t1
        assert self.time2 == t2
        assert self.time3 == t3
        assert self.time4 == t4
        assert self.time5 == t5

        assert id(self.time1) != id(t1)
        assert id(self.time2) != id(t2)
        assert id(self.time3) != id(t3)
        assert id(self.time4) != id(t4)
        assert id(self.time4) != id(t5)

    def test_tominutes(self) -> None:
        assert self.time1.tominutes() == 420
        assert self.time2.tominutes() == 857
        assert self.time3.tominutes() == 0
        assert self.time4.tominutes() == 1440

    def test_fromminutes(self) -> None:
        assert self.time1 == PTime.fromminutes(420)
        assert self.time2 == PTime.fromminutes(857)
        assert self.time3 == PTime.fromminutes(0)
        assert self.time4 == PTime.fromminutes(1440)

    def test_timeto(self) -> None:
        assert self.time1.timeto(self.time2) == 437
        assert self.time2.timeto(self.time1) == -437
        assert self.time3.timeto(self.time4) == 1440

    def test_timefrom(self) -> None:
        assert self.time1.timefrom(self.time2) == -437
        assert self.time2.timefrom(self.time1) == 437
        assert self.time3.timefrom(self.time4) == -1440

    def test_add(self) -> None:
        assert self.time1 + 34 == PTime(7, 34)
        assert self.time2 + 3 == PTime(14, 20)
        assert self.time3 + 180 == PTime(3)
        assert self.time4 + 1 == self.time4

    def test_sub(self) -> None:
        assert self.time1 - 34 == PTime(6, 26)
        assert self.time2 - 105 == PTime(12, 32)
        assert self.time3 - 1 == self.time3
        assert self.time4 - 1 == PTime(23, 59)

    def test_str(self) -> None:
        assert str(self.time1) == "07:00"
        assert str(self.time2) == "14:17"
        assert str(self.time3) == "00:00"
        assert str(self.time4) == "24:00"

    def test_repr(self) -> None:
        assert repr(self.time1) == "07:00"
        assert repr(self.time2) == "14:17"
        assert repr(self.time3) == "00:00"
        assert repr(self.time4) == "24:00"

    def test_eq(self) -> None:
        t1 = PTime(7)
        t2 = PTime(14, 17)
        t3 = PTime()
        t4 = PTime(24)
        t5 = PTime(isblank=True)

        assert self.time1 == t1
        assert self.time2 == t2
        assert self.time3 == t3 == self.time5 == t5
        assert self.time4 == t4

        assert self.time1 != self.time2
        assert self.time1 != self.time3
        assert self.time2 != self.time3

    def test_lt(self) -> None:
        assert self.time3 < self.time1 < self.time2 < self.time4
        assert not (self.time1 < self.time1)

    def test_gt(self) -> None:
        assert self.time4 > self.time2 > self.time1 > self.time3
        assert not (self.time1 > self.time1)

    def test_le(self) -> None:
        assert self.time3 <= self.time1 <= self.time2 <= self.time4
        assert self.time1 <= self.time1
        assert not (self.time1 <= self.time3)

    def test_ge(self) -> None:
        assert self.time4 >= self.time2 >= self.time1 >= self.time3
        assert self.time1 >= self.time1
        assert not (self.time3 >= self.time1)
