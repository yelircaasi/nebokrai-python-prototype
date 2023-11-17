from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Protocol, Union

from ..configuration import path_manager
from ..util import PDate, PTime
from ..util.prompt import (
    prompt_boolean,
    prompt_integer,
    prompt_natural,
    prompt_natural_sequence,
    prompt_time,
)

# class TrackerItem(Protocol):
#     """
#     Single item for tracking, corresponding to an activity such as 'time spent
#       practicing the piano' or 'workout'.
#     """
#     item_type: str
#     name: str
#     prompt: str
#     desirable: str

#     def prompt_interactively(self) -> None:
#         ...

#     def as_log_dict(self) -> dict[str, Any]:

#         return {}

#     def read_log_dict(self, log_dict: dict[str, Any]) -> None:
#         ...


class TrackerItem(Protocol):
    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str
    response: Any

    def prompt_interactively(self) -> None:
        ...

    def as_log_dict(self) -> dict[str, Any]:
        return {}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class TimeTrackerItem:
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
        return {}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class NaturalTrackerItem:
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
        return {}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class BoolTrackerItem:
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
        
    def prompt_interactively(self) -> None:
        self.response = prompt_boolean(self.prompt)

    def as_log_dict(self) -> dict[str, Any]:
        return {}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class NaturalSequenceTrackerItem:
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
        return {}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class CompositeTrackerItem: #TODO; recursive behavior makes this significantly trickier than others
    name: str
    prompt: str
    error_prompt: str = ""
    desirable: str
    item_type: str
    order: str
    response: Any

    def __init__(self, item_dict: dict[str, Any]) -> None:
        self.name: str = item_dict["name"]
        self.prompt: str = item_dict["prompt"]
        self.desirable: str = item_dict["desirable"]
        self.item_type: str = item_dict["type"]
        self.order: str = item_dict["order"]

    def prompt_interactively(self) -> None:
        ...

    def as_log_dict(self) -> dict[str, Any]:
        return {}

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


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
