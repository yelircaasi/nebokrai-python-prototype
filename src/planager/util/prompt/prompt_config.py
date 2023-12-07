from typing import Callable, Optional

from ..elementary_types import PromptTypeName, TrackingActivityType, prompt_type_mapping
from ..pdatetime import PTime
from .type_conversion import convert_time_amount

ConversionFuncType = Callable[[str], TrackingActivityType]
# from ..serde.custom_dict_types import (
#     PromptDispatcherType,
#     TimedDistance,
#     TimedDistanceWithElevation,
# )
conversion_func_dict: dict[PromptTypeName, ConversionFuncType] = {
    "float": float,
    "integer": int,
    "natural": int,
    "boolean": bool,
    "text": lambda x: x,
    "time_amount": convert_time_amount,
    "time": PTime.from_string,
}


class PromptConfig:
    """
    Container object to hold the information needed to run a specific type of prompt.
    """

    def __init__(
        self,
        prompt_type: PromptTypeName,
        conversion_func: Optional[ConversionFuncType] = None,
        quit_string: str = ":q",
        prompt_message: Optional[str] = None,
        invalid_input_message: Optional[str] = None,
        sequence_item_config: Optional["PromptConfig"] = None,
        components: Optional[dict[str, "PromptConfig"]] = None,
    ) -> None:
        self.prompt_type: PromptTypeName
        self.conversion_func: ConversionFuncType = conversion_func or conversion_func_dict.get(
            prompt_type, lambda x: x
        )
        self.quit_string: str = quit_string
        self.prompt_message: str = prompt_message or (
            f"Please give an input corresponding to '{prompt_type}'"
            f", parsable as {prompt_type_mapping[prompt_type]}"
            f" ('{quit_string}' to quit):  "
        )
        self.invalid_input_message: str = (
            invalid_input_message or f"Invalid input. {prompt_message}"
        )
        self.sequence_item_config: Optional["PromptConfig"] = sequence_item_config
        self.components: Optional[dict[str, "PromptConfig"]] = components


atomic_configs: dict[PromptTypeName, PromptConfig] = {
    pc.prompt_type: pc
    for pc in [
        PromptConfig(
            prompt_type="boolean",
            sequence_item_config=None,
            components=None,
        ),
        PromptConfig(
            prompt_type="natural",
            sequence_item_config=None,
            components=None,
        ),
        PromptConfig(
            prompt_type="integer",
            sequence_item_config=None,
            components=None,
        ),
        PromptConfig(
            prompt_type="text",
            sequence_item_config=None,
            components=None,
        ),
        PromptConfig(
            prompt_type="time_amount",
            sequence_item_config=None,
            components=None,
        ),
        PromptConfig(
            prompt_type="time",
            sequence_item_config=None,
            components=None,
        ),
    ]
}
composite_configs: dict[PromptTypeName, PromptConfig] = {
    pc.prompt_type: pc
    for pc in [
        PromptConfig(
            prompt_type="timed_distance_with_elevation",
            sequence_item_config=None,
            components={
                "kilometers": PromptConfig(prompt_type="float"),
                "seconds": PromptConfig(prompt_type="float"),
                "up": PromptConfig(prompt_type="float"),
                "down": PromptConfig(prompt_type="float"),
            },
        ),
        PromptConfig(
            prompt_type="timed_distance",
            sequence_item_config=None,
            components={
                "kilometers": PromptConfig(prompt_type="float"),
                "seconds": PromptConfig(prompt_type="float"),
            },
        ),
    ]
}
sequence_configs: dict[PromptTypeName, PromptConfig] = {
    pc.prompt_type: pc
    for pc in [
        PromptConfig(
            prompt_type="integer_sequence",
            sequence_item_config=atomic_configs["integer"],
        ),
        PromptConfig(
            prompt_type="natural_sequence",
            sequence_item_config=atomic_configs["natural"],
            components=None,
        ),
    ]
}

prompt_configs: dict[PromptTypeName, PromptConfig] = (
    atomic_configs | composite_configs | sequence_configs
)
