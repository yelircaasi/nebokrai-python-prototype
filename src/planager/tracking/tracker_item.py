from abc import ABCMeta, abstractmethod
from typing import Any, Protocol, Union

from ..configuration import path_manager

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

    def prompt_interactively(self) -> None:
        ...

    def as_log_dict(self) -> dict[str, Any]:
        ...

    def read_log_dict(self, log_dict: dict[str, Any]) -> None:
        ...


class CompositeTrackerItem:
    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str

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


class TimeTrackerItem:
    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str

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


class NaturalTrackerItem:
    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str

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


class BoolTrackerItem:
    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str

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


class SequenceTrackerItem:
    name: str
    prompt: str
    desirable: str
    item_type: str
    order: str

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


# TrackerItem = Union[
#     CompositeTrackerItem, TimeTrackerItem, NaturalTrackerItem, BoolTrackerItem, SequenceTrackerItem
# ]


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
            return SequenceTrackerItem(item_dict)
        case _:
            raise ValueError(f"{item_dict['type']} is not a valid tracker item type.")
