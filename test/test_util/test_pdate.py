from planager.util import PDate


def test_basic_pdate() -> None:
    date1 = PDate(2023, 2, 20)
    assert date1 == PDate(2023, 2, 20)


def test_from_string() -> None:
    assert PDate(2023, 2, 20) == PDate.from_string("2023-02-20")
    assert PDate(2023, 2, 20) == PDate.from_string("2023-2-20")
