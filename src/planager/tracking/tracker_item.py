from typing import Optional, Union

from ..util.elementary_types import (
    DesirabilityString,
    PromptTypeName,
    TrackingActivityType,
)
from ..util.prompt import (
    prompt_boolean,
    prompt_natural,
    prompt_natural_sequence,
    prompt_text,
    prompt_time,
    prompt_time_amount,
    prompt_timed_distance,
    prompt_timed_distance_with_elevation,
    prompt_typed_list,
)
from ..util.prompt.prompt import prompt_integer, prompt_integer_sequence
from ..util.serde.custom_dict_types import (
    ActivityDictParsed,
    ActivityDictRaw,
    PromptDispatcherType,
    RoutineItemDictRaw,
)
from ..util.serde.deserialization import parse_activity_dict

JSONDict = dict[str, Union[str, float, list[dict], dict[str, Union[list, dict, float, str]]]]


# class _TrackerItem(Protocol):
#     """
#     Generic type for tracker items; not actually used, except for static type checking.
#     """

#     name: str
#     prompt: str
#     desirable: str
#     item_type: str
#     order: float
#     response: Any

#     def prompt_interactively(self) -> None:
#         ...

#     def serialize(self) -> JSONDict:
#         ...

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         ...


def prompt_():
    ...


prompt_dispatcher: PromptDispatcherType = {
    "sequence": prompt_typed_list,
    "time": prompt_time,
    "integer": prompt_integer,
    "integer_sequence": prompt_integer_sequence,
    "natural": prompt_natural,
    "time_amount": prompt_time_amount,
    "boolean": prompt_boolean,
    "natural_sequence": prompt_natural_sequence,
    "text": prompt_text,
    "timed_distance": prompt_timed_distance,
    "timed_distance_with_elevation": prompt_timed_distance_with_elevation,
}


class TrackerItem:
    """
    Used to track activities.

    Acceptable types:
      - ...
    """

    name: str
    prompt: str
    error_prompt: str = ""
    quit_string: str = "q"
    desirable: DesirabilityString
    item_type: PromptTypeName
    order: float
    response: Optional[TrackingActivityType]

    def __init__(self, _item_dict: ActivityDictRaw) -> None:
        item_dict: ActivityDictParsed = parse_activity_dict(_item_dict)
        self.name = item_dict["name"]
        self.prompt = item_dict["prompt"]
        self.error_prompt = item_dict.get("error_prompt", "")
        self.quit_string = "q"
        self.desirable = item_dict["desirable"]
        self.item_type = item_dict.get("dtype", "boolean")
        _order: Optional[float] = item_dict.get("order", 50.0)
        self.order: float = float(_order or 50.0)
        self.response = None
        self.items: list[PromptTypeName] = []

    @classmethod
    def from_routine_item_dict(
        cls, routine_item_dict: RoutineItemDictRaw, routine_name: str, order: float
    ) -> "TrackerItem":
        """
        Opens a routine item as if it had been defined under "tracking".
        """
        name = f"[{routine_name}] {routine_item_dict['name']}"
        activity_item_dict: ActivityDictRaw = {
            "name": name,
            "desirable": "yes",
            "prompt": f"Did you complete '{name}'?",
            "dtype": "boolean",
            "order": order,
            "response": None,
        }

        # print(order, routine_name, routine_item_dict['name'])
        return cls(activity_item_dict)

    def prompt_interactively(self) -> None:
        """
        Master method for interactive prompting, supporting all prompt data types.
        """
        if self.item_type == "sequence":
            subtype: PromptTypeName = self.items[0] if (self.items) else "natural"
            self.response = prompt_dispatcher[self.item_type](
                self.prompt, subtype, self.quit_string
            )
        else:
            self.response = prompt_dispatcher[self.item_type](
                self.prompt, self.error_prompt, self.quit_string
            )

    def deserialize(self, log_dict: ActivityDictRaw) -> None:
        """
        Instantiate from an activity subdict of the 'tracker' subdict of declaration.json.
        """
        assert self.name == log_dict["name"]
        assert self.item_type == log_dict["dtype"]
        self.response = log_dict.get("response") or self.response

    def serialize(self) -> ActivityDictRaw:
        return {
            "name": self.name,
            "response": self.response,
            "dtype": self.item_type,
            "desirable": self.desirable,
            "prompt": self.prompt,
        }


# class TextTrackerItem:
#     """
#     Used to track activities whose type is 'time' (\\d\\d-\\d\\d).
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[str]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[str] = None

#     def prompt_interactively(self) -> None:
#         print("Time =====")
#         self.response = prompt_text(self.prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class TimeTrackerItem:
#     """
#     Used to track activities whose type is 'time' (\\d\\d-\\d\\d).
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[PTime]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[PTime] = None

#     def prompt_interactively(self) -> None:
#         print("Time =====")
#         self.response = prompt_time(self.prompt, self.error_prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class NaturalTrackerItem:
#     """
#     Used to track activities whose type is 'natural' (nonnegative integer).
#     """

#     name: str
#     prompt: str
#     error_prompt: str
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[int]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[int] = None

