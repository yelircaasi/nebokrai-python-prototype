import pytest

from planager.util.display.repr import tabularize, wrap_as_list, wrap_string


def test_tabularize() -> None:
    string1 = 100 * "="

    exp1 = "│ ============================================================================ │\n│   ========================                                                   │"

    assert tabularize(string1) == exp1


def test_wrap_as_list() -> None:
    string1 = 100 * "="
    exp1 = [
        "================================================================================",
        "  ====================",
    ]
    assert wrap_as_list(string1, 80, 2) == exp1
    assert True


def test_wrap_string() -> None:
    string1 = 100 * "="
    exp1 = "================================================================================\n  ===================="
    exp2 = "│ ============================================================================ │\n│   ========================                                                   │"
    assert wrap_string(string1) == exp1
    assert wrap_string(string1, borders=True) == exp2
    assert True
