import re
from typing import Any, Callable, Iterable, Union

from typing_extensions import TypedDict

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


def prompt_string(prompt_message: str) -> str:
    return input(prompt_message)


def prompt_boolean(
    prompt_message: str,
    valid_true: Iterable[str] = ("y", "true", "done", "yes", "yep"),
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
        "Invalid input. Please enter a sequence of natural numbers "
        "separated by spaces, commas, or both."
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


TimedDistance = TypedDict(
    "TimedDistance", {"time (s)": Union[int, float], "distance (km)": Union[int, float]}
)
TimedDistanceWithElevation = TypedDict(
    "TimedDistanceWithElevation",
    {
        "time (s)": Union[int, float],
        "distance (km)": Union[int, float],
        "up (m)": Union[int, float],
        "down (m)": Union[int, float],
    },
)


def prompt_numerical(
    prompt_message: str, invalid_input_message: str = "Please enter a number."
) -> float:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            value = float(input(prompt_message))
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return value


def prompt_time_amount(
    prompt_message: str,
    invalid_input_message: str = "Please enter either a number of seconds or a time duration in the form of `mm:ss`.",
) -> int:
    """
    Interactively prompts for an integer until an integer is given.
    """
    isvalid = False
    while not isvalid:
        try:
            string_value = (input(prompt_message)).strip()
            if ":" in string_value:
                min, sec = string_value.split(":")[:2]
                value = 60 * float(min) + float(sec)
            else:
                value = float(string_value)
            isvalid = True
        except ValueError:
            print(invalid_input_message)
            continue
    return int(value)


def prompt_timed_distance(prompt_message: str) -> TimedDistance:
    print(prompt_message)
    distance = prompt_numerical("Distance: ")
    time_seconds = prompt_time_amount("Time: ")
    return {"distance (km)": distance, "time (s)": time_seconds}


def prompt_timed_distance_with_elevation(prompt_message: str) -> TimedDistanceWithElevation:
    print(prompt_message)
    distance = prompt_numerical("Distance: ")
    time_seconds = prompt_time_amount("Time: ")
    up = prompt_numerical("Up (elevation gain): ")
    down = prompt_numerical("Down (elevation loss): ")
    return {"distance (km)": distance, "time (s)": time_seconds, "up (m)": up, "down (m)": down}


simple_prompt_functions: dict[str, Callable] = {
    "integer": prompt_integer,
    "boolean": prompt_boolean,
    "natural": prompt_natural,
    "[]natural": prompt_natural_sequence,
    "[]integer": prompt_integer_sequence,
    "text": prompt_string,
    "time": prompt_time,
    "timed distance": prompt_timed_distance,
    "timed distance with elevation": prompt_timed_distance_with_elevation,
}


def prompt_typed_list(item_type: str, prompt_message: str, quit_string: str = "q") -> list[Any]:
    """
    Interactively prompts for an item of type `item_type` until the quit_string is entered.
    """
    responses: list[Any] = []
    print(prompt_message)
    print(f"Enter {quit_string} when you are finished.")
    prompt_function = simple_prompt_functions[item_type]

    quit = False
    while not quit:
        response = prompt_function(prompt_message)
        quit = str(response).strip().lower() == quit_string
        if not quit:
            responses.append(response)
    return responses
