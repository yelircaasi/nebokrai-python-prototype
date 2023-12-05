from planager.util import round5


def test_round5() -> None:
    assert round5(1) == 0
    assert round5(2) == 0
    assert round5(3) == 5
    assert round5(1.5) == 0
    assert round5(-1) == 0
    assert round5(1) == 0
    assert round5(2.5) == 5
    assert round5(25) == 25
    assert round5(-45) == -45
    assert round5(-44) == -45
    assert round5(-45.5) == -45
    assert round5(23) == 25
    assert round5(22.5) == 25
