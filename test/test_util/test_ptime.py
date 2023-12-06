from planager.util import PTime


def test_basic_ptime() -> None:
    time1 = PTime()
    time2 = PTime(10, 43)
    time3 = PTime(24)

    assert time1.hour == 0
    assert time2.hour == 10
    assert time3.hour == 24

    assert time1.minute == 0
    assert time2.minute == 43
    assert time3.minute == 0


def test_from_string() -> None:
    assert PTime.from_string("15:32") == PTime(15, 32)
