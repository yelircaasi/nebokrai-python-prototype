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


# def prompt_integer_sequence(
#     prompt_message: str,
#     invalid_input_message: str = (
#         "Invalid input. Please enter a sequence of integers separated by spaces, commas, or both."
#     ),
#     _: str = "",
# ) -> list[int]:
#     """
#     Interactively prompts for an integer until an integer is given.
#     """
#     isvalid = False
#     while not isvalid:
#         try:
#             input_str = input(prompt_message).strip()
#             value = list(map(int, re.split("[, ]+", input_str)))
#             isvalid = True
#         except ValueError:
#             print(invalid_input_message)
#             continue
#     return value


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


# def prompt_time(prompt_message: str, invalid_input_message: str = "", _: str = "") -> PTime:
#     """
#     Interactively prompts for an integer until an integer is given.
#     """
#     isvalid = False
#     while not isvalid:
#         try:
#             value = PTime.from_string(input(prompt_message))
#             isvalid = True
#         except ValueError:
#             print(invalid_input_message)
#             continue
#     return value


# def prompt_numerical(
#     prompt_message: str, invalid_input_message: str = "Please enter a number."
# ) -> float:
#     """
#     Interactively prompts for a number until a number is given.
#     """
#     isvalid = False
#     while not isvalid:
#         try:
#             value = float(input(prompt_message))
#             isvalid = True
#         except ValueError:
#             print(invalid_input_message)
#             continue
#     return value


# def prompt_time_amount(
#     prompt_message: str,
#     invalid_input_message: str = (
#         "Please enter either a number of seconds or a time duration in the form of `mm:ss`."
#     ),
#     _: str = "",
# ) -> float:
#     """
#     Interactively prompts for an integer until an integer is given.
#     """
#     isvalid = False
#     while not isvalid:
#         try:
#             string_value = (input(prompt_message)).strip()
#             if ":" in string_value:
#                 mins, secs = string_value.split(":")[:2]
#                 value = 60 * float(mins) + float(secs)
#             else:
#                 value = float(string_value)
#             isvalid = True
#         except ValueError:
#             print(invalid_input_message)
#             continue
#     return int(value)


# def prompt_timed_distance(prompt_message: str, _1: str = "", _2: str = "") -> TimedDistance:
#     """
#     Interactively solicit distance and time, e.g. of a run/walk.
#     """
#     print(prompt_message)
#     distance: float = prompt_numerical("Distance: ")
#     seconds: float = prompt_time_amount("Time: ")
#     return {"kilometers": distance, "seconds": seconds}


# def prompt_timed_distance_with_elevation(
#     prompt_message: str, _1: str = "", _2: str = ""
# ) -> TimedDistanceWithElevation:
#     """
#     Interactively solicit distance, time, elevaition gain, and elevation loss, e.g. of a run/walk.
#     """

#     print(prompt_message)
#     distance = prompt_numerical("Distance: ")
#     time_seconds = prompt_time_amount("Time: ")
#     up = prompt_numerical("Up (elevation gain): ")
#     down = prompt_numerical("Down (elevation loss): ")
#     return {"kilometers": distance, "seconds": time_seconds, "up": up, "down": down}


# simple_prompt_functions: dict[PromptTypeName, Callable] = {
#     "integer": prompt_integer,
#     "boolean": prompt_boolean,
#     "natural": prompt_natural,
#     "natural_sequence": prompt_natural_sequence,
#     "integer_sequence": prompt_integer_sequence,
#     "text": prompt_text,
#     "time": prompt_time,
#     "timed_distance": prompt_timed_distance,
#     "timed_distance_with_elevation": prompt_timed_distance_with_elevation,
# }


# def prompt_typed_list(
#     prompt_message: str, quit_string: str, item_type: PromptTypeName
# ) -> list[TrackingActivityResponseType]:
#     """
#     Interactively prompts for an item of type `item_type` until the quit_string is entered.
#     """
#     responses: list[Any] = []
#     print(prompt_message)
#     print(f"Enter {quit_string} when you are finished.")
#     prompt_function = simple_prompt_functions[item_type]

#     quit_loop = False
#     while not quit_loop:
#         response = prompt_function(prompt_message)
#         if not quit_loop:
#             responses.append(response)
#         quit_loop = (
#             str(input(f"Type '{quit_string}' to quit; leave empty to continue.")).strip().lower()
#             == quit_string
#         )

#     return responses


# # prompt_dispatcher: PromptDispatcherType = {
# #     "sequence": prompt_typed_list,
# #     "time": prompt_time,
# #     "integer": prompt_integer,
# #     "float": prompt_integer,
# #     "integer_sequence": prompt_integer_sequence,
# #     "natural": prompt_natural,
# #     "time_amount": prompt_time_amount,
# #     "boolean": prompt_boolean,
# #     "natural_sequence": prompt_natural_sequence,
# #     "text": prompt_text,
# #     "timed_distance": prompt_timed_distance,
# #     "timed_distance_with_elevation": prompt_timed_distance_with_elevation,
# # }
