import pytest

from planager.util.misc import expand_task_segments, round5


def test_round5() -> None:
    assert round5(1) == 0
    assert round5(3) == 5
    assert round5(2.5) == 5
    assert round5(63) == 65
    assert round5(12) == 10


def test_expand_task_segments() -> None:
    abbr1 = "0-10"
    exp1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    abbr2 = "3-11"
    exp2 = ["3", "4", "5", "6", "7", "8", "9", "10", "11"]

    abbr3 = "1-5, A"
    exp3 = ["1", "2", "3", "4", "5", "A"]

    abbr4 = "1-5,A"
    exp4 = ["1", "2", "3", "4", "5", "A"]

    abbr5 = "1"
    exp5 = ["1"]

    abbr6 = "Section X"
    exp6 = ["Section X"]

    abbr7 = "Section 1, Section 2, Section 3"
    exp7 = ["Section 1", "Section 2", "Section 3"]

    abbr8 = "chapter1,chapter2,chapter3"
    exp8 = ["chapter1", "chapter2", "chapter3"]

    abbr9 = "4-5"
    exp9 = ["4", "5"]

    abbr10 = "1-4,A1-A4"
    exp10 = ["1", "2", "3", "4", "A1", "A2", "A3", "A4"]

    abbr11 = "10-17, A1-A7"
    exp11 = [
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
    ]

    abbr12 = "11-13,A1-A3,B0-B2,C2-C6"
    exp12 = [
        "11",
        "12",
        "13",
        "A1",
        "A2",
        "A3",
        "B0",
        "B1",
        "B2",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
    ]

    assert expand_task_segments(abbr1) == exp1
    assert expand_task_segments(abbr2) == exp2
    assert expand_task_segments(abbr3) == exp3
    assert expand_task_segments(abbr4) == exp4
    assert expand_task_segments(abbr5) == exp5
    assert expand_task_segments(abbr6) == exp6
    assert expand_task_segments(abbr7) == exp7
    assert expand_task_segments(abbr8) == exp8
    assert expand_task_segments(abbr9) == exp9
    assert expand_task_segments(abbr10) == exp10
    assert expand_task_segments(abbr11) == exp11
    assert expand_task_segments(abbr12) == exp12