#     def prompt_interactively(self) -> None:
#         print("Natural =====")
#         self.response = prompt_natural(self.prompt, self.error_prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class BoolTrackerItem:
#     """
#     Used to track activities whose type is 'boolean'. By default, any of {"y", "true", "done",
#       "yes", "yep"} is mapped to 'True'.
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[bool]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[bool] = None

#     @classmethod
#     def from_routine_item_dict(
#         cls, routine_item_dict: JSONDict, routine_name: str, order: float
#     ) -> "BoolTrackerItem":
#         """
#         Opens a routine item as if it had been defined under "tracking".
#         """
#         name = f"[{routine_name}] {routine_item_dict['name']}"
#         routine_item_dict.update(
#             {
#                 "name": name,
#                 "desirable": "yes",
#                 "prompt": f"Did you complete '{name}'?",
#                 "type": "boolean",
#                 "order": order,
#             }
#         )
#         # print(order, routine_name, routine_item_dict['name'])
#         return cls(routine_item_dict)

#     def prompt_interactively(self) -> None:
#         print("Bool =====")
#         self.response = prompt_boolean(self.prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class NaturalSequenceTrackerItem:
#     """
#     Used to track activities whose type is '[]natural' (list of nonnegative integers).
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[list[Any]]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[list[Any]] = None

#     def prompt_interactively(self) -> None:
#         print("Natural sequence =====")
#         self.response = prompt_natural_sequence(self.prompt, self.error_prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class TimeAmountTrackerItem:
#     """
#     Used to track activities whose type is 'time amount' (m minutes or hh:mm).
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[int]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[int] = None

#     def prompt_interactively(self) -> None:
#         print("Time amount =====")
#         self.response = prompt_time_amount(self.prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class TimedDistanceTrackerItem:
#     """
#     Used to track activities whose type is '[]natural' (list of nonnegative integers).
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[TimedDistance]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[dict[str, Union[int, float]]] = None

#     def prompt_interactively(self) -> None:
#         print("Timed distance =====")
#         self.response = prompt_timed_distance(self.prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# class TimedDistanceWETrackerItem:
#     """
#     Used to track activities whose type is '[]natural' (list of nonnegative integers).
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Optional[TimedDistanceWithElevation]

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         self.response: Optional[dict[str, Union[int, float]]] = None

#     def prompt_interactively(self) -> None:
#         print("Timed distance with elevation =====")
#         self.response = prompt_timed_distance_with_elevation(self.prompt)

#     def as_log_dict(self) -> JSONDict:
#         return {self.name: self.response}

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# # TODO; recursive behavior makes this significantly trickier than others
# class SequenceTrackerItem:
#     """
#     Used to track activities whose type is 'composite' - details defined in .json, potentially
#       recursively. In practice, typically used for exercise and food.

#     TODO: Cases to support:
#       - workout / exercise: list of either natural sequence, custom
#         custom -> "timed"? time distance; timed distance with elevation up and down
#       - food: quantified string
#     """

#     name: str
#     prompt: str
#     error_prompt: str = ""
#     desirable: str
#     item_type: str
#     order: float
#     response: Any

#     def __init__(self, item_dict: JSONDict) -> None:
#         self.name: str = item_dict["name"]
#         self.prompt: str = item_dict["prompt"].strip() + "  "
#         self.error_prompt: str = item_dict.get("error_prompt", "")
#         self.desirable: str = item_dict["desirable"]
#         self.item_type: str = item_dict["type"]
#         self.subitem_type: str = item_dict["item"]["type"]
#         _order = item_dict.get("order", 50.0)
#         self.order: float = float(_order or 50.0)
#         # self.subitems = [get_tracker_item(item_dict) for item_dict in item_dict["items"]]
#         self.response: list[Any] = []
#         self.quit_string = item_dict.get("quit_string") or "quit"

#     def prompt_interactively(self) -> None:
#         """
#         Print the main prompt (a sort of header here) and then run the interactive prompt for each
#           subitem.
#         """
#         # print("Sequence =====")

#         # print(self.prompt)
#         self.response.extend(
#             prompt_typed_list(self.subitem_type, self.prompt, quit_string=self.quit_string)
#         )

#     def as_log_dict(self) -> JSONDict:
#         return {
#             self.name: [
#                 subitem if isinstance(subitem, (str, int, float)) else subitem.as_log_dict()
#                 for subitem in self.response
#             ]
#         }

#     def read_log_dict(self, log_dict: JSONDict) -> None:
#         assert self.name == log_dict["name"]
#         self.response = log_dict.get("response") or self.response


# def get_tracker_item(item_dict: dict[str, Union[str, list, dict]]) -> TrackerItem:
#     match str(item_dict["type"]).lower():
#         case "sequence":
#             return SequenceTrackerItem(item_dict)
#         case "time":
#             return TimeTrackerItem(item_dict)
#         case "natural":
#             return NaturalTrackerItem(item_dict)
#         case "time_amount":
#             return TimeAmountTrackerItem(item_dict)
#         case "boolean":
#             return BoolTrackerItem(item_dict)
#         case "natural_sequence":
#             return NaturalSequenceTrackerItem(item_dict)
#         case "text":
#             return TimedDistanceTrackerItem(item_dict)
#         case _:
#             raise ValueError(f"{item_dict['type']} is not a valid tracker item type.")
