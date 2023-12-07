import sys
from typing import Callable, TypeVar

import pytest
from pytest import monkeypatch

from planager.util.elementary_types import TrackingActivityType
from planager.util.prompt import PromptConfig, prompt_any, prompt_configs

# from ..util import make_new_input


T = TypeVar("T")


# def make_prompt_helper(prompt_func: Callable[[], TrackingActivityType], ) -> Callable[[str, T], bool]:
#     def inner(input_str: str, expected: T) -> T:
#         monkeypatch.setattr("builtins.input", lambda _: input_str)
#         received = prompt_boolean(*arg_triplet)
#         return received == expected

#     return inner


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
