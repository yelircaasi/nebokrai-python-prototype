from typing import Any, Optional, Protocol, Union

from ..util import PTime
from ..util.prompt import (
    prompt_boolean,
    prompt_natural,
    prompt_natural_sequence,
    prompt_time,
    prompt_typed_list,
)


class TrackerItem(Protocol):
    """
    Generic type for tracker items; not actually used, except for static type checking.
    """

    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str
    response: Any

    def prompt_interactively(self) -> None:
        ...

    def as_log_dict(self) -> dict[str, Any]:
        ...

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class TimeTrackerItem:
    """
    Used to track activities whose type is 'time' (\\d\\d-\\d\\d).
    """

    name: str
    prompt: str
    error_prompt: str = ""
    desirable: str
    item_type: str
    order: str
    response: Optional[PTime]

    def __init__(self, item_dict: dict[str, Any]) -> None:
        self.name: str = item_dict["name"]
        self.prompt: str = item_dict["prompt"]
        self.desirable: str = item_dict["desirable"]
        self.item_type: str = item_dict["type"]
        self.order: str = item_dict["order"]
        self.response = None

    def prompt_interactively(self) -> None:
        self.response = prompt_time(self.prompt, self.error_prompt)

    def as_log_dict(self) -> dict[str, Any]:
        return {self.name: self.response}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        assert self.name == log_dict["name"]
        self.response = log_dict.get("response") or self.response


class NaturalTrackerItem:
    """
    Used to track activities whose type is 'natural' (nonnegative integer).
    """

    name: str
    prompt: str
    error_prompt: str
    desirable: str
    item_type: str
    order: str
    response: Optional[int]

    def __init__(self, item_dict: dict[str, Any]) -> None:
        self.name: str = item_dict["name"]
        self.prompt: str = item_dict["prompt"]
        self.desirable: str = item_dict["desirable"]
        self.item_type: str = item_dict["type"]
        self.order: str = item_dict["order"]

    def prompt_interactively(self) -> None:
        self.response = prompt_natural(self.prompt, self.error_prompt)

    def as_log_dict(self) -> dict[str, Any]:
        return {self.name: self.response}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        assert self.name == log_dict["name"]
        self.response = log_dict.get("response") or self.response


class BoolTrackerItem:
    """
    Used to track activities whose type is 'boolean'. By default, any of {"y", "true", "done",
      "yes", "yep"} is mapped to 'True'.
    """

    name: str
    prompt: str
    error_prompt: str = ""
    desirable: str
    item_type: str
    order: str
    response: Optional[bool]

    def __init__(self, item_dict: dict[str, Any]) -> None:
        self.name: str = item_dict["name"]
        self.prompt: str = item_dict["prompt"]
        self.desirable: str = item_dict["desirable"]
        self.item_type: str = item_dict["type"]
        self.order: str = item_dict["order"]
        self.response: Optional[bool]

    @classmethod
    def from_routine_item_dict(
        cls, routine_item_dict: dict[str, Any], routine_name: str
    ) -> "BoolTrackerItem":
        """
        Opens a routine item as if it had been defined under "tracking".
        """
        routine_item_dict.update(
            {
                "desirable": "yes",
                "prompt": f"Did you complete '{routine_name} : {routine_item_dict['name']}'?",
                "type": "boolean",
                "order": 99,
            }
        )
        return cls(routine_item_dict)

    def prompt_interactively(self) -> None:
        self.response = prompt_boolean(self.prompt)

    def as_log_dict(self) -> dict[str, Any]:
        return {self.name: self.response}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        assert self.name == log_dict["name"]
        self.response = log_dict.get("response") or self.response


class NaturalSequenceTrackerItem:
    """
    Used to track activities whose type is '[]natural' (list of nonnegative integers).
    """

    name: str
    prompt: str
    error_prompt: str = ""
    desirable: str
    item_type: str
    order: str
    response: Optional[list[Any]]

    def __init__(self, item_dict: dict[str, Any]) -> None:
        self.name: str = item_dict["name"]
        self.prompt: str = item_dict["prompt"]
        self.desirable: str = item_dict["desirable"]
        self.item_type: str = item_dict["type"]
        self.order: str = item_dict["order"]

    def prompt_interactively(self) -> None:
        self.response = prompt_natural_sequence(self.prompt, self.error_prompt)

    def as_log_dict(self) -> dict[str, Any]:
        return {self.name: self.response}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        assert self.name == log_dict["name"]
        self.response = log_dict.get("response") or self.response


# TODO; recursive behavior makes this significantly trickier than others
class CompositeTrackerItem:
    """
    Used to track activities whose type is 'composite' - details defined in .json, potentially
      recursively. In practice, typically used for exercise and food.

    TODO: Cases to support:
      - workout / exercise: list of either natural sequence, custom
        custom -> "timed"? time distance; timed distance with elevation up and down
      - food: quantified string
    """

    name: str
    prompt: str
    error_prompt: str = ""
    desirable: str
    item_type: str
    order: str
    response: Any

    def __init__(self, item_dict: dict[str, Any]) -> None:  # TODO
        self.name: str = item_dict["name"]
        self.prompt: str = item_dict["prompt"]
        self.desirable: str = item_dict["desirable"]
        self.item_type: str = item_dict["type"]
        self.order: str = item_dict["order"]
        self.subitems = [get_tracker_item(item_dict) for item_dict in item_dict["items"]]
        self.quit_string = item_dict.get("quit_string") or "quit"

    def prompt_interactively(self) -> None:
        """
        Print the main prompt (a sort of header here) and then run the interactive prompt for each
          subitem.
        """
        print(self.prompt)
        prompt_typed_list(self.item_type, self.prompt, quit_string=self.quit_string)

    def as_log_dict(self) -> dict[str, Any]:  # TODO
        return {self.name: [subitem.as_log_dict() for subitem in self.subitems]}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        assert self.name == log_dict["name"]
        self.response = log_dict.get("response") or self.response


def get_tracker_item(item_dict: dict[str, Union[str, list, dict]]) -> TrackerItem:
    match item_dict["type"]:
        case "composite":
            return CompositeTrackerItem(item_dict)
        case "time":
            return TimeTrackerItem(item_dict)
        case "natural":
            return NaturalTrackerItem(item_dict)
        case "boolean":
            return BoolTrackerItem(item_dict)
        case "[]natural":
            return NaturalSequenceTrackerItem(item_dict)
        case _:
            raise ValueError(f"{item_dict['type']} is not a valid tracker item type.")
