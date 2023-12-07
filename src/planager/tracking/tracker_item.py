from typing import Optional, Union

from ..util.elementary_types import (
    DesirabilityString,
    PromptTypeName,
    TrackingActivityType,
)
from ..util.prompt import PromptConfig, prompt_any, prompt_configs
from ..util.serde.custom_dict_types import (
    ActivityDictParsed,
    ActivityDictRaw,
    RoutineItemDictRaw,
)
from ..util.serde.deserialization import parse_activity_dict

JSONDict = dict[str, Union[str, float, list[dict], dict[str, Union[list, dict, float, str]]]]


print(prompt_configs)
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
        self.quit_string = ":q"
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
        item_prompt_config = self.prompt_config_from_info
        self.response = prompt_any(item_prompt_config)

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

    @property
    def prompt_config_from_info(self) -> PromptConfig:
        """
        Create an i4tance of PromptConfig from the information supplied in declaration.json,
          via the parsed activity dict.
        """
        # LOGIC TO HAPPEN HERE
        return PromptConfig("boolean")  # TODO
