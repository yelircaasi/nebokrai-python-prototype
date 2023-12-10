import sys
from typing import Optional, Tuple

import pytest

from nebokrai.util.elementary_types import TrackingActivityResponseType
from nebokrai.util.nkdatetime.nktime import NKTime
from nebokrai.util.prompt import (
    PromptConfig,
    prompt_any,
    prompt_atomic,
    prompt_composite,
    prompt_sequence,
)


def prompt_helper(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    pconf: PromptConfig,
    input_strings: Tuple[str, ...],
    expected_response: Optional[TrackingActivityResponseType],
    expected_error_message: Optional[str] = None,
) -> None:
    """
    Abstracts away the boilerplate code for testing input prompts.
    """
    string_iter = iter(input_strings)
    monkeypatch.setattr("builtins.input", lambda _: next(string_iter))  # type: ignore
    received = prompt_any(pconf)

    if expected_error_message is None:
        assert received == expected_response
    else:
        cap = capsys.readouterr()
        assert cap.out == expected_error_message


def test_prompt_config() -> None:
    ...


def test_prompt_atomic_boolean_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("boolean")
    assert (
        pc.prompt_message
        == "Please give an input corresponding to 'boolean', parsable as bool (':q' to quit):  "
    )

    prompt_helper(monkeypatch, capsys, pc, ("y",), True)
    prompt_helper(monkeypatch, capsys, pc, ("random",), False)


def test_prompt_atomic_float_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("float")
    pm = "Please give an input corresponding to 'float', parsable as float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("1.5",), 1.5)
    prompt_helper(monkeypatch, capsys, pc, ("random", "-3.897",), -3.897, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, (":q",), None, "")


def test_prompt_atomic_integer_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("float")
    pm = "Please give an input corresponding to 'float', parsable as float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("1.5",), 1.5)
    prompt_helper(monkeypatch, capsys, pc, ("random", "-3.897"), -3.897, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, (":q",), None, "")


def test_prompt_atomic_nonnegative_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("nonnegative")
    pm = "Please give an input corresponding to 'nonnegative', parsable as float and >= 0 (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("1.5",), 1.5)
    prompt_helper(monkeypatch, capsys, pc, ("-7", "10.9"), 10.9, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, (":q",), None, "")


def test_prompt_atomic_natural_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("natural")
    pm = "Please give an input corresponding to 'natural', parsable as int and >= 0 (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("34",), 34)
    prompt_helper(
        monkeypatch, capsys, pc, ("-16.02", "0.0", "0"), 0.0, "Invalid input.\nInvalid input.\n"
    )
    prompt_helper(monkeypatch, capsys, pc, (":q",), None, "")


def test_prompt_atomic_text_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("text")
    pm = "Please give an input corresponding to 'text', parsable as str (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("random text here",), "random text here")


def test_prompt_atomic_time_amount_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("time_amount")
    pm = "Please give an input corresponding to 'time_amount', parsable as NKTime or float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("3:45",), 225)
    prompt_helper(
        monkeypatch, capsys, pc, ("random", "3.5.7", "356"), 356, "Invalid input.\nInvalid input.\n"
    )


def test_prompt_atomic_time_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("time")
    pm = "Please give an input corresponding to 'time', parsable as NKTime (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("3:45",), NKTime(3, 45))
    prompt_helper(
        monkeypatch,
        capsys,
        pc,
        ("random", "3.5.7", "06:59"),
        NKTime(6, 59),
        "Invalid input.\nInvalid input.\n",
    )


def test_prompt_atomic_integer_sequence_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("integer_sequence")
    pm = "Please give an input corresponding to 'integer_sequence', parsable as list[int] (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("1 3 5 7 -9 ",), [1, 3, 5, 7, -9])
    prompt_helper(monkeypatch, capsys, pc, ("1, 3,5,7,-9 ",), [1, 3, 5, 7, -9])
    prompt_helper(monkeypatch, capsys, pc, ("1 3 5 7 -9 random", "1.5, 8", "-1, 0, 1"), [-1, 0, 1], "Invalid input.\nInvalid input.\n")


def test_prompt_atomic_natural_sequence_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("natural_sequence")
    pm = "Please give an input corresponding to 'natural_sequence', parsable as list[int] where each element > 0 (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("1 3 5 7  ",), [1, 3, 5, 7])
    prompt_helper(monkeypatch, capsys, pc, ("1, 3,5,7, ",), [1, 3, 5, 7])
    prompt_helper(monkeypatch, capsys, pc, ("random", "1 3 5 7 -9", "1.5, 8", "0, 1, 2"), [0, 1, 2], "Invalid input.\nInvalid input.\nInvalid input.\n")


def test_prompt_atomic_nonnegative_sequence_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("nonnegative_sequence")
    pm = "Please give an input corresponding to 'nonnegative_sequence', parsable as list[float] where each element > 0 (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, ("1 3 5 7  ",), [1.0, 3.0, 5.0, 7.0])
    prompt_helper(monkeypatch, capsys, pc, ("1.5, 3.3,5.5,7.7, ",), [1.5, 3.3, 5.5, 7.7])
    prompt_helper(monkeypatch, capsys, pc, ("random", "1 3 5 7 -9", "-1.5, 8", "0, 1.8, 2"), [0.0, 1.8, 2], "Invalid input.\nInvalid input.\nInvalid input.\n")
