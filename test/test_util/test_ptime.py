import pytest

from planager.util import PTime
from planager.util.pdatetime.ptime import NoneTime


def test_basic_ptime() -> None:
    time1 = PTime()
    time2 = PTime(10, 43)
    time3 = PTime(24)

    blank = PTime(isblank=True)
    assert not blank
    assert bool(blank) == False

    assert time1.hour == 0
    assert time2.hour == 10
    assert time3.hour == 24

    assert time1.minute == 0
    assert time2.minute == 43
    assert time3.minute == 0

    with pytest.raises(ValueError) as excinfo:  # type: ignore
        t1 = PTime(25)
    assert str(excinfo.value) == "Time must be within 00:00..24:00"

    with pytest.raises(ValueError) as excinfo:  # type: ignore
        t1 = PTime(-1)
    assert str(excinfo.value) == "Time must be within 00:00..24:00"

    with pytest.raises(ValueError) as excinfo:  # type: ignore
        t1 = PTime(24, 1)
    assert str(excinfo.value) == "Time must be within 00:00..24:00"

    copy1 = time1.copy()
    assert copy1 == time1
    assert id(copy1) != id(time1)


def test_string_ops() -> None:
    assert PTime.from_string("15:32") == PTime(15, 32)
    assert PTime.from_string("none") == PTime.from_string("None") == PTime.nonetime() == NoneTime()

    with pytest.raises(AssertionError) as excinfo:  # type: ignore
        t1 = PTime.from_string(3)  # type: ignore
    assert str(excinfo.value) == "Argument to PTime.from_string must be str, not '<class 'int'>'."

    with pytest.raises(AssertionError) as excinfo:  # type: ignore
        t2 = PTime.from_string("3")
    assert (
        str(excinfo.value)
        == f"Argument to PTime.from_string must have exactly one colon. Given: '3'."
    )

    with pytest.raises(AssertionError) as excinfo:  # type: ignore
        t3 = PTime.from_string("3:55:34")
    assert (
        str(excinfo.value)
        == f"Argument to PTime.from_string must have exactly one colon. Given: '3:55:34'."
    )

    assert str(PTime(16, 2)) == "16:02"
    assert str(PTime(1, 22)) == "01:22"
    assert str(PTime(3, 5)) == "03:05"


def test_arithmetic() -> None:
    time1 = PTime(9)
    time2 = PTime(10, 43)
    time3 = PTime(10, 43)

    assert time1.timeto(time2) == 103
    assert time2.timefrom(time1) == 103
    assert (time2 - 103) == time1
    assert (time1 + 103) == time2

    assert 3 != time1
    assert time1 != 3

    assert time2 == time3
    assert time1 < time2
    assert time1 <= time2
    assert time2 <= time3
    assert not (time1 == time2)
    assert not (time1 > time2)
    assert not (time1 >= time2)
    assert not (time2 < time1)
    assert not (time2 <= time1)
    assert not (time2 > time3)
    assert not (time3 > time2)
    assert not (time2 < time3)
    assert not (time3 < time2)


def test_nonetime() -> None:
    nt = NoneTime()
    other = PTime(9, 0)

    assert str(nt) == "XX:XX"

    assert not nt
    assert bool(nt) == False
    assert (nt + other) == nt
    assert (nt - other) == nt
    assert (nt + 3) == nt
    assert (nt - 3) == nt

    assert not (nt == other)
    assert not (nt < other)
    assert not (nt <= other)
    assert not (nt > other)
    assert not (nt >= other)

    assert not (other == nt)
    assert not (other < nt)
    assert not (other <= nt)
    assert not (other > nt)
    assert not (other >= nt)
