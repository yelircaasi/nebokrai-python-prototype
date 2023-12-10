from typing import Optional, Union

from ..util.elementary_types import (
    DesirabilityString,
    PromptTypeName,
    TrackingActivityResponseType,
)
from ..util.prompt import PromptConfig, prompt_any
from ..util.serde.custom_dict_types import (
    ActivityDictParsed,
    ActivityDictRaw,
    RoutineItemDictRaw,
)
from ..util.serde.deserialization import parse_activity_dict

JSONDict = dict[str, Union[str, float, list[dict], dict[str, Union[list, dict, float, str]]]]


# print(prompt_configs)


class TrackerItem:
    """
    Used to track activities.

    Acceptable types:
      - ...
    """

    name: str
    prompt_config: PromptConfig
    error_prompt: str = ""
    quit_string: str = "q"
    desirable: DesirabilityString
    item_type: PromptTypeName
    order: float
    response: Optional[TrackingActivityResponseType]

    def __init__(self, _activity_dict: ActivityDictRaw) -> None:
        activity_dict: ActivityDictParsed = parse_activity_dict(_activity_dict)
        self.name = activity_dict["name"]
        self.prompt_config = PromptConfig.from_activity_dict(activity_dict)
        # self.prompt = activity_dict["prompt"]
        # self.error_prompt = activity_dict.get("error_prompt", "")
        # self.quit_string = ":q"
        # self.item_type = activity_dict.get("dtype", "boolean")
        # self.components: dict[PromptTypeName, ActivityDictRaw] = {}
        # self.project_dict = self.prompt_config_from_info
        self.desirable = activity_dict["desirable"]
        _order: Optional[float] = activity_dict.get("order", 50.0)
        self.order: float = float(_order or 50.0)
        self.response = None
        # self.subactivity_dict =

    @classmethod
    def from_routine_activity_dict(
        cls, routine_activity_dict: RoutineItemDictRaw, routine_name: str, order: float
    ) -> "TrackerItem":
        """
        Opens a routine item as if it had been defined under "tracking".
        """
        name = f"[{routine_name}] {routine_activity_dict['name']}"
        activity_activity_dict: ActivityDictRaw = {
            "name": name,
            "desirable": "yes",
            "prompt": f"Did you complete '{name}'?",
            "dtype": "boolean",
            "order": order,
            "response": None,
        }

        # print(order, routine_name, routine_activity_dict['name'])
        return cls(activity_activity_dict)

    def prompt_interactively(self) -> None:
        """
        Master method for interactive prompting, supporting all prompt data types.
        """
        # item_prompt_config = self.prompt_config_from_info
        self.response = prompt_any(self.prompt_config)

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
            "dtype": self.prompt_config.prompt_type,
            "desirable": self.desirable,
            "prompt": self.prompt_config.prompt_message,
        }
