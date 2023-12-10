import re

from ..elementary_types import Natural


def prompt_integer(
    prompt_message: str,
    invalid_input_message: str = "",
    _: str = "",
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


def prompt_text(prompt_message: str, _1: str = "", _2: str = "") -> str:
    return input(prompt_message)


def prompt_natural(
    prompt_message: str,
    invalid_input_message: str = "Please enter a nonnegative integer.",
    _: str = "",
) -> int:
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


def prompt_natural_sequence(
    prompt_message: str,
    invalid_input_message: str = (
        "Invalid input. Please enter a sequence of natural numbers "
        "separated by spaces, commas, or both."
    ),
    _: str = "",
) -> list[Natural]:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            input_str = input(prompt_message).strip()
            if re.match(r"\d\d?-\d\d?$", input_str):
                start, end = input_str.split("-")[:2]
                return list(range(int(start), int(end) + 1))
            value = list(map(int, re.split("[, ]+", input_str)))
            assert all(map(lambda x: x >= 0, value))
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value
