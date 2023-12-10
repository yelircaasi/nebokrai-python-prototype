import sys
from typing import Callable, Optional, TypeVar, Union

import pytest

from nebokrai.util.elementary_types import TrackingActivityResponseType
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
    input_strings: Union[str, list[str]],
    expected_response: Optional[TrackingActivityResponseType],
    expected_error_message: Optional[str] = None,
) -> None:
    """
    Abstracts away the boilerplate code for testing input prompts.
    """
    if isinstance(input_strings, str):
        input_strings = [input_strings]
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

    prompt_helper(monkeypatch, capsys, pc, "y", True)
    prompt_helper(monkeypatch, capsys, pc, "random", False)


def test_prompt_atomic_float_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("float")
    pm = "Please give an input corresponding to 'float', parsable as float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, "1.5", 1.5)
    prompt_helper(monkeypatch, capsys, pc, ["random", "-3.897"], -3.897, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, ":q", None, "")


def test_prompt_atomic_integer_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("float")
    pm = "Please give an input corresponding to 'float', parsable as float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, "1.5", 1.5)
    prompt_helper(monkeypatch, capsys, pc, ["random", "-3.897"], -3.897, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, ":q", None, "")


def test_prompt_atomic_nonnegative_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_atomic_natural_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_atomic_text_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_atomic_time_amount_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_atomic_time_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_atomic_integer_sequence_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_atomic_natural_sequence_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


def test_prompt_composite_timed_distance_with_elevation_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("float")
    pm = "Please give an input corresponding to 'float', parsable as float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, "1.5", 1.5)
    prompt_helper(monkeypatch, capsys, pc, ["random", "-3.897"], -3.897, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, ":q", None, "")


def test_prompt_composite_timed_distance_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...
