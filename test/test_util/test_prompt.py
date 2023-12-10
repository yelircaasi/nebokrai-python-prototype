import sys
from typing import Callable, Optional, TypeVar, Union

import pytest

# from pytest import monkeypatch

from planager.util.elementary_types import TrackingActivityResponseType
from planager.util.prompt import (
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
    expected_response: TrackingActivityResponseType | ellipsis,
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
    prompt_helper(monkeypatch, capsys, pc, ":q", ..., "")


def test_prompt_atomic_integer_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    pc = PromptConfig("float")
    pm = "Please give an input corresponding to 'float', parsable as float (':q' to quit):  "
    assert pc.prompt_message == pm

    prompt_helper(monkeypatch, capsys, pc, "1.5", 1.5)
    prompt_helper(monkeypatch, capsys, pc, ["random", "-3.897"], -3.897, "Invalid input.\n")
    prompt_helper(monkeypatch, capsys, pc, ":q", ..., "")


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
    # pc = PromptConfig("")
    # prompt_helper(monkeypatch, pc, [""], ...)


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
    prompt_helper(monkeypatch, capsys, pc, ":q", ..., "")


def test_prompt_composite_timed_distance_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    ...


# def test_prompt_boolean_parsing(monkeypatch) -> None:
#     # def prompt_helper(input_str: str, expected: bool) -> bool:
#     #     monkeypatch.setattr("builtins.input", lambda _: input_str)
#     #     received = prompt_boolean("Placeholder message")
#     #     return received == expected

#     prompt_helper = make_prompt_helper(prompt_boolean)

#     assert prompt_helper("true", True)
#     assert prompt_helper("True", True)
#     assert prompt_helper("TRUE", True)
#     assert prompt_helper("y", True)
#     assert prompt_helper("Y", True)
#     assert prompt_helper("done", True)
#     assert prompt_helper("Done", True)
#     assert prompt_helper("yes", True)
#     assert prompt_helper("YES", True)
#     assert prompt_helper("yep", True)
#     assert prompt_helper("Yep", True)
#     assert prompt_helper("some random string", False)
#     assert prompt_helper("no", False)
#     assert prompt_helper("No", False)
#     assert prompt_helper("n", False)
#     assert prompt_helper("", False)


# def test_prompt_boolean_prompt(capsys, monkeypatch) -> None:
#     # def new_input(prmpt: str) -> str:
#     #     sys.stdout.write(prmpt)
#     #     return "y"

#     monkeypatch.setattr("builtins.input", make_new_input("y"))
#     received = prompt_boolean("New prompt")
#     cap = capsys.readouterr()
#     assert cap.out == "New prompt"
#     assert received == True


# def test_prompt_integer_parsing(monkeypatch) -> None:
#     assert False


# def test_prompt_integer_prompt(monkeypatch) -> None:
#     # def new_input(prmpt: str) -> str:
#     #     sys.stdout.write(prmpt)
#     #     return "y"

#     monkeypatch.setattr("builtins.input", new_input)
#     received = prompt_boolean("New prompt")
#     cap = capsys.readouterr()
#     assert cap.out == "New prompt"
#     assert received == True


# def test_prompt_integer_sequence(monkeypatch) -> None:

#     assert False


# def test_prompt_natural(monkeypatch) -> None:

#     assert False


# def test_prompt_natural_sequence(monkeypatch) -> None:

#     assert False


# def test_prompt_numerical(monkeypatch) -> None:

#     assert False


# def test_prompt_text(monkeypatch) -> None:

#     assert False


# def test_prompt_time(monkeypatch) -> None:

#     assert False


# def test_prompt_time_amount(monkeypatch) -> None:

#     assert False


# def test_prompt_timed_distance(monkeypatch) -> None:

#     assert False


# def test_prompt_timed_distance_with_elevation(monkeypatch) -> None:

#     assert False


# def test_prompt_typed_list(monkeypatch) -> None:

#     assert False


# def test_simple_prompt_functions(monkeypatch) -> None:

#     assert False
