import re
from typing import Iterable

from .pdatetime import PTime


def prompt_integer(prompt_message: str, invalid_input_message: str = "") -> int:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            value = int(input(prompt_message))
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value


def prompt_boolean(
    prompt_message: str,
    valid_true: Iterable[str] = {"y", "true", "done", "yes", "yep"},
) -> bool:
    """
    Interactively prompts for an boolean. Inputs in 'valid_true' are treated as True; others are
      interpreted as False.
    """
    value = input(prompt_message).strip().lower() in valid_true
    return value


def prompt_natural(prompt_message: str, invalid_input_message: str = "") -> int:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            value = int(input(prompt_message))
            assert value >= 0
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value


def prompt_integer_sequence(
    prompt_message: str,
    invalid_input_message: str = (
        "Invalid input. Please enter a sequence of integers separated by spaces, commas, or both."
    ),
) -> int:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            value = int(input(prompt_message))
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value


def prompt_natural_sequence(
    prompt_message: str,
    invalid_input_message: str = (
        "Invalid input. Please enter a sequence of natural numbers separated by spaces, commas, or both."
    ),
) -> list[int]:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            input_str = input(prompt_message).strip()
            value = list(map(int, re.split("[, ]+", input_str)))
            assert all(map(lambda x: x >= 0, value))
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value


def prompt_time(prompt_message: str, invalid_input_message: str = "") -> PTime:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            value = PTime.from_string(input(prompt_message))
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value
